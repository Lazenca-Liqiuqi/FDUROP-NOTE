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
#import "@preview/zebraw:0.4.3": zebraw
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
        institution: [Fudan University],
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

= 模式的结果

== boxplot

#set page(columns: 2)
#image("image.png", height: 190pt)
#image("image-1.png", height: 190pt)
#image("image-2.png", height: 190pt)
#image("image-3.png", height: 190pt)

== 垂直剖面
#set page(columns: 2)
#image("image-5.png")
#image("image-6.png")

== 偏差
#set page(columns: 2)
#image("image-7.png")
#image("image-12.png")

== 泰勒图

#image("image-8.png")
#image("image-9.png")
#image("image-10.png")
#image("image-11.png")


