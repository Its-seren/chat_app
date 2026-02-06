## Multi-Client Python Chat Application with MySQL Integration

This is a Python-based chat application designed for multiple clients to communicate in real-time. All messages are persistently stored in a MySQL database, enabling efficient data management. Built with threading and socket programming, this project demonstrates backend development skills and database integration.

## Features

- Supports multiple clients chatting in real-time
- Broadcasts messages to all connected clients
- Persists all messages in a MySQL database
- Server can send messages to all clients
- Uses environment variables for secure credential management

## Setup Instructions

1. **Clone the repository**

git clone https://github.com/Its-seren/chat_app.git
cd chat_app

2. **Install Required Python Packages**

pip install mysql-connector-python

3. **Set environment variables**

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=chat_db

4. **Run the server**
 
python server.py

5. **Run the client in separate terminals**

python client.py

6. **Start chatting!!**
Messages will be saved in chat_db.messages
