
# Heavily mangled from an example by Jon Berg , turtlemeat.com

"""
This script runs a web server that will accept requests to:
  /shutdown
  /reboot
  /sleep
  /hibernate
  /test

  And nothing else, including not to "/" or "/index".

  I'm starting it using the process documented here:
    http://answers.microsoft.com/en-us/windows/forum/windows_vista-performance/how-do-i-create-a-user-defined-service/ed290a19-3115-4c26-abee-5122181877e1?auth=1
"""

import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):

    # List of URLs accepted, and what command to run when we get them.
    commands = {
      '/shutdown' : 'shutdown.exe -s',
      '/reboot' : 'shutdown.exe -r',
      '/sleep' : 'shutdown.exe -h',
      '/hibernate' : 'shutdown.exe -h',
      '/test' : None,
    }

    try:
      if self.path in commands.keys():
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        # Don't really do anything for /test
        if not commands[self.path]:
          self.wfile.write("Success.")
          self.wfile.close()
          return

        self.wfile.write("Attempting...")
        self.wfile.close()
        subprocess.call(commands[self.path], shell=True)

    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)

def main():
  try:
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()
  except KeyboardInterrupt:
    server.socket.close()

if __name__ == '__main__':
  main()
