# 批量全图水印

为图片添加文字水印
可设置文字**大小、颜色、旋转、间隔、透明度**

## 程序来源

文件作用：批量给图片加水印  
源码链接：[Github仓库链接](https://github.com/2Dou/watermarker)  
改动：[cr-zhichen](https://github.com/cr-zhichen/zc--)  

## 用法

需要PIL库 `pip install Pillow`

|变量        |默认
|------------|------------
|输入位置    |默认为./input
|水印文字    |默认为用户输入
|输出位置    |默认为./output
|字体颜色    |十六进制颜色 推荐为#8B8B1B
|文字间距    |默认为75
|水印旋转角度|默认为30
|文字大小    |默认为50
|不透明度    |默认为0.15
|字体        |默认为./font/Font.ttf

## 效果图片

![测试图片](https://www.chengrui.xyz/images/2020/06/12/Demoefdbb08c1b5b3d96.png)
