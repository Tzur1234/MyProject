# Flask Chat Application
### Video Demo: https://www.youtube.com/watch?v=jvGsq23wQps&t=42s
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


---------------------------------------------------------------------------------------------------------------------------------------

<ins>Server.py:</ins>
Do  3 things at the same time:
1. Looking for a new connection
2. Reading new messages from each connected user (in his socket)
3. Send the new message to all other users (by using their socket)

<ins>Thread:</ins>

I have  also learned alot about threads and there advantages: Thread are tiny unit of process and process is another word for a program that running and consume the CPU resources for completing task. For example - consistently running and cheking new received connection to the server - this is just one example for a task in my app running by Thread.
What interesting even more is that the CPU is’nt always used by one function. it’s called  “dead-times”. This is when threads come into the picture and can use CPU hardware sources more efficiently by utilize it during the “dead-times”. To make it even more simple, we use threads to execute all server’s functions at the same time (looking for new connections, reading and writing sockets)

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Multithreaded_process.svg/1024px-Multithreaded_process.svg.png)


<ins>Client.py:</ins>

In this module I wrote the Client object, which represents each user when they connecting to the server (to the chat app). 
 The methods inside the class are: 
1. sending messages
2. receiving messages
3. Auxiliary converting functions (like in server.py)

The format of the messages received or sent from Client are equall to the format in **<ins>server.py</ins>**, without that they couldn’t interact with each other


**<ins>main.py</ins>**
this is the third chain and the most important part in the backend scripts. The user movement between the login and index page is manged in this module, using Flask framework. I chose this framework because we already got use to it in the course.
Every time a new user sign in, he launches the index page where he can start to write messages to other users and watch there messages.
During the sign in process, a new **Client object** created and stored in the session object in main,py. I remember that what special about session is that it allows to store the each user’s thought all routes’ functions.

###<ins>Frontend - index.js</ins>

By using Javascript the message from the send box on <ins>index.html</ins> page is extracted once the user press the sending buttom (‘send’). Than, behind the scenes the <ins>send_message()</ins> is activated and the message is transferred to server.py and from there to all of the connected users. Moreover, by using Javascript the browser always checking for a new message (every 1000 milliseconds) and if there are new messages, they are displayed in the chetbox in the <ins>index.html</ins> page (thanks to the the <ins>update()</ins> function)

<ins>in Index.js : update every 1 second </ins>


![alt text](https://github.com/Tzur1234/MyProject/blob/main/TEST/test.py/js.JPG)

----------------------------------------------

In addition as the convention of Flask framework folders should look like, there is a templates folder where you can find all of the HTML pages I have built. There is the basic <ins>**template**</ins> folder called base.html two other major HTML files inherited , index and login.


## To Sum Up:

The application consists four major components: server.py, main.py client.py and index.js 

Those are working separately and responsible for the dynamic message transferring between the individual user to all other users. 

I believe that if I had had more time I would have learned more about SocketIO object which could have made the all server.py server much more simple. I also would have learned Javascript and maybe the AJAX library more deeply in order to have a better understanding how to connect between the backend and the frontend. 
I think I have learned alot from my first programming project and can’t wait for the next optional CS50 courses.

Thank you !  








