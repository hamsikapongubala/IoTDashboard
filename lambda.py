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

    # You can delete the item using DynamoDB.Table.delete_item():
    table.delete_item(
        Key={
            'deviceID': event['deviceID']
        }
    )

    # Once you have a DynamoDB.Table resource you can add new items to the table using DynamoDB.Table.put_item():
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

    # You can then update attributes of the item in the table:
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

    # Send to SNS
    response = client.publish(
        TopicArn='arn:aws:sns:us-east-1:576305613970:mytestsns1',
        Message='Temperature is too high',
        Subject='Temperature Alert',
        MessageStructure='string'
    )

    # IoT control (optional)
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
    
    response = cloudwatch.put_metric_data(
    MetricData = [
        {
            'MetricName': 'KPIs',
            'Dimensions': [
                {
                    'Name': 'DEVICES TEMP',
                    'Value': 'Temperature'
                },
                {
                    'Name': 'APP_VERSION',
                    'Value': '1.0'
                },
            ],
            'Unit': 'None',
            'Value': random.randint(1, 500)
        },
    ],
    Namespace='CoolApp'
    )

    print(response)
    
    json_response = {
        "view": "timeSeries",
        "stacked": False,
        "region": "us-east-1",
        "metrics": [
            [ "AWS/Lambda", "Invocations", "FunctionName", "CMPE181LambdaPython1" ]
        ]
    }
    

    response = cloudwatch.get_metric_widget_image(MetricWidget=json.dumps(json_response))
    
    with open ('chart.png', 'w') as f:
       f.write(response["MetricWidgetImage"])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'isBase64Encoded': False,
        'headers': {}

    }


