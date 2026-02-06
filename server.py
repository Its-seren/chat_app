import socket
import threading
import os
import mysql.connector

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()

# GLOBAL VARIABLES
clients = []          # list of client sockets
usernames = {}        # client_socket -> username
user_count = 100
lock = threading.Lock()


# HANDLE CLIENT
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            print(f"{usernames[client_socket]}: {message}")

            # this will save message to database
            cursor.execute(
                "INSERT INTO messages (sender, message) VALUES (%s, %s)",
                (usernames[client_socket], message)
            )
            db.commit()

            # this will broadcast to all other clients
            with lock:
                for c in clients:
                    if c != client_socket:
                        try:
                            c.send(f"{usernames[client_socket]}: {message}".encode())
                        except:
                            pass

        except:
            break

    # Cleanup on disconnect
    with lock:
        clients.remove(client_socket)
        username = usernames.pop(client_socket)
    print(f"{username} disconnected")
    client_socket.close()


# SERVER BROADCAST
def server_broadcast():
    while True:
        msg = input()  # server types message
        if msg.strip() == "":
            continue

        # Save server message to database
        cursor.execute(
            "INSERT INTO messages (sender, message) VALUES (%s, %s)",
            ("Server", msg)
        )
        db.commit()

        # Send to all clients
        with lock:
            for c in clients:
                try:
                    c.send(f"Server: {msg}".encode())
                except:
                    pass


# SERVER SETUP

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 5000

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# Start server broadcast thread
threading.Thread(target=server_broadcast, daemon=True).start()

# Accept clients
while True:
    client_socket, _ = server_socket.accept()

    with lock:
        username = f"user{user_count}"
        user_count += 1
        clients.append(client_socket)
        usernames[client_socket] = username

    print(f"{username} connected")

    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()