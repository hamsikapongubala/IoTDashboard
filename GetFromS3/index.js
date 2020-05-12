const AWS = require('aws-sdk');
//*/ get reference to S3 client 
var s3 = new AWS.S3();
exports.handler = (event, context, callback) => {
    var params = {
  "Bucket": "finalproject181",
  "Key": 'cloudwatch_metric_chart.png',  
    };
    s3.getObject(params, function(err, data){
       if(err) {
           callback(err, null);
       } else {
           let response = {
        "statusCode": 200,
        "headers": {
            "my_header": "my_value"
        },
        "body": JSON.stringify(data),
        "isBase64Encoded": false
    };
           callback(null, response);
    }
    });
    
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
        'isBase64Encoded': false,
        'headers': {}
    };
    return response;
    
};

