### **Pre Processing**
Below are the pre-processing steps

1.Download files from latest folder of wiki dumps.

2.Creates **wikipedia** db if it does not exists.

3.Loads data from sql files into tables.

4.Pre computes outdated pages data into **outdated_page_list** table for top 10 categories.

##### Implementation Notes
* Only four tables related to pages and categories are considered for the sake of simplicity.
* The whole of wiki dump is rather huge in size(~ 17 TB) and would require powerful clusters to process.
* The dumps related to the 4 tables in consideration are .sql files, which deletes and recreates the table.
While we could have parsed the file and converted to csv to further process them as inserts and updates, the chances of
updates are higher compared to inserts.Hence its better to recreate as the number of tables is limited and downtime is 
acceptable.
* Precomputed tables are necessary to reduce the response time of api also since the data is static till the next 
refresh.
* There would be an avg downtime of 30min while data is refreshed,mainly due to data load of pagelinks 
which is quite large ~1 billion.



### WIKI APP Rest API
There are two rest API's which runs on port **8000**
* **_RawSQL API:_**  

This is POST call that takes raw sql query as request body, 
and returns a json formatted response of executed query.

##### Example
`curl -i -X POST http://<hostname>:8000/api/v1/rawquery -d {"query": "select count(1) as count from category"}`

* **_Oudated Page API:_** 

    * This is a GET call, which gives most outdated pages for a category. 

    * If Category is not provided then outdated pages of all categories are returned.
 
 
 ##### Example
* `curl -i http://<hostname>:8000/api/v1/outdatedpages`
* `curl -i http://<hostname>:8000/api/v1/outdatedpages?category_name=Commons_category_link_is_on_Wikidata`



#### Scope for Improvement
* Authentication
* Pagination for the query results.
* Advanced checks for SQL injection.



### App Deployment:
App is distributed across 3 docker images.
* Mysql DB 
* REST API Server
* PreProcessing Engine


#### Deployment Orchestration:
docker-compose and Makefile are used for docker orchestration.
* docker-compose.yaml contains mysqldb(wikiDB) and RestAPI server(wiki_app) images configs
* make file has following targets. 
    * run_mysql: Starts Mysql container.
    * run_preprocessing: Executes preprocessing engine.
    * run_wiki_app: Builds and Runs the wiki rest api server.
    * schedule_preprocessing: Creates cron job to run `run_preprocessing` target 2nd of every month at 12PM.
    * stop_all: stops all the containers.
    * run_all: This task runs by default, it executes `run_mysql,run_preprocessing,run_wiki_app,schedule_preprocessing` 
      in sequence.

#### How to Deploy
```
    cd $<path_to_project>
    make
```
* Once the make command is issued it runs `run_all` task and schedules the monthly job.

##### Implementation Notes
* Dockers are easy and powerful tool for creating and managing applications without depending on environments, easy to 
    share as image across developers.
* Makefile is simple yet powerful build tool to organise tasks and execute.
* cronjob is available by default in almost all linux flavours.

#### Scope for Improvement
* `Airflow` is very powerful DAG based orchestrator, it provides mechanism to back fill data in case of failure and easy 
to integrate with something like pager duty to send alerts.
* Since Airflow requires db configuration and periodic upgrades,wasn't an ideal candidate for short development cycle 
like this one.

### Cloud Hosting
Although the initial choice was AWS, the free tier limits instance type to t2.micro(1GB RAM) which is too less to host 
the apps and db.
However GCP provided a much better compute engine.

Below is the end points for the GCP hosted wiki assistant app

http://35.200.225.142:8000/api/v1/outdatedpages
http://35.200.225.142:8000/api/v1/outdatedpages?category_name=Commons_category_link_is_on_Wikidata
http://35.200.225.142:8000/api/v1/rawquery
