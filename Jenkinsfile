// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_host = credentials('forage_host_test')
        server_name = credentials('forage_test_name')
        ssh_key = credentials('forage_etl_devops')
        
    }

    stages {
        stage('Ssh to connect test server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    
                    remote.allowAnyHosts = true
                    remote.identityFile = ssh_key
                    remote.user = ssh_key_USR
                    remote.name = server_name
                    remote.host = server_host
                    
                }
            }
        }
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                       
                    mkdir ~/forage_etl
                        
                    """
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
