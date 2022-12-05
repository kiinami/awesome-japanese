"""
collect.py

Created by kinami on 2022-12-05
"""
import json
import os

from dotenv import load_dotenv
import requests


def main():
    req = requests.request(
        method="GET",
        url=f'{os.getenv("SERVER_URL")}/api/bookmarks',
        headers={
            "Authorization": os.getenv("API_KEY"),
        },
    )
    response = json.loads(req.text)["results"]
    items = [e for e in response if 'japanese' in e['tag_names'] and 'aggregate' in e['tag_names']]
    items.sort(key=lambda x: x['title'])
    # delete the tags 'japanese' and 'aggregate' from the list
    for item in items:
        item['tag_names'] = [e for e in item['tag_names'] if e not in ['japanese', 'aggregate']]
    with open('README.md', 'w') as f:
        with open('header.md', 'r') as hf:
            f.write(hf.read())
        for item in items:
            f.write(
                f'- *[{item["title"]}]({item["url"]})*{": " if item["description"] else ""}{item["description"]}\n\n'
                f'  {" ".join(["`" + e + "`" for e in sorted(item["tag_names"])])}\n\n'
            )


if __name__ == "__main__":
    load_dotenv()
    main()
