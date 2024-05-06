import socket
import threading

from config import ADMIN_PASS, BAN_FILE, HOST, PORT

# Get: Host IP and Port
host_ip = socket.gethostbyname(socket.gethostname())

# Start: Server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

# List: For Clients and Their Nicknames
clients_list = []
nicknames_list = []


def broadcast_message(message):
    """Function to broadcast messages to all connected clients."""
    for client in clients_list:
        client.send(message)


def handle_client(client):
    """Function to handle messages from a single client."""
    while True:
        try:
            received_msg = message = client.recv(1024)
            if received_msg.decode("utf-8").startswith("KICK"):
                if nicknames_list[clients_list.index(client)] == "admin":
                    name_to_kick = received_msg.decode("utf-8")[5:]
                    kick_user(name_to_kick)
                else:
                    client.send(b"Command was refused!")

            elif received_msg.decode("utf-8").startswith("BAN"):
                if nicknames_list[clients_list.index(client)] == "admin":
                    name_to_ban = received_msg.decode("utf-8")[4:]
                    kick_user(name_to_ban)
                    with open(BAN_FILE, "a") as f:
                        f.write(f"{name_to_ban}\n")
                    print(f"{name_to_ban} is banned")
                else:
                    client.send(b"Command was refused!")
            else:
                broadcast_message(message)
        except Exception:
            if client in clients_list:
                index = clients_list.index(client)
                clients_list.remove(client)
                client.close()
                nickname = nicknames_list[index]
                broadcast_message(f"{nickname} has left the chat!".encode())
                nicknames_list.remove(nickname)
                break


def receive_messages():
    """Function to continuously accept connections from clients."""
    while True:
        client_connection, address = server_socket.accept()
        print(f"Connected with {str(address)}")

        client_connection.send(b"NICK")
        nickname = client_connection.recv(1024).decode("utf-8")

        with open(BAN_FILE) as f:
            bans = f.readlines()

        if nickname + "\n" in bans:
            client_connection.send(b"BAN")
            client_connection.close()
            continue

        if nickname == "admin":
            client_connection.send(b"PASS")
            password = client_connection.recv(1024).decode("utf-8")

            if password != ADMIN_PASS:
                client_connection.send(b"REFUSE")
                client_connection.close()
                continue

        nicknames_list.append(nickname)
        clients_list.append(client_connection)

        print(f"Nickname is {nickname}")
        broadcast_message(f"{nickname} joined!".encode())
        client_connection.send(b"Connected to server!")

        thread = threading.Thread(
            target=handle_client, args=(client_connection,)
        )
        thread.start()


def kick_user(name):
    """Function to kick a user from the chat."""
    if name in nicknames_list:
        name_index = nicknames_list.index(name)
        client_to_kick = clients_list[name_index]
        clients_list.remove(client_to_kick)
        print(f"{name} was kicked by an admin!")
        client_to_kick.send(b"You were kicked by an admin!")
        client_to_kick.close()
        nicknames_list.remove(name)
        broadcast_message(f"{name} was kicked by an admin!".encode())


print("Server is listening")
receive_messages()
