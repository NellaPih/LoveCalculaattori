import json
import boto3
import os
from botocore.vendored import requests


def sendEmail(event, context):
    data = event['body'] 
    print(data)   
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
        <body>
            <h4>Hei """ +  fname + """ ja """ + sname + """!</h4>
            <p>Rakkausprosenttinne on: """ + str(percentage) + """%. 
            <br>Tulos: """ + str(result) + """</p>
            <p>Terveisin LoveGurus  
        <br>Ira ja Nella </p>
        </body>
        <p><img src="https://lovecalculaattori.s3.eu-central-1.amazonaws.com/rakkauslaskuri-1.jpg" alt="Love" width="600" height="350" /></p>"""

    #_message = "Hei " + fname + " ja " + sname + "!\n" + "Rakkausprosenttinne on: " + str(percentage) + "%.\nTulos: " + str(result) + "\n\n" + "Terveisin\n" + "LoveGurus Ira ja Nella\n\n" + love_pic
    
    client = boto3.client('ses' )    
        
    response = client.send_email(
        Destination={
            'ToAddresses': [destination]
            },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': love_pic,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=source,
    )
    return love_pic