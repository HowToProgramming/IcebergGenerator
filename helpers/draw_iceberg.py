import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def concat(images):
    res = images[0]
    for i in images[1:]:
        res = get_concat_v(res, i)
    return res

def draw_iceberg(levels, save=None):
    img = Image.open("resources/iceberg.jpg")
    width, height = img.size
    height *= 4
    width *= 5
    height //= 2
    width //= 2
    img = img.resize((width, height))
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    

    # draw.text((x, y),"Sample Text",(r,g,b))
    def add_text(pos, txt, font, color=(255,0,0)):
        draw.text(pos, txt, color, font=font)

    def add_section_text(section, highest_pos=0, lowest_pos=height):
        fontsize = int((height / 2 * width / len(levels) / sum([len(i) for i in section])) ** 0.5)
        font = ImageFont.truetype('resources/arialbold.ttf', fontsize)
        pos = []
        # check if the text position is valid (not overlap with other text)
        def is_valid_position(x, y, text):
            textx, texty = font.getsize(text)
            for a, b, a2, b2 in pos:
                if ((a < x < a2 or a < x + textx < a2) and (b < y < b2 or b < y + texty < b2)):
                    return False
                if ((x < a < x + textx or x < a2 < x + textx) and (y < b < y + texty or y < b2 < y + texty)):
                    return False
            return True
        # random position until the position is valid
        def random_position(text):
            textx , texty = font.getsize(text)
            x = random.random() * (width - textx)
            y = random.random() * (lowest_pos - highest_pos - texty) + highest_pos
            while not is_valid_position(x, y, text):
                x = random.random() * (width - textx)
                y = random.random() * (lowest_pos - highest_pos - texty) + highest_pos
            pos.append([x,y,x+textx,y+texty])
            return x, y
        
        for text in section:
            x, y = random_position(text)
            add_text((x,y), text, font)



    for i, lvl in enumerate(levels):
        highest_pos = int(height / len(levels) * i)
        lowest_pos = int(height / len(levels) * (i + 1))
        add_section_text(lvl, highest_pos, lowest_pos)
        if i < len(levels) - 1:
            draw.line((0, lowest_pos, width, lowest_pos))
    
    if save:
        img.save(save, 'JPEG', optimize=True)
    return img


def get_iceberg_image_with_right_pic(levels, pics: list, save=None):
    iceberg = draw_iceberg(levels)
    num_pics = len(pics)
    a = int(iceberg.height / len(levels))
    imgs = []
    for i in range(len(levels)):
        if i == num_pics: break
        imgs.append(Image.open(pics[i]).resize((a,a)))
    right = concat(imgs)
    img = get_concat_h(iceberg, right)
    if save:
        img.save(save, 'JPEG', optimize=True)
    return img