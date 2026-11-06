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
                        
                        # Grant execution permissions to local node binaries
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