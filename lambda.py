import json
import boto3
import random

cloudwatch = boto3.client('cloudwatch')
print('Loading function')

# Get the dynamodb service resource.
dynamodb = boto3.resource('dynamodb')

# Get the SNS client
client = boto3.client('sns')

# Get the IoT client
iotdataclient = boto3.client('iot-data')

iotclient = boto3.client('iot')

cloudwatch = boto3.client('cloudwatch')



def lambda_handler(event, context):
    # TODO implement
    print("Received event: " + json.dumps(event, indent=2))
    print("deviceID = " + event['deviceID'])
    print("batteryVoltage = " + event['batteryVoltage'])
    print("temperature = " + event['temperature'])

    # Instantiate a table resource object without actuallyccreating a DynamoDB table.
    # Note that the attributes of this table are lazy-loaded: a request is not made nor are the attribute
    table = dynamodb.Table('CMPE181testmulti1')

    # Print out some data about the table.
    print(table.creation_date_time)

    # Delete the item using DynamoDB.Table.delete_item():
    table.delete_item(
        Key={
            'deviceID': event['deviceID']
        }
    )

    # Add new items to the table using DynamoDB.Table.put_item():
    table.put_item(
        Item={
            'deviceID': event['deviceID'],
            'batteryVoltage': event['batteryVoltage'],
            'temperature': event['temperature'],
        }
    )

    # You can then retrieve the object using DynamoDB.Table.get_item():
    response = table.get_item(
        Key={
            'deviceID': event['deviceID']
        }
    )
    item = response['Item']
    print(item['temperature'])

    #Update attributes of the item in the table:
    newtemp = int((int(item['temperature']) - 32) * 5 / 9)  # Fahrenheit to Celsius
    table.update_item(
        Key={
            'deviceID': event['deviceID']
        },
        UpdateExpression='SET temperature = :val1',
        ExpressionAttributeValues={
            ':val1': newtemp
        }
    )

    # IoT control
    response = iotclient.describe_endpoint(
        endpointType='iot:Data-ATS'
    )
    print(response)

    # IoT Data publish
    message = {}
    message['message'] = "test message"
    message['sequence'] = "1"
    messageJson = json.dumps(message)
    iotdataclient.publish(
        topic="CMPE181return",
        qos=1,
        payload=messageJson  # b'0101'
    )
    
    #Create Cloudwatch Metric
    val = item['temperature'] #simulated temperature from dynamoDB
    response = cloudwatch.put_metric_data(
        Namespace='Device App',
        MetricData = [
            {
                'MetricName': 'Device Temperature',
                'Dimensions': [
                    {
                        'Name': 'Device Temperature',
                        'Value': 'Temperature'
                    },
                ],
                'StatisticValues': {
                    'SampleCount': 1,
                    'Sum': int(val),
                    'Minimum': 50,
                    'Maximum': 125.0
                },
                'Values': [
                    int(val)
                ],
                
                'Unit': 'Count/Second',
                'StorageResolution': 60
            },
        ]
    
    )

    print(response)
    
    json_response = {
        "view": "timeSeries",
        "stacked": False,
        "metrics": [
            [ "Device App", "Device Temperature", "Device Temperature", "Temperature" ]
        ],
        "region": "us-east-1"
    }

  
    # Get MetricWidgetImage from CloudWatch Metrics
    response = cloudwatch.get_metric_widget_image(MetricWidget=json.dumps(json_response))
    data = response['MetricWidgetImage']
    
    bucket_name = 'finalproject181' # for temporary public file
    filename = 'cloudwatch_metric_chart.png'
    # Create temporary public file on S3
    boto3.client('s3').put_object(ACL='public-read', Body=data,
                                  Bucket=bucket_name, Key=filename)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'isBase64Encoded': False,
        'headers': {}

    }
