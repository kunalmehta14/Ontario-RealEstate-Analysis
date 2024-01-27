### Jenkins Pipeline Groovy Scripts

This directory contains Groovy scripts designed for Jenkins pipelines to facilitate Continuous Integration and Continuous Deployment (CICD) processes. These scripts are integrated into Jenkins instances using Source Code Management (SCM) to streamline automated deployment and spider function runs.

#### Key Features:

##### CICD Automation:
> The scripts in this repository are tailored for CICD purposes, enabling automated deployment from Git to production servers. They are also designed for the automated execution of scrapy spider functions.
##### Script Descriptions:
+ [DataCollectorDeployment](DataCollectorDeployment)
> Used for CICD, it pulls code from the GitHub repository triggered by GitHub webhook events (e.g., pushes to the main branch).
>
> The pipeline then fetches the updated code on the production server, updates the Docker image, and starts the container.
+ [RealEstateSpider](ONRealEstateSpider)
> Initiates the real estate spider function on designated spider nodes.
>
> Configured on the Jenkins instance to run periodically.
+ [WalkscoreSpider](ONWalkscoreSpider)
> Utilizes the walkscore spider to retrieve walkscore information for the collected real estate data.

### Jenkins Architecture
![Jenkins Architecture](jenkins-architecture.svg)
