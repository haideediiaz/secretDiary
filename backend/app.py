from flask import Flask, request
from extensions import db, bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diario.db'

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
# La secret key sirve para firmar los tokens, sea cual sea la identidad
app.config['JWT_SECRET_KEY'] = 'hola'

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
        token = create_access_token(identity = str(username_found.id))
        return {"token": token, "username": username_found.username}
    else:
        return {"error" : "contrasenya incorrecta"}, 401

# En este caso, se juntan dos decoradores. El primero registra la ruta (como los casos anteriores)
@app.route('/entries', methods=['POST'])
# El segundo exige que venga un token valido antes de poder entrar
@jwt_required()
def new_entry():
    data = request.get_json()
    entry_content = data.get('content')
    user_id = get_jwt_identity()
    new_entry = Entry(content = entry_content, date = datetime.utcnow(), user_id = user_id)
    db.session.add(new_entry)
    db.session.commit()
    return {"exito": "se ha guardado correctamente"}, 201

@app.route('/entries', methods=['GET'])
@jwt_required()
def get_entries():
    user_id = get_jwt_identity()
    entries = Entry.query.filter_by(user_id = user_id).all()
    resultado = []
    for e in entries:
        resultado.append({"id": e.id, "content": e.content, "date": e.date})
    return resultado

@app.route('/entries/<int:entry_id>', methods = ['PUT'])
@jwt_required()
def edit_entry(entry_id):
    user_id = int(get_jwt_identity())
    entry = Entry.query.get(entry_id)
    if not (entry):
        return {"error" : "entrada no encontrada"}, 404
    if (entry.user_id != user_id):
        return {"error" : "entrada no encontrada"}, 404
    data = request.get_json()
    entry.content = data.get('content')
    db.session.commit()
    return {"exito" : "se ha editado correctamente"}

@app.route('/entries/<int:entry_id>', methods = ['DELETE'])
@jwt_required()
def delete_entry(entry_id):
    user_id = int(get_jwt_identity())
    entry = Entry.query.get(entry_id)
    if not (entry):
        return {"error" : "entrada no encontrada"}, 404
    if (entry.user_id != user_id):
        return {"error" : "entrada no encontrada"}, 404
    db.session.delete(entry)
    db.session.commit()
    return {"exito" : "se ha borrado correctamente"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

