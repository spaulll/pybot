import subprocess
import requests
import socket
import time
import re

# Telegram bot token and chat ID
bot_token = "bot_token_here"
chat_id = "chat_id_for_a_specific_user"

# Linux command to run on startup
command = "nohup {command here} > gh.txt &"   #enter linux command here 

# File to save command output to
output_file = "gh.txt"

def check_internet_availability():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def countdown(t):
    while t:
        
        time_left = "Checking for internet availability in next {:02d} secs::".format(t)
        print(time_left, end="\r")
        time.sleep(1)
        t -= 1

while True:
    if check_internet_availability():
        # Run command and save output to file
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",json={"chat_id": chat_id,"text": e})
        else:
            time.sleep(15) # Wait for 15 seconds after executing the command
            # Read contents of output file
            with open(output_file, "r") as f:
                output = f.read()
            # Extract links from output
            links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)
            # Prepare the message with the link
            message=links[1]
            # Send output to Telegram bot
            try:
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage",json={"chat_id": chat_id,"text": message})
                print(message)
            except Exception as e:
                print(f"An error occurred while sending the message: {e}")
            exit()
    else:
        countdown(20)
        print("\r")
        print("Still not internet:(\nChecking again.")

