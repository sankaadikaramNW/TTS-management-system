pipeline {
    agent any
    stages {
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh '''
                        # Download and install Node.js locally for this build if missing
                        export VERSION=v20.11.0
                        export DISTRO=linux-x64
                        curl -fsSL https://nodejs.org/dist/$VERSION/node-$VERSION-$DISTRO.tar.xz -o node.tar.xz
                        tar -xJf node.tar.xz
                        export PATH=$PWD/node-$VERSION-$DISTRO/bin:$PATH
                        
                        npm install
                        npm run build
                    '''
                }
            }
        }
        stage('Deploy to Server') {
            steps {
                sh '''
                    APP_DIR="/home/itwekala-ttsmp/htdocs/ttsmp.itwekala.com.lk"
                    cd $APP_DIR
                    git pull origin main
                    
                    # Update backend virtual environment
                    source venv/bin/activate
                    pip install -r requirements.txt
                    
                    # Copy frontend build assets to CloudPanel public root
                    rm -rf public_html/*
                    cp -r frontend/dist/* public_html/
                    
                    # Reload Nginx safely
                    sudo systemctl reload nginx
                '''
            }
        }
    }
}