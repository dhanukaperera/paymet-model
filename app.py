from flask import Flask, jsonify,request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'bankdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

User = {
    'uid':'',
    'name':'',
    'address':'',
    'contact':'',
    'email':'',
    'password':''
}

@app.route("/",methods=['GET'])
def main():
    return 'Payment Gateway is running...'


@app.route("/createuser",methods=['POST'])
def createUser():
    if request.method  == 'POST':
        result = request.form
        # print(result)
        User['name'] = result.get('name')
        User['address'] = result.get('address')
        User['contact'] = result.get('contact')
        User['email'] = result.get('email')
        User['password'] = result.get('password')
        print(User)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            CREATE_USER_QUERY = "INSERT INTO users (name,address,contact,email,password) VALUES ('"+User.get('name')+"','"+User.get('address')+"','"+User.get('contact')+"','"+User.get('email')+"','"+User.get('password')+"')"
            print(CREATE_USER_QUERY)
            cursor.execute(CREATE_USER_QUERY)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        except Exception as e:
            print(e)
            resp = jsonify('Error')
            resp.status_code = 400
            return resp
        finally:
            cursor.close()
            conn.close()
    return

if __name__ == '__main__':
    app.run(debug=True)
