
slide.pdf: slide.tex
	latexmk -pdf $<
	latexmk -c

clean:
	latexmk -C
	rm -f slide.pdf
