# telegram_channel_reader
Python api to read messages from public telegram channels. Perfect for integration with integration platforms like n8n.

# Setup
## VEnv
Advised to always use a VENV to install the python deps:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Telethon Session Init
To initialize the Telethon session, you need to run the `init_session.py` script. This will create a session file that is required for authentication.
This script will prompt you for your phone number and send a code to that number for verification.
```
python init_session.py
```
This file will avoid the need to enter your phone number and code every time you use the API. 
The infos are stored in a file called `session_info.txt` and `telegram_channel_reader.session` in the same directory as the script.
Remember to keep this files secure as they contains your session information. And deploy them to your server in the same directory as the API if you want to use the api without having access to the console to interactively enter your code.
# Test Me

curl -X POST http://localhost:5000/get_messages \
  -H "Content-Type: application/json" \
  -d '{
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH",
    "phone": "YOUR_PHONE_NUMBER",
    "channel": "CHANNEL_USERNAME_OR_ID",
    "after_date": "2024-07-27T09:00:00"  # Optional, can be removed
  }'