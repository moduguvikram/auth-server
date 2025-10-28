from mangum import Mangum
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from auth_server.app import app  

handler = Mangum(app)
