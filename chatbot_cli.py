import requests
import ast

API_URL = "http://localhost:8000/api"  # Adjust if your FastAPI server is running elsewhere

def register_user(username, password):
    response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def login_user(username, password):
    response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def send_message(user_id, message):
    response = requests.post(f"{API_URL}/message", json={"user_id": user_id, "message": message})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

def get_chat_history(user_id, limit):
    response = requests.post(f"{API_URL}/history", json={"user_id": user_id, "limit": limit})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}
    
def delete_user(username, password):
    response = requests.delete(f"{API_URL}/delete_user", json={"username": username, "password": password})
    return response.json() if response.status_code == 200 else {"error": response.text}

def main():
    print("Welcome to Probot ! I am here to solve your queries\n")
    counter_history = 1
    clear_counter_history = 1
    while True:
        action = input("\nDo you want to (register/login/delete)? Or type 'exit' to quit: ").strip().lower()
        
        if action == 'exit':
            print("\nGoodbye! Visit Again\n")
            break

        username = input("\nEnter your username: ")
        password = input("Enter your password: ")

        if action == 'delete':
            delete_response = delete_user(username, password)
            if 'error' in delete_response:
                print("\nInvalid Username or Password\n")
            else:
                print("\n{}\n".format(delete_response[0]))
        elif action == 'register':
            check_pass = input("Confirm Password: ")
            print("\n")
            if password != check_pass:
                print("\nPassword does not match !\n")
                continue
            register_response = register_user(username, password)
            # register_response = ast.literal_eval(register_response)
            print(f"{register_response['message']} Please Wait while we redirect you to the chatbot. Thank you !\n")

            login_response = login_user(username, password)
            if 'error' in login_response:
                details = ast.literal_eval(login_response['error'])
                print("Login failed: {}\n".format(details['detail']))
                continue

            user_id = login_response['user']['id']
            print("\nLogin successful!")
            print("Hi I am Probot ! How may I help you today ?\n")

            while True:
                message = input("{}: ".format(username))
                print("\n")
                if message.lower() == "exit":
                    print("Logging out...\n")
                    break

                # Send the message to the chatbot
                response = send_message(user_id, message)
                if 'error' in response:
                    print("Error sending message: {}\n".format(response['error']))
                else:
                    print("Probot: {}\n".format(response['response']))

                counter_history += 1
                clear_counter_history += 1
                want = False
                if counter_history % 5 == 0:
                    print("\nWant to see previous chats ? (Y/N)")
                    inp = input()
                    want = inp == 'Y'
                    counter_history= 1

                # Optionally fetch and display chat history
                if want == True:
                    print("\nHow many previous chats would you like to see? \n")
                    limit = int(input())
                    history_response = get_chat_history(user_id, limit)
                    if 'error' in history_response:
                        print(f"Error fetching chat history: {history_response['error']}")
                    else:
                        print("Chat History:\n")
                        print(history_response['history'])

                if clear_counter_history % 10 == 0:
                    clear_counter_history = 1
                    clear_action = input("\nDo you want to clear your chat history? (Yes/No): ").strip().lower()
                    if clear_action == 'yes':
                        clear_response = requests.delete(f"{API_URL}/clear_history", json={"username": username, "password": password})
                        if clear_response.status_code == 200:
                            print("Chat history cleared.\n")
                        else:
                            print(f"Error clearing chat history: {clear_response.text}\n")
        elif action == 'login':
            login_response = login_user(username, password)
            if 'error' in login_response:
                details = ast.literal_eval(login_response['error'])
                print("Login failed: {}\n".format(details['detail']))
                continue

            user_id = login_response['user']['id']
            print("\nLogin successful!")
            print("Hi I am Probot ! How may I help you today ?\n")

            while True:
                message = input("{}: ".format(username))
                print("\n")
                if message.lower() == "exit":
                    print("Logging out...\n")
                    break

                # Send the message to the chatbot
                response = send_message(user_id, message)
                if 'error' in response:
                    print("Error sending message: {}\n".format(response['error']))
                else:
                    print("Probot: {}\n".format(response['response']))

                counter_history += 1
                clear_counter_history += 1
                want = False
                if counter_history % 5 == 0:
                    print("\nWant to see previous chats ? (Y/N)")
                    inp = input()
                    want = inp == 'Y'
                    counter_history= 1

                # Optionally fetch and display chat history
                if want == True:
                    print("\nHow many previous chats would you like to see? \n")
                    limit = int(input())
                    history_response = get_chat_history(user_id, limit)
                    if 'error' in history_response:
                        print(f"Error fetching chat history: {history_response['error']}")
                    else:
                        print("Chat History:\n")
                        print(history_response['history'])

                if clear_counter_history % 10 == 0:
                    clear_counter_history = 1
                    clear_action = input("\nDo you want to clear your chat history? (Yes/No): ").strip().lower()
                    if clear_action == 'yes':
                        clear_response = requests.delete(f"{API_URL}/clear_history", json={"username": username, "password": password})
                        if clear_response.status_code == 200:
                            print("Chat history cleared.\n")
                        else:
                            print(f"Error clearing chat history: {clear_response.text}")

if __name__ == "__main__":
    main()
