## Ontario Real Estate Data Pipeline

### Overview 
> This repository contains a comprehensive solution for collecting real estate data in Ontario, Canada. 
> The project leverages web scraping techniques, Docker Compose for container orchestration, MySQL for data storage, and Jenkins for continuous integration andcontinuous deployment (CI/CD)

### Features

+ #### Dockerized Environment
> Docker Compose is utilized to automate the setup of the scraper worker and MySQL database containers. This ensures a consistent and portable development and deployment environment.
+ #### Database Configuration
> The MySQL container is configured using a SQL script to set up the database schema and associated tables needed to store the collected data. 
> This organized structure simplifies data management and analysis.
+ #### CI/CD Pipeline
> The project includes a Jenkinsfile that defines a CI/CD pipeline.
> This pipeline automates the deployment process to the production server.

### Architectural Setup
> To ensure the robust operation of the Ontario Real Estate Data Pipeline project, the following system architecture is utilized:
> + VMware hypervisor to host virtual machines (VMs). These VMs will serve as the execution environment for your Docker containers and other services.
> + The services has been distributed across VMs and docker container for easier scalability and isolation.
> + Jenkins on a dedicated VM to manage the CI/CD pipeline. Jenkins can automatically build and deploy your application updates to the production server, triggered by changes in the project's repository.
> +  Implement monitoring and logging solutions to track the health and performance of your application. Tools like Prometheus and Grafana to help collect and visualize metrics from Docker containers.

### Setting up the Ontario Real Estate Data Pipeline
> Follow the steps below to setup the Docker container environment:
> + Clone this repository to your local machine:
````
git clone https://github.com/kunalmehta14/Ontario-RealEstate-DataPipeline.git
cd Ontario-RealEstate-DataPipeline
````
> + Build and start the Docker container using Docker Compose:
````
docker compose up -d
````
> + Wait for the containers to start.
> + Initialize the master crawler function:
````
docker exec -i scraperapp python3 /opt/app/spiders/main.py
````
> Note: The scraperapp docker container is configured to send all the crawler functions related logs to Docker stdout. 
>
> Docker management related documentation can be found here: ['Docker Management'](https://github.com/kunalmehta14/scripts-for-systems-admin/blob/master/Linux/docker-management.md 'Docker Management')