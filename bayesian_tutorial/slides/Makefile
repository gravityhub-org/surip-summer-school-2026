all: slide.pdf

slide.pdf: slide.tex cointossposterior.pdf
	latexmk -pdf $<
	latexmk -c

clean:
	latexmk -C
	rm -f slide.pdf
