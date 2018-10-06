all:
	latexmk -pdf modeles.tex
	latexmk -pdf ruler.tex

modeles:
	latexmk -pdf modeles.tex

ruler:
	latexmk -pdf ruler.tex

clean:
	latexmk -c modeles.tex
	latexmk -c ruler.tex
	rm -f *.synctex.gz
