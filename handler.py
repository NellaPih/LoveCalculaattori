import json
import boto3
import os
from botocore.vendored import requests

dynamodb = boto3.client('dynamodb')
myEmail = os.environ.get('SOURCE')

def update_index(tableName,email):
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'email': {'S': email}
            }
        ) 

def sendEmail(event, context):
    data = event['body']   
    source = myEmail   
    subject = 'Love Calculator'    
    destination = data['destination']
    fname = data['fname']
    sname = data['sname']
    error_message = None

    update_index('calculator_collection',destination)

    url = "https://love-calculator.p.rapidapi.com/getPercentage"
    querystring = {"fname":fname,"sname":sname}

    headers = {
    'x-rapidapi-host': "love-calculator.p.rapidapi.com",
    'x-rapidapi-key': "6890862800mshdc4c568aa3befd3p1344b1jsn81f0def35768"
    }
    output = requests.request("GET", url, headers=headers, params=querystring)

    json_output = json.loads(output.text)

    try:
        if json_output['message']:
            print("Hei")
            error_message = """
            <body>
                <p>Rakkauslaskurissa on ruuhkaa. Yritä hetken kuluttua uudelleen.</p>
            </body>"""
            return error_message
    except KeyError:
        pass
                 

    percentage = json_output['percentage']

    if int(percentage) <= 10:
        result = "Välitön ero on ainoa vaihtoehto"
    elif int(percentage) <= 20:
        result = "Harkitkaa pariterapiaa"
    elif int(percentage) <= 30:
        result = "Siinä ja siinä, että kannattaako olla yhdessä"
    elif int(percentage) <= 40:
        result = "Teillä on joskus hyviäkin päiviä"
    elif int(percentage) <= 50:
        result = "Ette tule eroamaan aivan heti"
    elif int(percentage) <= 60:
        result = "Sovitte yllättävän hyvin yhteen"
    elif int(percentage) <= 70:
        result = "Oho, nyt on kyllä hyvä pari"
    elif int(percentage) <= 80:
        result = "Teillä on vielä pitkä yhteinen taival edessä"
    elif int(percentage) <= 90:
        result = "Voiko noin onnellista parisuhdetta ollakaan!"
    elif int(percentage) <= 100:
        result = "Huijarit! Yksikään pari ei ole noin täydellinen"

    love_pic = """
        <body>
        <h4>Hei """ +  fname + """ ja """ + sname + """!</h4>
        <p>Rakkausprosenttinne on: """ + str(percentage) + """% 
        <br>Tuomio: """ + str(result) + """</p>
        <p>Terveisin LoveGurus  
        <br>Ira ja Nella </p>
        </body>
        <p><img src="https://lovecalculaattori.s3.eu-central-1.amazonaws.com/rakkauslaskuri-1.jpg" alt="Love" width="600" height="350" /></p>"""
    
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