// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_host = credentials('forage_host_test')
        credentials_id = 'forage_devops_test'
    }

    stages {
        stage('Ssh to connect test server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    withCredentials([usernamePassword(credentialsId: credentials_id, usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    remote.allowAnyHosts = true
                    remote.user = $USERNAME
                    remote.password = $PASSWORD
                    remote.host = server_host

                     }
                   
                    
                }
            }
        }
        stage('Download latest release') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        
                        if [ ! -d forage_etl ]; then
                            mkdir ./forage_etl
                        fi
                        cd /forage_etl
                        rm -rf src
                        curl -LOk https://github.com/jchemutt/lswms_forage_etl/releases/latest/download/releaseForageEtl.zip
                        unzip -o releaseForageEtl.zip
                        rm -fr releaseForageEtl.zip
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
