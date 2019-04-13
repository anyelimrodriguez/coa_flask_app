PYTHON     = pipenv run
SRC_FILES := $(shell find . -name "*.py")

.PHONY: help
help:
	@echo "Usage:"
	@echo "    help:   Prints this screen"
	@echo "    format: Formats the code"
	@echo "    fmt:    An alias for format"
	@echo "    lint:   Lints the code"
	@echo "    run:    Run the flask application"
	@echo ""

.PHONY: format
format:
	 $(PYTHON) autopep8 -i $(SRC_FILES)

.PHONY: fmt
fmt: format

.PHONY: lint
lint:
	 $(PYTHON) mypy --ignore-missing-imports $(SRC_FILES)
	 $(PYTHON) pylint $(SRC_FILES)

.PHONY: run
run:
	FLASK_APP=coa_flask_app FLASK_ENV=development $(PYTHON) flask run --host=0.0.0.0
