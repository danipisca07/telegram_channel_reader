from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import os
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser  # pip install python-dateutil

app = Flask(__name__)

@app.route('/get_messages', methods=['POST'])
def get_messages():
    data = request.json or {}

    required_fields = ['channel']
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({
            'error': 'Missing required fields.',
            'missing_fields': missing
        }), 400

    api_id = data.get('api_id')
    api_hash = data.get('api_hash')
    phone = data.get('phone')
    channel = data['channel']

    #if parameters are not provided, read them from the session_info.txt file
    if not (api_id and api_hash and phone):
        if not os.path.exists('session_info.txt'):
            return jsonify({'error': 'Session info file not found. Please run init_session.py first.'}), 400
        with open('session_info.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) < 3:
                return jsonify({'error': 'Session info file is incomplete.'}), 400
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone = lines[2].strip()

    # Parse date or fallback to 24h ago
    if 'after_date' in data:
        try:
            after_date = date_parser.parse(data['after_date'])
        except Exception:
            return jsonify({'error': 'Invalid after_date format. Use ISO 8601 like 2024-07-27T09:00:00'}), 400
    else:
        after_date = datetime.now(timezone(timedelta(hours=0,minutes=0))) - timedelta(days=1)

    try:
        output = asyncio.run(fetch_messages(api_id, api_hash, phone, channel, after_date))
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


async def fetch_messages(api_id, api_hash, phone, channel, after_date):
    client = TelegramClient('telegram_channel_reader', api_id, api_hash)
    await client.start(phone)

    entity = await client.get_entity(channel)

    # Fetch messages with paging
    all_messages = []
    offset_id = 0
    while True:
        history = await client(GetHistoryRequest(
            peer=entity,
            limit=100,
            offset_id=offset_id,
            offset_date=None,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        messages = history.messages
        if not messages:
            break

        for msg in messages:
            if msg.date <= after_date:
                await client.disconnect()
                return all_messages  # Done, no more recent messages
            if msg.message:
                all_messages.append({
                    'id': msg.id,
                    'date': str(msg.date),
                    'text': msg.message
                })

        offset_id = messages[-1].id

    await client.disconnect()
    return all_messages


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
