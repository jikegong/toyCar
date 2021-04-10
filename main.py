from machine import Pin
import network
try:
  import usocket as socket
except:
  import socket

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="toycar", password="jikegong")

while ap.active() == False:
  pass


a = Pin(5, Pin.OUT)
b = Pin(4, Pin.OUT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

a.off()
b.off()

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  if request.find('/off') == 6:
    a.off()
    b.off()
  if request.find('/left') == 6:
    a.on()
    b.off()
  if request.find('/right') == 6:
    b.on()
    a.off()
  if request.find('/on') == 6:
    a.on()
    b.on()
  response = """<html><head><title>toyCar</title><meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"><style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>Toy Car</h1> 
  <p><a href="/on"><button class="button">ON</button></a></p>
  <p><a href="/off"><button class="button">OFF</button></a></p>
  <p><a href="/left"><button class="button">LEFT</button></a></p>
  <p><a href="/right"><button class="button">RIGHT</button></a></p></body></html>"""
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
