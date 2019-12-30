import jwt
from config import Config

def en_jwt(password):
    encoded_jwt = jwt.encode({'password': password}, Config.SECRET_KEY, algorithm='HS256')
    return encoded_jwt # token

def de_jwt(e_jwt):
    decode_jwt = jwt.decode(e_jwt, Config.SECRET_KEY, algorithms=['HS256'])
    return decode_jwt # {'some': 'payload'}

