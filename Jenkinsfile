pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    credentialsId: 'journalID', 
                    url: 'https://github.com/gopika0003/PersonalJournal.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building project...'
              // Create a virtual environment
                bat 'python -m venv venv'
                // Activate the virtual environment and install dependencies
                bat 'venv\\Scripts\\pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                // Add test execution commands here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                // Add deployment steps here
            }
        }
    }
}