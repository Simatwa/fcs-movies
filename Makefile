.PHONY: install test-apis test-api-v1 test-api-v2 test-non-apis runserver-dev runserver download-db deploy

PYTHON := python3
PIP := $(PYTHON) -m pip
DOWNLOAD_DB_TO := assets/db.sqlite3.part

default: install test runserver

# Target to install dependencies
install:
	$(PIP) install -r requirements.txt

# Target to run tests
test: test-apis test-non-apis

# Target to test RestAPI V1
test-api-v1:
	$(PYTHON) -m pytest tests/test_v1.py -xv

# Target to test RestAPI V2
test-api-v2:
	$(PYTHON) -m pytest tests/test_v2.py -xv

test-apis: test-api-v1 test-api-v2

# Target to test non-APIs
test-non-apis:
	$(PYTHON) -m pytest tests/test_non_*.py -xv

# Target to run development server
runserver-dev:
	$(PYTHON) -m fastapi dev

# Target to run production server
runserver:
	$(PYTHON) -m fastapi run

# Target to download movies database
download-db:
	wget https://raw.githubusercontent.com/Simatwa/movies-dataset/main/data/combined.db \
	-O $(DOWNLOAD_DB_TO) --continue
	mv $(DOWNLOAD_DB_TO) assets/db.sqlite3

# Target to setup production environment
# and actually run the server
deploy: install test download-db runserver