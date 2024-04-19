// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_host = credentials('forage_host_test')
        user = credentials('forage_test_user')
        password = credentials('forage_test_pass')
        
    }

    stages {
        stage('Ssh to connect test server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    
                    remote.allowAnyHosts = true
                    remote.user = user
                    remote.password = password
                    remote.host = server_host
                    
                }
            }
        }
        stage('Download latest release') {
            steps {
                script {
                    def sshCommand = "sshpass -p '${password}' ssh -o StrictHostKeyChecking=no ${user}@${server_host} '
                    echo Hello, World!'"
                    
                    // Execute the SSH command
                    sh sshCommand
                }
            }
        }
        
          
    }
    
    post {
        failure {
            script {
                echo 'fail'
            }
        }

        success {
            script {
                echo 'everything went very well, api in production'
            }
        }
    }
 
}
