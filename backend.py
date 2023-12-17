import boto3
from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, create_access_token
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '17b9Junp4u9ESG_yfioo-TyqvjK2qO4='
jwt = JWTManager(app)

dynamodb = boto3.resource('dynamodb')
table = resource('dynamodb').Table('textbase')
authority_table = resource('dynamodb').Table('authority_table')


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
    print(requ_time)
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



@app.route('/register', methods=["POST"])
def register():
    email = request.form.get('email')
    response = authority_table.scan(
        FilterExpression=Key('user_id').eq(email)
    )
    items = response['Items']
    if items:
        return 'All ready registered', 500

    password = request.form.get('password')
    authority_table.put_item(
        Item={
            'email': email,
            'key': password,
        }
    )
    access_token = create_access_token(identity=email, expires_delta=timedelta(days=180))
    return jsonify(access_token=access_token)
@app.route('/login', methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    response = authority_table.scan(
        FilterExpression=Key('email').eq(email) & Attr('key').eq(password)
    )
    items = response['Items']
    if items:
        access_token = create_access_token(identity=email,expires_delta=timedelta(days=180))
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@app.route('/get', methods=['GET'])
@jwt_required()
def get_text():
    username = request.args.get('id')
    databack = new_check(username)
    if databack:
        feedback = jsonify(databack)
    else:
        feedback = {'status': 'success'}
    return feedback

@app.route('/update', methods=['POST'])
@jwt_required()
def upload_text():
    data = request.form
    insert(data['id'],data['text'])
    databack = new_check(data['id'])
    if databack:
        feedback = jsonify(databack)
    else:
        feedback = {'status': 'success'}
    return feedback

@app.route('/switch', methods=['POST'])
@jwt_required()
def switch_status():
    data = request.form
    status_switch(data['id'],data['text'])
    return jsonify({'status': 'success'})

@app.route('/end', methods=['GET'])
@jwt_required()
def delete_temp():
    username = request.args.get('id')
    temp_check(username=username)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    requ_time = '2023-12-09T21:05:04.958156'
    app.run(debug=True)
