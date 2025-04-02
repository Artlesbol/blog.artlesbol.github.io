---
tags:
- blog
- astro
- github
categories:
- tech
banner: null
title: "Astro\u535A\u5BA2\u90E8\u7F72\u5230Github Pages"
lastmod: 2025-03-27 07:52:34+08:00
pubDate: 2025-03-23 08:45:23+08:00
description: "\n## 1 \u603B\u4F53\u65B9\u6848\n\n\u8FD9\u6B21\u7684\u535A\u5BA2\u6D89\
  \u53CA\u591A\u4E2A\u6D41\u7A0B\uFF0C\u4E3B\u8981\u5206\u4E3A\u5BFC\u51FA\u548C\u53D1\
  \u5E03\u4E24\u4E2A\u9636\u6BB5\u3002\n\n- \u5BFC\u51FA\n  - \u5728 Obsidian \u7F16\
  \u5199\u535A\u5BA2\u5185\u5BB9\uFF08\u5305\u542B\u56FE\u7247\uFF0C\u751F\u6210 obsidian\
  \ \u7BA1\u7406\u7684 metadata \uFF09\n "
---

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

### 3.1 修正 data 为 pubData

obsidian 生成的 metadata 的 key 是`data`但是博客系统里需要读取的是`pubData`，有一点点差异，所以在处理脚本里找到对应的`data`替换成`pubData`即可

**（To Do）完成自动化工作的脚本**

### 3.2 添加 description

我的 obsidian 里面是不包含 description 这个 metadata 的，但是这个博客框架里面这个属于必须字段。而且我觉得确实是需要在页面里填充一些字才会显得不那么空，所以选择在导出后加上一个字段

但是如果自己写 description 又比较麻烦，所以还是做个自动化脚本来做这个事情吧

如果只是把文章的第一段的内容作为 description 的话稍微有些单调，所以生成 description 这个事情可以用大模型来处理。

**（ToDo）用一个便宜的小模型来做生成工作**

### 3.3 自动把图片上传到 cloudflare R2

另外我的图片如果全部存到 Github 仓库里的话，100M 的空间很快就用完了，这样不太好。

所以我选择使用 cloudflare R2 的对象存储作为图床，先根据[官网](https://www.cloudflare.com/zh-cn/developer-platform/products/r2/)提示注册和创建对象存储。

然后写一个脚本上传图片到 R2 的 bucket 里，然后再替换图片的链接就可以了。

```python
# To Do
```

大部分图片是文章目录里的 attachment 目录，逐个扫一遍即可；还有一些图片是头图，头图我全部放在根目录的 attachment 里，所以也要扫一下

**（ToDo）相同图片是否会重复，如何避免重复上传**

### 3.4 添加 Git hook

根据[Git - githooks Documentation](https://git-scm.com/docs/githooks)，Git Hooks 可以实现自动执行脚本，然后再 commit 的功能，符合我们的需求。因此把刚刚写好的脚本放到 pre-commit 的 hook 里就行了。不过需要注意，这个是本地执行，所以里面的命令需要本地有环境才可以。

**（ToDo）配置 hook**

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
- git add & git push

等待 Github Action 执行完毕，刷新博客页就行了。

## 7 Dev

如果还需要修改博客的样式之类的，可以在模板仓库来做

然后在文章仓库这边，如果需要更新，则使用同步的命令进行更新

```shell
 git submodule update --remote --merge
```
