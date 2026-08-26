from flask import Flask, request
from extensions import db, bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diario.db'

db.init_app(app)
bcrypt.init_app(app)

from models import User, Entry

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 1. Comprobar si el usuario ya existe
    if User.query.filter_by(username=username).first():
        return {"error": "Ya existe"}, 400 # 2. Si existe, devolver un error

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # 3. Hashear la contra
    # 4. Crear el usuario y guardarlo
    new_user = User(username = username, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    # 5. Devolver una respuesta de éxito
    return {"exito" : "se ha creado correctamente"}, 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    username_found = User.query.filter_by(username = username).first()
    if not username_found:
        return {"error" : "usuario no encontrado"}, 401
    if bcrypt.check_password_hash(username_found.password, password):
        return {"exito" : "inicio de sesion correcto"}
    else:
        return {"error" : "contrasenya incorrecta"}, 401
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
