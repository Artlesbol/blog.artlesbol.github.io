---
share: true
tags: 
categories:
  - 编程语言
banner: 
title: C++容器整理
date: 2024-10-28T07:07:28+08:00
lastmod: 2024-10-28T08:39:44+08:00
---
之前编程都没怎么用容器，还是C风格的写法。正好最近在学习[现代 C++ 教程: 高速上手 C++ 11/14/17/20](https://changkun.de/modern-cpp/zh-cn/00-preface/)里面介绍了很多内容，今天总结一下关于现代Cpp的容器使用，就截止到C++20吧，更新的版本中的特性就不写了。
## 1. 序列容器（Sequence containers）
### 1.1 array
`std::array`封装了固定大小数组的容器
#### 函数模板
`template<class T, std::size_t N> struct array;`
+ T：元素类型，需要是可移动构造和可移动赋值的
+ N：数组中的元素数量，可以为0
#### 初始化
构造时使用聚合初始化
> [!INFO] 聚合初始化
> 从初始化器列表初始化聚合体。
> 语法是`T object = {arg1, arg2, ...};`或`T object{arg1, arg2, ...};`
> 从**C++20**开始也可以使用指派初始化器`.`：
> ```cpp
> struct A { int x; int y; int z; };
> A a{.y = 2, .x = 1}; // error; designator order does not match declaration order
> A b{.x = 1, .z = 2}; // ok, b.y initialized to 0
> ```
#### 元素访问
+ `at`
+ `operator[]`
+ `front`
+ `back`
+ `data`
### 2.1 vector
动态的连续数组，可以通过迭代器和常规指针访问元素。
#### 存储实现
vector 的存储是自动管理的，按需扩张收缩。`vector` 通常占用多于静态数组的空间，因为要分配更多内存以管理将来的增长。`vector` 所用的方式不在每次插入元素时，而只在额外内存耗尽时进行重分配。分配的内存总量可用 [capacity()](https://zh.cppreference.com/w/cpp/container/vector/capacity "cpp/container/vector/capacity") 函数查询。可以通过调用 `shrink_to_fit()`返回多余的内存给系统。重分配通常是性能上有开销的操作。如果元素数量已知，那么 [reserve()](https://zh.cppreference.com/w/cpp/container/vector/reserve "cpp/container/vector/reserve") 函数可用于消除重分配。
#### 性能
`vector` 上的常见操作复杂度（效率）如下：
- 随机访问——常数 𝓞(1)。
- 在末尾插入或移除元素——均摊常数 𝓞(1)。
- 插入或移除元素——与到 vector 结尾的距离成线性 𝓞(n)。
### 3.1 deque
双端队列
### 4.1 forward_list
单链表
### 5.1 list
双链表
## 2. 关联容器（Associative containers）
关联容器实现能快速查找（O(log n) 复杂度）的有序数据结构。
### 2.1 set
唯一键的集合，按照键排序
### 2.2 map
键值对的集合，按照键排序，键是唯一的
### 2.3 multiset
键的集合，按照键排序
### 2.4 multimap
键值对的集合，按照键排序
## 3. 无序关联容器（Container adaptors）
无序关联容器提供能快速查找（平均 O(1)，最坏情况 O(n) 的复杂度）的无序（散列）数据结构。
### 3.1 unordered_set
唯一键的集合，按照键生成散列
### 3.2 unordered_map
键值对的集合，按照键生成散列，键是唯一的
### 3.3 unordered_multiset
键的集合，按照键生成散列
### 3.4 unordered_multimap
键值对的集合，按照键生成散列
## 4. 容器适配器
容器适配器是用于提供某种功能的类模板，
### 4.1 stack
适配一个容器以提供栈（LIFO 数据结构）
### 4.2 queue
队列，默认用双端队列，支持序列容器，提供FIFO数据结构。
```cpp
template<
    class T,
    class Container = std::deque<T>
> class queue;
```
### 4.3 priority_queue
优先队列
+ 用堆实现
+ 它提供常数时间的（默认）最大元素查找，对数代价的插入与提取
+ 可以通过用户提供的 `Compare` 更改顺序，例如， `std::greater<T>`用将导致最小元素作为`top()`出现
```cpp
template<
    class T,
    class Container = std::vector<T>,
    class Compare = std::less<typename Container::value_type>
> class priority_queue;
```

## Reference
+ [Containers library - cppreference.com](https://en.cppreference.com/w/cpp/container)
+ [第 4 章 容器 现代 C++ 教程: 高速上手 C++ 11/14/17/20 - Modern C++ Tutorial: C++ 11/14/17/20 On the Fly](https://changkun.de/modern-cpp/zh-cn/04-containers/)