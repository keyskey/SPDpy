import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from PIL import Image, ImageDraw
import matplotlib.animation as animation
import re

def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

picList=sorted(glob.glob('*.png'), key=numericalSort)

images = []
     
for i in range(len(picList)):  
    tmp = Image.open(picList[i])
    images.append(tmp)
    
images[0].save('Dg_0.1.gif',
               save_all=True, append_images=images[1:], optimize=False, duration = 500, loop = 0)    #loop=0 で無限ループ   

