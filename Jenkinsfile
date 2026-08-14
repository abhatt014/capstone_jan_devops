pipeline {
    agent {"dev"}
    environment {
        IMAGE_C = 'docker.io/amitfreeze/cart_service'
        IMAGE_CAT = 'docker.io/amitfreeze/catalog_service'
        IMAGE_F = 'docker.io/amitfreeze/frontend'
        IMAGE_O = 'docker.io/amitfreeze/order_service'
        TAG = "${env.BUILD_NUMBER}"
    }
    stages {

        stage('build') {
            steps {
                sh 'docker build -t "$IMAGE_C:$TAG" -t "$IMAGE_C:latest" ./cart_service'
                sh 'docker build -t "$IMAGE_CAT:$TAG" -t "$IMAGE_CAT:latest" ./catalog_service'
                sh 'docker build -t "$IMAGE_F:$TAG" -t "$IMAGE_F:latest" ./frontend'
                sh 'docker build -t "$IMAGE_O:$TAG" -t "$IMAGE_O:latest" ./order_service'

            }    
            
        }
        stage('push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKERHUB_PWD', usernameVariable: 'DOCKERHUB_USER')]) {
                    sh 'echo "$DOCKERHUB_PWD" | docker login -u $DOCKERHUB_USER --password-stdin'
                    sh 'docker push "$IMAGE_C:$TAG"'
                    sh 'docker push "$IMAGE_C:latest"'
                    sh 'docker push "$IMAGE_CAT:$TAG"'
                    sh 'docker push "$IMAGE_CAT:latest"'
                    sh 'docker push "$IMAGE_F:$TAG"'
                    sh 'docker push "$IMAGE_F:latest"'
                    sh 'docker push "$IMAGE_O:$TAG"'
                    sh 'docker push "$IMAGE_O:latest"'
                }

            }
            
        }
        stage('deploy') {
            steps {
                sh 'docker pull "$IMAGE_C:latest"'
                sh 'docker pull "$IMAGE_CAT:latest"'
                sh 'docker pull "$IMAGE_F:latest"'
                sh 'docker pull "$IMAGE_O:latest"'
                sh 'docker rm -f frontend || true'
                sh 'docker rm -f catalog || true'
                sh 'docker rm -f cart || true'
                sh 'docker rm -f order || true'
                sh 'docker run -d -p 3306:3306 --name mysql_db -v init.sql:/docker-entrypoint-initdb.d/init.sql:Z mysql:8.0'
                sh 'docker run -d -p 5000:5000 --name frontend "$IMAGE_F:latest"'
                sh 'docker run -d -p 5001:5001 --name catalog "$IMAGE_CAT:latest"'
                sh 'docker run -d -p 5002:5002 --name cart "$IMAGE_C:latest"'
                sh 'docker run -d -p 5003:5003 --name order "$IMAGE_O:latest"'
            }
        }
        stage('test') {
            steps {
                sh 'echo "test app visit http://192.168.81.161:5000"'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}
