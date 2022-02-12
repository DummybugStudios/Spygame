import socket
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))
    s.listen()
    print(f"Listening on PORT {PORT}")
    print(f"IP ADDR: {socket.gethostbyname(socket.gethostname())}")
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data: 
                break 
            if data.startswith(b"GET"):
                print("Exiting...")
                break
            print(data)
