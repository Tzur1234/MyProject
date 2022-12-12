# Flask Chat Application
### Video Demo: ???
### Description:

In this project I have built a simple chat app using the Flask framework, Python, Html and JavaScript. At first, I thought it would be an easy project, but the further I got with it, the more I understood the complexity of it.


Unlike the content of the CS50 course, which is really well organized and delivered, outside of that environment I found it quite overwhelming to navigate huge amounts of information about how to write a chat app using the Flask framework.
I think that the most challenging aspect was to clearly understand what I needed to learn before beginning the project. 

I learned that Socket is an object that plays a major role in communication between devices. The first thing I focused on was about sockets and how to work with them, especially how to use it with the Flask framework. Basically, every device, from smartphones to computers and servers utilizes sockets for managing the communication with other devices on the network.
To be even more accurate, each device has several programs and each of them uses sockets **to receive information and to send information** to other devices through the internet. In my case, I had to use sockets in order to manage the communication between different users (different devices, different IP addresses) sending and receiving messages in the chat app.

The main idea of the project was to build a chat group application.The user can simply sign in to the app at the **<ins>login.html</ins>** page by writing their name and then launches to the **<ins>index.html</ins>** page where they can watch the messages from other users and can also write some messages themselves. 

The main focus of the project was to establish two servers which manage all user activity on the website: from signing into the app - to using the chat app. Basically,
I created two servers: **server.py and main.py.**

**server.py:** this server continuously accepts new connections from other users, reads new messages sent from other users and forwards each new message to all other users <ins>**- all simultaneously !**</ins>

<ins>main.py:</ins>  this is the web server, taking care of the users transitions between login page to index page. This is the primary chain connecting between the server side and the user side. 

Both servers,  web server (**main.py**) and main server (**server.py**) <ins>use a list of objects to track their users that are connected to the chat.</ins>

<ins>server.py</ins> uses the **Person** object, each person object stores the users’ socket, the name of the user and its IP address. Meanwhile, <ins> main.py </ins> uses the **Client** object to also store the user’s socket. Both sockets on each server represent the same users, but on the other side of the connection.

![alt text](https://github.com/Tzur1234/MyProject/blob/main/TEST/test.py/3232.JPG)


The main functions used for sending information between servers and users are:
**recv()
send()**

Both are built-in functions from the socket object. As we have learned on the course, information is transferred through the network in “small-pieces”, in other words - bytes. In relation to my app, before a message is sent, it is first disassembled to small pieces, or, bytes. Then these pieces are sent in small packages. It is much more reliable to transfer the data in small pieces than in larger pieces.

Beyond learning about those two functions, I have also learned about the standard practice of sending each message with a “header”. A header is a fixed number of bytes concatenated to the message. In the beginning, it contains information about the length of the message. For example, if we want to send the message ‘hello’. 
The ‘hello’ message has five characters, hence the first 10 characters at the beginning of the message are going to be the number 5 and the other part of the message is the message itself. By using headers, we can have a better view of received messages and know if all the parts were successfully received. 

In both servers, **server.py and client.py** I wrote auxiliary functions such as <ins>**conver_to_b and conver_to_msg**</ins> , those make the translating processes, translate from byte to string message or visa versa more efficiently.
By the way - recv() and send() both accept and return only bytesand therefore I had to write **conver_to_b() and conver_to_msg()**

![alt text](https://github.com/Tzur1234/MyProject/blob/main/TEST/test.py/111.JPG)
![alt text](https://github.com/Tzur1234/MyProject/blob/main/TEST/test.py/222.JPG)
![alt text](https://github.com/Tzur1234/MyProject/blob/main/TEST/test.py/333.JPG)
![alt text](https://github.com/Tzur1234/MyProject/blob/main/TEST/test.py/444.JPG)












