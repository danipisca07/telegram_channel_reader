# telegram_channel_reader
Python api to read messages from public telegram channels. Perfect for integration with integration platforms like n8n.

#Run me


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