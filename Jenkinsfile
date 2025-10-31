pipeline {
    agent any
    
    environment {
        DATABRICKS_HOST = credentials('databricks-host')
        DATABRICKS_TOKEN = credentials('databricks-token')
        WORKSPACE_ROOT = '/Shared/vehicle-maintenance'
    }
    
    stages {
        stage('Validate Notebooks') {
            steps {
                script {
                    // Basic validation of notebook files
                    sh 'python -m json.tool databricks/notebooks/*.ipynb > /dev/null'
                }
            }
        }
        
        stage('Deploy to Databricks') {
            steps {
                script {
                    // Install Databricks CLI
                    sh 'pip install databricks-cli'
                    
                    // Configure Databricks CLI
                    sh """
                        databricks configure --token <<EOF
                        ${DATABRICKS_HOST}
                        ${DATABRICKS_TOKEN}
                        EOF
                    """
                    
                    // Create workspace directory if not exists
                    sh "databricks workspace mkdirs ${WORKSPACE_ROOT}"
                    
                    // Import notebooks
                    sh """
                        for notebook in databricks/notebooks/*.ipynb; do
                            databricks workspace import \$notebook "${WORKSPACE_ROOT}/\$(basename \$notebook)" -l PYTHON -f JUPYTER -o
                        done
                    """
                }
            }
        }
        
        stage('Run Setup Notebook') {
            steps {
                script {
                    // Run the setup notebook to initialize everything
                    def notebook_path = "${WORKSPACE_ROOT}/00_setup"
                    sh """
                        databricks jobs submit --json '{
                            "run_name": "Setup Pipeline",
                            "existing_cluster_id": "\${DATABRICKS_CLUSTER_ID}",
                            "notebook_task": {
                                "notebook_path": "${notebook_path}"
                            }
                        }'
                    """
                }
            }
        }
        
        stage('Validate Pipeline') {
            steps {
                script {
                    // Run a small test ingestion to verify pipeline
                    def test_notebook = "${WORKSPACE_ROOT}/01_bronze_ingestion"
                    sh """
                        databricks jobs submit --json '{
                            "run_name": "Test Ingestion",
                            "existing_cluster_id": "\${DATABRICKS_CLUSTER_ID}",
                            "notebook_task": {
                                "notebook_path": "${test_notebook}",
                                "base_parameters": {
                                    "env": "test"
                                }
                            }
                        }'
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline deployed successfully!'
        }
        failure {
            echo 'Pipeline deployment failed!'
        }
    }
}