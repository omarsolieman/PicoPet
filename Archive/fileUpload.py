import network
import usocket as socket
import uos

# Setup WiFi
def setup_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network config:', wlan.ifconfig())

# Create a simple HTTP server to handle file uploads
def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    print('Server listening on port 80')
    
    while True:
        conn, addr = server_socket.accept()
        print('Connection from', addr)
        
        try:
            request = conn.recv(1024)
            if not request:
                print('No data received')
                conn.close()
                continue

            request_line = str(request).split('\r\n')[0]
            print('Request line:', request_line)
            
            if request_line.startswith('b\'GET'):
                if b'favicon.ico' in request:
                    conn.send(b'HTTP/1.1 200 OK\r\n')
                    conn.send(b'Content-Type: image/x-icon\r\n')
                    conn.send(b'Connection: close\r\n\r\n')
                elif b'/style.css' in request:
                    try:
                        with open('Web/style.css', 'r') as f:
                            css_content = f.read()
                        conn.send(b'HTTP/1.1 200 OK\r\n')
                        conn.send(b'Content-Type: text/css\r\n')
                        conn.send(b'Connection: close\r\n\r\n')
                        conn.send(css_content.encode())
                    except Exception as e:
                        print('Error reading CSS file:', str(e))
                        conn.send(b'HTTP/1.1 500 Internal Server Error\r\n')
                        conn.send(b'Content-Type: text/plain\r\n')
                        conn.send(b'Connection: close\r\n\r\n')
                        conn.send(b'Internal Server Error: ' + str(e).encode())
                else:
                    try:
                        with open('Web/index.html', 'r') as f:
                            html_content = f.read()
                        conn.send(b'HTTP/1.1 200 OK\r\n')
                        conn.send(b'Content-Type: text/html\r\n')
                        conn.send(b'Connection: close\r\n\r\n')
                        conn.send(html_content.encode())
                    except Exception as e:
                        print('Error reading HTML file:', str(e))
                        conn.send(b'HTTP/1.1 500 Internal Server Error\r\n')
                        conn.send(b'Content-Type: text/plain\r\n')
                        conn.send(b'Connection: close\r\n\r\n')
                        conn.send(b'Internal Server Error: ' + str(e).encode())
                conn.close()
            elif request_line.startswith('b\'POST'):
                try:
                    content_length = int(request.split(b'Content-Length: ')[1].split(b'\r\n')[0])
                    print('Content-Length:', content_length)

                    while len(request) < content_length:
                        request += conn.recv(1024)

                    boundary = None
                    for line in request.split(b'\r\n'):
                        if line.startswith(b'Content-Type: multipart/form-data; boundary='):
                            boundary = line.split(b'boundary=')[1]
                            break
                    
                    if boundary:
                        request_parts = request.split(b'--' + boundary)
                        
                        for part in request_parts[1:-1]:
                            header_part, file_content = part.split(b'\r\n\r\n', 1)
                            
                            filename = None
                            for line in header_part.split(b'\r\n'):
                                if line.startswith(b'Content-Disposition'):
                                    filename = line.split(b';')[2].split(b'=')[1].strip(b'"')
                                    break
                            
                            if filename:
                                with open('EmotionsW/' + filename.decode('utf-8'), 'wb') as f:
                                    f.write(file_content)
                                
                                conn.send(b'HTTP/1.1 303 See Other\r\n')
                                conn.send(b'Location: http://192.168.1.64:80?upload=success\r\n')
                                conn.send(b'Connection: close\r\n\r\n')
                                break
                            else:
                                print('Filename not found in request')
                                conn.send(b'HTTP/1.1 400 Bad Request\r\n')
                                conn.send(b'Content-Type: text/plain\r\n')
                                conn.send(b'Connection: close\r\n\r\n')
                                conn.send(b'Bad Request')
                    else:
                        print('Boundary not found in request')
                        conn.send(b'HTTP/1.1 400 Bad Request\r\n')
                        conn.send(b'Content-Type: text/plain\r\n')
                        conn.send(b'Connection: close\r\n\r\n')
                        conn.send(b'Bad Request')
                except Exception as e:
                    conn.send(b'HTTP/1.1 500 Internal Server Error\r\n')
                    conn.send(b'Content-Type: text/plain\r\n')
                    conn.send(b'Connection: close\r\n\r\n')
                    conn.send(b'Internal Server Error: ' + str(e).encode())
            else:
                print('Unhandled request method')
                conn.send(b'HTTP/1.1 405 Method Not Allowed\r\n')
                conn.send(b'Content-Type: text/plain\r\n')
                conn.send(b'Connection: close\r\n\r\n')
                conn.send(b'Method Not Allowed')
            
            conn.close()
        except Exception as e:
            print('Error:', str(e))
            conn.send(b'HTTP/1.1 500 Internal Server Error\r\n')
            conn.send(b'Content-Type: text/plain\r\n')
            conn.send(b'Connection: close\r\n\r\n')
            conn.send(b'Internal Server Error: ' + str(e).encode())
            conn.close()

# Main function to setup WiFi and create server
def main():
    setup_wifi('ODesigns', 'omartaher2004')
    create_server()

if __name__ == "__main__":
    main()
