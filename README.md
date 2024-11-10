# Livechat-Probot
This repository contains the code to **Probot**, a real-time chatbot with exceptional reasoning and human interaction capabilities. Inspired with integration with Large Language Models from LLaMA-3.1 family, Probot offers multiple services of real-time problem solving without having the need to open web hosted interfaces of models like ChatGPT. You can directly download the codebase, install the required libraries and modules and you have your own personal Chatbot Probot.

 Probot also offers multiple users on a single system i.e. multiple people can register, login and interact with the Probot while providing complete security to your personal data and chats. Probot can handle a wide range of problems like text summarization, mathematical reasoning, word problems, inferencing tasks, text generation, QnA problems, MCQs, logical reasoning and a lot more. Its one stop to everyday tasks from your homework to assignments, quizzes and much more ! Probot also retains your previous chats so that you can always access them. Probot also offers the feature of chat deletion. You can customize your deletion and look back options accordingly by changing the base code suited for your own purpose. Probot offers complete security and prevents any breach of personal data among multiple users using the same system

# Setup and Installation
The setup and installation of Probot is very easy and needs some simple downloads. Probot uses FastAPI for app server side and Postgres database for storing your data. Thus you need to download and setup your Postgres database (PG Admin) [https://youtu.be/KuQUNHCeKCk?si=DYbbn-aX_QxbSPMD]. After downloading Postgres, you need your personal Postgres username, database name for connecting your probot to your database (You can have a simple look at the code for database to get full understanding). For FastAPI, you can just run a simple command on terminal : `pip install fastapi`. You can just directly run a command using the requirements.txt file for installing all other libraries and modules.

`pip install -r requirements.txt`

For running the Probot, open a terminal/shell and go to the directory where your downloaded folders are placed. Run the following command then :

`uvicorn app:app --reload`

Now open a new terminal, go to the same directory and run the command :

`python chatbot_cli.py`

 # Features Of Probot & Using Them
## Register
![Screenshot 2024-11-09 224938](https://github.com/user-attachments/assets/6b52b20b-0e02-4cc8-a150-a652e7ba9536)

Registering as a new user is as simple as on any other platforms that you might have used till now. You just need to create your username and password. A two-way authentication passage checks the validity of your password and confirms your password twice before it becomes final. After that, the API redirects you directly to the Probot-CLI interface where you can start chatting. Your username and password gets stored automatically in the connected database while creation of user so that it can be used next time for validation during subsequent logins by the user.

### Rules for creating Username & Password
- Password must contain atleast 8 characters.
- Password must can contain only alphabets, numerals and special characters.
- Password must contain atleast one uppercase alphabet.
- Password must contain atleast one lowercase alphabet.
- Password must contain atleast one special character.
- Password must contain atleast one numeric character.
- Username has no restrictions.


## Login
![Screenshot 2024-11-10 185528](https://github.com/user-attachments/assets/6e6345f3-d347-43d3-8574-b9f92eacb1d8)

Login is very simple and user only needs his username and password for authentication purpose. Once login, you can start using Probot !


## Delete 
![Screenshot 2024-11-10 192213](https://github.com/user-attachments/assets/0433283e-b748-4735-8985-ea7856d21e34)


Deleting a user from database is also quite an easy process but strictly needs the correct username and password for it. Also after deleting a user, you are redirected to the menu section for further options.



