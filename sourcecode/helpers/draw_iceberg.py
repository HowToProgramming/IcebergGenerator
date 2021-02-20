from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random


def draw_iceberg(levels, save=None):
    img = Image.open("resources/iceberg.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/ArialUnicodeMS.ttf', 20)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    width, height = img.size

    # draw.text((x, y),"Sample Text",(r,g,b))
    def add_text(pos, txt, color=(255,0,0)):
        draw.text(pos, txt, color, font=font)

    def add_section_text(section, highest_pos=0, lowest_pos=height):
        
        pos = []
        def is_valid_position(x, y, text):
            textx, texty = font.getsize(text)
            for a, b, a2, b2 in pos:
                if ((a < x < a2 or a < x + textx < a2) and (b < y < b2 or b < y + texty < b2)):
                    return False
                if ((x < a < x + textx or x < a2 < x + textx) and (y < b < y + texty or y < b2 < y + texty)):
                    return False
            return True
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
            add_text((x,y), text)



    for i, lvl in enumerate(levels):
        highest_pos = int(height / len(levels) * i)
        lowest_pos = int(height / len(levels) * (i + 1))
        add_section_text(lvl, highest_pos, lowest_pos)
        draw.line((0, lowest_pos, width, lowest_pos), width=10)
    
    if save:
        img.save(save, 'JPEG', optimize=True)
    return img
