# Code Challenge Template
## Weather Data Ingestion Script (weather_data_ingestion.py)
- This is a Python script that ingests weather data from text files into a PostgreSQL database and calculates statistics on the ingested data. The script uses the psycopg2 library to interact with the database and assumes that the weather data files are stored in a directory called wx_data in the same directory as the script.

## Installation
- Install Python 3.x from the official website
- Install PostgreSQL from the official website
- Install the psycopg2 library using pip: pip install psycopg2
## Packages
The following packages are used in the script:

- os: provides a way to interact with the file system
- psycopg2: provides a way to interact with a PostgreSQL database
- datetime: provides a way to work with dates and times
- logging: provides a way to log information to a file
## Getting Started
- Clone or download the repository
- Install the required packages as described above
- Open a terminal or command prompt and navigate to the directory containing the script
- Run the script using the command python weather_data_ingestion.py
## How to Run
- python weather_data_ingestion.py or python3 weather_data_ingestion.py .

The script performs the following steps:

- Connects to the PostgreSQL database using the connect_to_database() function
- Creates the weather_data table in the database using the create_weather_data_table() function
- Ingests weather data from files in the wx_data directory using the insert_weather_data() function
- Creates the weather_stats table in the database using the create_weather_stats_table() function
- Calculates weather statistics using the calculate_weather_stats() function
- Closes the database connection
- The script logs information to a file called weather_data_ingestion.log. The log file contains information about - - The start and end times of the ingestion process, the number of records ingested from each file, and the total time taken to ingest the data.

## Dependencies
- This script requires Python 3.x and the psycopg2 library to be installed. It also assumes that a PostgreSQL database is running and that the user has permission to create tables and insert data into the database. The script expects the weather data files to be stored in a directory called wx_data in the same directory as the script.

## API for Weather Data Retrieval (app.py)
- This Python script provides a RESTful API for retrieving weather data from a PostgreSQL database. It uses Flask to handle HTTP requests and psycopg2 to interact with the database. The API supports pagination and filtering by station ID and date for weather data, and filtering by station ID and year for weather statistics.

## Installation
- Install Python 3.x from the official website
- Install PostgreSQL from the official website
- Install the following Python packages using pip: Flask, Flask-Swagger-UI, psycopg2
- pip install Flask Flask-Swagger-UI psycopg2

## Getting Started
- Clone or download the repository
- Install the required packages as described above
- Open a terminal or command prompt and navigate to the directory containing the script
- Run the script using the command python weather_api.py
- Open a web browser and navigate to http://localhost:5000/api/docs to view the Swagger documentation for the API

## Packages
The following packages are required to run the app:

- Flask
- flask_swagger_ui
- psycopg2

## API Endpoints
- GET /api/weather
- Retrieves weather data from the database. Supports pagination and filtering by station ID and date.
- Example request: http://localhost:5000/api/weather
- GET /api/weather?station_id=USC00110072&year=1985-01-01&offset=0&limit=10
- Using filters
  - http://localhost:5000/api/weather?station_id=USC00110072&date=1985-01-01&offset=0&limit=10

- GET /api/weather/stats
- Retrieves weather statistics data from the database. Supports pagination and filtering by station ID and date.
- Example request: http://localhost:5000/api/weather/stats
- GET /api/weather/stats?station_id=USC00110072&year=1985&offset=0&limit=10
- Using filters
  - http://localhost:5000/api/weather/stats?station_id=USC00110072&date=1985&offset=0&limit=10

## How to Run
- python app.py or python3 app.py
- This will start the Flask development server and serve the API on http://localhost:5000
- Enter this url on web for example: chrome -  http://localhost:5000/api/weather/stats and you can see a json response on the web for weather stats data.
- Enter this url on web for example: chrome -  http://localhost:5000/api/weather and you can see a json response on the web for weather data.
- Using filters
  -  http://localhost:5000/api/weather/stats?station_id=USC00110072&date=1985&offset=0&limit=10 for weather stats data on web.
  - http://localhost:5000/api/weather?station_id=USC00110072&date=1985-01-01&offset=0&limit=10 for weatrher data on web.

## Testing (app_test.py)
- This Python script provides unit tests for testing the Flask API created in the app_test.py file. The script uses the built-in unittest module to define and run tests on the API endpoints. The tests check whether the API returns a valid response and whether the response includes the expected data.

## Installation

- The test script requires the same installation requirements as the Flask API itself. Please refer to the Flask API's installation section for more information.

## Getting Started

- Clone or download the repository
- Install the required packages as described in the Flask API's installation section
- Open a terminal or command prompt and navigate to the directory containing the script
- Run the script using the command python app_test.py or python3 app_test.py

## API Endpoints Tested

- GET /api/weather
- GET /api/weather/stats

## Running the tests

- Open a terminal or command prompt and navigate to the directory containing the script
Run the script using the command python app_test.py or python3 app_test.py
If all tests pass, you should see an output similar to the following:

Ran 2 tests in 0.123s
OK
If any of the tests fail, you will see an error message indicating which tests failed and why.

## DEPLOYMENT STEPS ON AWS CLOUD CONTAINERIZING THE API
### BETTER APPROACH
- Containerize the API: You can use Docker to containerize the API code and its dependencies.

- Set up a database: You can use Amazon Relational Database Service (RDS) to create a managed relational database for storing the data. Choose a database engine that is compatible with your application, such as MySQL or PostgreSQL.

- Create an AWS Elastic Container Service (ECS) cluster: An ECS cluster is a logical grouping of ECS tasks that run on a group of container instances. You can create an ECS cluster and specify the number of container instances to launch. ECS allows you to easily manage and scale containerized applications.

- Deploy the containerized API to ECS: You can use Amazon Elastic Container Registry (ECR) to store your Docker images and then deploy the API to ECS using Amazon Elastic Container Service (ECS). ECS allows you to easily manage and scale containerized applications.

- Create an Amazon CloudWatch Events rule: CloudWatch Events allow you to schedule your data ingestion code to run on a schedule. You can create a rule to trigger a Lambda function to run at a specific time interval or pattern.

- Deploy the data ingestion code as a scheduled Lambda function: You can use AWS Lambda to run the data ingestion code as a serverless function. Lambda can be scheduled to run at a specific time interval or pattern using the CloudWatch Events rule created in step 5.

- Set up security: You can use AWS Identity and Access Management (IAM) to manage access to AWS resources. You should set up IAM policies and roles to control access to the ECS cluster, RDS database, and Lambda function.

- Test and monitor: Once the deployment is complete, you should test the API and monitor the resources using CloudWatch. You can use CloudWatch Logs to view logs generated by your API and Lambda function.

## DEPLOYMENT STEPS ON AWS CLOUD WITHOUT CONTAINERIZING THE API (EC2)

- Set up a virtual machine: You can use Amazon Elastic Compute Cloud (EC2) to create a virtual machine to host the API and data ingestion code. Choose an EC2 instance type that meets the requirements of your application.

- Install the necessary software: Install the required software dependencies for your application, such as Python and any necessary libraries. You can use a package manager like apt-get or yum to install these dependencies.

- Set up a database: You can use Amazon Relational Database Service (RDS) to create a managed relational database for storing the data. Choose a database engine that is compatible with your application, such as MySQL or PostgreSQL.

- Deploy the API code: Copy the API code to the EC2 instance and start the application. You can use a process manager like Systemd or Supervisor to manage the API process.

- Create an Amazon CloudWatch Events rule: CloudWatch Events allow you to schedule your data ingestion code to run on a schedule. You can create a rule to trigger a script or a scheduled task to run at a specific time interval or pattern.

- Deploy the data ingestion code: Copy the data ingestion code to the EC2 instance and schedule it to run at the specified time interval using the CloudWatch Events rule created in step 5.

- Set up security: You can use AWS Identity and Access Management (IAM) to manage access to AWS resources. You should set up IAM policies and roles to control access to the EC2 instance and RDS database.

- Test and monitor: Once the deployment is complete, you should test the API and monitor the resources using CloudWatch. You can use CloudWatch Logs to view logs generated by your API and data ingestion code.

## Improvements

- All the packages should be put in requirements.txt
- The requirements.txt should have the libraries being used in the project along with their version
- The DB connection credentials should go in a config.ini file and the secrets should not be exposed in the application. 

