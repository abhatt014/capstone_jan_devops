pipeline {
    // using dev env
    agent { label 'dev' }
    
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
        stage('Update Manifests in Git') {
            when { branch 'main' }
            steps {
                // 1. Update the tags in the YAML files using standard sed
                sh '''
                    sed -i "s|image: docker.io/amitfreeze/cart_service:.*|image: docker.io/amitfreeze/cart_service:${BUILD_NUMBER}|g" k8s_specifications/cart.yaml
                    sed -i "s|image: docker.io/amitfreeze/catalog_service:.*|image: docker.io/amitfreeze/catalog_service:${BUILD_NUMBER}|g" k8s_specifications/catalog.yaml
                    sed -i "s|image: docker.io/amitfreeze/order_service:.*|image: docker.io/amitfreeze/order_service:${BUILD_NUMBER}|g" k8s_specifications/order.yaml
                    sed -i "s|image: docker.io/amitfreeze/frontend:.*|image: docker.io/amitfreeze/frontend:${BUILD_NUMBER}|g" k8s_specifications/frontend.yaml
                '''
                
                // 2. Commit and push the changes back to GitHub
                withCredentials([usernamePassword(credentialsId: 'github', passwordVariable: 'GIT_TOKEN', usernameVariable: 'GIT_USER')]) {
                    sh '''
                        git config user.name "student"
                        git config user.email "student@example.com.com"
                        
                        git add k8s_specifications/*.yaml
                        
                        # Only commit if there are actually changes
                        if ! git diff-index --quiet HEAD --; then
                            # The [skip ci] tag prevents Jenkins from running the pipeline again in an infinite loop
                            git commit -m "Update image tags to build ${BUILD_NUMBER} [skip ci]"
                            git push https://${GIT_USER}:${GIT_TOKEN}@github.com/abhatt014/capstone_jan_devops.git HEAD:main
                        else
                            echo "No changes to commit"
                        fi
                    '''
                }
            }
        }
        stage('Cleanup Local Jenkins Images') {
            steps {
                sh '''
                    # Calculate the previous build number
                    PREV_BUILD=$((BUILD_NUMBER - 1))
                    
                    echo "Deleting local images from build ${PREV_BUILD}..."
                    
                    # The '|| true' ensures the pipeline doesn't fail if the image was already deleted
                    docker rmi docker.io/amitfreeze/cart_service:${PREV_BUILD} || true
                    docker rmi docker.io/amitfreeze/catalog_service:${PREV_BUILD} || true
                    docker rmi docker.io/amitfreeze/order_service:${PREV_BUILD} || true
                    docker rmi docker.io/amitfreeze/frontend:${PREV_BUILD} || true
                    
                    # Clean up any dangling unused layers
                    docker image prune -f
                '''
            }
        }        
        // stage('deploy') {
        //
        //     steps {
        //         sh 'docker pull "$IMAGE_C:latest"'
        //         sh 'docker pull "$IMAGE_CAT:latest"'
        //         sh 'docker pull "$IMAGE_F:latest"'
        //         sh 'docker pull "$IMAGE_O:latest"'
                
        //         // 1. Clean up ALL previous containers including the database
        //         sh 'docker rm -f frontend catalog cart order mysql_db || true'
                
        //         // 2. Create a custom network for container-to-container communication
        //         sh 'docker network create ecommerce_net || true'
                
        //         // 3. Start Database with the required password variable and attach to network
        //         sh 'docker run -d --network ecommerce_net -p 3306:3306 -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=ecomm_db --name mysql_db -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql:z mysql:8.0'
                
        //         // Wait briefly to give MySQL time to initialize before the APIs try to connect
        //         sh 'sleep 15'
                
        //         // 4. Start Microservices - Map external ports to internal port 5000 and attach to network
        //         sh 'docker run -d --network ecommerce_net -p 5000:5000 --name frontend "$IMAGE_F:latest"'
        //         sh 'docker run -d --network ecommerce_net -p 5001:5000 --name catalog "$IMAGE_CAT:latest"'
        //         sh 'docker run -d --network ecommerce_net -p 5002:5000 --name cart "$IMAGE_C:latest"'
        //         sh 'docker run -d --network ecommerce_net -p 5003:5000 --name order "$IMAGE_O:latest"'
        //     }
        // }
        
        // stage('test') {
        //     steps {
        //         sh 'echo "test app visit http://192.168.81.161:5000"'
        //     }
        // }
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
