import bcrypt
from .logger_util import logger


def generate_hash(password:bytes):
    try:
        hashed=bcrypt.hashpw(password,bcrypt.gensalt())
        return hashed
    except Exception as e:
        logger.error(f"error occured while encrypting password :{e}")
        raise 

def verify_password(password:bytes,hashed_password:bytes):
    try:
        password_match=bcrypt.checkpw(password=password,hashed_password=hashed_password)
        return password_match
    except Exception as e:
     logger.error(f'error occured while verifying password :{e} ')
