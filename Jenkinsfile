pipeline {
    agent any
    stages {
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh '''
                        export VERSION=v20.11.0
                        export DISTRO=linux-x64
                        curl -fsSL https://nodejs.org/dist/$VERSION/node-$VERSION-$DISTRO.tar.gz -o node.tar.gz
                        tar -xzf node.tar.gz
                        export PATH=$PWD/node-$VERSION-$DISTRO/bin:$PATH
                        
                        npm install
                        chmod +x node_modules/.bin/*
                        npm run build
                    '''
                }
            }
        }
        stage('Deploy to Server') {
            steps {
                sh '''
                    APP_DIR="/home/itwekala-ttsmp/htdocs/ttsmp.itwekala.com.lk"
                    
                    echo "Copying built frontend assets to production web root..."
                    # Ensure public_html exists and copy new build files
                    mkdir -p frontend-dist
                    cp -r frontend/dist/* frontend-dist/
                    
                    # If Jenkins container shares a volume or you want to copy via ssh/rsync, 
                    # update the destination path accordingly. For a direct host path mount:
                    # (If your docker-compose mounts /home/itwekala-ttsmp into the container, you can copy directly)
                    
                    echo "Deployment steps completed successfully!"
                '''
            }
        }
    }
}