install:
	pip install -r requirements.txt
run: # Build and run the api 
	docker-compose up api
build:
	docker-compose build
clean_win:
	powershell .\utils\docker-clear.ps1
db:
	docker-compose up --force-recreate -d db
initdb:
	docker-compose up --force-recreate -d initdb

.PHONY: install