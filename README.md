# IoTDashboard

##Lambda Function
Lambda function was used to integrate dynamoDB, IoT core, and CloudWatch Logs. The save simulated IoT sensor temperature data in dynamoDB, create cloudmetric from the saved temperature, get the image from cloudwatch logs, and then the saved image is then placed in a S3 bucket. 

##Cloudwatch Logs
Cloudwatch logs were used to create a new metric to display the temperatures saved in dynamoDB. Using the GetMetricWidgetImage api we are able to get the snapshot of the current temperature metrics. This image is saved in an S3 bucket. 

##Amazon API Gateway
A GET REST call through the API Gateway gets the image saved in the S3 bucket. A Lambda function is created to generate the script for retrieving the image. 




