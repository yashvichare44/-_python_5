import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Use '0.0.0.0' to allow connections from external IPs
PORT = 12345

# List to keep track of connected clients
clients = []

# Function to handle each client connection
def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                remove_client(client_socket)
                break
            print(f"Message from {client_address}: {message}")
            broadcast(f"{client_address}: {message}", client_socket)
        except:
            remove_client(client_socket)
            break

# Function to broadcast messages to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

# Function to remove a client from the list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server running on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    main()
