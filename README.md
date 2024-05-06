# Chat Application with Client-Server Communication

## Description

This repository contains a simple chat application implemented in Python, facilitating communication between clients and a server over a network. The application consists of two main components: a client-side script (`client.py`) and a server-side script (`server.py`).

## Features

- **Client Interaction:** The `client.py` script allows users to connect to the server, choose a nickname, and engage in real-time chat with other connected clients.
- **Server Management:** The `server.py` script manages client connections, broadcasting messages to all connected clients, and handling administrative commands such as kicking and banning users.

## Functionality

- **User Authentication:** Users can choose a nickname upon connection, with special privileges reserved for an "admin" user.
- **Real-Time Communication:** Messages sent by clients are immediately broadcasted to all other connected clients, enabling real-time communication.
- **Admin Commands:** The "admin" user can execute commands such as kicking and banning other users from the chat using `?kick` and `?ban` commands.

## Planned Updates

- **Database Integration:** Future updates will include integrating a database to store chat history, user profiles, and banned users.
- **GUI Implementation:** A graphical user interface (GUI) will be developed for a more user-friendly chat experience.
- **Deployment:** The application will be deployed on a server, allowing users to access the chat application from anywhere with an internet connection.

## Usage

1. Run the `server.py` script to start the server.
2. Run the `client.py` script on each client machine to connect to the server.
3. Choose a nickname and start chatting with other connected clients.

## Note

- Ensure Python 3.x is installed on your system to run the scripts.
- Modify the `server.py` script to change the host IP and port number if required.
- Admin privileges are granted based on the chosen nickname. Ensure to use the correct admin password defined in the scripts.
