# pybot
This code is a Python script that checks for internet availability and sends a message with a link extracted from the output of a Linux command to a Telegram bot. The code runs in an infinite loop until internet becomes available or it is interrupted. If an error occurs while sending the message, the error is displayed.
This is usefull while using cloudflared or ngrok in every boot, this script will automatically run and send that link to a telegram chat.
This script this specifically made for cloudflared