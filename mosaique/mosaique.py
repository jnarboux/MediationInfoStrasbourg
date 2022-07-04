from PIL import Image
from math import *
# import image_slicer
import itertools
from itertools import zip_longest
import numpy


def ilen(it):
    '''Return the length of an iterable.
    
    >>> ilen(range(7))
    7
    '''
    return sum(1 for _ in it)

def grouper(iterable, n, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

#def grouper(l,groupsize):
#    print(len(l))
#    print(list(range(0, len(l), groupsize)))
#    print(l[n] for n in range(0, len(l), groupsize))
#    print("toto")
#    r= [l[n:(n+groupsize)] for n in list(range(0, len(l), groupsize))]
#    return(r)

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

def name_of_tile(basename,i,j):
    return("{file}_{x:02d}_{y:02d}".format(file=basename,x=i,y=j))


def rle_encode_list_list(l):
    return(list(map(runlength_enc, l)))

def add_implicit_color(l):
    for x in l:
        if(x[0][1]==0):
            x.insert(0,(0,1))

def rle_encode_tile(basename, i, j, tile_size):
    img = Image.open(name_of_tile(basename,i,j)+".png")
    img_dta = grouper(img.getdata(),tile_size)
    codes = list(map(list,rle_encode_list_list(img_dta)))
    print (codes[0][0][1])
    add_implicit_color(codes)
    codes=list(map(list,map(lambda l: map(lambda x: x[0], l),codes)))
    return(codes)

def create_tiles(basename,tile_size):
    imgorig = Image.open(basename+".png").convert('RGBA')
    background = Image.new("RGBA", imgorig.size, (255, 255, 255)) # white background 
    alpha_composite = Image.alpha_composite(background, imgorig) # blend alpha channel
    imgorig = alpha_composite.convert("L") # to monochrome
    threshold = 240
    imgorig = imgorig.point(lambda p: p > threshold and 255) # O or 255 with threshold
    #imgorig.save(basename + "_bw.png")
    imgwidth, imgheight = imgorig.size
    for i in range(imgheight//tile_size):
        for j in range(imgwidth//tile_size):
            box = (j*tile_size, i*tile_size, (j+1)*tile_size, (i+1)*tile_size)
            imgorig.crop(box).save(name_of_tile(basename,i+1,j+1)+".png")
#            imgorig.crop(box).save(name_of_tile(basename,i+1,j+1)+".pdf")

def latex_code(image_filename,i,j,rlecode,tile_size):
    source_template=r"""
\parbox{\textwidth}{
Ecrire au dos du quadrillage: Ligne: xxx, Colonne: yyy.\\
\smallskip

\begin{tabular}{cl}
\begin{tikzpicture}
\draw (0,0) grid[step=1] (8,8);
\end{tikzpicture}
\begin{minipage}[b]{.46\linewidth}
\baselineskip=1cm
zzz
\end{minipage}
\end{tabular}
}
\vfill

%\newpage

%\fbox{\includegraphics[width=\textwidth]{nomimage}}

%\newpage
    """
    s1=source_template.replace("xxx", str(i)).replace("yyy", str(j))
    s2=s1.replace("zzz", str(rlecode)).replace("nomimage", name_of_tile(image_filename,i,j)+".png" )
    return(s2)


def presentation_of_code(ll):
    return("\\\\".join(map (lambda l:",".join(map(str,l)),ll)))

def create_exercises(basename,tile_size):
    imgorig = Image.open(basename+".png")
    width, height = imgorig.size
    nbx = height//tile_size
    print("nbx",nbx)
    nby = width//tile_size
    print("nby",nby)
    header=r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage{graphicx}

\begin{document}"""
    footer=r"""
\end{document}
    """
    f = open(basename+'_codes.tex', 'w')
    print(header,file=f)
    for i in range(1,nbx+1):
        for j in range(1,nby+1):
            print("Tile",i,j)
            code=rle_encode_tile(basename,i,j,tile_size)
            print (latex_code(basename,i,j,presentation_of_code(code),tile_size),file=f)
    print(footer,file=f)
    f.close()

def create_solutions(basename,tile_size):
    imgorig = Image.open(basename+".png")
    width, height = imgorig.size
    nbx = height//tile_size
    print("nbx",nbx)
    nby = width//tile_size
    print("nby",nby)
    tile_inv= 0.8 / nby
    s=""
    for i in range(1,nbx+1):
        for j in range(1,nby+1):
            s+=r"""\fbox{\includegraphics[width=\tilesize]{file.png}}
""".replace("file",name_of_tile(basename,i,j))
        s+="\\\\\n"
    header=r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{tikz}
\usepackage{fullpage}
\usepackage{graphicx}

\newlength{\tilesize}
\setlength{\tilesize}{xxx\textwidth}

\begin{document}
\noindent
"""
    footer=r"""\end{document}"""
    f = open(basename+'_solutions.tex', 'w')
    print (header.replace("xxx",str(tile_inv))+s+footer,file=f)
    f.close()
    
def create_all(basename,tile_size):
    print("Creating the tiles")
    create_tiles(basename,tile_size)
    print("Creating the codes")
    create_exercises(basename,tile_size)
    print("Creating solution")
    create_solutions(basename,tile_size)

create_all("panda-aime-science",8)
