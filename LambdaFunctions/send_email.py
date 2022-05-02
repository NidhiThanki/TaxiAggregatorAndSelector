import json
import boto3
import base64
import pprint

def lambda_handler(event, context):
    try:
        res = -1
        data=event['body']
        byte_data = base64.b64decode(data)
        data =json.loads(str(byte_data, 'utf-8'))   
        print(data)
        email_id = data["email_id"]
        msg = data["msg"]
        status = data["status"]
        print(msg)
        ses_client = boto3.client("ses", region_name="us-east-1") 
        email_list = ses_client.list_identities(IdentityType = 'EmailAddress',MaxItems=10)
        print(email_list['Identities'])
        if email_id not in email_list['Identities']:
            # for email verification
            response = ses_client.verify_email_identity(EmailAddress=email_id)
            res = 0
        else:
            print(f"Email: {email_id} captured !")
            res = 1
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
                    "Data": status,
                },
            },
            Source=email_id
        )
        return res
    except Exception as e:
        pprint.pprint(str(e))
        return -1