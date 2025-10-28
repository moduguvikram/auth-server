from mangum import Mangum
from auth_server.app import app  

handler = Mangum(app)
