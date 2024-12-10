pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                sh '''
                    # Create and activate a virtual environment with Python 3.x (compatible version)
                    python3 -m venv mlipproj
                    . mlipproj/bin/activate

                    # Upgrade pip and setuptools
                    pip install --upgrade pip setuptools wheel

                    # Install numpy separately if needed to avoid build issues
                    pip install numpy==1.26.0

                    # Install coverage
                    pip install coverage

                    # Install remaining dependencies from requirements.txt using PEP 517 installer option
                    pip install -r requirements.txt --use-pep517 || {
                        echo "requirements.txt not found, installing manually"
                        pip install pandas scikit-learn pytest flask kafka-python scikit-surprise
                    }
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    # Activate the virtual environment
                    . mlipproj/bin/activate

                    export PYTHONPATH='/var/lib/jenkins/workspace/Milestone2'

                    # Run tests using pytest
                    # pytest --maxfail=1 --disable-warnings
                    coverage run -m pytest --continue-on-collection-errors || true

                    # Print out coverage
                    coverage report || true

                    # Create coverage HTML
                    coverage html || true
                '''
            }
        }

        stage('Publish Coverage Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'HTML Coverage Report'
                ])
            }
        }

        // stage('Build Docker Image') {
        //     steps {
        //         sh '''
        //             # Navigate to the flask_app directory
        //             cd flask_app

        //             # Build the Docker image
        //             docker build -t flask_app_image:latest .
        //         '''
        //     }
        // }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "Deployment goes here."
                '''
            }
        }
    }
}
