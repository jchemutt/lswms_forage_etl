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
                    try {
                        echo "Downloading latest release..."
                        sshCommand remote: remote, command: """
                            cd /opt/etlwms
                            rm -rf src
                            curl -LOk https://github.com/jchemutt/lswms_forage_etl/releases/latest/download/releaseForageEtl.zip
                            unzip -o releaseForageEtl.zip
                            rm -fr releaseForageEtl.zip
                        """
                        echo "Download completed."
                    } catch (Exception e) {
                        // Log any errors that occur during download
                        echo "Failed to download latest release: ${e.getMessage()}"
                        error "Failed to download latest release"
                    }
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