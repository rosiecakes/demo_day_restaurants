import os
import binascii

from restaurate import app

if __name__ == '__main__':
    app.debug = True
    app.secret_key = binascii.hexlify(os.urandom(24))
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
