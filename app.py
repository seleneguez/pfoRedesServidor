from flask import Flask, request, jsonify, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear la base de datos (solo una vez)
with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return 'Servidor Flask funcionando'

# POST /registro
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    datos = request.get_json()
    nombre = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if not nombre or not contraseña:
        return jsonify({"error": "Faltan campos"}), 400

    if Usuario.query.filter_by(usuario=nombre).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    contraseña_hasheada = generate_password_hash(contraseña)
    nuevo_usuario = Usuario(usuario=nombre, contraseña=contraseña_hasheada)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

# POST /login
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    nombre = datos.get('usuario')
    contraseña = datos.get('contraseña')

    if not nombre or not contraseña:
        return jsonify({"error": "Faltan campos"}), 400

    usuario = Usuario.query.filter_by(usuario=nombre).first()

    if not usuario or not check_password_hash(usuario.contraseña, contraseña):
        return jsonify({"error": "Credenciales inválidas"}), 401

    return jsonify({"mensaje": f"Bienvenido/a {usuario.usuario}"}), 200

# GET /tareas
@app.route('/tareas', methods=['GET'])
def tareas():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bienvenida</title>
    </head>
    <body>
        <h1>¡Bienvenida/o a tu panel de tareas!</h1>
        <p>Aca podrás gestionar tus tareas.</p>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)

  
