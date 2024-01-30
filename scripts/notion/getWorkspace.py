from dotenv import load_dotenv
import os
load_dotenv()
import requests
import json

NOTION_API_KEY = os.environ["NOTION_API_KEY"]

class GetPages:
  def __init__(self, pageID=None):
    self.allPages = self.getAllPages()
    pagesByPageID = self.getPagesFromParent(pageID)
    # print(pagesByPageID)

  def getAllPages(self):
    url = f'https://api.notion.com/v1/search'
    headers = {
      'Authorization': f'Bearer {NOTION_API_KEY}',
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28'
    }
    data = {
      "filter": {
          "value": "page",
          "property": "object"
      }
    }

    res = requests.post(url, headers=headers, json=data)

    if res.status_code == 200:
      print("Patch request successful")
    else:
      print(f"Patch request failed with response: {res.status_code}")
      return

    data = json.loads(res.text)
    return data["results"]

  def getPagesFromParent(self, pageID=None):
    pages = []
    for page in self.allPages:
      if (pageID):
        if page["parent"]["type"] == "page_id" and page["parent"]["page_id"] == pageID:
          pages.append({
            "title": page["properties"]["title"]["title"][0]["plain_text"],
            "id": page["id"]
          })
      else:  
        if page["parent"]["type"] == "workspace":
          pages.append({
            "title": page["properties"]["title"]["title"][0]["plain_text"],
            "id": page["id"]
          })
    return pages


if __name__ == "__main__":
  # GetPages()
  # GetPages("362e87c2-032b-44d3-95e1-925bddfb9e22")
  GetPages("83015762-4318-4b4a-b24b-b20847c0590f")


# exampleResponse = {
#     "object": "list",
#     "results": [
#         {
#             "object": "page",
#             "id": "898ce680-907a-47a5-84f2-2093f0a22441",
#             "created_time": "2024-01-24T07:05:00.000Z",
#             "last_edited_time": "2024-01-29T23:29:00.000Z",
#             "created_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "last_edited_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "cover": null,
#             "icon": null,
#             "parent": {
#                 "type": "page_id",
#                 "page_id": "43b5c113-2c84-4ab2-82cd-8d15c7d1e7d6",
#             },
#             "archived": false,
#             "properties": {
#                 "title": {
#                     "id": "title",
#                     "type": "title",
#                     "title": [
#                         {
#                             "type": "text",
#                             "text": {"content": "integration-v1", "link": null},
#                             "annotations": {
#                                 "bold": false,
#                                 "italic": false,
#                                 "strikethrough": false,
#                                 "underline": false,
#                                 "code": false,
#                                 "color": "default",
#                             },
#                             "plain_text": "integration-v1",
#                             "href": null,
#                         }
#                     ],
#                 }
#             },
#             "url": "https://www.notion.so/integration-v1-898ce680907a47a584f22093f0a22441",
#             "public_url": null,
#         },
#         {
#             "object": "page",
#             "id": "7324de66-ad74-40d0-9914-b078005985fb",
#             "created_time": "2024-01-29T23:27:00.000Z",
#             "last_edited_time": "2024-01-29T23:27:00.000Z",
#             "created_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "last_edited_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "cover": null,
#             "icon": null,
#             "parent": {"type": "workspace", "workspace": true},
#             "archived": false,
#             "properties": {
#                 "title": {
#                     "id": "title",
#                     "type": "title",
#                     "title": [
#                         {
#                             "type": "text",
#                             "text": {"content": "Hello World Parent", "link": null},
#                             "annotations": {
#                                 "bold": false,
#                                 "italic": false,
#                                 "strikethrough": false,
#                                 "underline": false,
#                                 "code": false,
#                                 "color": "default",
#                             },
#                             "plain_text": "Hello World Parent",
#                             "href": null,
#                         }
#                     ],
#                 }
#             },
#             "url": "https://www.notion.so/Hello-World-Parent-7324de66ad7440d09914b078005985fb",
#             "public_url": null,
#         },
#         {
#             "object": "page",
#             "id": "0a4fd38f-de37-4348-9dac-c9a3a56a0729",
#             "created_time": "2024-01-29T23:27:00.000Z",
#             "last_edited_time": "2024-01-29T23:27:00.000Z",
#             "created_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "last_edited_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "cover": null,
#             "icon": null,
#             "parent": {
#                 "type": "page_id",
#                 "page_id": "7324de66-ad74-40d0-9914-b078005985fb",
#             },
#             "archived": false,
#             "properties": {
#                 "title": {
#                     "id": "title",
#                     "type": "title",
#                     "title": [
#                         {
#                             "type": "text",
#                             "text": {"content": "Hello World Child", "link": null},
#                             "annotations": {
#                                 "bold": false,
#                                 "italic": false,
#                                 "strikethrough": false,
#                                 "underline": false,
#                                 "code": false,
#                                 "color": "default",
#                             },
#                             "plain_text": "Hello World Child",
#                             "href": null,
#                         }
#                     ],
#                 }
#             },
#             "url": "https://www.notion.so/Hello-World-Child-0a4fd38fde3743489dacc9a3a56a0729",
#             "public_url": null,
#         },
#         {
#             "object": "page",
#             "id": "41168aaa-c0d2-49f8-98dd-4c1edb46ff79",
#             "created_time": "2024-01-27T05:17:00.000Z",
#             "last_edited_time": "2024-01-29T23:01:00.000Z",
#             "created_by": {
#                 "object": "user",
#                 "id": "79716ee3-d257-47b4-81a5-9692d4f90c44",
#             },
#             "last_edited_by": {
#                 "object": "user",
#                 "id": "ac48e727-e8b6-4556-94b6-02cee69e7e8c",
#             },
#             "cover": null,
#             "icon": null,
#             "parent": {
#                 "type": "page_id",
#                 "page_id": "898ce680-907a-47a5-84f2-2093f0a22441",
#             },
#             "archived": false,
#             "properties": {
#                 "title": {
#                     "id": "title",
#                     "type": "title",
#                     "title": [
#                         {
#                             "type": "text",
#                             "text": {"content": "testing-2", "link": null},
#                             "annotations": {
#                                 "bold": false,
#                                 "italic": false,
#                                 "strikethrough": false,
#                                 "underline": false,
#                                 "code": false,
#                                 "color": "default",
#                             },
#                             "plain_text": "testing-2",
#                             "href": null,
#                         }
#                     ],
#                 }
#             },
#             "url": "https://www.notion.so/testing-2-41168aaac0d249f898dd4c1edb46ff79",
#             "public_url": null,
#         },
#         {
#             "object": "page",
#             "id": "43b45e4f-9dfb-4c33-af5e-cf7412ffae4c",
#             "created_time": "2024-01-24T08:43:00.000Z",
#             "last_edited_time": "2024-01-24T08:43:00.000Z",
#             "created_by": {
#                 "object": "user",
#                 "id": "ac48e727-e8b6-4556-94b6-02cee69e7e8c",
#             },
#             "last_edited_by": {
#                 "object": "user",
#                 "id": "ac48e727-e8b6-4556-94b6-02cee69e7e8c",
#             },
#             "cover": null,
#             "icon": null,
#             "parent": {
#                 "type": "database_id",
#                 "database_id": "6f74ec65-2d65-4291-921a-72acab2b11b0",
#             },
#             "archived": false,
#             "properties": {
#                 "Name": {
#                     "id": "title",
#                     "type": "title",
#                     "title": [
#                         {
#                             "type": "text",
#                             "text": {"content": "testing-2", "link": null},
#                             "annotations": {
#                                 "bold": false,
#                                 "italic": false,
#                                 "strikethrough": false,
#                                 "underline": false,
#                                 "code": false,
#                                 "color": "default",
#                             },
#                             "plain_text": "testing-2",
#                             "href": null,
#                         }
#                     ],
#                 }
#             },
#             "url": "https://www.notion.so/testing-2-43b45e4f9dfb4c33af5ecf7412ffae4c",
#             "public_url": null,
#         },
#     ],
#     "next_cursor": null,
#     "has_more": false,
#     "type": "page_or_database",
#     "page_or_database": {},
#     "request_id": "9c037f36-ee19-41cb-a9b7-fa23f08a5107",
# }
