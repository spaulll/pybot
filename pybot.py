import subprocess
import requests
import socket
import time
import re

# Telegram bot token and chat ID
bot_token = "5773081826:AAFoVqcMm6UuA1VAPNyrqG4NQpPajV2lSc8"
chat_id = "579397885"

# Linux command to run on startup
command = "nohup cloudflared  --url localhost > gh.txt &"

# File to save command output to
output_file = "gh.txt"

def check_internet_availability():
    try:
        # Connect to the Google DNS server to check internet availability
        socket.gethostbyname("1.1.1.1")
        return True
    except socket.gaierror:
        return False


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
    else:
        print("No internet connection, trying again in 10 seconds...")
        time.sleep(10)
