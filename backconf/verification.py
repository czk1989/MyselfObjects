
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import random
import os,json
import math, string
from backconf import redis_conf

REDIS_CONN=redis_conf.redis_conn()
DIR=os.path.dirname(os.path.abspath(__file__))
#字体的位置，不同版本的系统会有不同
font_path=os.path.join(DIR,r'fonts\arial.ttf')

#生成几位数的验证码
number = 4

#生成验证码图片的高度和宽度
size = (100,30)

#背景颜色，默认为白色
bgcolor = (255,255,255)

#字体颜色，默认为蓝色
fontcolor = (0,0,255)

#干扰线颜色。默认为红色
linecolor = (255,0,0)

#是否要加入干扰线
draw_line = True

#加入干扰线条数的上下限
line_number = (1,5)

def gen_text():
    '''随机生成4位验证码字符串'''
    source = list(string.ascii_letters + string.digits)
    return ''.join(random.sample(source,number))


#用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill = linecolor)

def gene_code():
    width,height = size #宽和高
    image = Image.new('RGBA',(width,height),bgcolor) #创建图片
    font = ImageFont.truetype(font_path,25) #验证码的字体和字体大小
    draw = ImageDraw.Draw(image) #创建画笔
    text = gen_text() #生成字符串
    # print(text)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height ) / number),text,font= font,fill=fontcolor) #填充字符串

    if draw_line:
        gene_line(draw, width, height)
        gene_line(draw, width, height)
        gene_line(draw, width, height)

    image = image.transform((width + 20, height +10), Image.AFFINE, (1, -0.5, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
    # image.save('%s/%s.png' %(save_path,filename))  # 保存验证码图片
    # print("savepath:",save_path)
    REDIS_CONN.set('%s'%text,json.dumps(image),15)

    return text

# if __name__ == "__main__":
#     gene_code(os.path.join(DIR,r'img'),'test1') #会把生成的图片存成/tmp/test.png



