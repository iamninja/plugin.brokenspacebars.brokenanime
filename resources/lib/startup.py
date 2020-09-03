# -*- coding: utf-8 -*-

import logging
from BaseHTTPServer import HTTPServer
from service import server


logger = logging.getLogger('plugin.brokenspacebars.brokenanime')
logger.debug("----------Service file----------")
# server.run()
print("------Broken HTTP Server Started-------")
logger.debug("Service started")
server_address = ('127.0.0.1', 6969)
httpd = HTTPServer(server_address, server.BrokenHTTPRequestHandler)
logger.debug("HTTP server started on port localhost:6969")
httpd.serve_forever()

