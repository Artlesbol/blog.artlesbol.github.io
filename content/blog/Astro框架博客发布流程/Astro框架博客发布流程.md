---
tags:
  - blog
categories:
  - Unclassified
banner: 
title: Astro框架博客发布流程
description: Astro框架博客发布流程
date: 2025-03-23T08:29:13+08:00
lastmod: 2025-03-23T08:56:52+08:00
---
## 1 前言

这次的博客涉及多个流程，主要分为导出和发布两个阶段。

+ 导出
    + 在Obsidian编写博客内容（包含图片，生成obsidian管理的metadata）
    + 导出（将md导出，替换图片链接为html形式，将相关图片放到对应目录下，将图片处理为webp）
    + 脚本处理（将图片上传到R2对象存储中，替换文章中的链接；调用大模型api生成文章的description；处理博客的metadata为blog发布形式）
+ 发布
    + 将md文件push到文章仓库
    + 在博客仓库同步并发布