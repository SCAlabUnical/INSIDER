#!/bin/bash

# Test the advise endpoint
echo "Testing advise endpoint..."

# Define a minimal workflow for testing
sample_result='
{
    "result": [
        {
            "abstractservice_id": 0,
            "abstractservice_name": "Web Interface",
            "abstractservice_type": "Communication",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Integration", "Messaging"],
            "aws_services": [
                {
                    "service_id": "20",
                    "service_name": "Amazon Route 53",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["DNS", "Networking", "Scalable", "Highly Available", "Managed"]
                },
                {
                    "service_id": "25",
                    "service_name": "Amazon Virtual Private Cloud",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["VPC", "Networking", "Isolation", "Security", "Scalability"]
                },
                {
                    "service_id": "54",
                    "service_name": "Greengrass - Bluetooth IoT Gateway",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Managed", "Scalability"]
                },
                {
                    "service_id": "59",
                    "service_name": "Greengrass - Stream Manager",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Streaming", "Scalability"]
                },
                {
                    "service_id": "1",
                    "service_name": "Amazon API Gateway ",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "API Management",
                        "Serverless",
                        "Security",
                        "Integration",
                        "RESTful"
                    ]
                },
                {
                    "service_id": "18",
                    "service_name": "Amazon Pinpoint",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Customer Engagement",
                        "Messaging",
                        "Email",
                        "SMS",
                        "Push Notifications"
                    ]
                },
                {
                    "service_id": "22",
                    "service_name": "Amazon Simple Notification Service",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": ["Messaging", "A2A", "A2P", "Managed", "Scalability"]
                }
            ]
        },
        {
            "abstractservice_id": 1,
            "abstractservice_name": "Publish-Subscribe Broker",
            "abstractservice_type": "Communication",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Integration", "Messaging"],
            "aws_services": [
                {
                    "service_id": "20",
                    "service_name": "Amazon Route 53",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["DNS", "Networking", "Scalable", "Highly Available", "Managed"]
                },
                {
                    "service_id": "25",
                    "service_name": "Amazon Virtual Private Cloud",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["VPC", "Networking", "Isolation", "Security", "Scalability"]
                },
                {
                    "service_id": "54",
                    "service_name": "Greengrass - Bluetooth IoT Gateway",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Managed", "Scalability"]
                },
                {
                    "service_id": "59",
                    "service_name": "Greengrass - Stream Manager",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Streaming", "Scalability"]
                },
                {
                    "service_id": "1",
                    "service_name": "Amazon API Gateway ",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "API Management",
                        "Serverless",
                        "Security",
                        "Integration",
                        "RESTful"
                    ]
                },
                {
                    "service_id": "18",
                    "service_name": "Amazon Pinpoint",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Customer Engagement",
                        "Messaging",
                        "Email",
                        "SMS",
                        "Push Notifications"
                    ]
                },
                {
                    "service_id": "22",
                    "service_name": "Amazon Simple Notification Service",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": ["Messaging", "A2A", "A2P", "Managed", "Scalability"]
                }
            ]
        },
        {
            "abstractservice_id": 2,
            "abstractservice_name": "Public Event Collector",
            "abstractservice_type": "Computation",
            "abstractservice_layer": "cloud",
            "abstractservice_tags": ["Monitoring", "Observability", "Logs"],
            "aws_services": [
                {
                    "service_id": "2",
                    "service_name": "Amazon AppStream 2.0",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Virtual Applications",
                        "Streaming",
                        "Managed",
                        "Scalability",
                        "Desktop"
                    ]
                },
                {
                    "service_id": "4",
                    "service_name": "Amazon CloudWatch",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["Monitoring", "Observability", "DevOps", "Metrics", "Logs"]
                },
                {
                    "service_id": "5",
                    "service_name": "Amazon Cognito",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Authentication",
                        "Authorization",
                        "User Management",
                        "Security",
                        "Identity"
                    ]
                },
                {
                    "service_id": "8",
                    "service_name": "Amazon EC2 Auto Scaling",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Auto Scaling",
                        "EC2",
                        "Compute",
                        "Availability",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "11",
                    "service_name": "Amazon EMR",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "near-edge", "cloud"],
                    "service_tags": ["Big Data", "Hadoop", "Spark", "Managed", "Scalability"]
                },
                {
                    "service_id": "12",
                    "service_name": "Amazon Forecast",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Forecasting",
                        "Managed",
                        "Scalability",
                        "AI"
                    ]
                },
                {
                    "service_id": "13",
                    "service_name": "Amazon Kinesis Data Steam",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Streaming Data",
                        "Real-Time",
                        "Analytics",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "14",
                    "service_name": "Amazon Kinesis Video Streams",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "cloud"],
                    "service_tags": [
                        "Video Streaming",
                        "Real-Time",
                        "Analytics",
                        "Machine Learning",
                        "Managed"
                    ]
                },
                {
                    "service_id": "15",
                    "service_name": "Amazon Lightsail",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["VPS", "Compute", "Managed", "Scalability", "Cost-Effective"]
                },
                {
                    "service_id": "16",
                    "service_name": "Amazon Location Service",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Location", "Maps", "Geocoding", "Geofencing", "Managed"]
                },
                {
                    "service_id": "21",
                    "service_name": "Amazon SageMaker",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "27",
                    "service_name": "Amazon WorkLink",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Secure Access",
                        "Mobile",
                        "Corporate Websites",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "29",
                    "service_name": "Amazon WorkSpaces Family",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["DaaS", "Desktop", "Secure", "Managed", "Scalability"]
                },
                {
                    "service_id": "30",
                    "service_name": "AWS Amplify",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Full-Stack", "Mobile", "Web", "Secure", "Scalable"]
                },
                {
                    "service_id": "31",
                    "service_name": "AWS App Runner",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Containerized Applications",
                        "APIs",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "32",
                    "service_name": "AWS CodeBuild",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Continuous Integration",
                        "Build",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "33",
                    "service_name": "AWS CodeDeploy",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Deployment",
                        "Automation",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "34",
                    "service_name": "AWS CodePipeline",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Continuous Delivery",
                        "Automation",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "35",
                    "service_name": "AWS Compute Optimizer",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Optimization",
                        "Machine Learning",
                        "Cost Reduction",
                        "Performance",
                        "Managed"
                    ]
                },
                {
                    "service_id": "36",
                    "service_name": "AWS Config",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Configuration",
                        "Audit",
                        "Evaluation",
                        "Managed",
                        "Governance"
                    ]
                },
                {
                    "service_id": "37",
                    "service_name": "AWS Data Exchange",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Data Exchange",
                        "Third-Party Data",
                        "Managed",
                        "Scalability",
                        "Analytics"
                    ]
                },
                {
                    "service_id": "39",
                    "service_name": "AWS Device Farm",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["App Testing", "Android", "iOS", "Web", "Developer Tools"]
                },
                {
                    "service_id": "41",
                    "service_name": "AWS EC2",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["Compute", "Scalable", "Managed", "Cloud", "EC2"]
                },
                {
                    "service_id": "42",
                    "service_name": "AWS Elastic Beanstalk",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Web Applications",
                        "Deployment",
                        "Scaling",
                        "Managed",
                        "Compute"
                    ]
                },
                {
                    "service_id": "43",
                    "service_name": "AWS Glue",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "ETL",
                        "Data Preparation",
                        "Analytics",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "44",
                    "service_name": "AWS Identity and Access Management",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Security",
                        "Identity",
                        "Access Management",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "45",
                    "service_name": "AWS IoT Analytics",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["IoT", "Analytics", "Managed", "Scalability", "Data"]
                },
                {
                    "service_id": "46",
                    "service_name": "AWS IoT Device Management",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "IoT",
                        "Device Management",
                        "Security",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "47",
                    "service_name": "AWS IoT SiteWise",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "cloud"],
                    "service_tags": [
                        "IoT",
                        "Industrial Equipment",
                        "Data Collection",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "48",
                    "service_name": "AWS Lambda",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "cloud"],
                    "service_tags": [
                        "Serverless",
                        "Compute",
                        "Managed",
                        "Scalability",
                        "Cost-Effective"
                    ]
                },
                {
                    "service_id": "50",
                    "service_name": "AWS Serverless Application Repository",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Serverless",
                        "Applications",
                        "Repository",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "51",
                    "service_name": "AWS Systems Manager",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Management", "Governance", "Visibility", "Control", "Managed"]
                },
                {
                    "service_id": "56",
                    "service_name": "Greengrass - ML Inference",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Inference",
                        "Greengrass",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "58",
                    "service_name": "Tensorflow on AWS",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Framework",
                        "Development",
                        "Deployment"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 5,
            "abstractservice_name": "Real-Time Traffic Monitoring (Web)",
            "abstractservice_type": "Computation",
            "abstractservice_layer": "cloud",
            "abstractservice_tags": ["Monitoring", "Observability", "Logs"],
            "aws_services": [
                {
                    "service_id": "2",
                    "service_name": "Amazon AppStream 2.0",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Virtual Applications",
                        "Streaming",
                        "Managed",
                        "Scalability",
                        "Desktop"
                    ]
                },
                {
                    "service_id": "4",
                    "service_name": "Amazon CloudWatch",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["Monitoring", "Observability", "DevOps", "Metrics", "Logs"]
                },
                {
                    "service_id": "5",
                    "service_name": "Amazon Cognito",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Authentication",
                        "Authorization",
                        "User Management",
                        "Security",
                        "Identity"
                    ]
                },
                {
                    "service_id": "8",
                    "service_name": "Amazon EC2 Auto Scaling",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Auto Scaling",
                        "EC2",
                        "Compute",
                        "Availability",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "11",
                    "service_name": "Amazon EMR",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "near-edge", "cloud"],
                    "service_tags": ["Big Data", "Hadoop", "Spark", "Managed", "Scalability"]
                },
                {
                    "service_id": "12",
                    "service_name": "Amazon Forecast",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Forecasting",
                        "Managed",
                        "Scalability",
                        "AI"
                    ]
                },
                {
                    "service_id": "13",
                    "service_name": "Amazon Kinesis Data Steam",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Streaming Data",
                        "Real-Time",
                        "Analytics",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "14",
                    "service_name": "Amazon Kinesis Video Streams",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "cloud"],
                    "service_tags": [
                        "Video Streaming",
                        "Real-Time",
                        "Analytics",
                        "Machine Learning",
                        "Managed"
                    ]
                },
                {
                    "service_id": "15",
                    "service_name": "Amazon Lightsail",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["VPS", "Compute", "Managed", "Scalability", "Cost-Effective"]
                },
                {
                    "service_id": "16",
                    "service_name": "Amazon Location Service",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Location", "Maps", "Geocoding", "Geofencing", "Managed"]
                },
                {
                    "service_id": "21",
                    "service_name": "Amazon SageMaker",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "27",
                    "service_name": "Amazon WorkLink",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Secure Access",
                        "Mobile",
                        "Corporate Websites",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "29",
                    "service_name": "Amazon WorkSpaces Family",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["DaaS", "Desktop", "Secure", "Managed", "Scalability"]
                },
                {
                    "service_id": "30",
                    "service_name": "AWS Amplify",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Full-Stack", "Mobile", "Web", "Secure", "Scalable"]
                },
                {
                    "service_id": "31",
                    "service_name": "AWS App Runner",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Containerized Applications",
                        "APIs",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "32",
                    "service_name": "AWS CodeBuild",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Continuous Integration",
                        "Build",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "33",
                    "service_name": "AWS CodeDeploy",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Deployment",
                        "Automation",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "34",
                    "service_name": "AWS CodePipeline",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Continuous Delivery",
                        "Automation",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "35",
                    "service_name": "AWS Compute Optimizer",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Optimization",
                        "Machine Learning",
                        "Cost Reduction",
                        "Performance",
                        "Managed"
                    ]
                },
                {
                    "service_id": "36",
                    "service_name": "AWS Config",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Configuration",
                        "Audit",
                        "Evaluation",
                        "Managed",
                        "Governance"
                    ]
                },
                {
                    "service_id": "37",
                    "service_name": "AWS Data Exchange",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Data Exchange",
                        "Third-Party Data",
                        "Managed",
                        "Scalability",
                        "Analytics"
                    ]
                },
                {
                    "service_id": "39",
                    "service_name": "AWS Device Farm",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["App Testing", "Android", "iOS", "Web", "Developer Tools"]
                },
                {
                    "service_id": "41",
                    "service_name": "AWS EC2",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["Compute", "Scalable", "Managed", "Cloud", "EC2"]
                },
                {
                    "service_id": "42",
                    "service_name": "AWS Elastic Beanstalk",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Web Applications",
                        "Deployment",
                        "Scaling",
                        "Managed",
                        "Compute"
                    ]
                },
                {
                    "service_id": "43",
                    "service_name": "AWS Glue",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "ETL",
                        "Data Preparation",
                        "Analytics",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "44",
                    "service_name": "AWS Identity and Access Management",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Security",
                        "Identity",
                        "Access Management",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "45",
                    "service_name": "AWS IoT Analytics",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["IoT", "Analytics", "Managed", "Scalability", "Data"]
                },
                {
                    "service_id": "46",
                    "service_name": "AWS IoT Device Management",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "IoT",
                        "Device Management",
                        "Security",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "47",
                    "service_name": "AWS IoT SiteWise",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "cloud"],
                    "service_tags": [
                        "IoT",
                        "Industrial Equipment",
                        "Data Collection",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "48",
                    "service_name": "AWS Lambda",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "cloud"],
                    "service_tags": [
                        "Serverless",
                        "Compute",
                        "Managed",
                        "Scalability",
                        "Cost-Effective"
                    ]
                },
                {
                    "service_id": "50",
                    "service_name": "AWS Serverless Application Repository",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Serverless",
                        "Applications",
                        "Repository",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "51",
                    "service_name": "AWS Systems Manager",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Management", "Governance", "Visibility", "Control", "Managed"]
                },
                {
                    "service_id": "56",
                    "service_name": "Greengrass - ML Inference",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Inference",
                        "Greengrass",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "58",
                    "service_name": "Tensorflow on AWS",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Framework",
                        "Development",
                        "Deployment"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 6,
            "abstractservice_name": "Cyber-Physical Interface",
            "abstractservice_type": "Communication",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Integration", "Messaging"],
            "aws_services": [
                {
                    "service_id": "20",
                    "service_name": "Amazon Route 53",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["DNS", "Networking", "Scalable", "Highly Available", "Managed"]
                },
                {
                    "service_id": "25",
                    "service_name": "Amazon Virtual Private Cloud",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["VPC", "Networking", "Isolation", "Security", "Scalability"]
                },
                {
                    "service_id": "54",
                    "service_name": "Greengrass - Bluetooth IoT Gateway",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Managed", "Scalability"]
                },
                {
                    "service_id": "59",
                    "service_name": "Greengrass - Stream Manager",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Streaming", "Scalability"]
                },
                {
                    "service_id": "1",
                    "service_name": "Amazon API Gateway ",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "API Management",
                        "Serverless",
                        "Security",
                        "Integration",
                        "RESTful"
                    ]
                },
                {
                    "service_id": "18",
                    "service_name": "Amazon Pinpoint",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Customer Engagement",
                        "Messaging",
                        "Email",
                        "SMS",
                        "Push Notifications"
                    ]
                },
                {
                    "service_id": "22",
                    "service_name": "Amazon Simple Notification Service",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": ["Messaging", "A2A", "A2P", "Managed", "Scalability"]
                }
            ]
        },
        {
            "abstractservice_id": 7,
            "abstractservice_name": "Streaming Protocol",
            "abstractservice_type": "Communication",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Integration", "Streaming"],
            "aws_services": [
                {
                    "service_id": "20",
                    "service_name": "Amazon Route 53",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["DNS", "Networking", "Scalable", "Highly Available", "Managed"]
                },
                {
                    "service_id": "25",
                    "service_name": "Amazon Virtual Private Cloud",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["VPC", "Networking", "Isolation", "Security", "Scalability"]
                },
                {
                    "service_id": "54",
                    "service_name": "Greengrass - Bluetooth IoT Gateway",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Managed", "Scalability"]
                },
                {
                    "service_id": "59",
                    "service_name": "Greengrass - Stream Manager",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Streaming", "Scalability"]
                },
                {
                    "service_id": "1",
                    "service_name": "Amazon API Gateway ",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "API Management",
                        "Serverless",
                        "Security",
                        "Integration",
                        "RESTful"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 8,
            "abstractservice_name": "Real-Time Traffic Monitoring (Devices)",
            "abstractservice_type": "Computation",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Monitoring", "Observability", "Logs"],
            "aws_services": [
                {
                    "service_id": "4",
                    "service_name": "Amazon CloudWatch",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["Monitoring", "Observability", "DevOps", "Metrics", "Logs"]
                },
                {
                    "service_id": "8",
                    "service_name": "Amazon EC2 Auto Scaling",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Auto Scaling",
                        "EC2",
                        "Compute",
                        "Availability",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "21",
                    "service_name": "Amazon SageMaker",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "41",
                    "service_name": "AWS EC2",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["Compute", "Scalable", "Managed", "Cloud", "EC2"]
                },
                {
                    "service_id": "56",
                    "service_name": "Greengrass - ML Inference",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Inference",
                        "Greengrass",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "58",
                    "service_name": "Tensorflow on AWS",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Framework",
                        "Development",
                        "Deployment"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 9,
            "abstractservice_name": "Cyber-Physical Interface",
            "abstractservice_type": "Communication",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Integration", "Messaging"],
            "aws_services": [
                {
                    "service_id": "20",
                    "service_name": "Amazon Route 53",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["DNS", "Networking", "Scalable", "Highly Available", "Managed"]
                },
                {
                    "service_id": "25",
                    "service_name": "Amazon Virtual Private Cloud",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["VPC", "Networking", "Isolation", "Security", "Scalability"]
                },
                {
                    "service_id": "54",
                    "service_name": "Greengrass - Bluetooth IoT Gateway",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Managed", "Scalability"]
                },
                {
                    "service_id": "59",
                    "service_name": "Greengrass - Stream Manager",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Streaming", "Scalability"]
                },
                {
                    "service_id": "1",
                    "service_name": "Amazon API Gateway ",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "API Management",
                        "Serverless",
                        "Security",
                        "Integration",
                        "RESTful"
                    ]
                },
                {
                    "service_id": "18",
                    "service_name": "Amazon Pinpoint",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Customer Engagement",
                        "Messaging",
                        "Email",
                        "SMS",
                        "Push Notifications"
                    ]
                },
                {
                    "service_id": "22",
                    "service_name": "Amazon Simple Notification Service",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": ["Messaging", "A2A", "A2P", "Managed", "Scalability"]
                }
            ]
        },
        {
            "abstractservice_id": 11,
            "abstractservice_name": "Taxi Monitoring",
            "abstractservice_type": "Computation",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Monitoring", "Observability", "Logs"],
            "aws_services": [
                {
                    "service_id": "4",
                    "service_name": "Amazon CloudWatch",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["Monitoring", "Observability", "DevOps", "Metrics", "Logs"]
                },
                {
                    "service_id": "8",
                    "service_name": "Amazon EC2 Auto Scaling",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Auto Scaling",
                        "EC2",
                        "Compute",
                        "Availability",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "21",
                    "service_name": "Amazon SageMaker",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "41",
                    "service_name": "AWS EC2",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["Compute", "Scalable", "Managed", "Cloud", "EC2"]
                },
                {
                    "service_id": "56",
                    "service_name": "Greengrass - ML Inference",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Inference",
                        "Greengrass",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "58",
                    "service_name": "Tensorflow on AWS",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Framework",
                        "Development",
                        "Deployment"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 12,
            "abstractservice_name": "Cyber-Physical Interface",
            "abstractservice_type": "Communication",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Integration", "Messaging"],
            "aws_services": [
                {
                    "service_id": "20",
                    "service_name": "Amazon Route 53",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["DNS", "Networking", "Scalable", "Highly Available", "Managed"]
                },
                {
                    "service_id": "25",
                    "service_name": "Amazon Virtual Private Cloud",
                    "service_type": "Communication",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["VPC", "Networking", "Isolation", "Security", "Scalability"]
                },
                {
                    "service_id": "54",
                    "service_name": "Greengrass - Bluetooth IoT Gateway",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Managed", "Scalability"]
                },
                {
                    "service_id": "59",
                    "service_name": "Greengrass - Stream Manager",
                    "service_type": "Communication",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["IoT", "Bluetooth", "Gateway", "Streaming", "Scalability"]
                },
                {
                    "service_id": "1",
                    "service_name": "Amazon API Gateway ",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "API Management",
                        "Serverless",
                        "Security",
                        "Integration",
                        "RESTful"
                    ]
                },
                {
                    "service_id": "18",
                    "service_name": "Amazon Pinpoint",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Customer Engagement",
                        "Messaging",
                        "Email",
                        "SMS",
                        "Push Notifications"
                    ]
                },
                {
                    "service_id": "22",
                    "service_name": "Amazon Simple Notification Service",
                    "service_type": "Communication",
                    "service_layers": ["cloud"],
                    "service_tags": ["Messaging", "A2A", "A2P", "Managed", "Scalability"]
                }
            ]
        },
        {
            "abstractservice_id": 14,
            "abstractservice_name": "Passenger Monitoring",
            "abstractservice_type": "Computation",
            "abstractservice_layer": "far-edge",
            "abstractservice_tags": ["Monitoring", "Observability", "Logs"],
            "aws_services": [
                {
                    "service_id": "4",
                    "service_name": "Amazon CloudWatch",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["Monitoring", "Observability", "DevOps", "Metrics", "Logs"]
                },
                {
                    "service_id": "8",
                    "service_name": "Amazon EC2 Auto Scaling",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Auto Scaling",
                        "EC2",
                        "Compute",
                        "Availability",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "21",
                    "service_name": "Amazon SageMaker",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "41",
                    "service_name": "AWS EC2",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["Compute", "Scalable", "Managed", "Cloud", "EC2"]
                },
                {
                    "service_id": "56",
                    "service_name": "Greengrass - ML Inference",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Inference",
                        "Greengrass",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "58",
                    "service_name": "Tensorflow on AWS",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Framework",
                        "Development",
                        "Deployment"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 15,
            "abstractservice_name": "Web Data Storage",
            "abstractservice_type": "Storage",
            "abstractservice_layer": "cloud",
            "abstractservice_tags": ["Object Storage"],
            "aws_services": [
                {
                    "service_id": "3",
                    "service_name": "Amazon Aurora",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Relational Database",
                        "High Performance",
                        "Managed",
                        "Scalability",
                        "Availability"
                    ]
                },
                {
                    "service_id": "6",
                    "service_name": "Amazon DocumentDB",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Document Database",
                        "MongoDB",
                        "Managed",
                        "Scalability",
                        "Availability"
                    ]
                },
                {
                    "service_id": "7",
                    "service_name": "Amazon DynamoDB",
                    "service_type": "Storage",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "NoSQL",
                        "Key-Value",
                        "Document Database",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "9",
                    "service_name": "Amazon Elastic Block Store",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": [
                        "Block Storage",
                        "EC2",
                        "Persistent Storage",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "10",
                    "service_name": "Amazon ElastiCache",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "near-edge", "cloud"],
                    "service_tags": [
                        "In-Memory Cache",
                        "Redis",
                        "Memcached",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "17",
                    "service_name": "Amazon MemoryDB",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "In-Memory Database",
                        "Redis",
                        "Managed",
                        "Scalability",
                        "Performance"
                    ]
                },
                {
                    "service_id": "19",
                    "service_name": "Amazon RDS",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Relational Database",
                        "Managed",
                        "Scalability",
                        "Availability",
                        "Performance"
                    ]
                },
                {
                    "service_id": "23",
                    "service_name": "Amazon Simple Storage Service (Amazon S3)",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "cloud"],
                    "service_tags": [
                        "Object Storage",
                        "Scalability",
                        "Availability",
                        "Security",
                        "Performance"
                    ]
                },
                {
                    "service_id": "24",
                    "service_name": "Amazon Timestream",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Time Series Database",
                        "IoT",
                        "Operational Applications",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "55",
                    "service_name": "Greengrass - InfluxDB",
                    "service_type": "Storage",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Time Series Database",
                        "InfluxDB",
                        "Managed",
                        "Scalability",
                        "Performance"
                    ]
                },
                {
                    "service_id": "57",
                    "service_name": "Greengrass - Postgresql DB",
                    "service_type": "Storage",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Relational Database",
                        "PostgreSQL",
                        "Managed",
                        "Scalability",
                        "Performance"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 16,
            "abstractservice_name": "Device Data Storage",
            "abstractservice_type": "Storage",
            "abstractservice_layer": "cloud",
            "abstractservice_tags": ["Time Series Database"],
            "aws_services": [
                {
                    "service_id": "3",
                    "service_name": "Amazon Aurora",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Relational Database",
                        "High Performance",
                        "Managed",
                        "Scalability",
                        "Availability"
                    ]
                },
                {
                    "service_id": "6",
                    "service_name": "Amazon DocumentDB",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Document Database",
                        "MongoDB",
                        "Managed",
                        "Scalability",
                        "Availability"
                    ]
                },
                {
                    "service_id": "7",
                    "service_name": "Amazon DynamoDB",
                    "service_type": "Storage",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "NoSQL",
                        "Key-Value",
                        "Document Database",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "9",
                    "service_name": "Amazon Elastic Block Store",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": [
                        "Block Storage",
                        "EC2",
                        "Persistent Storage",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "10",
                    "service_name": "Amazon ElastiCache",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "near-edge", "cloud"],
                    "service_tags": [
                        "In-Memory Cache",
                        "Redis",
                        "Memcached",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "17",
                    "service_name": "Amazon MemoryDB",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "In-Memory Database",
                        "Redis",
                        "Managed",
                        "Scalability",
                        "Performance"
                    ]
                },
                {
                    "service_id": "19",
                    "service_name": "Amazon RDS",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Relational Database",
                        "Managed",
                        "Scalability",
                        "Availability",
                        "Performance"
                    ]
                },
                {
                    "service_id": "23",
                    "service_name": "Amazon Simple Storage Service (Amazon S3)",
                    "service_type": "Storage",
                    "service_layers": ["on-premise", "cloud"],
                    "service_tags": [
                        "Object Storage",
                        "Scalability",
                        "Availability",
                        "Security",
                        "Performance"
                    ]
                },
                {
                    "service_id": "24",
                    "service_name": "Amazon Timestream",
                    "service_type": "Storage",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Time Series Database",
                        "IoT",
                        "Operational Applications",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "55",
                    "service_name": "Greengrass - InfluxDB",
                    "service_type": "Storage",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Time Series Database",
                        "InfluxDB",
                        "Managed",
                        "Scalability",
                        "Performance"
                    ]
                },
                {
                    "service_id": "57",
                    "service_name": "Greengrass - Postgresql DB",
                    "service_type": "Storage",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Relational Database",
                        "PostgreSQL",
                        "Managed",
                        "Scalability",
                        "Performance"
                    ]
                }
            ]
        },
        {
            "abstractservice_id": 17,
            "abstractservice_name": "ML Train",
            "abstractservice_type": "Computation",
            "abstractservice_layer": "cloud",
            "abstractservice_tags": ["Machine Learning", "AI", "Compute"],
            "aws_services": [
                {
                    "service_id": "2",
                    "service_name": "Amazon AppStream 2.0",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Virtual Applications",
                        "Streaming",
                        "Managed",
                        "Scalability",
                        "Desktop"
                    ]
                },
                {
                    "service_id": "4",
                    "service_name": "Amazon CloudWatch",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "cloud"],
                    "service_tags": ["Monitoring", "Observability", "DevOps", "Metrics", "Logs"]
                },
                {
                    "service_id": "5",
                    "service_name": "Amazon Cognito",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Authentication",
                        "Authorization",
                        "User Management",
                        "Security",
                        "Identity"
                    ]
                },
                {
                    "service_id": "8",
                    "service_name": "Amazon EC2 Auto Scaling",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Auto Scaling",
                        "EC2",
                        "Compute",
                        "Availability",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "11",
                    "service_name": "Amazon EMR",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "near-edge", "cloud"],
                    "service_tags": ["Big Data", "Hadoop", "Spark", "Managed", "Scalability"]
                },
                {
                    "service_id": "12",
                    "service_name": "Amazon Forecast",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Forecasting",
                        "Managed",
                        "Scalability",
                        "AI"
                    ]
                },
                {
                    "service_id": "13",
                    "service_name": "Amazon Kinesis Data Steam",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Streaming Data",
                        "Real-Time",
                        "Analytics",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "14",
                    "service_name": "Amazon Kinesis Video Streams",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "cloud"],
                    "service_tags": [
                        "Video Streaming",
                        "Real-Time",
                        "Analytics",
                        "Machine Learning",
                        "Managed"
                    ]
                },
                {
                    "service_id": "15",
                    "service_name": "Amazon Lightsail",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["VPS", "Compute", "Managed", "Scalability", "Cost-Effective"]
                },
                {
                    "service_id": "16",
                    "service_name": "Amazon Location Service",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Location", "Maps", "Geocoding", "Geofencing", "Managed"]
                },
                {
                    "service_id": "21",
                    "service_name": "Amazon SageMaker",
                    "service_type": "Computation",
                    "service_layers": ["far-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "27",
                    "service_name": "Amazon WorkLink",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Secure Access",
                        "Mobile",
                        "Corporate Websites",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "29",
                    "service_name": "Amazon WorkSpaces Family",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["DaaS", "Desktop", "Secure", "Managed", "Scalability"]
                },
                {
                    "service_id": "30",
                    "service_name": "AWS Amplify",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Full-Stack", "Mobile", "Web", "Secure", "Scalable"]
                },
                {
                    "service_id": "31",
                    "service_name": "AWS App Runner",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Containerized Applications",
                        "APIs",
                        "Managed",
                        "Scalability",
                        "Deployment"
                    ]
                },
                {
                    "service_id": "32",
                    "service_name": "AWS CodeBuild",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Continuous Integration",
                        "Build",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "33",
                    "service_name": "AWS CodeDeploy",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Deployment",
                        "Automation",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "34",
                    "service_name": "AWS CodePipeline",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Continuous Delivery",
                        "Automation",
                        "Managed",
                        "Scalability",
                        "Developer Tools"
                    ]
                },
                {
                    "service_id": "35",
                    "service_name": "AWS Compute Optimizer",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Optimization",
                        "Machine Learning",
                        "Cost Reduction",
                        "Performance",
                        "Managed"
                    ]
                },
                {
                    "service_id": "36",
                    "service_name": "AWS Config",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Configuration",
                        "Audit",
                        "Evaluation",
                        "Managed",
                        "Governance"
                    ]
                },
                {
                    "service_id": "37",
                    "service_name": "AWS Data Exchange",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Data Exchange",
                        "Third-Party Data",
                        "Managed",
                        "Scalability",
                        "Analytics"
                    ]
                },
                {
                    "service_id": "39",
                    "service_name": "AWS Device Farm",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["App Testing", "Android", "iOS", "Web", "Developer Tools"]
                },
                {
                    "service_id": "41",
                    "service_name": "AWS EC2",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": ["Compute", "Scalable", "Managed", "Cloud", "EC2"]
                },
                {
                    "service_id": "42",
                    "service_name": "AWS Elastic Beanstalk",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Web Applications",
                        "Deployment",
                        "Scaling",
                        "Managed",
                        "Compute"
                    ]
                },
                {
                    "service_id": "43",
                    "service_name": "AWS Glue",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "ETL",
                        "Data Preparation",
                        "Analytics",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "44",
                    "service_name": "AWS Identity and Access Management",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Security",
                        "Identity",
                        "Access Management",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "45",
                    "service_name": "AWS IoT Analytics",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["IoT", "Analytics", "Managed", "Scalability", "Data"]
                },
                {
                    "service_id": "46",
                    "service_name": "AWS IoT Device Management",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "IoT",
                        "Device Management",
                        "Security",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "47",
                    "service_name": "AWS IoT SiteWise",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "cloud"],
                    "service_tags": [
                        "IoT",
                        "Industrial Equipment",
                        "Data Collection",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "48",
                    "service_name": "AWS Lambda",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "cloud"],
                    "service_tags": [
                        "Serverless",
                        "Compute",
                        "Managed",
                        "Scalability",
                        "Cost-Effective"
                    ]
                },
                {
                    "service_id": "50",
                    "service_name": "AWS Serverless Application Repository",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": [
                        "Serverless",
                        "Applications",
                        "Repository",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "51",
                    "service_name": "AWS Systems Manager",
                    "service_type": "Computation",
                    "service_layers": ["cloud"],
                    "service_tags": ["Management", "Governance", "Visibility", "Control", "Managed"]
                },
                {
                    "service_id": "56",
                    "service_name": "Greengrass - ML Inference",
                    "service_type": "Computation",
                    "service_layers": ["on-device", "on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "Inference",
                        "Greengrass",
                        "Managed",
                        "Scalability"
                    ]
                },
                {
                    "service_id": "58",
                    "service_name": "Tensorflow on AWS",
                    "service_type": "Computation",
                    "service_layers": ["on-premise", "far-edge", "near-edge", "cloud"],
                    "service_tags": [
                        "Machine Learning",
                        "AI",
                        "Framework",
                        "Development",
                        "Deployment"
                    ]
                }
            ]
        }
    ]
}

'

# Test with minimal input
echo -e "\n\n[INFO] Testing advise endpoint with minimal input..."
response=$(curl -X POST http://localhost:8000/api/v1/advise/2 \
	-H "Content-Type: application/json" \
	-d "$sample_result")

# Print the response
echo -e "\n\n[INFO] Advise response: $response"