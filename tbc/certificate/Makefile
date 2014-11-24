# Makefile for Python Textbook Companion Certificate

# bashful package available @
# http://www.ctan.org/tex-archive/macros/latex/contrib/bashful

# pst-barcode package available @
# http://www.ctan.org/tex-archive/graphics/pstricks/contrib/pst-barcode

# target is not a real file
.PHONY: help tbc clean

# default help
help:
	@echo "current make version is: "$(MAKE_VERSION)
	@echo "Please use \`make <target>' where <target> is one of"
	@echo ""
	@echo "tbc	        Generate Python tbc certificate."
	@echo "clean		clean all tmp and pdf files."
	@echo "help		Show this help."
	@echo ""

# certificate
tbc:	tbc_certificate.pdf

tbc_certificate.pdf: tbc_certificate.tex fossee.png bashful.sty
	pdflatex -shell-escape tbc_certificate.tex

clean:	
	@echo "removing all tmp+pdf files"
	-rm -rvf *.pdf *~ *.aux *.log *.vrb *.out *.toc *.nav *.snm
	-rm -rvf *.std* *.sh
