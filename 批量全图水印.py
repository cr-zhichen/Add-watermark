"""
文件作用：批量给图片加水印
源码来源：https://github.com/2Dou/watermarker
二改：cr-zhichen
"""

import argparse
import os
import sys
import math
import PIL

from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageChops

print("-------------------")
print("本程序作用为 批量全图水印  \n源码来源：https://github.com/2Dou/watermarker \n二改：cr-zhichen")
print("-------------------")
print("请将需要加水印的图片放置于程序目录下input文件夹中 \n本程序输出文件位置为程序目录下output文件夹")

字体 = './font/Font.ttf'

输入位置="./input"  #默认为./input
水印文字=input("请输入水印文字(输入完成请按回车)：")
输出位置="./output" #默认为./output
字体颜色="#000000"  #十六进制颜色 推荐为#8B8B1B
文字间距=100    #默认为75
水印旋转角度=30 #默认为30
文字大小=50 #默认为50
不透明度=0.15   #默认为0.15
if 水印文字=="":
    水印文字="请正确输入水印文字"

自定义=input("是否需要自定义其他选项?\n需要请输入T，否则请直接下按回车：")
自定义bool=False

if 自定义=="T"or 自定义=="t":
    自定义bool=True

def custom():
    global 文字间距
    global 文字大小
    global 不透明度
    try:
        文字间距= int(input("请输入文字间距 默认为100(输入完成请按回车)："))
        文字大小= int(input("请输入文字大小 默认为50(输入完成请按回车)："))
        不透明度= float(input("请输入不透明度 默认为0.15(输入完成请按回车)："))
    except:
        print("请输入正确参数")
        custom()

if 自定义bool==True:
    custom()

print("-------------------")
print("水印文字："+水印文字+"\n"+"文字间距："+str(文字间距)+"\n"+"文字大小："+str(文字大小)+"\n"+"不透明度："+str(不透明度))
print("-------------------")

def add_mark(imagePath, mark, args):
    '''
    添加水印，然后保存图片
    '''
    im = Image.open(imagePath)

    image = mark(im)
    if image:
        name = os.path.basename(imagePath)
        if not os.path.exists(args.out):
            os.mkdir(args.out)

        new_name = os.path.join(args.out, name)
        if os.path.splitext(new_name)[1] != '.png':
            image = image.convert('RGB')
        image.save(new_name)

        print(name + " Success.")
    else:
        print(name + " Failed.")

def set_opacity(im, opacity):
    '''
    设置水印透明度
    '''
    assert opacity >= 0 and opacity <= 1

    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def crop_image(im):
    '''裁剪图片边缘空白'''
    bg = Image.new(mode='RGBA', size=im.size)
    diff = ImageChops.difference(im, bg)
    del bg
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def gen_mark(args):
    '''
    生成mark图片，返回添加水印的函数
    '''
    # 字体宽度
    width = len(args.mark) * args.size

    # 创建水印图片(宽度、高度)
    mark = Image.new(mode='RGBA', size=(width, args.size*2))

    # 生成文字
    draw_table = ImageDraw.Draw(im=mark)
    draw_table.text(xy=(0, 0),
        text=args.mark,
        fill=args.color,
        font=ImageFont.truetype(字体,
        size=args.size))
    del draw_table

    # 裁剪空白
    mark = crop_image(mark)

    # 透明度
    set_opacity(mark, args.opacity)

    def mark_im(im):
        ''' 在im图片上添加水印 im为打开的原图'''

        # 计算斜边长度
        c = int(math.sqrt(im.size[0]*im.size[0] + im.size[1]*im.size[1]))

        # 以斜边长度为宽高创建大图（旋转后大图才足以覆盖原图）
        mark2 = Image.new(mode='RGBA', size=(c, c))

        # 在大图上生成水印文字，此处mark为上面生成的水印图片
        y, idx = 0, 0
        while y < c:
            # 制造x坐标错位
            x = -int((mark.size[0] + args.space)*0.5*idx)
            idx = (idx + 1) % 2

            while x < c:
                # 在该位置粘贴mark水印图片
                mark2.paste(mark, (x, y))
                x = x + mark.size[0] + args.space
            y = y + mark.size[1] + args.space

        # 将大图旋转一定角度
        mark2 = mark2.rotate(args.angle)

        # 在原图上添加大图水印
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        im.paste(mark2, # 大图
            (int((im.size[0]-c)/2), int((im.size[1]-c)/2)), # 坐标
            mask=mark2.split()[3])
        del mark2
        return im

    return mark_im

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-f", "--file", default=输入位置, type=str, help="image file path or directory")
    parse.add_argument("-m", "--mark", default=水印文字, type=str, help="watermark content")
    parse.add_argument("-o", "--out", default=输出位置, help="image output directory, default is ./output")
    parse.add_argument("-c", "--color", default=字体颜色, type=str, help="text color like '#000000', default is #8B8B1B")
    parse.add_argument("-s", "--space", default=文字间距, type=int, help="space between watermarks, default is 75")
    parse.add_argument("-a", "--angle", default=水印旋转角度, type=int, help="rotate angle of watermarks, default is 30")
    parse.add_argument("--size", default=文字大小, type=int, help="font size of text, default is 50")
    parse.add_argument("--opacity", default=不透明度, type=float, help="opacity of watermarks, default is 0.15")

    args = parse.parse_args()

    if isinstance(args.mark, str) and sys.version_info[0] < 3:
        args.mark = args.mark.decode("utf-8")

    mark = gen_mark(args)

    if os.path.isdir(args.file):
        names = os.listdir(args.file)
        for name in names:
            image_file = os.path.join(args.file, name)
            add_mark(image_file, mark, args)
    else:
        add_mark(args.file, mark, args)

if __name__ == '__main__':
    main()

input("输出完成\n输出目录为："+输出位置+"\n按回车关闭程序")