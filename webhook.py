from json import dumps
from httplib2 import Http


def main(texto):
    """Google Chat incoming webhook that starts or replies to a message thread."""
    url = "https://chat.googleapis.com/v1/spaces/AAQAQI3Do4M/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=poG3A2pJAA9k1JOaVqICuCJyBuvpA_xaZReT-Ej40xE"
    app_message = {
        "text": texto,
        
    }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)


if __name__ == "__main__":
    main()