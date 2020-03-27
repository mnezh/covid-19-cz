
.PHONY: install
.PHONY: get
.PHONY: convert

default: all

all: install get convert

install:
	pipenv install

get:
	pipenv run ./get_mzcr_data.py

convert:
	pipenv run ./convert_data.py
