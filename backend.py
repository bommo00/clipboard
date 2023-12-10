import boto3
import json
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, jsonify, request
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = resource('dynamodb').Table('textbase')
def insert(username,text):
    global requ_time
    requ_time = datetime.now().isoformat()
    table.put_item(
        Item={
            'user_id': username,
            'created_date': requ_time,
            'status': 'temp',
            'content': text,
        }
    )

def new_check(username):
    global requ_time
    response = table.scan(
        FilterExpression=Key('user_id').eq(username) & Attr('created_date').gt(requ_time)
    )
    items = response['Items']
    requ_time = datetime.now().isoformat()
    return items

def temp_check(username):
    response = table.scan(
        FilterExpression=Key('user_id').eq(username) & Attr('status').eq('temp')
    )
    items = response['Items']
    for item in items:
        table.delete_item(
            Key={
                'user_id': username,
                'created_date': item['created_date'],
            }
        )

def status_switch(username,text):
    response = table.scan(
        FilterExpression=Key('user_id').eq(username) & Attr('content').eq(text)
    )
    items = response['Items']
    item = items[0]
    if item['status'] == 'temp':
        table.update_item(
            Key={
                'user_id': username,
                'created_date': item['created_date'],
            },
            UpdateExpression='set #st = :s',
            ExpressionAttributeNames={
                '#st': 'status'
            },
            ExpressionAttributeValues={
                ':s': 'fixed'}
        )
    else:
        table.update_item(
            Key={
                'user_id': username,
                'created_date': item['created_date'],
            },
            UpdateExpression='set #st = :s',
            ExpressionAttributeNames={
                '#st': 'status'
            },
            ExpressionAttributeValues={
                ':s': 'temp'}
        )


app = Flask(__name__)



# @app.route('/login', methods=['GET'])
# def log_in():
#     item_id = request.args.get('id')
#     response = table.get_item(Key={'id': item_id})
#     return jsonify(response['Item'])

@app.route('/get', methods=['GET'])
def get_text():
    username = request.args.get('id')
    databack = new_check(username)
    return databack

@app.route('/update', methods=['POST'])
def upload_text():
    data = request.form
    insert(data['id'],data['text'])
    databack = new_check(data['id'])
    return databack

@app.route('/switch', methods=['POST'])
def switch_status():
    data = request.form
    status_switch(data['id'],data['text'])
    return jsonify({'status': 'success'})

@app.route('/end', methods=['GET'])
def delete_temp():
    username = request.args.get('id')
    temp_check(username=username)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    requ_time = '2023-12-09T21:05:04.958156'
    app.run(debug=True)
