
# Simple makefile for pyp2p

test:
	@echo "Running tests..."
	PYTHONPATH=. nosetests -v
	@echo "Done."

pep8:
	@echo "Cheking PEP8 coding style..."
	@pep8 . --exclude="docs,test*" --max-line-length=90 --ignore=E127,E265
	@echo "Done."

check: test pep8 



