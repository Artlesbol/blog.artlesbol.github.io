---
tags:
- blog
- astro
- github-pages
categories:
- tech
banner: null
title: "\u300CAstro+Github Pages+CloudFlare R2\u300D\u6211\u7684\u535A\u5BA2\u53D1\
  \u5E03\u64B0\u5199\u548C\u53D1\u5E03\u6D41\u7A0B"
lastmod: 2025-04-03 01:36:17+08:00
pubDate: 2025-03-23 08:45:23+08:00
description: "\n\uFF08\u610F\u4E49\u4E0D\u660E\u7684\u524D\u8A00\uFF09\u53C8\u662F\
  \u4E00\u7BC7\u535A\u5BA2\u6D41\u7A0B\u535A\u5BA2\uFF0C\u4F9D\u7A00\u8BB0\u5F97\u4E0A\
  \u4E00\u7BC7\u535A\u5BA2\u4E5F\u662F\u4ECB\u7ECD\u6211\u7684\u5DE5\u4F5C\u6D41\u3002\
  \u4F46\u662F\uFF01\u8FD9\u6B21\u6211\u5E26\u6765\u4E86\u66F4\u4F18\u79C0\u7684\u5DE5\
  \u4F5C\u6D41\uFF0C\u6211\u4F1A\u575A\u6301\u53D1\u5E03\u535A\u5BA2\u7684\u3002\n\
  \n## 1 \u603B\u4F53\u65B9\u6848\n\n\u8FD9\u6B21\u7684\u535A\u5BA2\u6D89\u53CA\u591A\
  \u4E2A\u6D41\u7A0B\uFF0C\u4E3B\u8981\u5206\u4E3A\u5BFC\u51FA\u548C\u53D1"
---

（意义不明的前言）又是一篇博客流程博客，依稀记得上一篇博客也是介绍我的工作流。但是！这次我带来了更优秀的工作流，我会坚持发布博客的。

## 1 总体方案

这次的博客涉及多个流程，主要分为导出和发布两个阶段。

- 导出
  - 在 Obsidian 编写博客内容（包含图片，生成 obsidian 管理的 metadata ）
  - 导出（将 md 导出，替换图片链接为 html 形式，将相关图片放到对应目录下，将图片处理为 webp ）
  - 脚本处理（将图片上传到 R2 对象存储中，替换文章中的链接；调用大模型 api 生成文章的 description；处理博客的 metadata 为 blog 发布形式）
- 发布
  - 将 md 文件 push 到文章仓库
  - 在博客仓库同步并发布

## 2 准备仓库

原本的博客框架是：[EveSunMaple/Frosti](https://github.com/EveSunMaple/Frosti)，是 MIT 协议，但是我希望我的博客内容遵守 CC-BY-NC-SA 4.0 所以分别放在两个仓库里面，以 submodel 的形式链接

```shell
git submodule add <子模块仓库URL> <子模块路径>
```

仓库说明：

- [Artlesbol/blog.artlesbol.github.io](https://github.com/Artlesbol/blog.artlesbol.github.io)：存放博客文章
- [Artlesbol/Frosti-myblog](https://github.com/Artlesbol/Frosti-myblog)：存放博客前端

## 3 博客导出和处理

### 3.1 自动维护 yaml

**任务一：修正 data 为 pubData**

obsidian 生成的 metadata 的 key 是`data`但是博客系统里需要读取的是`pubData`，有一点点差异，所以在处理脚本里找到对应的`data`替换成`pubData`即可

**任务二：添加 description**

我的 obsidian 里面是不包含 description 这个 metadata 的，但是这个博客框架里面这个属于必须字段。而且我觉得确实是需要在页面里填充一些字才会显得不那么空，所以选择在导出后加上一个字段

但是如果自己写 description 又比较麻烦，所以还是做个自动化脚本来做这个事情吧

目前只是把文章的第一段的内容作为 description ，稍微有些单调。生成 description 这个事情后续可以用大模型来处理。**（ToDo）用一个免费的小模型来做生成工作**

```python
import os
import yaml

def update_yaml_in_md_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Check if the file has YAML front matter
                if lines[0].strip() == '---':
                    # Find the end of the YAML front matter
                    yaml_end_index = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == '---'), None)
                    if yaml_end_index is not None:
                        yaml_content = ''.join(lines[1:yaml_end_index])
                        content = ''.join(lines[yaml_end_index + 1:])

                        # Parse and update YAML
                        yaml_data = yaml.safe_load(yaml_content)
                        if 'date' in yaml_data:
                            yaml_data['pubDate'] = yaml_data.pop('date')
                        if 'description' not in yaml_data:
                            # 取出文章前 100 个字符作为文章描述
                            yaml_data['description'] = content[:100]

                        updated_yaml = yaml.dump(yaml_data, sort_keys=False)

                        # Write updated content back to the file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write('---\n')
                            f.write(updated_yaml)
                            f.write('---\n')
                            f.write(content)

if __name__ == "__main__":
    content_dir = os.path.join(os.path.dirname(__file__), "../content")
    update_yaml_in_md_files(content_dir)
```

### 3.2 自动把图片上传到 cloudflare R2

另外我的图片如果全部存到 Github 仓库里的话，100M 的空间很快就用完了，这样不太好。

所以我选择使用 cloudflare R2 的对象存储作为图床，先根据[官网](https://www.cloudflare.com/zh-cn/developer-platform/products/r2/)提示注册和创建对象存储。

- 具体申请的过程可以参考这个博客：[从零开始搭建你的免费图床系统（Cloudflare R2 + WebP Cloud）](https://www.pseudoyu.com/zh/2024/06/30/free_image_hosting_system_using_r2_webp_cloud_and_picgo)
- 如果你的域名没有托管在 cloudflare，则需要参考这个：[从零开始搭建你的免费图床系统（Cloudflare R2 + WebP Cloud）](https://www.pseudoyu.com/zh/2024/06/30/free_image_hosting_system_using_r2_webp_cloud_and_picgo)把他托管过来

然后写一个脚本上传图片到 R2 的 bucket 里，然后再替换图片的链接就可以了。因为在 obsidian 里面已经把名字做了 hash 处理了，所以在桶里面是不可能重名的，所以不需要再建立子目录，直接传到同一个目录里就好了。

大部分图片是文章目录里的 attachment 目录，逐个扫一遍即可；还有一些图片是头图，头图我全部放在根目录的 attachment 里，所以也要扫一下，头图单独放到一个目录里。

r2 的密钥的都放在同目录的 r2_key.yaml 里了，不能公开出来了(/////////)

```python
import boto3
from botocore.config import Config
import os
import re

# 从 r2_key.yaml 文件中加载 R2 配置信息
import yaml

r2_key_path = f"{os.path.dirname(__file__)}/r2_key.yaml"

with open(r2_key_path, 'r', encoding='utf-8') as key_file:
    r2_config = yaml.safe_load(key_file)

access_key = r2_config['access_key']
secret_key = r2_config['secret_key']
url = r2_config['url']

visit_url = 'https://r2.artlesbol.top'
bucket_name = 'blog'

# 创建 S3 客户端
config = Config(signature_version='s3v4')
s3_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url=url,
    config=config
)


def upload_to_r2(local_file_path, bucket_file_name):
    """上传文件到 R2"""
    try:
        s3_client.upload_file(local_file_path, bucket_name, bucket_file_name)
        print(f"Uploaded {local_file_path} to {bucket_file_name}")
        return f"{visit_url}/{bucket_name}/{bucket_file_name}"
    except Exception as e:
        print(f"Failed to upload {local_file_path}: {e}")
        return None

def process_directory(base_dir):
    """遍历目录并处理 attachment 文件夹和 .md 文件"""
    for root, dirs, files in os.walk(base_dir):
        if 'attachment' in dirs:
            attachment_dir = os.path.join(root, 'attachment')
            md_files = [f for f in files if f.endswith('.md')]

            # 上传 attachment 目录中的文件
            for file_name in os.listdir(attachment_dir):
                local_file_path = os.path.join(attachment_dir, file_name)
                bucket_file_name = f"content/img/{file_name}"
                bucket_file_name = bucket_file_name.replace("\\", "/")  # 替换为 R2 兼容路径
                r2_url = upload_to_r2(local_file_path, bucket_file_name)
                print(r2_url)

                # 替换同级 .md 文件中的图片路径
                if r2_url:
                    for md_file in md_files:
                        md_file_path = os.path.join(root, md_file)
                        replace_image_path(md_file_path, file_name, r2_url)

def replace_image_path(md_file_path, file_name, r2_url):
    """替换 .md 文件中的图片路径为 R2 路径"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换图片路径
        updated_content = re.sub(
            #匹配图片路径，如：img src="attachment/d8fc267508bb5e274aaf90b19d486d3d.webp"
            fr'img src="attachment/{file_name}"',
            f'img src="{r2_url}"',
            content
        )

        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        print(f"Updated image path in {md_file_path}")
    except Exception as e:
        print(f"Failed to update {md_file_path}: {e}")

if __name__ == "__main__":
    content_dir = os.path.join(os.path.dirname(__file__), "../content")
    process_directory(content_dir)
```

参考文章：

- [【Python Cloudflare R2 API 调用】用 python 调用 Cloudflare 的 R2 存储桶的 api 接口-CSDN 博客](https://blog.csdn.net/weixin_46625757/article/details/140652861)

## 4 编写 Github CI wrokflow config

Astro 官方提供了一个部署脚本：[部署你的 Astro 站点至 GitHub Pages | Docs](https://docs.astro.build/zh-cn/guides/deploy/github/)

需要做一点点修改：由于我们分离仓库的操作，需要添加一个 cp 命令，这样目录里才有文章

```yaml
name: Deploy to GitHub Pages

on:
  # 每次推送到 `main` 分支时触发这个“工作流程”
  # 如果你使用了别的分支名，请按需将 `main` 替换成你的分支名
  push:
    branches: [ main ]
  # 允许你在 GitHub 上的 Actions 标签中手动触发此“工作流程”
  workflow_dispatch:

# 允许 job 克隆 repo 并创建一个 page deployment
permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout your repository using git
        uses: actions/checkout@v4
        with:
          submodules: true  # 拉取子模块
      - name: copy contents
        run: cp -rf ./content/blog ./Frosti-myblog/src/content/blog
      - name: Install, build, and upload your site
        uses: withastro/action@v3
        with:
          path: ./Frosti-myblog # 存储库中 Astro 项目的根位置。（可选）
          node-version: 20 # 用于构建站点的特定 Node.js 版本，默认为 20。（可选）
          package-manager: pnpm@latest # 应使用哪个 Node.js 包管理器来安装依赖项和构建站点。会根据存储库中的 lockfile 自动检测。（可选）


  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

## 5 配置 Github Pages

这一步没什么好说的，就在仓库的配置页面里选上 Github Action 部署就行，也就是上面配的 CI。

## 6 编写博客和发布

万事俱备，只欠东风。

这时候我只需要几步就可以顺利发布文章了

- 从 obsidian 里用 markdown-export 插件把我的文章导出到文章仓库里
- 执行自动格式化脚本：`bash runscript.sh`
- 添加和上传：`git add && git push`

等待 Github Action 执行完毕，刷新博客页就行了。

## 7 Dev

如果还需要修改博客的样式之类的，可以在模板仓库来做

然后在文章仓库这边，如果需要更新，则使用同步的命令进行更新

```shell
 git submodule update --remote --merge
```
