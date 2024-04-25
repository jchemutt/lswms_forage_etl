// Define an empty map for storing remote SSH connection parameters
def remote = [:]

pipeline {
    agent any

    environment {
        server_name = credentials('forage_etl_name')
        server_host = credentials('forage_etl_host')
        ssh_key = credentials('forage_etl_devops')
    }

    stages {
        stage('Ssh to connect server') {
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
                        cd /opt/etlwms
                        rm -rf src
                        curl -LOk https://github.com/jchemutt/lswms_forage_etl/releases/latest/download/releaseForageEtl.zip
                        unzip -o releaseForageEtl.zip
                        rm -fr releaseForageEtl.zip
                        
                        # Copy secret files from Jenkins credentials to the remote server
                        withCredentials([file(credentialsId: 'forage_etl_data_file', variable: 'DATA_FILE'),
                                         file(credentialsId: 'forage_etl_gee_file', variable: 'GEE_FILE')]) {
                            sh "scp -i ${ssh_key} \${DATA_FILE} ${ssh_key_USR}@${server_host}:/opt/etlwms/src/data.json"
                            sh "scp -i ${ssh_key} \${GEE_FILE} ${ssh_key_USR}@${server_host}:/opt/etlwms/src/private_key.json"
                            
                        }
                
                    """
                }
            }
        }
    }

    post {
        failure {
            script {
                echo 'Fail: ETL deployment unsuccessful'
            }
        }

        success {
            script {
                echo 'Success: ETL deployment successful'
            }
        }
    }
}