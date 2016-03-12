#!/usr/bin/make
.PHONY: tests
tests:
	tox

.PHONY: clean
clean:
	@rm -rf .cache
	@find . -name "*.pyc" -type f -delete
	@find . -name "__pycache__" | xargs rm -rf
	@find . -name "*.DS_Store" -type f -delete

.PHONY: spotless
spotless: clean
	@rm -rf .tox
