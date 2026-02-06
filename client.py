import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to chat server (type 'quit' to exit)")


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            # Print message even if user is typing
            print(f"\n{message}")
            print("> ", end="", flush=True)
        except:
            break


# Start thread to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

# Main loop to send messages
while True:
    msg = input("> ")
    if msg.lower() == "quit":
        break
    client_socket.send(msg.encode())

client_socket.close()
print("Disconnected")
