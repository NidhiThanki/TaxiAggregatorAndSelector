import json
import boto3
import base64

def lambda_handler(event, context):
    try:
        data=event['body']
        byte_data = base64.b64decode(data)
        data =json.loads(str(byte_data, 'utf-8'))   
        email_id = data["email_id"]
        msg = data["msg"]
        print(msg)
        ses_client = boto3.client("ses", region_name="us-east-1") 
        CHARSET = "UTF-8"
        response = ses_client.send_email(
            Destination={
                "ToAddresses": [
                    email_id
                ],
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": CHARSET,
                        "Data": msg,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": "Booking Status",
                },
            },
            Source=email_id
        )
        return 1
    except Exception as e:
        return -1