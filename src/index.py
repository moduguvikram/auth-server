from mangum import Mangum
from src.auth_server.app import app  

handler = Mangum(app)
