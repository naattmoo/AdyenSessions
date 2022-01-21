import json
import requests
from flask import Flask, render_template, request, send_from_directory
import os
import config as config
from makeCall import makeCall
import uuid
from config import read_config


app = Flask(__name__)


def page_not_found(error):
    return render_template('error.html'), 404


# Register 404 handler
app.register_error_handler(404, page_not_found)
app.secret_key='adyen'

read_config()

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == "GET" and len(request.args) != 0:

        return render_template('redirect.html', session=request.args.get('sessionId'),
                               redirectResult=request.args.get('redirectResult'))
    else:

        url = 'https://checkout-test.adyen.com/v68/sessions'
        headers = {
            'x-API-key': 'AQEyhmfxK4jNbBFGw0m/n3Q5qf3VaY9UCJ1+XWZe9W27jmlZiks7sn/tSrs5FcgNcC9XxmAQwV1bDb7kfNy1WIxIIkxgBw==-9GRUbq2jXealS5MHIKH36IymgyK9tbAkXrzZtArnLhA=-gKDq9kW#93AQV[Jt',
            'content-type': 'application/json',

        }
        body = {
            'amount': {
                'currency': 'EUR',
                'value': 12500
            },
            'reference': 'Session',
            'merchantAccount': 'MerchantTestNatalia',
            'returnUrl': 'http://localhost:3020/'
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        return render_template('home.html', session=response.text)

@app.route('/makePayment', methods=['GET', 'POST'])
def makePayment():
    data = request.json

    if ('storedPaymentMethodId' in data['paymentMethod']):
       data['shopperInteraction'] = 'ContAuth'
       data['recurringProcessingModel'] = 'CardOnFile'
       data['shopperReference'] = "xee6f62b4-9a22-4860-b6c9-e69de062ba61"
    #if(data['paymentMethod']['brand']=='maestro'):
    #        data['shopperInteraction'] = 'Ecommerce'
    if ('storePaymentMethod' in data) and (data['storePaymentMethod'] == True):
        data['shopperInteraction'] = 'Ecommerce'
        data['recurringProcessingModel'] = 'CardOnFile'
        data['shopperReference'] = "xee6f62b4-9a22-4860-b6c9-e69de062ba61"


    reference = str(uuid.uuid4())
    returnUrl = 'http://localhost:3020/'

    body_string = """{
                "enablePayOut" : true,
               "merchantAccount": \"""" + config.merchant_account + """\",
               "amount": {
                       "currency": "EUR",
                   "value": 6000
               },""" + json.dumps(data).replace('\'', '\"')[1: -1] + """,
              "reference": \"""" + reference + """\",
              "shopperLocale": "en_US",
              "countryCode": "NL",
              "shopperIP":"192.0.2.1",
              "channel":"web",
              "additionalData": {
                      "allow3DS2": true
               },
               "shopperEmail":"natalia.moreno@personal.example.com",
               "shopperName":{
                  "firstName":"Testperson-se",
                  "gender":"UNKNOWN",
                  "lastName":"Approved"
               },
               "shopperStatement":"prueba de Shopper Statement",
               "billingAddress": {
                      "country": "ES",
                      "city": "Madrid",
                      "street": "Atocha",
                      "houseNumberOrName": "1",
                      "stateOrProvince": "N/A",
                      "postalCode": "28002"
               },
               "returnUrl": \"""" + returnUrl + """\"
            }"""
    # "threeDSAuthenticationOnly":true, //Flujo autenticacion y autorizacion por separado.
    # "additionalData": {
    #    "allow3DS2": true
    # },
    # "shopperReference": "xee6f62b4-9a22-4860-b6c9-e69de062ba61",
    #"customRoutingFlag": "mcDebit"
    #"riskData":{
    #"profileReference":"8016358411114661"
    #},
    #"shopperReference": "prueba",
    #"paymentMethod": {"type": "paypal",
    #                  "storedPaymentMethodId": "831641981497793F"},
    #"shopperInteraction": "ContAuth",

    body = json.loads(body_string)

    resp = makeCall('payments', json.dumps(body), config.checkout_apikey)

    '''if('action' in resp.json()):
        if(resp.json()['action']['type']== "redirect"):
            global paymentData
            paymentData=resp.json()['action']['paymentData']'''
    print(resp)
    return resp.text


@app.route('/makeDetailsCall', methods=['GET', 'POST'])
def makeDetailsCall():
    print(request.json)

    data = request.json

    resp = makeCall('payments/details', json.dumps(data), config.checkout_apikey)

    return resp.text

@app.route('/result/success', methods=['GET'])
def checkout_success():
    return render_template('checkout-success.html')


@app.route('/result/failed', methods=['GET'])
def checkout_failure():
    return render_template('checkout-failed.html')

@app.route('/result/error', methods=['GET'])
def checkout_error():
    return render_template('checkout-failed.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')

if __name__ == '__main__':
    #ssl_context='adhoc',
    app.run(debug=True, host='0.0.0.0', port=8000)
