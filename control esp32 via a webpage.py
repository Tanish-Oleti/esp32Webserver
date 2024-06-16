import machine
import usocket as socket
import time
import network

timeout = 0 #WiFi connection Timeout variable
wifi=network.WLAN(network.STA_IF)
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

wifi.connect("TANYOG","bulbul12")

if not wifi.isconnected():
    print("connecting...")
    while (not wifi.isconnected() and timeout<5):
        print(5-timeout)
        timeout=timeout+1
        time.sleep(1)
        
if wifi.isconnected():
    print('connected...')
    print(" network config",wifi.ifconfig())
    
#HTML Document
html='''<!DOCTYPE html>
<html>
<center><h2>ESP32 Webserver </h2></center>
<form>
<center>
<h3>LED</h3>
<button name="LED" value='ON' type='submit'> ON </button>
<button name="LED" value='OFF' type='submit'> OFF </button>
</center>
'''

#output pin declaration
LED =machine.Pin(2,machine.Pin.OUT)
LED.value(0)

#Initialising socket
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM) #AF_INET-Internet socket ,SOCK_STREAM-tcp protocol

Host=''#empty means it will allow all IP addresses to connect
Port = 80#HTTP port
s.bind((Host,Port))
#addr=socket.getaddrinfo('0.0.0.0',80)[0][-1]
#s.bind(addr)

s.listen(5) # It will handle maximum 5 clients at a time
n=0
#main loop
while True:
    connection_socket,address =s.accept()# storing Conn_socket and address of new client connected "
    print("got a connection from" ,address)
    n=n+1
    print(n)
    request =connection_socket.recv(1024)#storing response coming from client
    print("content",request)#printing response
    request=str(request)#converting bytes to string
    #print(request)
    #comparing & finding position of word in string
    LED_ON=request.find('/?LED=ON')
    print(LED_ON)
    LED_OFF=request.find('/?LED=OFF')
    
    if (LED_ON==6):
        LED.value(1)
    if (LED_OFF==6):
        LED.value(0)
        
    # sending HTML document in response everytime to all connected clients
    response=html
    connection_socket.send(response)
    
    #Closing the socket
    connection_socket.close()

    