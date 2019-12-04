import json
import boto3
import os
from botocore.vendored import requests


def sendEmail(event, context):
    data = event['body']    
    source = 'nella.pihlajaniemi@gmail.com'    
    subject = 'Love Calculator Result'    
    destination = data['destination']
    fname = data['fname']
    sname = data['sname']

    url = "https://love-calculator.p.rapidapi.com/getPercentage"
    querystring = {"fname":fname,"sname":sname}

    headers = {
    'x-rapidapi-host': "love-calculator.p.rapidapi.com",
    'x-rapidapi-key': "6890862800mshdc4c568aa3befd3p1344b1jsn81f0def35768"
    }
    output = requests.request("GET", url, headers=headers, params=querystring)

    json_output = json.loads(output.text)
        

    percentage = json_output['percentage']
    result = json_output['result']

    love_pic = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Love Calculator</title>
    </head>
    <body>
        <img src="https://lovecalculaattori.s3.eu-central-1.amazonaws.com/rakkauslaskuri.jpg">   
    </body>
    </html>"""

    _message = "Hei " + fname + " ja " + sname + "!\n" + "Rakkausprosenttinne on: " + str(percentage) + "%.\nTulos: " + str(result) + "\n\n" + "Terveisin\n" + "LoveGurus Ira ja Nella\n\n" + love_pic
    
    client = boto3.client('ses' )    
        
    response = client.send_email(
        Destination={
            'ToAddresses': [destination]
            },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': _message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=source,
)
    return _message