SHELL = /bin/bash
SRC = src
DATA = data

# Development-related targets

# list dependencies
requirements:
	pipreqs --force --savepath requirements/prod.txt $(SRC)

# install dependencies for production
install: install-dev
	pip install -r requirements/prod.txt

# install dependencies for development
install-dev:
	pip install -r requirements/dev.txt

# remove Python file artifacts
clean:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +

# check style
lint: format
	pylint --exit-zero --jobs=0 --output-format=colorized $(SRC)
	pycodestyle --show-source $(SRC)
	pydocstyle $(SRC)

# format according to style guide
format:
	yapf --in-place --recursive $(SRC)
	isort -rc $(SRC)

# Data-related targets

# remove all data. Be careful with this one.
remove:
	@rm -rf $(DATA)
	@mkdir $(DATA)
	@mkdir $(DATA)/html

.PHONY: requirements install install-dev clean lint format remove
