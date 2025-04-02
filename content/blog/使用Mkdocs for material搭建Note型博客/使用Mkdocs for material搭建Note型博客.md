---
tags:
- blog
- github-pages
categories:
- tech
banner: null
title: "\u4F7F\u7528Mkdocs for material\u642D\u5EFANote\u578B\u535A\u5BA2"
lastmod: 2025-04-03 01:40:23+08:00
share: false
pubDate: 2023-10-07 10:46:06+08:00
description: "\n# \u5907\u6599\n\n\u8BA1\u5212\u642D\u5EFA\u4E00\u4E2A\u4F7F\u7528\
  \u4E2A\u4EBA\u57DF\u540D\u7684 note \u578B\u535A\u5BA2\uFF0C\u6258\u7BA1\u5728 Github\
  \ Page \u4E0A\uFF0C\u56E0\u6B64\u53EA\u9700\u8981\u51C6\u5907\n\n- Github \u4ED3\
  \u5E93\n- \u4E2A\u4EBA\u57DF\u540D\n\n# \u90E8\u7F72\u6B65\u9AA4\n\n## 1 \u521B\u5EFA\
  \u65B0\u7684 Githu"
---

# 备料

计划搭建一个使用个人域名的 note 型博客，托管在 Github Page 上，因此只需要准备

- Github 仓库
- 个人域名

# 部署步骤

## 1 创建新的 Github 仓库

一个用于存放博客和自动部署的 Github 仓库，命名为`<username>.github.io`

<img src="https://r2.artlesbol.top/blog/content/img/761c66cede7abe12ab0b0e3bb9192059.webp" />

## 2 本地安装 mkdocs for material

使用 pip 包管理器安装 mkdocs-material，如果没有安装 python 则需要先安装 python

```shell
pip install mkdocs-material
```

然后将刚才创建的 github 仓库 clone 到本地，新建站点，仓库里原有的多余文件可以删掉

```
mkdocs new .
```

然后打开`mkdocs.yml`，加入`thmem`的配置

```yml
theme:
  name: material
```

最后在本地启动预览，可以查看效果

```shell
mkdocs serve
```

## 3 配置 github actions 工作流

在刚才的仓库中，新建文件`.github/workflows/ci.yml`，内容为 mkdocs material 官网提供的[CI 配置](https://squidfunk.github.io/mkdocs-material/publishing-your-site/#with-github-actions)，抄上去之后 commit 并 push

来到 github 仓库页面，Action 处发现 ci 已经在执行了

<img src="https://r2.artlesbol.top/blog/content/img/b953cac5ea54bf4fad8e3fd93ab4d082.webp" />

ci 执行结束后可以看到 code 中出现了新的分支`gh-pages`，这就是生成好的页面，可以进行发布

<img src="https://r2.artlesbol.top/blog/content/img/21c2bda6a6eda63ea4568d5ba573ad55.webp" />

## 4 配置 github pages 和 DNS 解析

在仓库上方的`Setting`中可以找到`Pages`的配置选项，这里选择从分支部署，然后选择 gh-pages 分支即可

<img src="https://r2.artlesbol.top/blog/content/img/b19c6f7c989362ee7df77f8085191cd3.webp" />

如果需要配置自定义域名，就在下面输入一下自定义域名

<img src="https://r2.artlesbol.top/blog/content/img/da794c377229d77de3d361e948701d73.webp" />

然后按照[官方文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site?platform=linux#configuring-a-subdomain)提示，去 DNS 服务商，添加一条指向`<username>.github.io`的`CNAME`记录。等待 DNS 扩散后，就可以通过配置的域名访问了

<img src="https://r2.artlesbol.top/blog/content/img/6e10d87c9c0c23eef812208f4224f8c7.webp" />
