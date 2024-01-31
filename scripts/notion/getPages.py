from dotenv import load_dotenv
import os
load_dotenv()
import requests
import json

NOTION_API_KEY = os.environ["NOTION_API_KEY"]

class GetPages:
  def __init__(self, pageID=None):
    self.allPages = self.getAllPages()
    pagesByPageID = self.getChildrenPagesFromParentID(pageID)
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

  def getChildrenPagesFromParentID(self, parentPageID=None):
    pages = []
    for page in self.allPages:
      if (parentPageID):
        if page["parent"]["type"] == "page_id" and page["parent"]["page_id"] == parentPageID:
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
  
  def getParentIDFromChildID(self, childID):
    for page in self.allPages:
      if page["id"] == childID:
        return page["parent"]["page_id"]
    return None


if __name__ == "__main__":
  # GetPages()
  # GetPages("362e87c2-032b-44d3-95e1-925bddfb9e22")
  GetPages("83015762-4318-4b4a-b24b-b20847c0590f")
