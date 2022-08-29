import requests, json
from dotenv import load_dotenv
import os

load_dotenv()
# load the token from the environment variable
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}
# Requests all pages with
def query_database(database_id):
    body = {"filter": {"property": "Status", "select": {"equals": "Backlog for Today"}}}
    data = requests.post(
        f"https://api.notion.com/v1/databases/{database_id}/query", headers=HEADERS, data=json.dumps(body)
    ).json()
    return data


def get_pages_properties(page_id, property_id):
    url = f"https://api.notion.com/v1/pages/{page_id}/properties/{property_id}"
    data = requests.get(url, headers=HEADERS).json()
    return data


def get_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = requests.get(url, headers=HEADERS).json()
    return data


if __name__ == "__main__":
    pages = query_database(DATABASE_ID)
    for page in pages["results"]:
        pg_id = page["id"]
        response = get_pages_properties(pg_id, "title")
        if len(response["results"]) > 1:
            title_array = [item["title"]["plain_text"] for item in response["results"]]
            title = " ".join(title_array)
            print(title)
        else:
            print(response["results"][0]["title"]["plain_text"])
    # print(json.dumps(data, indent=4))
