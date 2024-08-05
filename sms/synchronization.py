import requests
from sms.models import User, List


def synchronize_list(list_id, endpoint, params):
    list_obj = List.objects.get(id=list_id)  # getting List object from the db
    response = requests.get(endpoint, params=params)  # accepts the URL of a third-party API

    if response.status_code == 200:
        users_data = response.json()  # response data is converted into JSON format

        for user_data in users_data:
            # user search by phone number
            user, created = User.objects.get_or_create(
                number=user_data["number"],
                # if number does not exist, a new user is created
                defaults={"name": user_data.get("name", "")}
            )
            list_obj.users.add(user)

        list_obj.save()
    else:
        raise Exception(f"Synchronization failed with status code {response.status_code}")
