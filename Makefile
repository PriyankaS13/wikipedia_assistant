.PHONY: run_all run_mysql preprocessing run_wiki_app stop_all

preprocessing_image := lynx_pre_processing:latest
db_container_name := wikiDB
wiki_app_container_name := wiki_app

run_all: run_mysql run_preprocessing run_wiki_app schedule_preprocessing

run_mysql:
	@echo "Starting MySQL Server"
	docker-compose up -d $(db_container_name)

run_preprocessing:
	@echo "Building preprocessing docker image"
	cd wiki_preprocessing && docker build -t $(preprocessing_image) -f Dockerfile .
	@echo "Running preprocessing"
	docker run --rm $(preprocessing_image) python3 main.py

run_wiki_app:
	@echo "Building WikiApp"
	docker-compose build $(wiki_app_container_name)
	@echo "Starting WikiApp"
	docker-compose up -d $(wiki_app_container_name)

schedule_preprocessing:
	#echo new cron into cron file
	echo "1 12 02 * * make run_preprocessing -C /home/suceepriyanka/lynx" >> lynxcron
	#install new cron file
	crontab lynxcron
	rm lynxcron

stop_all:
	docker-compose stop