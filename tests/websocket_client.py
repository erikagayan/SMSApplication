"""Test WebSocket server"""
import asyncio
import websockets
import json


async def test_websocket():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        message = {
            "sender_id": 1,
            "receiver_id": 2,
            "content": "Hello, this is a test message."
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.run(test_websocket())
