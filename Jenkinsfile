pipeline {
    agent any
    tools {
        nodejs 'node' // Matches the name of the Node.js installation in Global Tool Configuration
    }
    stages {
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                    sh 'npm run build'
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