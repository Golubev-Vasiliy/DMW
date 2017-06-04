import sys, os
import socket
import re
import DB
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
from steganography.steganography import Steganography

FONT = 'Arial.ttf'

def server(): 
    sock = socket.socket()
    sock.bind(('', 9090));
    sock.listen(100)
    conn, addr = sock.accept()
    print 'connected:', addr

    data = conn.recv(1027)
    print data
    
    inst = re.search('\*(\d)', data)
    num = int(inst.group(1))
    print num
    #sign-in sign-out
    if num == 1:
        inst = re.search('\*(\d)\*([A-Za-z0-9]+)\*([A-Za-z0-9]+)\*([A-Za-z0-9]+\@[A-Za-z0-9]+\.[A-Za-z0-9]+)', data)
        user = inst.group(2)
        print user
        password = inst.group(3)
        print password
        print inst.group(4)
        DB.insert_user(inst.group(2),inst.group(3),inst.group(4))
        DB.select_user(user, password)
        conn.sendall(str(DB.id))
    if num == 2:
        inst = re.search('\*(\d)\*([A-Za-z0-9]+)\*([A-Za-z0-9]+)', data)
        user = inst.group(2)
        print user
        password = inst.group(3)
        print password
        DB.select_user(user, password)
        conn.sendall(str(DB.id))
    if num == 3:
        inst = re.search('\*(\d)\*(\d+)\*([A-Za-z0-9]+)', data)
        id_u = inst.group(2)
        print id_u
        stegocode = inst.group(3)
        print stegocode
        DB.insert_dmg(id_u, stegocode)
    if num == 4:
        inst = re.search('\*(\d)\*(\d+)', data)
        id_u = inst.group(2)
        print id_u
        DB.select_dwm(id_u)
        add_watermark('1.jpg', "(C)")

    conn.close()
    
    data=''

def add_watermark(in_file, text, out_file = "copyright.jpg", angle = 0, opacity = 0.5):
    img = Image.open(in_file).convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 45
    n_font  = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    #while (n_width + n_height < watermark.size[0]):
    #    size += 1
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width)/1, (watermark.size[1] - n_height)/1), text, font=n_font)
    watermark = watermark.rotate(angle, Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
    encode(DB.steg)

def encode(steg):
    path = "copyright.jpg"
    output_path = "copyright++.jpg"
    text = 'The quick brown fox jumps over the lazy dog.'
    Steganography.encode(path, output_path, steg)

def decode(output_path):
    secret_text = Steganography.decode(output_path)
    print secret_text



while (1):
    server()



#add_watermark('1.jpg', "(C) cop")

#decode('copyright++.jpg')