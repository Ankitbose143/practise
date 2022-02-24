from flask import Flask,jsonify,request,make_response,url_for,redirect
import requests, json

app = Flask(__name__)

url = 'https://hooks.zapier.com/hooks/catch/xxxxx/yyyyy/'

@app.route('/create-row-in-gs', methods=['GET','POST'])
def create_row_in_gs():
    if request.method == 'GET':
        return make_response('failure')
    if request.method == 'POST':
        t_id = request.json['id']
        t_name = request.json['name']
        created_on = request.json['created_on']
        modified_on = request.json['modified_on']
        desc = request.json['desc']

        create_row_data = {'id': str(t_id),'name':str(t_name),'created-on':str(created_on),'modified-on':str(modified_on),'desc':str(desc)}

        response = requests.post(
            url, data=json.dumps(create_row_data),
            headers={'Content-Type': 'application/json'}
        )
        return response.content

if __name__ == '__main__':
    app.run(host='localhost',debug=False, use_reloader=True)