pipeline {
    agent any
    environment {
        DATA_COLLECTOR_IP = credentials('data_collector_ip')
    }
    stages {
        stage('Clone the repo') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    echo 'clone the repo'
                    sh 'rm -fr Ontario-RealEstate-Analysis'
                    sh 'git clone https://github.com/kunalmehta14/Ontario-RealEstate-Analysis.git'
                }
            }
        }
        stage('Deploy it on datacollector server') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sshagent(['data_collector_ssh']) {
                        sh 'ssh -o StrictHostKeyChecking=no -l jenkins $DATA_COLLECTOR_IP "git init /opt/appdir"'
                        sh 'ssh -o StrictHostKeyChecking=no -l jenkins $DATA_COLLECTOR_IP "git config --global --add safe.directory /opt/appdir"'
                        sh 'ssh -o StrictHostKeyChecking=no -l jenkins $DATA_COLLECTOR_IP "git -C /opt/appdir pull https://github.com/kunalmehta14/Ontario-RealEstate-Analysis.git"'
                    }
                }
            }
        }
        stage('Copy Environmental Variables'){
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    withCredentials([file(credentialsId: 'data_collector_env', variable: 'DATA_COLLECTOR_ENV'),
                                file(credentialsId: 'data_collector_docker_env', variable: 'DATA_COLLECTOR_DOCKER_ENV')]) {
                        sshagent(['data_collector_ssh']) {
                            sh 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r $DATA_COLLECTOR_ENV jenkins@$DATA_COLLECTOR_IP:/opt/appdir/scraperapp/app'
                            sh 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -r $DATA_COLLECTOR_DOCKER_ENV jenkins@$DATA_COLLECTOR_IP:/opt/appdir'
                        }
                    }
                }
            }
        }
        stage('Stop Existing Docker Services'){
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sshagent(['data_collector_ssh']) {
                        sh 'ssh -o StrictHostKeyChecking=no -l jenkins $DATA_COLLECTOR_IP "docker stop scraperapp mysql"'
                    }
                }
                
            }
        }
        stage('Remove Existing Docker Services'){
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sshagent(['data_collector_ssh']) {
                        sh 'ssh -o StrictHostKeyChecking=no -l jenkins $DATA_COLLECTOR_IP "docker rm scraperapp mysql"'
                    }
                }
                
            }
        }
        stage('Start Docker Services'){
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sshagent(['data_collector_ssh']) {
                        sh 'ssh -o StrictHostKeyChecking=no -l jenkins $DATA_COLLECTOR_IP "docker compose -f /opt/appdir/docker-compose.yaml up -d --no-deps --build --always-recreate-deps"'
                    }
                }
                
            }
        }
    }
}