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
                    sshCommand remote: remote, command: """
                        
                        if [ ! -d /home/admin01/forage_etl ]; then
                            mkdir ./home/admin01/forage_etl
                        fi
                        cd /home/admin01/forage_etl
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
