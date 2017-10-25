from PIL import Image
import os

def crop(infile,height,width,step):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    #for i in range(0,imgwidth-width,2):
    for j in range(0,imgwidth-width,step):
        #for j in range(0,imgheight-height,2):
        for i in range(0,imgheight-height,step):
            box = (i, j, (i+width), (j+height))
            yield im.crop(box)

if __name__=='__main__':
    #infile='test_images/small50kmh.jpg'
    infile='test_images/stoppskilt5.jpg'
    height=32
    width=32
    step=1
    start_num=0
    for k,piece in enumerate(crop(infile,height,width,step),start_num):
        img=Image.new('RGB', (height,width), 255)
        img.paste(piece)
        #path=("IMG-%s.jpg" % k)
        path=("res_images/IMG-%s.jpg" % k)
        img.save(path)
