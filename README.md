# SMSApplication

This project is a server for synchronising users from a third-party API and storing them in a database. The server provides API for managing user lists and sending SMS, and supports WebSocket for creating SMS.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Start the development server:

    ```bash
    python manage.py runserver
    ```

## Models
### The project includes the following models:
- User: Stores user information (phone number and name).
- List: Stores lists of users. One list can contain many users.
- SMS: Stores SMS messages.
- Configuration: Stores configuration parameters.


# Usage

### Endpoints

#### User Creation

- **Endpoint**: `/api/users/`
- **Method**: `POST`
- **Payload**:
```json
{
    "number": "1234567890",
    "name": "John Doe"
}
```

#### List creation
- **Endpoint**: `/api/lists/`
- **Method**: `POST`
- **Payload**:
```json
{
    "name": "My List",
    "users": [1, 2],
    "created_by": 1
}
```

#### Adding/removing a user from the list
- **Endpoint**: `/api/lists/<list_id>/add_user/`
- **Method**: `POST`
- **Payload**:
```json
{
    "user_id": 1
}
```

- **Endpoint**: `/api/lists/<list_id>/remove_user/`
- **Method**: `POST`
- **Payload**:
```json
{
    "user_id": 1
}
```

#### Send SMS
- **Endpoint**: `/api/lists/<list_id>/send_sms/`
- **Method**: `POST`
- **Payload**:
```json
{
    "sender_id": 1,
    "content": "Hello, this is a test message."
}
```

#### List synchronisation
- **Endpoint**: `/api/lists/<list_id>/synchronize/`
- **Method**: `POST`
- **Payload**:
```json
{
    "endpoint": "http://localhost:8081",
    "params": {}
}
```


### WebSocket
1. pip install websockets
2. python websocket_server.py
3. python websocket_client.py
#### Test
- python manage.py shell
```python
from sms.models import SMS

sms = SMS.objects.get(id=1)
print(f"Sender: {sms.sender}, Receiver: {sms.receiver}, Content: {sms.content}")
```
