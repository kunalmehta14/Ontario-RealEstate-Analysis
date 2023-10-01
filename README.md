## Ontario Real Estate Data Analysis

### Overview
> Welcome to the Ontario Real Estate Data Analysis project! 
> This repository contains a comprehensive solution for collecting, analyzing, and visualizing real estate data in Ontario, Canada. 
> The project leverages web scraping techniques, Docker Compose for container orchestration, MySQL for data storage, and Jenkins for continuous integration andcontinuous deployment (CI/CD)

### Features
+ #### Data Collection
> A Python worker powered by Scrapy is used to scrape data from various sources, including Zillow, information regarding Ontario's educational institutes, Yelp, and more.
+ #### Dockerized Environment
> Docker Compose is utilized to automate the setup of the scraper worker and MySQL database containers. This ensures a consistent and portable development and deployment environment.
+ #### Database Configuration
> The MySQL container is configured using a SQL script to set up the database schema and associated tables needed to store the collected data. 
> This organized structure simplifies data management and analysis.
+ #### CI/CD Pipeline
> The project includes a Jenkinsfile that defines a CI/CD pipeline.
> This pipeline automates the deployment process to the production server, making it easy to keep your real estate data analysis up to date.

### Architectural Setup

> To ensure the robust operation of the Ontario Real Estate Data Analysis project, the following system architecture is utilized:
> + VMware hypervisor to host virtual machines (VMs). These VMs will serve as the execution environment for your Docker containers and other services.
> + The services has been distributed across VMs and docker container for easier scalability and isolation.
> + Implement Traefik as a reverse proxy service. Traefik can dynamically route incoming requests to the appropriate containers based on hostnames or URL paths. It provides load balancing, SSL termination, and other features crucial for managing containerized applications.
> + Jenkins on a dedicated VM to manage the CI/CD pipeline. Jenkins can automatically build and deploy your application updates to the production server, triggered by changes in the project's repository.
> +  Implement monitoring and logging solutions to track the health and performance of your application. Tools like Prometheus and Grafana to help collect and visualize metrics from Docker containers.
+ ##### System Architecture:
![System Architecture](architecture_design.svg)
+ ##### Crawler Architecture:
![System Architecture](datacrawler_architecture.svg)