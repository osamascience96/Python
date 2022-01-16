import socket

# here we passed 2 params in the socket function
# 1. AF_INET that is the address family that we have to specify to the socket {in this case we have IPV4 Address}
# 2. SOCK_STREAM is the socket type of tcp/ip protcol that we have to specifiy the protocol.
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# while connecting to the server, we gave the domain name (address of the website) and port to connect in that server 
domain = 'data.pr4e.org'
port = 80
mysocket.connect((domain, port))
# here in the specifc string we have defined the method of the request and the address concatenated with
# domain and the HTTP Version (1.0) the escape characters refer to enter 2 times when we are in the server
cmd = 'GET http://' + domain + '/page1.htm HTTP/1.0\r\n\r\n';
cmd = cmd.encode()
mysocket.send(cmd) # send the command

while True:
    data = mysocket.recv(512)
    # if the data buffered from the socket is less than 1
    if len(data) < 1:
        break
    # decode the receive the buffered bytes from the socket
    print(data.decode(), end='')


# close the socket
mysocket.close()
