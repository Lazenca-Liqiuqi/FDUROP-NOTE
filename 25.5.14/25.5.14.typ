#import "@preview/touying:0.6.1": *
#import themes.university: *
#import "@preview/cetz:0.3.2"
//这是一个绘图包
#import "@preview/fletcher:0.5.4" as fletcher: node, edge
//这是一个画各种流程图的包
#import "@preview/numbly:0.1.0": numbly
//这是一个制定编号格式的包
#import "@preview/theorion:0.3.0": *
//这是一个定理包
#import "@preview/zebraw:0.5.4": zebraw
//显示代码片段

#import cosmos.clouds: *
#show: show-theorion

// cetz and fletcher 和投影进行链接
#let cetz-canvas = touying-reducer.with(reduce: cetz.canvas, cover: cetz.draw.hide.with(bounds: true))
#let fletcher-diagram = touying-reducer.with(reduce: fletcher.diagram, cover: fletcher.hide)

//初始化这个主题
#show: university-theme.with(
  aspect-ratio: "16-9", //长宽比
  progress-bar: true, //进度条
  header: utils.display-current-heading(level: 2), //页眉
  header-right: image("/asset/大气与海洋科学系logo.png", height: 40pt), //页眉右侧的图片
  footer-columns: (25%, 1fr, 25%), //底部的分栏
  align: horizon,
  // config-common(handout: true),
  config-common(frozen-counters: (theorem-counter,)),
  // 冻结定理计数器的动画
  //config-common(show-notes-on-second-screen: right),
  //在副屏显示讲稿
  config-info(
    title: [组会报告],
    subtitle: [],
    author: [Li "Lazenca" Qiuqi],
    date: datetime.today(),
    institution: [Fudan University ff],
  ), //信息
)
//全局设置区
#set heading(numbering: numbly("{1}.", default: "1.1")) //标题编号
#set text(
  font: (
    (name: "Fira Code", covers: "latin-in-cjk"),
    (name: "LXGW WenKai"),
  ),
  size: 20pt,
)
#show raw: set text(
  font: (
    (name: "Fira Code", covers: "latin-in-cjk"),
    (name: "LXGW WenKai"),
  ),
  size: 14pt,
)
//标题页
//
//
//
#title-slide()

== Outline <touying:hidden>

#components.adaptive-columns(outline(title: none, indent: 1em))//目录

//接下来开始文档的编辑
//
//
//
// 分割线
= NCEP-NCAR风输入

#pagebreak()

下载了NCEP的数据，并且处理成模式输入格式

https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html

#image("image.png")

主要问题：原始数据规模为(1460,17,73,144),模式输入格式为(1460,17,89,144)

== 数据批量下载

Windows不使用api（没有api？）的办法

1. 使用脚本生成下载文件的链接列表
2. idm批量添加任务，可续传

== 线性插值

#zebraw(
  // The first line number will be 2.
  numbering-offset: 0,
  ```Python
  for t in tqdm(range(vector.shape[0])):
    for p in range(vector.shape[1]):
        for lon_idx in range(vector.shape[3]):
            f = interp1d(
                lat_original,
                vector[t, p, :, lon_idx],
                kind="linear",
                fill_value="extrapolate",
            )
            new_vector[t, p, :, lon_idx] = f(new_lat)
  ```,
)

= HIPPO

== 下载

https://data.eol.ucar.edu/master_lists/generated/hippo-1/


其中的HiPPO Merged 10-second Meteorology, Atmospheric Chemistry!and Aerosol Data [Wofsy, et. al.]包含了HIPPO-1到HIPPO-5的10秒分辨率的所有资料。

#image("image-1.png")

== 其他处理

- 把HIPPO预处理并且加入旧数据集

- 把数据集的信息（包括名称、颜色、持续时间等）使用文件导入，增加代码可维护性。













