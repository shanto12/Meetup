# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

KEY="s7kl5loshv3hqa1jvcaar80720"
SECRET="peuo9ef44is3hd7icfqai1shc2"
REDIRECT_URL="https://www.google.com"

KEY2="la2gm742d4qeohvbrqfi0m8h7m"
SECRET2="mcu6k28pcpuak69hueutbk565d"
REDIRECT_URL2="https://www.youtube.com"

HTML_LOCATION = r"C:\Users\shant\Desktop\mypage.html"
CODE="48db59f35c3e45134ca63f43bd3dc0a4" # This code has to be obtained from the output of the authorize api call. By going into the URL and logging in.

CONFIG = "config.json"

TOP_PERC="20"

import requests
from meetup.client import Client
import json
from datetime import date, timedelta

def save_json_text(file_path, json_obj_text):
    with open(file_path, 'w+') as f:
        json.dump(json_obj_text, f)


def json_to_dict(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def save_html(file_path, text):
    with open(file_path, 'w+') as f:
        f.write(text.strip())

def refersh_token(key, secret, config):
    json_dict = json_to_dict(config)
    param = dict()
    param["client_id"] = key
    param["client_secret"] = secret
    param["grant_type"] = "refresh_token"
    param["refresh_token"] = json_dict.get("refresh_token")

    r = requests.post("https://secure.meetup.com/oauth2/access", data=param)
    r_json = r.json()
    save_json_text(config, r_json)

    print(r.text)


def get_token(key, code, secret):
    param = dict()
    param["client_id"] = key
    param["client_secret"] = secret
    param["grant_type"] = "authorization_code"
    # param["response_type"] = "code"
    param["redirect_uri"] = REDIRECT_URL
    param["code"] = code

    r = requests.post("https://secure.meetup.com/oauth2/access", data=param)
    r_json = r.json()
    print(r.text)

    return r_json

def get_code(key, secret):
    param = dict()
    param["client_id"]=key
    # param["client_secret"] = secret
    # param["grant_type"] = "anonymous_code"
    param["response_type"] = "code"
    param["redirect_uri"] = REDIRECT_URL

    # r=requests.post("https://secure.meetup.com/oauth2/access", data=param)
    r = requests.post("https://secure.meetup.com/oauth2/authorize", data=param)
    r_text=r.text

    save_html(HTML_LOCATION, r_text)

def print_events(event_list, event_perc):
    event_len = len(event_list)
    top_events_num = (event_len * int(event_perc)) // 100
    sorted_event_list = sorted(event_list, key=lambda k: k['yes_rsvp_count'], reverse=True)
    print(f"There are {event_len} found.")
    print(f"top_events_num: {top_events_num}.")
    print("=" * 50)
    for event in sorted_event_list[:top_events_num]:
        print(event.get("name"))
        print(event.get("yes_rsvp_count"))
        print(event.get("local_date"))
        print(event.get("waitlist_count"))
        print(event.get("venue", dict()).get('address_1'))
        print(event.get('city'))
        print(event.get('status'))
        print("="*50)

    print(f"There are {event_len} found.")
    print(f"top_events_num: {top_events_num}.")



def get_end_date(days=7, date_format="%Y-%m-%dT%H:%M:%S"):
    start_date=date.today()
    end_date = start_date + timedelta(days=days)

    return end_date.strftime(date_format)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    # CODE=get_code(KEY, SECRET) hopefully will not need to execute again as we have refresh token already.
    # token_json = get_token(KEY, CODE, SECRET)

    # save_json_text(CONFIG, token_json)

    # refersh_token(KEY, SECRET, CONFIG)

    json_dict = json_to_dict(CONFIG)

    meetup_client = Client(access_token=json_dict.get("access_token"))

    end_date_str = get_end_date(days=20)

    params = dict()
    params["order"]="time"
    params["to_df"] = False
    params["page"] = "200"
    params["radius"] = "smart"
    params["end_date_range"] = end_date_str

    # r_json=meetup_client.get(url="/find/upcoming_events", to_df=False, page=200, radius='smart', end_date_range=end_date_str)
    # r_json = meetup_client.get(url="/find/upcoming_events", **params)
    r_json = meetup_client.get(url="/self/calendar", **params)
    print_events(r_json.get('events') if isinstance(r_json, dict) else r_json, event_perc=TOP_PERC)


    print("DONE")

    # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

