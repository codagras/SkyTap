import http.server
import socketserver
from multiprocessing import Process

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return
    
    def translate_path(self, path):
        return http.server.SimpleHTTPRequestHandler.translate_path(self, '/webFiles' + path)

def startWebserver(port):

    Handler = QuietHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("**Display at http://localhost:" + str(port))
    server_process = Process(target=httpd.serve_forever)
    server_process.start()
    return

if __name__=="__main__":
    port = 8000
    startWebserver(port)


    
