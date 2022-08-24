from ast import keyword
from unittest import result
from flask import Flask, request
from flask_mysqldb import MySQL
from flask import jsonify
import yaml

# access image with url /static/file_name.jpg
app = Flask(__name__, static_folder='gambar')

db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/wisata', methods=['GET'])
def wisata():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT id, nama, wilayah FROM wisata")
    if result > 0:
        wisata = cur.fetchall()
        return jsonify({'data': wisata}, 200)
 
@app.route('/kategori/<kategori_id>', methods=['GET'])
def kategori_by_id(kategori_id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM wisata where kategori = %s", kategori_id)
    if result > 0:
        kategori = cur.fetchall()
        return jsonify({'data': kategori}, 200)

@app.route('/detail/<detail_id>', methods=['GET'])
def detail_by_id(detail_id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM wisata where id = %s", detail_id)
    if result > 0:
        detail = cur.fetchone()
        return jsonify({'data': detail}, 200)

@app.route('/rekomendasi', methods=['GET'])
def rekomendasi_by_id():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM wisata where rekomendasi = 'Y'")
    if result > 0:
        rekomendasi = cur.fetchall()
        return jsonify({'data': rekomendasi}, 200)

    
# @app.route('/search', methods=['GET', 'POST'])
# def search_by_id(search_id):
#     cur = mysql.connection.cursor()
#     result = cur.execute("SELECT * FROM wisata WHERE nama LIKE %s OR wilayah LIKE %s", search_id)
#     if result > 0:
#         search = cur.fetchall()
#         return jsonify({'data': search}, 200)    
@app.route('/search', methods=['GET'])
def search():
    nama = args.get('nama')
    wilayah = args.get('wilayah')
    if None not in (nama, wilayah):
        result = {key: value for key, value in wisata.items() if key == nama and value == wilayah}
    elif nama is not None:
        result = {key: value for key, value in wisata.items() if key == nama}
    elif wilayah is not None:
        result = {key: value for key, value in wisata.items() if value == wilayah}
    return result

@app.route('/register', methods=['POST'])
def register():
        user = request.form
        username = user['username']
        password = user['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(username, password, role) VALUES(%s, %s, 2)",(username, password))
        mysql.connection.commit()
        cur.close()
        return jsonify({'data': user}, 200)
    
@app.route('/profil/<profil_id>', methods=['GET'])
def profil(profil_id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM user where id = %s", profil_id)
    if result > 0:
        jenis = cur.fetchall()
        return jsonify({'data': jenis}, 200)
    
if __name__ == '__main__':
    app.run(debug=True)