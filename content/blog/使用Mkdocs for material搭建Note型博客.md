---
share: true
tags: []
categories:
  - tech
banner: 
title: "使用Mkdocs for material搭建Note型博客"
description: "如何搭建Note型博客"
pubDate: 2023-10-07T10:46:06+08:00
lastmod: 2024-10-28T07:19:13+08:00
---
# 备料
计划搭建一个使用个人域名的note型博客，托管在Github Page上，因此只需要准备
+ Github仓库
+ 个人域名
# 部署步骤
## 1. 创建新的Github仓库
一个用于存放博客和自动部署的Github仓库，命名为`<username>.github.io`
<!-- ![](attachments/Pasted%20image%2020231007114347.png) -->
## 2. 本地安装mkdocs for material
使用pip包管理器安装mkdocs-material，如果没有安装python则需要先安装python
```shell
pip install mkdocs-material
```
然后将刚才创建的github仓库clone到本地，新建站点，仓库里原有的多余文件可以删掉
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
## 3. 配置github actions工作流
在刚才的仓库中，新建文件`.github/workflows/ci.yml`，内容为mkdocs material官网提供的[CI配置](https://squidfunk.github.io/mkdocs-material/publishing-your-site/#with-github-actions)，抄上去之后commit并push

来到github仓库页面，Action处发现ci已经在执行了

<!-- ![](attachments/Pasted%20image%2020231007115359.png) -->

ci执行结束后可以看到code中出现了新的分支`gh-pages`，这就是生成好的页面，可以进行发布

![[../../../../attachments/Pasted image 20231007143950.png|../../../../attachments/Pasted image 20231007143950.png]]

## 4. 配置github pages和DNS解析

在仓库上方的`Setting`中可以找到`Pages`的配置选项，这里选择从分支部署，然后选择gh-pages分支即可

![[../../../../attachments/Pasted image 20231007145016.png|../../../../attachments/Pasted image 20231007145016.png]]

如果需要配置自定义域名，就在下面输入一下自定义域名

![[../../../../attachments/Pasted image 20231007145028.png|../../../../attachments/Pasted image 20231007145028.png]]

然后按照[官方文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site?platform=linux#configuring-a-subdomain)提示，去DNS服务商，添加一条指向`<username>.github.io`的`CNAME`记录。等待DNS扩散后，就可以通过配置的域名访问了

![[../../../../attachments/Pasted image 20231007145343.png|../../../../attachments/Pasted image 20231007145343.png]]