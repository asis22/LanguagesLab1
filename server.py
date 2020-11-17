from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import json

from pytz import timezone
from dateutil import parser


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @staticmethod
    def _process_date(date_as_string):
        date = json.loads(date_as_string.replace("'", "\""))
        if 'tz' in date and date['tz'] is not None:
            date['tz'] = timezone(date['tz'])
            date['date'] = parser.parse(date['date'])
            date['date'] = datetime(str(date['date']), tzinfo=date['tz'])
        else:
            date['date'] = parser.parse(date['date'])
        return date


    def do_GET(self):
        o = urlparse(self.path)
        resp_name = o.path[1:]
        args = parse_qs(o.query)
        logging.info(resp_name)
        logging.info(args)
        if resp_name == "":
            self._set_response()
            self.wfile.write("Server current time:\n".encode('utf-8'))
            self.wfile.write(str(datetime.now()).encode('utf-8'))
        elif resp_name == "favicon.ico":
            self.send_response(404)
        else:
            tz = timezone(resp_name)
            self._set_response()
            self.wfile.write(f"Get time for timezone with name {resp_name}:\n".encode('utf-8'))
            time = str(datetime.now(tz=tz))
            logging.info(time)
            self.wfile.write(time.encode('utf-8'))

    def do_POST(self):
        o = urlparse(self.path)
        resp_name = o.path[1:]
        args = parse_qs(o.query)
        logging.info(resp_name)
        logging.info(args)
        self._set_response()
        start = self._process_date(args['start'][0])
        end = self._process_date(args['end'][0])
        logging.info(start)
        logging.info(end)
        self.wfile.write(str(start).encode('utf-8'))
        self.wfile.write(str(end).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8090):
    logging.basicConfig(level=logging.INFO)
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    run()
