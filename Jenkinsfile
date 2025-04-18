
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout([ 
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[ 
                        url: 'https://github.com/gopika0003/PersonalJournal.git', 
                        credentialsId: 'journalID' 
                    ]] 
                ])
            }
        }

        stage('Build') {
            steps {
                echo 'Building Docker Compose services...'
                bat 'docker-compose -p personaljourna build'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker Compose...'
                bat 'docker-compose -p personaljournal up -d'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                bat 'docker-compose -p personaljourna run --rm web pytest tests/'
            }
        }
    }
}