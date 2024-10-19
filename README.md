## About the Project

File Reconciliation APIs

#### This application allows you to reconcile between two different csv files and return the differences between the two files. 

1. An endpoint to accept two CSV files (source and target) for reconciliation.

2. Data normalization logic to handle potential data transformation issues (e.g., date formats, case sensitivity, leading/trailing spaces).

4. Reconciliation logic:

4. Identify records present in source but missing in target and vice versa.

5. Compare records that exist in both files to identify discrepancies in specific
fields.

6. An endpoint to return the reconciliation report in a desired format(CSV, HTML, or JSON).

Reconciliation Results Display:
After successful upload and processing, display the results:
1. Records missing in the target.

2. Records missing in the source.

3. Records with discrepancies, highlighting the fields that differ.

4. Error Handling:

5. Display error messages if the file upload fails or if there are validation errors.

IF you have Docker follow the setup below, or clone the repository and run it the best way you could locally

### Installation RUN the commands below in the terminal (Docker is required)
- cd ~/path/to/the/directory/where/you/download/the/project
- cp .env.example .env
- Add the database configuration to the .env file
- docker compose build
- docker compose ps -a (To see the list of containers started) 
- docker compose up -d
- docker exec -it recon_app /bin/sh
- Create the migrations (python manage.py makemigrations)
- Run the migrations (python manage.py migrate)

### If you know how to use Makefile, check the Makefile and run the commands for easy setup
- make install_all
- make appinstall package_name
- make build
- make fresh_build
- make start
- make stop
- make restart
- make start_app
- make rand_key (Run this to generate random key for the Django secret key)

### HOW to use the application
- To access the application base url .........http://localhost:8001/

### UPLOAD FILE ENDPOINTS
- POST upload file .........http://localhost:8001/api/reconcile/upload/

### FILE REPORT ENDPOINTS
- GET upload file .........http://localhost:8001/api/reconcile/report/{hash_key}/
- GET upload file .........http://localhost:8001/api/reconcile/report/{hash_key}/{format}/