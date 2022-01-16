from socket import *

# defines the maximum number of calls that can be made to the server
MAX_CALLS_QUEUE = 5

def createServer():
    # configure the socket
    serverSocket = socket(AF_INET, SOCK_STREAM);
    try:
        # bind the server to the localhost and to the port 9000
        serverSocket.bind(('127.0.0.1', 9000))
        # define the number requests that can queue when request the data from the server
        serverSocket.listen(MAX_CALLS_QUEUE); 

        while(1):
            (clientSocket, address) = serverSocket.accept()

            rd = clientSocket.recv(5000).decode()
            pieces = rd.split("\n")
            if(len(pieces) > 0):
                print(pieces[0])
            
            # write the data for the response
            data = "HTTP/1.1 200 OK\r\n"
            data += "Content-Type:text/html; charset=utf-8\r\n"
            data += "\r\n"
            data += "<html><body>Hello World</body></html>"

            # response back to the server
            clientSocket.sendall(data.encode())
            # close the connection to the client
            clientSocket.shutdown(SHUT_WR)
    except KeyboardInterrupt:
        print("\n Shutting Down...\n");
    except Exception as exc:
        print("Error \n");
        print(exc)
    
    # close the socket
    serverSocket.close()

print('Access http://localhost:9000')
createServer()