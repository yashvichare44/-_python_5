import tkinter as tk
from tkinter import messagebox
import socket
import threading

# Server settings
HOST = '127.0.0.1'
PORT = 12345

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + '\n')
            chat_box.config(state=tk.DISABLED)
            chat_box.see(tk.END)
        except:
            print("Connection to the server was lost.")
            client_socket.close()
            break

# Function to send a message
def send_message():
    message = message_entry.get()
    client_socket.send(message.encode('utf-8'))
    message_entry.delete(0, tk.END)

# Main client function
def main():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    root = tk.Tk()
    root.title("Chat Application")

    global chat_box
    chat_box = tk.Text(root, state=tk.DISABLED)
    chat_box.pack(pady=10)

    global message_entry
    message_entry = tk.Entry(root, width=50)
    message_entry.pack(pady=5)

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
