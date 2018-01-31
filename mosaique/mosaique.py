from PIL import Image
import image_slicer
import itertools
import numpy

filename='trois-brigands'
tile_size = 10

def ilen(it):
    '''Return the length of an iterable.
    
    >>> ilen(range(7))
    7
    '''
    return sum(1 for _ in it)

def runlength_enc(xs):
    '''Return a run-length encoded version of the stream, xs.
    
    The resulting stream consists of (count, x) pairs.
    
    >>> ys = runlength_enc('AAABBCCC')
    >>> next(ys)
    (3, 'A')
    >>> list(ys)
    [(2, 'B'), (3, 'C')]
    '''
    return ((ilen(gp), x) for x, gp in itertools.groupby(xs))

def name_of_tile(filename,i,j):
    return(filename+'_'+str(i).zfill(2)+'_'+str(j).zfill(2)+'.png')

def rle_encode_tile(filename, i, j):
    img = Image.open(name_of_tile(filename,i,j))
    greyscaleimg=img.convert('L')
    bwimg=Image.eval(greyscaleimg, lambda px: 0 if px <= 100 else 255)
    img_dta = list(bwimg.getdata())
    return(map(lambda (x,y):x,list(runlength_enc(img_dta))))

def create_tiles():
    '''Create tiles'''
    imgorig = Image.open(filename+".jpg")
    width, height = imgorig.size
    image_slicer.slice(filename+".jpg", (width/tile_size)*(height/tile_size))

def latex_code(image_filename,i,j,rlecode):
    source_template=r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}

\begin{document}

Mosaique xxx yyy.

\begin{tikzpicture}
\draw[step=0.5cm,black,thin] (0,0) grid (taille,taille);
\end{tikzpicture}

Code:
zzz

\newpage

\includegraphics{nomimage}
\end{document}
    """
    s1=source_template.replace("taille", str(tile_size))
    s2=s1.replace("xxx", str(i))
    s3=s2.replace("yyy", str(j))
    s4=s3.replace("zzz", rlecode)
    s5=s4.replace("nomimage", name_of_tile(filename,i,j) )
    return(s5)
    
def create_exercises():
    for i in range(1,33):
        for j in range(1,33):
            code=rle_encode_tile(filename,i,j)
            f = open(name_of_tile(filename,i,j)+'.tex', 'w')
            print >>f, (latex_code(filename,i,j,str(code)))
            f.close()

create_tiles()
create_exercises()
        
        
