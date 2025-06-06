angular.module('app')
    .directive('result', function () {
        return {
            restrict: 'E',
            scope: {
                result: '=' // Receives the pre-merged { nodes, connections }
            },
            templateUrl: 'result/result.template.html?v=' + Date.now(),
            controller: ['$scope', function ($scope) {

                // Initialize zoom functionality (matching main flowchart pattern)
                $scope.scale = 1;
                const minScale = 0.3; // Allow more zoom out than main flowchart
                const maxScale = 3;   // Allow more zoom in than main flowchart

                // Deployment icons functionality
                $scope.gcpDeploymentIcons = {
                    "Access Context Manager": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "AlloyDB": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Anthos": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Anthos Config Management": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Anthos Service Mesh": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "API Gateway": "../assets/deploy-icons/gcp/cloud_api_gateway.png",
                    "Apigee": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "App Engine": "../assets/deploy-icons/gcp/app_engine.png",
                    "Artifact Registry": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Assured Workloads": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "AutoML": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Backup and DR": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Bare Metal Solution": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Batch": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "BeyondCorp": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "BigQuery": "../assets/deploy-icons/gcp/bigquery.png",
                    "BigQuery Data Transfer Service": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "BigQuery ML": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "BigQuery Omni": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Binary Authorization": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Certificate Authority Service": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Certificate Manager": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Chronicle": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Armor": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Asset Inventory": "../assets/deploy-icons/gcp/cloud_asset_inventory.png",
                    "Cloud Billing": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Bigtable": "../assets/deploy-icons/gcp/bigtable.png",
                    "Cloud Build": "../assets/deploy-icons/gcp/cloud_build.png",
                    "Cloud CDN": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Code": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Composer": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Data Catalog": "../assets/deploy-icons/gcp/data_catalog.png",
                    "Cloud Data Fusion": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Data Loss Prevention": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Dataflow": "../assets/deploy-icons/gcp/dataflow.png",
                    "Cloud Dataprep": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Datastore": "../assets/deploy-icons/gcp/datastore.png",
                    "Cloud Deploy": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Deployment Manager": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud DNS": "../assets/deploy-icons/gcp/cloud_dns.png",
                    "Cloud Domains": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Endpoints": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Functions": "../assets/deploy-icons/gcp/cloud_functions.png",
                    "Cloud Healthcare API": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud IAM": "../assets/deploy-icons/gcp/identity_and_access_management.png",
                    "Cloud IDS": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Interconnect": "../assets/deploy-icons/gcp/cloud_interconnect.png",
                    "Cloud Key Management Service": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Load Balancing": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Logging": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Monitoring": "../assets/deploy-icons/gcp/cloud_monitoring.png",
                    "Cloud NAT": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Natural Language": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Resource Manager": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Router": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Run": "../assets/deploy-icons/gcp/cloud_run.png",
                    "Cloud Scheduler": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Security Command Center": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Shell": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Spanner": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud SQL": "../assets/deploy-icons/gcp/cloud_sql.png",
                    "Cloud Storage": "../assets/deploy-icons/gcp/cloud_storage.png",
                    "Cloud Tasks": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud TPU": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Translation": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Video Intelligence": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud Vision": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Cloud VPN": "../assets/deploy-icons/gcp/cloud_vpn.png",
                    "Cloud Workstations": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Compute Engine": "../assets/deploy-icons/gcp/compute_engine.png",
                    "Connectors": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Contact Center AI": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Container Registry": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Data Catalog": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Database Migration Service": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Dataflow": "../assets/deploy-icons/gcp/dataflow.png",
                    "Dataform": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Dataplex": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Dataprep": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Dataproc": "../assets/deploy-icons/gcp/dataproc.png",
                    "Dataproc Metastore": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Datastream": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Deep Learning Containers": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Deep Learning VM Image": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Dialogflow": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Document AI": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Error Reporting": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Eventarc": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Filestore": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Authentication": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Cloud Messaging": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Crashlytics": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Hosting": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Realtime Database": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Remote Config": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firebase Test Lab": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Firestore": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Fleet Engine": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Game Servers": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "GKE Autopilot": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Google Cloud Marketplace": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Google Distributed Cloud": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Google Distributed Cloud Edge": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Google Drive/Docs": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Google Kubernetes Engine (GKE)": "../assets/deploy-icons/gcp/google_kubernetes_engine.png",
                    "Google Maps Platform": "../assets/deploy-icons/gcp/google_maps_platform.png",
                    "Identity and Access Management": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Identity-Aware Proxy": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Intelligence Suite": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "IoT Core": "../assets/deploy-icons/gcp/iot_core.png",
                    "Looker": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Looker Studio": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Managed Service for Microsoft Active Directory": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Media Translation": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Memorystore": "../assets/deploy-icons/gcp/memorystore.png",
                    "Migrate to Containers": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Migrate to Virtual Machines": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Network Connectivity Center": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Network Intelligence Center": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Network Security": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Operations Suite": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Organization Policy": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Persistent Disk": "../assets/deploy-icons/gcp/persistent_disk.png",
                    "Policy Intelligence": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Private Google Access": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Private Service Connect": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Pub/Sub": "../assets/deploy-icons/gcp/pubsub.png",
                    "Recommendations AI": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Resource Manager": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "reCAPTCHA Enterprise": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Secret Manager": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Security Command Center": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Sensitive Data Protection": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Service Directory": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Service Mesh": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Service Usage": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Speech-to-Text": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Storage Transfer Service": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Text-to-Speech": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Traffic Director": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Transfer Appliance": "../assets/deploy-icons/gcp/transfer_appliance.png",
                    "Vertex AI": "../assets/deploy-icons/gcp/vertexai.png",
                    "Vertex AI Forecasting": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Vertex AI Matching Engine": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Vertex AI Pipelines": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Vertex AI Workbench": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Video Intelligence": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Virtual Private Cloud": "../assets/deploy-icons/gcp/virtual_private_cloud.png",
                    "VMware Engine": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Web Risk": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Web Security Scanner": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Workflows": "../assets/deploy-icons/gcp/gcp-default-icon.svg",
                    "Workspace": "../assets/deploy-icons/gcp/gcp-default-icon.svg"
                };

                $scope.awsDeploymentIcons = {
                    "Amazon API Gateway": "../assets/deploy-icons/aws/Arch_Amazon-API-Gateway_64.png",
                    "Amazon AppStream 2.0": "../assets/deploy-icons/aws/Arch_Amazon-AppStream_64.png",
                    "Amazon Aurora": "../assets/deploy-icons/aws/Arch_Amazon-Aurora_64.png",
                    "Amazon CloudWatch": "../assets/deploy-icons/aws/Arch_Amazon-CloudWatch_64.png",
                    "Amazon Cognito": "../assets/deploy-icons/aws/Arch_Amazon-Cognito_64.png",
                    "Amazon DocumentDB": "../assets/deploy-icons/aws/Arch_Amazon-DocumentDB_64.png",
                    "Amazon DynamoDB": "../assets/deploy-icons/aws/Arch_Amazon-DynamoDB_64.png",
                    "Amazon EC2 Auto Scaling": "../assets/deploy-icons/aws/Arch_Amazon-EC2-Auto-Scaling_64.png",
                    "Amazon Elastic Block Store": "../assets/deploy-icons/aws/Arch_Amazon-Elastic-Block-Store_64.png",
                    "Amazon ElastiCache": "../assets/deploy-icons/aws/Arch_Amazon-ElastiCache_64.png",
                    "Amazon EMR": "../assets/deploy-icons/aws/Arch_Amazon-EMR_64.png",
                    "Amazon Forecast": "../assets/deploy-icons/aws/Arch_Amazon-Forecast_64.png",
                    "Amazon Kinesis Data Steam": "../assets/deploy-icons/aws/Arch_Amazon-Kinesis-Data-Streams_64.png",
                    "Amazon Kinesis Video Streams": "../assets/deploy-icons/aws/Arch_Amazon-Kinesis-Video-Streams_64.png",
                    "Amazon Lightsail": "../assets/deploy-icons/aws/Arch_Amazon-Lightsail_64.png",
                    "Amazon Location Service": "../assets/deploy-icons/aws/Arch_Amazon-Location-Service_64.png",
                    "Amazon MemoryDB": "../assets/deploy-icons/aws/Arch_Amazon-MemoryDB-for-Redis_64.png",
                    "Amazon Pinpoint": "../assets/deploy-icons/aws/Arch_Amazon-Pinpoint_64.png",
                    "Amazon RDS": "../assets/deploy-icons/aws/Arch_Amazon-RDS_64.png",
                    "Amazon Route 53": "../assets/deploy-icons/aws/Arch_Amazon-Route-53_64.png",
                    "Amazon SageMaker": "../assets/deploy-icons/aws/Arch_Amazon-SageMaker_64.png",
                    "Amazon Simple Notification Service": "../assets/deploy-icons/aws/Arch_Amazon-Simple-Notification-Service_64.png",
                    "Amazon Simple Storage Service (Amazon S3)": "../assets/deploy-icons/aws/Arch_Amazon-Simple-Storage-Service_64.png",
                    "Amazon Timestream": "../assets/deploy-icons/aws/Arch_Amazon-Timestream_64.png",
                    "Amazon Virtual Private Cloud": "../assets/deploy-icons/aws/Arch_Amazon-Virtual-Private-Cloud_64.png",
                    "Amazon WorkDocs": "../assets/deploy-icons/aws/Arch_Amazon-WorkDocs_64.png",
                    "Amazon WorkLink": "../assets/deploy-icons/aws/Arch_Amazon-WorkLink_64.png",
                    "Amazon WorkMail": "../assets/deploy-icons/aws/Arch_Amazon-WorkMail_64.png",
                    "Amazon WorkSpaces Family": "../assets/deploy-icons/aws/Arch_Amazon-WorkSpaces_64.png",
                    "AWS Amplify": "../assets/deploy-icons/aws/Arch_AWS-Amplify_64.png",
                    "AWS App Runner": "../assets/deploy-icons/aws/Arch_AWS-App-Runner_64.png",
                    "AWS CodeBuild": "../assets/deploy-icons/aws/Arch_AWS-CodeBuild_64.png",
                    "AWS CodeDeploy": "../assets/deploy-icons/aws/Arch_AWS-CodeDeploy_64.png",
                    "AWS CodePipeline": "../assets/deploy-icons/aws/Arch_AWS-CodePipeline_64.png",
                    "AWS Compute Optimizer": "../assets/deploy-icons/aws/Arch_AWS-Compute-Optimizer_64.png",
                    "AWS Config": "../assets/deploy-icons/aws/Arch_AWS-Config_64.png",
                    "AWS Data Exchange": "../assets/deploy-icons/aws/Arch_AWS-Data-Exchange_64.png",
                    "AWS DataSync": "../assets/deploy-icons/aws/Arch_AWS-DataSync_64.png",
                    "AWS Device Farm": "../assets/deploy-icons/aws/Arch_AWS-Device-Farm_64.png",
                    "AWS Direct Connect": "../assets/deploy-icons/aws/Arch_AWS-Direct-Connect_64.png",
                    "AWS EC2": "../assets/deploy-icons/aws/Arch_Amazon-EC2_64.png",
                    "AWS Elastic Beanstalk": "../assets/deploy-icons/aws/Arch_AWS-Elastic-Beanstalk_64.png",
                    "AWS Glue": "../assets/deploy-icons/aws/Arch_AWS-Glue_64.png",
                    "AWS Identity and Access Management": "../assets/deploy-icons/aws/Arch_AWS-Identity-and-Access-Management_64.png",
                    "AWS IoT Analytics": "../assets/deploy-icons/aws/Arch_AWS-IoT-Analytics_64.png",
                    "AWS IoT Device Management": "../assets/deploy-icons/aws/Arch_AWS-IoT-Device-Management_64.png",
                    "AWS IoT SiteWise": "../assets/deploy-icons/aws/Arch_AWS-IoT-SiteWise_64.png",
                    "AWS Lambda": "../assets/deploy-icons/aws/Arch_AWS-Lambda_64.png",
                    "AWS Private 5G": "../assets/deploy-icons/aws/Arch_AWS-Private-5G_64.png",
                    "AWS Serverless Application Repository": "../assets/deploy-icons/aws/Arch_AWS-Serverless-Application-Repository_64.png",
                    "AWS Systems Manager": "../assets/deploy-icons/aws/Arch_AWS-Systems-Manager_64.png",
                    "AWS Transfer Family": "../assets/deploy-icons/aws/Arch_AWS-Transfer-Family_64.png",
                    "AWS Transit Gateway": "../assets/deploy-icons/aws/Arch_AWS-Transit-Gateway_64.png",
                    "Greengrass - Bluetooth IoT Gateway": "../assets/deploy-icons/aws/Arch_AWS-IoT-Greengrass_64.png",
                    "Greengrass - InfluxDB": "../assets/deploy-icons/aws/Arch_AWS-IoT-Greengrass_64.png",
                    "Greengrass - ML Inference": "../assets/deploy-icons/aws/Arch_AWS-IoT-Greengrass_64.png",
                    "Greengrass - Postgresql DB": "../assets/deploy-icons/aws/Arch_AWS-IoT-Greengrass_64.png",
                    "Tensorflow on AWS": "../assets/deploy-icons/aws/Arch_TensorFlow-on-AWS_64.png",
                    "Greengrass - Stream Manager": "../assets/deploy-icons/aws/Arch_AWS-IoT-Greengrass_64.png"
                }

                $scope.handleWheel = function (event) {
                    event.preventDefault(); // Prevent the default scroll behavior
                    if (event.originalEvent.deltaY < 0) {
                        $scope.zoomIn();
                    } else {
                        $scope.zoomOut();
                    }
                    // Note: $apply() is handled by the onWheel directive, no need to call it here
                };

                $scope.zoomIn = function () {
                    if ($scope.scale < maxScale) {
                        $scope.scale += 0.07; // Same increment as main flowchart
                    }
                };

                $scope.zoomOut = function () {
                    if ($scope.scale > minScale) {
                        $scope.scale -= 0.07; // Same decrement as main flowchart
                    }
                };

                $scope.resetZoom = function () {
                    $scope.scale = 1;
                };

                $scope.$watch('result', function (newVal) {
                    // Validate input
                    if (!newVal || !Array.isArray(newVal.nodes) || !Array.isArray(newVal.connections)) {
                        $scope.staticChart = null;
                        console.err('[result] Invalid or incomplete data (missing nodes or connections array), setting staticChart to null.');
                        return;
                    }

                    // Use the pre-merged data directly
                    $scope.staticChart = new flowchart.ChartViewModel(newVal);

                    // Reset the icons for all nodes
                    $scope.staticChart.nodes.forEach(function (node) {
                        node.data.icon = ''; // Reset icon to empty string
                    });
                    // Assign an icon to each node based on the name of the service assigned to it
                    $scope.staticChart.nodes.forEach(function (node) {
                        if ($scope.hasBestService(node)) {
                            const serviceName = node.data.best_service;
                            if ($scope.isGcpService(serviceName)) {
                                node.data.icon = $scope.gcpDeploymentIcons[serviceName];
                            } else if ($scope.isAwsService(serviceName)) {
                                node.data.icon = $scope.awsDeploymentIcons[serviceName];
                            }
                        } else {
                            node.data.icon = ''; // No icon if no best service is assigned
                        }
                        console.log(node.data.icon);
                    });
                }, true);

                $scope.hasBestService = function (node) {
                    return node && node.data && node.data.best_service;
                };

                $scope.isGcpService = function (serviceName) {
                    if ($scope.gcpDeploymentIcons[serviceName]) {
                        return true;
                    }
                    return false;
                }

                $scope.isAwsService = function (serviceName) {
                    if ($scope.awsDeploymentIcons[serviceName]) {
                        return true;
                    }
                    return false;
                };
            }]
        };
    });
