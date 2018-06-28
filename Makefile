run: # Build and run the api 
	docker-compose up api
build:
	docker-compose build
clean_win:
	powershell .\utils\docker-clear.ps1