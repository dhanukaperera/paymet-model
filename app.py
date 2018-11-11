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
    'nic':'',
    'address':'',
    'contact':'',
    'email':'',
    'password':''
}

Card = {
    'cid':'',
    'nic':'',
    'card_no':'',
    'exp':'',
    'card_holder_name':'',
    'csv':'',
    'amount':''
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
        User['nic'] = result.get('nic')
        User['address'] = result.get('address')
        User['contact'] = result.get('contact')
        User['email'] = result.get('email')
        User['password'] = result.get('password')
        print(User)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            CREATE_USER_QUERY = "INSERT INTO users (name,nic,address,contact,email,password) VALUES ('"+User.get('name')+"','"+User.get('nic')+"','"+User.get('address')+"','"+User.get('contact')+"','"+User.get('email')+"','"+User.get('password')+"')"
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

@app.route("/updateUser",methods=['PUT'])
def updateUser():
    if request.method  == 'PUT':
        result = request.form
        # print(result)
        User['name'] = result.get('name')
        User['nic'] = result.get('nic')
        User['address'] = result.get('address')
        User['contact'] = result.get('contact')
        User['email'] = result.get('email')
        User['password'] = result.get('password')
        print(User)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            UPDATE_USER_QUERY = "UPDATE users SET name = '"+User.get('name')+"', nic = '"+User.get('nic')+"', address = '"+User.get('address')+"', contact = '"+User.get('contact')+"' , email = '"+User.get('email')+"', password = '"+User.get('password')+"'"
            print(UPDATE_USER_QUERY)
            cursor.execute(UPDATE_USER_QUERY)
            conn.commit()
            resp = jsonify('User update successfully!')
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


@app.route("/addCard",methods=['POST'])
def addCard():
    if request.method  == 'POST':
        result = request.form
        # print(result)
        Card['nic'] = result.get('nic')
        Card['card_no'] = result.get('card_no')
        Card['exp'] = result.get('exp')
        Card['card_holder_name'] = result.get('card_holder_name')
        Card['csv'] = result.get('csv')
        print(Card)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            ADD_CARD_QUERY = "INSERT INTO cards (nic,card_no,exp,card_holder_name,csv) VALUES ('"+Card.get('nic')+"','"+Card.get('card_no')+"','"+Card.get('exp')+"','"+Card.get('card_holder_name')+"','"+Card.get('csv')+"')"
            print(ADD_CARD_QUERY)
            cursor.execute(ADD_CARD_QUERY)
            conn.commit()
            resp = jsonify('Card added successfully!')
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

@app.route("/deposit",methods=['PUT'])
def deposit():
    if request.method  == 'PUT':
        result = request.form
        # print(result)
        _card_no = result.get('card_no')
        _exp = result.get('exp')
        _card_holder_name = result.get('card_holder_name')
        _csv = result.get('csv')
        _amount:float = result.get('amount')

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            CHECK_CARD_QUERY = "SELECT amount FROM cards WHERE card_no ='"+_card_no+"' AND exp = '"+_exp+"' AND card_holder_name = '"+_card_holder_name+"' AND csv = '"+_csv+"'"
            print(CHECK_CARD_QUERY)
            cursor.execute(CHECK_CARD_QUERY)
            amount = cursor.fetchall()
            curretBalance:float = amount[0][0]
            conn.commit()
            print(amount)
            if len(amount) == 1:
                depositAmount = float(curretBalance) + float(_amount)
                DEPOSIT_QUERY = "UPDATE cards SET amount ='"+str(depositAmount)+"' WHERE card_no ='"+_card_no+"' AND exp = '"+_exp+"' AND card_holder_name = '"+_card_holder_name+"' AND csv = '"+_csv+"'"
                cursor.execute(DEPOSIT_QUERY)
                conn.commit()
                resp = jsonify('Deposit amount successfully!')
                resp.status_code = 200
                return resp
        
            resp = jsonify('Card Not Found!')
            resp.status_code = 404
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

@app.route("/withdraw",methods=['PUT'])
def withdraw():
    if request.method  == 'PUT':
        result = request.form
        # print(result)
        _card_no = result.get('card_no')
        _exp = result.get('exp')
        _card_holder_name = result.get('card_holder_name')
        _csv = result.get('csv')
        _amount:float = result.get('amount')

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            CHECK_CARD_QUERY = "SELECT amount FROM cards WHERE card_no ='"+_card_no+"' AND exp = '"+_exp+"' AND card_holder_name = '"+_card_holder_name+"' AND csv = '"+_csv+"'"
            print(CHECK_CARD_QUERY)
            cursor.execute(CHECK_CARD_QUERY)
            amount = cursor.fetchall()
            curretBalance:float = amount[0][0]
            conn.commit()
            print(amount)
            if len(amount) == 1:
                if(curretBalance < _amount):
                    resp = jsonify('No Credits to withdraw!')
                    resp.status_code = 404
                    return resp

                depositAmount = float(curretBalance) - float(_amount)
                DEPOSIT_QUERY = "UPDATE cards SET amount ='"+str(depositAmount)+"' WHERE card_no ='"+_card_no+"' AND exp = '"+_exp+"' AND card_holder_name = '"+_card_holder_name+"' AND csv = '"+_csv+"'"
                cursor.execute(DEPOSIT_QUERY)
                conn.commit()
                resp = jsonify('Withdraw amount successfully!')
                resp.status_code = 200
                return resp
        
            resp = jsonify('Card Not Found!')
            resp.status_code = 404
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

@app.route("/getBalance",methods=['POST'])
def getBalace():
    if request.method  == 'POST':
        result = request.form
        # print(result)
        _nic = result.get('nic')
       
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            TOTAL_BALANCE_QUERY = "SELECT SUM(amount) from cards WHERE nic = '"+_nic+"'"
            print(TOTAL_BALANCE_QUERY)
            cursor.execute(TOTAL_BALANCE_QUERY)
            amount = cursor.fetchall()
            curretBalance:float = amount[0][0]
            conn.commit()
            print(amount)
            print(curretBalance)
            if curretBalance != None:
                balanceObj = {
                    'balance':curretBalance
                }
                resp = jsonify(balanceObj)
                resp.status_code = 200
                return resp
        
            resp = jsonify('Card Not Found!')
            resp.status_code = 404
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
    app.run(host="0.0.0.0",debug=True)
