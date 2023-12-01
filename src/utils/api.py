import requests
from os.path import exists
from . import config

def get_session_id(filename):
    with open(filename) as f:
        return f.read().strip()
    
SESSION = get_session_id(config.SESSION_ID_FILE)
COOKIES = {"session": SESSION}

def get_url(year, day):
    return config.URL.format(year=year, day=day)


def get_input(day):
    path = config.INPUTS_DIR + "/" + format(str(day).zfill(2)) + ".txt"

    if not exists(path):
        url = get_url(config.YEAR, day)
        response = requests.get(url, cookies=COOKIES)
        if not response.ok:
            raise RuntimeError(
                f"Request failed\n\tstatus code: {response.status_code}\n\tmessage: {response.content}"
            )
        with open(path, "w") as f:
            f.write(response.text[:-1])

    with open(path, "r") as f:
        return f.read()
