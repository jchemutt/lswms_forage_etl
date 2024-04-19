// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {

    agent any

    environment {
        server_host = credentials('forage_host_test')
        credentials_id = 'forage_devops_test'
    }

    stages {
        stage('Ssh to connect bigelow server') {
            steps {
                script {
                    // Set up remote SSH connection parameters
                    def credentials = usernamePassword(credentialsId: credentials_id, usernameVariable: 'username', passwordVariable: 'password')
                    remote.allowAnyHosts = true
                    remote.user = credentials.username
                    remote.password = credentials.password
                    remote.host = server_host
                    
                }
            }
        }
        stage('Download latest release and create enviroment') {
            steps {
                script {
                    sshCommand remote: remote, command: """
                        
                        if [ ! -d api_WP ]; then
                            mkdir ./api_WP
                        fi
                        cd /api_WP
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
