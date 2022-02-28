from flask import Flask , request , jsonify , Response
from flask_sqlalchemy import SQLAlchemy
import sqlite3 as sql
import os , datetime
# import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/daba.db'
db = SQLAlchemy(app)
print(db)
conn1= sql.connect('D:\\daba1.db')
# c = conn1.cursor()
# c.execute("""CREATE TABLE employees(
#     first text,
#     last text,
#     pay integer
# )""")
# conn1.commit()
# conn1.close()
class Example(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    location = db.Column(db.String(50))
    date_created = db.Column(db.DateTime,default = datetime.datetime.now) 
@app.route('/enter')
def new_student():
    return render_template()


@app.route('/ank',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        first = data['first']
        last = data['last']
        pay = data['pay']
        with sql.connect("D:\\daba1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO employees VALUES (?,?,?)",(first,last,pay))
            con.commit()
        # return jsonify({'data' :e.fetchall()})
        return jsonify({'first' :first,'last':last,'pay':pay})

    if request.method == 'GET':
        with sql.connect("D:\\daba1.db") as con:
            cur = con.cursor()
            #   cur.execute("INSERT INTO students (name) VALUES (?)",(name))
            sa = cur.execute("SELECT * from employees")
            # con.commit()
            # from pdb import set_trace
            # set_trace()
            
            # return jsonify({'data':sa.fetchall()})
    # # conn1.commit()
    # return response.json(data)
    #a = jsonify({'a':1})\d
            # li = []
            # print(f)
            # data = {}
            # for i in range(len(sa.fetchall())-1):
            #     data['first'] = sa.fetchall()[i][0]
            #     data['last'] = sa.fetchall()[i][1]
            #     data['pay'] = sa.fetchall()[i][2]
            #     li.append(data)

            # con.commit()
    # return jsonify(sa.fetchmany())
        return jsonify({'data':sa.fetchall()}) #"{} is the value".format(7*8)
        #  return jsonify({'name' :name,'location':location,'randomlist':randomlist})
    # if request.method == 'GET':
    # data1 = request.get_json()
    # name = data1['name']
    # location = data['location']
    # randomlist = data['randomlist']
        # value = request.json['name']
    # return name
    # return jsonify({'name' :name})
# app.config['SQLALCHEMY_DATABASE'] = 'sqlite:///C:/Users/ankit.bose/Documents/dab.db'
conn1.close()

@app.route('/try', methods=['GET','POST'])
def insert_reading():
    print(os.path)
    # try:
    if request.method == 'POST':
        # pass
        data: {
        name: "paul rudd",
        movies: ["I Love You Man", "Role Models"] }
        return jsonify(data)
    # conn =  sql.connect('C:\\Users\\ankit.bose\\Documents\\daba.db')
    # conn.execute('Select * from users')
    # s = conn.execute('Select * from users')
    # print("Open DB")
    # DATABS = 'sqlite:///C:/Users/ankit.bose/Documents/daba.db'
    # DATABASE = 'C:\\Users\\ankit.bose\\Documents\\daba.db'
    # with sql.connect(DATABS) as con:
    #     cur = con.cursor()
    #     cur.execute('Select * from users')
    #     cur.commit()
    # return jsonify({"data":{"id":2,"name":"fuchsia rose","year":2001,"color":"#C74375","pantone_value":"17-2031"}})

    # except Exception as e:
    #     print(e)

@app.route('/Hi', methods=['GET','POST'])
def hello():
    result = {'a':'b'}
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']
    # print("Hello World!")
    # return '<h1>"HEllo World" {}</h1>'.format(arg)
    # return jsonify(result)
    # return jsonify({'name' :name,'location':location,'randomlist':randomlist})
    # return jsonify({'username':'Ankit",'emailid': "ank.gramener.com",'id':"ank123"})

    # name = db.Column(db.)


if __name__ == "__main__":
    app.run(port=1000)