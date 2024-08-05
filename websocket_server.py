import os
import django
import asyncio
import websockets
import json
from asgiref.sync import sync_to_async

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smsApplication.settings')
django.setup()

from sms.models import User, SMS


async def create_sms(websocket, path):  # Asynchronous function that handles a WebSocket connection
    async for message in websocket:  # Asynchronous loop to process incoming messages.
        data = json.loads(message)  # Decodes an incoming message from JSON
        sender_id = data.get("sender_id")  # Extracts data from the decoded message
        receiver_id = data.get("receiver_id")
        content = data.get("content")

        if sender_id and receiver_id and content:
            try:
                # Asynchronously fetches the sender from the database.
                sender = await sync_to_async(User.objects.get)(id=sender_id)
                receiver = await sync_to_async(User.objects.get)(id=receiver_id)

                # Asynchronously creates a new SMS message.
                sms = await sync_to_async(SMS.objects.create)(sender=sender, receiver=receiver, content=content)

                # Sends back to the client a JSON message confirming the creation of the SMS.
                await websocket.send(json.dumps({"status": "SMS created", "sms_id": sms.id}))
            except User.DoesNotExist:
                await websocket.send(json.dumps({"error": "User not found"}))
        else:
            await websocket.send(json.dumps({"error": "Invalid data"}))

'''
Configures a WebSocket server to handle connections to localhost:8765 using the create_sms function to handle messages.
'''
start_server = websockets.serve(create_sms, "localhost", 8765)

print("Starting WebSocket server on ws://localhost:8765")
# Starts the server and waits for it to initialise.
asyncio.get_event_loop().run_until_complete(start_server)
# Starts an infinite loop to process incoming connections.
asyncio.get_event_loop().run_forever()
