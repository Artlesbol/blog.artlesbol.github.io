---
title: "\u4E2D\u6587\u6D4B\u8BD5\uFF0C\u975E\u4E25\u683C\u8BED\u6CD5\u6D4B\u8BD5\uFF0C\
  \u516C\u5F0F\u6D4B\u8BD5"
description: Here is a sample of some basic Markdown syntax that can be used when
  writing Markdown content in Astro.
pubDate: Jul 01 2024
image: /image/image3.png
categories:
- tech
tags:
- Makrdown
badge: Pin
---
## 1 ML Refresher
### 1.1 机器学习算法的构成
+ The hypothesis class：预设的分类
+ The loss function：损失函数，告知机器如何是好的
+ An optimization method：优化器，让参数的losses最小，以优化模型
## 2 softmax regression （softmax回归）
### 2.1 算法设置
记号说明：$x^{i} \in \Re^{n}$是实数域内的n维向量
$$
x^{(i)} = \begin{bmatrix}
x^{(i)}_1 \\
x^{(i)}_2 \\
\cdots \\
x^{(i)}_n
\end{bmatrix}
$$

数据说明
+ 训练数据：$x^{i} \in \Re^{n}, y^{(i)} \in \{1,\dots,k\}$ for $i = 1,\dots,m$
+ n = 输入数据的维度
+ k = 分类的类别
+ m = 训练集中的点的数量
### 2.2 线性假设函数（Linear hypothesis function）
线性预设函数是一个将$x \in \Re^n$映射到$k$维向量的函数，即
$$h:\Re^n \rightarrow \Re^k$$
使用一个线性表示来实现这个变换
$$y^{(i)} = \theta^T x^{(i)}$$

### 2.3 损失函数
#### 2.3.1 交叉熵损失
交叉熵损失（corss-entropy loss）是利用信息论中的交叉熵概念量化模型的方式，一般和softmax或者sigmoid函数一起用，将网络的输出转化为概率然后计算交叉熵
**softmax**：
softmax算子是用于将网络量化出的”可能性“转化为真正的概率的工具，由于网络可能会得到负的可能性，所以用exp处理将其转化为正值，然后再进行归一化
$$z_i = p(label=i)=\frac{\exp(h_i(x))}{\sum^k_{j=1}\exp(h_j(x))}\Leftrightarrow z\equiv normalize(\exp(h(x))) $$
**使用softmax的交叉熵损失函数**：
$$l_{ce}(h(x),y)=-\log p(label=y)=-h_{y}(x)+\log \sum^k_{j=1}\exp(h_{j}(x))$$
### 2.4 优化器
#### 2.4.1 softmax回归优化问题
优化器最终是要让求得的损失函数在全局最小，也就是下面的优化问题，让所有样本的平均损失最小
$$
\mathop{\text{minimize}}_{\theta} \frac{1}{m}\sum^m_{i=1}l(h_{\theta} (x^{(i)}),y^{(i)})
$$
也就是
$$
\mathop{\text{minimize}}_{\theta} \frac{1}{m}\sum^m_{i=1}l(\theta^Tx^{(i)},y^{(i)})
$$
#### 2.4.2 梯度下降
梯度实际上是一个偏导数的矩阵，例如函数$f:\mathbb{R}^{n\times k}\to\mathbb{R}$的$\theta$的梯度，记号如下：
$$
\nabla_{\theta} f(\theta) \in \mathbb{R}^{n \times k} = 
\begin{bmatrix}
\frac{\partial f(\theta)}{\partial \theta_{1,1}} & \cdots & \frac{\partial f(\theta)}{\partial \theta_{1,k}} \\
\vdots & \ddots & \vdots \\
\frac{\partial f(\theta)}{\partial \theta_{n,1}} & \cdots & \frac{\partial f(\theta)}{\partial \theta_{n,k}}
\end{bmatrix}
$$
梯度方向就是这个参数向最小值或最大值的方向，因此优化的方法是迭代$\theta$
$$
\theta:=\theta-\alpha\nabla_\theta f(\theta)
$$
 其中$\alpha$是学习率，决定了一步的大小，太小迭代太慢，太大可能不收敛
#### 2.4.3 随机梯度下降算法（SGD）
[11.4. 随机梯度下降 — 动手学深度学习 2.0.0 documentation](https://zh.d2l.ai/chapter_optimization/sgd.html#id2)
将数据规模m每B个切分成一个miniBatch，分别计算梯度，此时有
 $$ X \in \mathbb{R}^{B \times n}, y \in \{1, \ldots, k\}^B$$
 那么更新方法就是
 $$\theta := \theta - \frac{\alpha}{B} \sum_{i=1}^{B} \nabla_{\theta} \ell(h_{\theta}(x^{(i)}), y^{(i)})$$
但是这样比较慢，因为需要计算其中每一个的梯度
SGD算法：S（stochastic），选择其中一个梯度计算，然后以这一个样本的结果代替整个batch的结果，降低了计算量
#### 2.4.4 对$\theta$求偏导
要求
$$\nabla_{\theta} \ell_{ce}(\theta^T x, y) = ?$$
根据链式法则，先求$\nabla_h \ell_{ce}(h, y)$
对于每一个分量$h_{i}$有
$$
\frac{\partial \ell_{ce}(h, y)}{\partial h_i} = \frac{\partial}{\partial h_i} \left( -h_y + \log \sum_{j=1}^{k} \exp h_j \right) = -1 \{i = y\} + \frac{\exp h_i}{\sum_{j=1}^{k} \exp h_j}
$$
因此，整个矩阵的表示为
$$\nabla_h \ell_{ce}(h, y) = z - e_y$$
其中，$e_{y}$表示规模为$y$的单位阵，$z = \text{normalize}(\exp(h))$

随后需要求矩阵的导数，求导原理比较复杂，参考[矩阵求导原理](../../0072_理论/矩阵求导原理.md)

