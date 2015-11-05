#!/usr/bin/make
.PHONY: tests
tests:
	tox
	make clean

.PHONY: clean
clean:
	@rm -rf .cache
	@find . -name "*.pyc" -print | xargs rm -rf
	@find . -name "__pycache__" | xargs rm -rf

.PHONY: spotless
spotless: clean
	@rm -rf .tox
