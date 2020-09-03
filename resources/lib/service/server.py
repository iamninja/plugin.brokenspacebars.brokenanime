# -*- coding: utf-8 -*-

import os
import logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import xbmc
import xbmcaddon

logger = logging.getLogger('plugin.brokenspacebars.brokenanime')

class BrokenHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.addon_id = 'plugin.brokenspacebars.brokenanime'
        # addon = xbmcaddon.Addon(self.addon_id)
        self.chunk_size = 1024 * 64
        try:
            self.base_path = xbmc.translatePath('special://temp/%s' % self.addon_id).decode('utf-8')
        except AttributeError:
            self.base_path = xbmc.translatePath('special://temp/%s' % self.addon_id)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    # Handle GET requests
    def do_GET(self):
        addon = xbmcaddon.Addon('plugin.brokenspacebars.brokenanime')
        print('HTTPServer: Request uri path |{path}|'.format(path = self.path))

        if self.path == '/api':
            html = self.api_config_page()
            html = html.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(html))
            self.end_headers()
            for chunk in self.get_chunks(html):
                self.wfile.write(chunk)
            else:
                self.send_error(501)

    def get_chunks(self, data):
        for i in range(0, len(data), self.chunk_size):
            yield data[i:i + self.chunk_size]

    @staticmethod
    def api_config_page():
        addon = xbmcaddon.Addon('plugin.video.youtube')
        # i18n = addon.getLocalizedString
        # api_key = addon.getSetting('youtube.api.key')
        # api_id = addon.getSetting('youtube.api.id')
        # api_secret = addon.getSetting('youtube.api.secret')
        html = Pages().api_configuration.get('html')
        css = Pages().api_configuration.get('css')
        html = html.format(css=css, title="test", api_key_head="test", api_id_head="test",
                           api_secret_head="test", api_id_value="api_id", api_key_value="api_key",
                           api_secret_value="api_secret", submit="test", header="test")
        return html

class Pages(object):
    api_configuration = {
        'html':
            u'<!doctype html>\n<html>\n'
            u'<head>\n\t<meta charset="utf-8">\n'
            u'\t<title>{title}</title>\n'
            u'\t<style>\n{css}\t</style>\n'
            u'</head>\n<body>\n'
            u'\t<div class="center">\n'
            u'\t<h5>{header}</h5>\n'
            u'\t<form action="/api_submit" class="config_form">\n'
            u'\t\t<label for="api_key">\n'
            u'\t\t<span>{api_key_head}</span><input type="text" name="api_key" value="{api_key_value}" size="50"/>\n'
            u'\t\t</label>\n'
            u'\t\t<label for="api_id">\n'
            u'\t\t<span>{api_id_head}</span><input type="text" name="api_id" value="{api_id_value}" size="50"/>\n'
            u'\t\t</label>\n'
            u'\t\t<label for="api_secret">\n'
            u'\t\t<span>{api_secret_head}</span><input type="text" name="api_secret" value="{api_secret_value}" size="50"/>\n'
            u'\t\t</label>\n'
            u'\t\t<input type="submit" value="{submit}">\n'
            u'\t</form>\n'
            u'\t</div>\n'
            u'</body>\n</html>',

        'css':
            u'body {\n'
            u'  background: #141718;\n'
            u'}\n'
            u'.center {\n'
            u'  margin: auto;\n'
            u'  width: 600px;\n'
            u'  padding: 10px;\n'
            u'}\n'
            u'.config_form {\n'
            u'  width: 575px;\n'
            u'  height: 145px;\n'
            u'  font-size: 16px;\n'
            u'  background: #1a2123;\n'
            u'  padding: 30px 30px 15px 30px;\n'
            u'  border: 5px solid #1a2123;\n'
            u'}\n'
            u'h5 {\n'
            u'  font-family: Arial, Helvetica, sans-serif;\n'
            u'  font-size: 16px;\n'
            u'  color: #fff;\n'
            u'  font-weight: 600;\n'
            u'  width: 575px;\n'
            u'  height: 20px;\n'
            u'  background: #0f84a5;\n'
            u'  padding: 5px 30px 5px 30px;\n'
            u'  border: 5px solid #0f84a5;\n'
            u'  margin: 0px;\n'
            u'}\n'
            u'.config_form input[type=submit],\n'
            u'.config_form input[type=button],\n'
            u'.config_form input[type=text],\n'
            u'.config_form textarea,\n'
            u'.config_form label {\n'
            u'  font-family: Arial, Helvetica, sans-serif;\n'
            u'  font-size: 16px;\n'
            u'  color: #fff;\n'
            u'}\n'
            u'.config_form label {\n'
            u'  display:block;\n'
            u'  margin-bottom: 10px;\n'
            u'}\n'
            u'.config_form label > span {\n'
            u'  display: inline-block;\n'
            u'  float: left;\n'
            u'  width: 150px;\n'
            u'}\n'
            u'.config_form input[type=text] {\n'
            u'  background: transparent;\n'
            u'  border: none;\n'
            u'  border-bottom: 1px solid #147a96;\n'
            u'  width: 400px;\n'
            u'  outline: none;\n'
            u'  padding: 0px 0px 0px 0px;\n'
            u'}\n'
            u'.config_form input[type=text]:focus {\n'
            u'  border-bottom: 1px dashed #0f84a5;\n'
            u'}\n'
            u'.config_form input[type=submit],\n'
            u'.config_form input[type=button] {\n'
            u'  width: 150px;\n'
            u'  background: #141718;\n'
            u'  border: none;\n'
            u'  padding: 8px 0px 8px 10px;\n'
            u'  border-radius: 5px;\n'
            u'  color: #fff;\n'
            u'  margin-top: 10px\n'
            u'}\n'
            u'.config_form input[type=submit]:hover,\n'
            u'.config_form input[type=button]:hover {\n'
            u'  background: #0f84a5;\n'
            u'}\n'
    }


def run():
    print("------Broken HTTP Server Started-------")
    logger.debug("Service started")
    server_address = ('127.0.0.1', 6969)
    httpd = HTTPServer(server_address, BrokenHTTPRequestHandler)
    logger.debug("HTTP server started on port localhost:6969")
    httpd.serve_forever()

