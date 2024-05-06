import socket
import threading

from config import HOST, PORT

# Choose: Nickname
user_nickname = input("Choose your nickname: ")
if user_nickname == "admin":
    user_password = input("Enter the admin password: ")

# Connect: To Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

stop_thread = False


def receive_messages():
    """Function to continuously receive messages from the server."""
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            received_message = client_socket.recv(1024).decode("utf-8")
            if received_message == "NICK":
                client_socket.send(user_nickname.encode("utf-8"))
                next_message = client_socket.recv(1024).decode("utf-8")
                if next_message == "PASS":
                    client_socket.send(user_password.encode("utf-8"))
                    if client_socket.recv(1024).decode("utf-8") == "REFUSE":
                        print("Wrong Password! Connection refused.")
                        stop_thread = True
                elif next_message == "BAN":
                    print("Connection refused because of a ban!")
                    client_socket.close()
                    stop_thread = True
            else:
                print(received_message)
        except Exception:
            print("An error occurred!")
            client_socket.close()
            break


def send_messages():
    """Function to continuously send messages to the server."""
    while True:
        if stop_thread:
            break
        message = f'{user_nickname}: {input("")}'
        if message[len(user_nickname) + 2 :].startswith("?"):
            if user_nickname == "admin":
                if message[len(user_nickname) + 2 :].startswith("?kick"):
                    client_socket.send(
                        f"KICK {message[len(user_nickname)+2+6:]}".encode()
                    )
                elif message[len(user_nickname) + 2 :].startswith("?ban"):
                    client_socket.send(
                        f"BAN {message[len(user_nickname)+2+5:]}".encode()
                    )
            else:
                print("Commands can only be executed by admin!")
        else:
            client_socket.send(message.encode("utf-8"))


# Start: Threads For Receiving and Sending Messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
