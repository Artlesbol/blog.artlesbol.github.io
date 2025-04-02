---
tags:
- obsidian
- blog
- github-pages
categories:
- tech
banner: null
title: "Hugo+Obsidian+Github Pages\u4E00\u7AD9\u5F0F\u535A\u5BA2\u521B\u4F5C"
lastmod: 2025-04-03 01:39:08+08:00
pubDate: 2023-12-23 03:38:07+08:00
description: "\n## 1 \u53D1\u5E03\u65B9\u6848\u603B\u89C8\n\n\u7531\u4E8E\u6211\u592A\
  \u559C\u6B22 obsidian \u4E86\uFF0C\u73B0\u5728\u51E0\u4E4E\u6240\u6709\u7684\u7B14\
  \u8BB0\u548C\u8D44\u6599\u90FD\u5728 obsidian \u91CC\u3002\u6B63\u597D\u6700\u8FD1\
  \u51C6\u5907\u91CD\u542F\u535A\u5BA2\uFF0C\u6240\u4EE5\u6211\u60F3\u628A\u6211\u7684\
  \u535A\u5BA2\u7F16\u5199\u4E5F\u653E\u5230 ob \u91CC\u3002\u76EE\u524D\u4F53\u9A8C\
  \u8FD9\u5957\u6D41\u7A0B\u51E0\u4E4E\u662F"
---

## 1 发布方案总览

由于我太喜欢 obsidian 了，现在几乎所有的笔记和资料都在 obsidian 里。正好最近准备重启博客，所以我想把我的博客编写也放到 ob 里。目前体验这套流程几乎是零压力发布 ob 的方案，非常好用。

### 1.1 效果

- 创建笔记的时候会生成 frontmatter，自动维护 date, lastmod, title
- 勾选 frontmatter 里的 share 之后点击左侧快捷按钮即可发布，可以发布一个也可以批量发布
- 发布时附件图片会自动上传到对应的资源目录
  <img src="https://r2.artlesbol.top/blog/content/img/a54a5fea11d01389370ad1354dec6b8a.webp" />

### 1.2 方案目录

- 博客系统：Hugo
  - 博客主题：stack
  - 博客托管：GitHub Pages
- Obsidian 插件
  - Linter：自动生成 frontmatter
  - Github Publisher：管理和发布文档
  - Commander：添加快捷按钮（可选）

## 2 配置

首先建一个自己用来存博客文章的仓库，克隆到本地

### 2.1 Hugo

#### 2.1.1 Hugo 本体

Reference：[Quick start | Hugo (gohugo.io)](https://gohugo.io/getting-started/quick-start/)

参考官方文档直接使用包管理器安装 hugo

```bash
sudo apt install hugo
```

然后生成 hugo 站，初始化目录，这里把 quickstart 改成自己的站名

```bash
hugo new site quickstart
cd quickstart
```

然后把里面的东西都 copy 到自己仓库的目录里，这样 Hugo 站本体生成就完成了

#### 2.1.2 Hugo 主题

Reference：[Getting Started | Stack (jimmycai.com)](https://stack.jimmycai.com/guide/getting-started)

我用的主题是 Stack，非常好看（大概）

根据 hugo 官方文档，安装方法是在仓库目录下执行以下命令，当然你可以换成对应的其他主题。**这里建议自己 fork 一个主题仓库，因为可能需要添加图标或者其他的东西。**

```bash
git submodule add git@github.com:Artlesbol/hugo-theme-stack.git themes/hugo-theme-stack
```

#### 2.1.3 Hugo 配置

hugo 通过根目录下的`config.yaml`文件进行配置，这里我直接用了主题提供的配置文件进行修改，具体可以参考对应主题的文档和[hugo 官方文档](https://gohugo.io/getting-started/configuration/)，都会有一些参数和配置说明。你至少需要配置`theme = 'hugo-theme-stack'`来使用主题。

配置好之后可以用下面的命令在本地编译并启动服务，可以预览一下

```bash
hugo server
```

### 2.2 Github Pages

Reference：[Host on GitHub Pages | Hugo (gohugo.io)](https://gohugo.io/hosting-and-deployment/hosting-on-github/)

我选择使用 Github Pages 来托管博客，参考官方文档：

1. 首先设置 Pages 的发布源为 Github Actions
   <img src="https://r2.artlesbol.top/blog/content/img/8b9534f1ec735b36a1d715a22cd705b4.webp" />
2. 创建`.github/workflows/hugo.yaml`在其中写入如下内容

```yaml
## Sample workflow for building and deploying a Hugo site to GitHub Pages
name: Deploy Hugo site to Pages

on:
  # Runs on pushes targeting the default branch
  push:
    branches:
      - main

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

## Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

## Allow only one concurrent deployment, skipping runs queued between the run in-progress and latest queued.
## However, do NOT cancel in-progress runs as we want to allow these production deployments to complete.
concurrency:
  group: "pages"
  cancel-in-progress: false

## Default to bash
defaults:
  run:
    shell: bash

jobs:
  # Build job
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.121.0
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb \
          && sudo dpkg -i ${{ runner.temp }}/hugo.deb
      - name: Install Dart Sass
        run: sudo snap install dart-sass
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4
      - name: Install Node.js dependencies
        run: "[[ -f package-lock.json || -f npm-shrinkwrap.json ]] && npm ci || true"
      - name: Build with Hugo
        env:
          # For maximum backward compatibility with Hugo modules
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./public

  # Deployment job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3
```

3. 然后就配置好了，可以提交一个 commit 测试一下有没有成功触发，如果触发了就可以访问自己的站了
4. （可选）配置自己的域名，先在 dns 服务商处添加一天 CNAME 解析，指向`<user>.github.io`，然后在 Pages 设置里写入自己的域名即可
   <img src="https://r2.artlesbol.top/blog/content/img/77ccf11d3098ac6687bc17769805e975.webp" />

### 2.3 Obsidian

#### 2.3.1 Linter

Linter 是为了自动维护 frontmatter 而启用的插件，需要配置多个地方，你也可以根据自己的需要调整。

我这里用了`share`,`tags`,`categories`,`banner`,`title`,`date`,`lastmod`

##### 2.3.1.1 自动格式化

设置自动格式化，可以在保存和切换的时候格式化，自动维护

<img src="https://r2.artlesbol.top/blog/content/img/874bad6903bad01316d809844f129e35.webp" />

##### 2.3.1.2 插入的属性

这里插入需要手动写的属性即可，下面会有其他自动维护的

<img src="https://r2.artlesbol.top/blog/content/img/987f988a89a1f891e65a87d7a2cbe8cb.webp" />

##### 2.3.1.3 时间戳

用于显示文档创建时间和最后修改时间

<img src="https://r2.artlesbol.top/blog/content/img/2618f02134b18c5dedd402071ffa99e2.webp" />

##### 2.3.1.4 标题

获取文件名作为 title

<img src="https://r2.artlesbol.top/blog/content/img/0599338d35bf2c326a8e047a4a773c58.webp" />

#### 2.3.2 Github Publisher

Github Publisher 是用于发布的插件

##### 2.3.2.1 基础

你需要生成一个 Github token 用于插件与 GIthub 的交互，生成方式可以点击插件上的链接

<img src="https://r2.artlesbol.top/blog/content/img/e0bba02509b5ce6371c4c90a60a311a0.webp" />

##### 2.3.2.2 上传路径

首先配置文件的路径，这里的 Root folder 表示上传到仓库的目录，这里选择`Obsidian Path`即可，他会按照 Obsidian 的目录结构上传，由于 Hugo 不在乎目录结构，所以如此管理即可。

<img src="https://r2.artlesbol.top/blog/content/img/102052bc57440e5950901ea92676b6eb.webp" />

其次是附件上传，Hugo 从 static 目录读取静态资源，为了保持路径一致，我在 Obsidian 中的图片全部保存在`attachments`目录下，然后附件自动上传目录设置为`static/attachments`即可。

<img src="https://r2.artlesbol.top/blog/content/img/24b6d41462b214c2785ed7bf77c90617.webp" />

<img src="https://r2.artlesbol.top/blog/content/img/905fe0b69ae41839ea8a4e81cd19aac5.webp" />

#### 2.3.3 Commander

配置到这里其实就已经可以使用了，`Ctrl + P`输入`Github Publisher`即可看到所有的指令。

<img src="https://r2.artlesbol.top/blog/content/img/706199f0f5442d9b76862681df0f6094.webp" />

这里常用的是发布单个文件，每次都要输一下很麻烦，所以我用 Commander 插件做了一个快捷按键，来到插件配置页，选着左侧边栏，添加命令即可。

<img src="https://r2.artlesbol.top/blog/content/img/67985b4aafb610f7b613c789873e334c.webp" />

## 3 总结

到此所有的配置都做完了，仅仅勾选 share 就可以无压力的发布 Obsidian 的文档到 Hugo。
