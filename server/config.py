from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = b'268b58d7b78e4826dffcb3702baecaf3e458840b016b1b7e849c42eb2c725eb4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = b"b70b1e29b93ede85b4348353e86e16c1911e8c4abea45346869e856b1dadb98e"
app.json.compact = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

api = Api(app)

jwt = JWTManager(app)