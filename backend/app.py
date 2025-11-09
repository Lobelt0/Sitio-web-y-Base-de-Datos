from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1402'
app.config['MYSQL_DB'] = 'Inventario_Conexion'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/api/test')
def test_db():
    cursor = mysql.connection.cursor()
    cursor.execute("SHOW TABLES;")
    tablas = cursor.fetchall()
    cursor.close()
    return jsonify(tablas)

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({
            "message": "Login exitoso",
            "role": user['role']
        }), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401

if __name__ == '__main__':
    app.run(debug=True)
