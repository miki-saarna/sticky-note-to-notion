# import subprocess
import sys
sys.path.append("/Users/mikitosaarna/Projects/notion/scan-photo-to-note")
from scripts.notion.getPages import GetPages
from scripts.notion.promptPageSelection import PromptPageSelection
from dotenv import load_dotenv
from scan_image import ScanImageWithChatGPT
from cli_chatgpt import start_interactive_chat
import os
load_dotenv()
from openai import OpenAI
import requests
import typer
from inquirer import List, prompt

app = typer.Typer()
client = OpenAI()
NOTION_API_KEY = os.environ["NOTION_API_KEY"]

class AddNoteToNotion:
  def __init__(self, image_file_path):
    image_text = ScanImageWithChatGPT(image_file_path).image_text
    prompt = f"Using the `gpt4_vision` model, I deciphered a handwritten message on a sticky note I have. I would like to proceed by recording the message to a note-taking platform. Since this is a hand-written note on a small sticky note, can you give me 3 recommendations on the final version of the message I should use? In your recommendations, please ensure you fix any and all grammatical or sentence structure errors you find. However, do not alter the core content of the message; you can only paraphrase it to the best of your ability. After I select a suitable recommendation, please repeat the selected recommendation verbatim - the reason for repeating is for easy retrieval of the value (DO NOT prefix/suffix the recommendation. Simply repeat the recommendation and only the recommendation. Additionally, when repeating the recommendation, ensure that it isn't wrapped with quotations). Here is the message: {image_text}. Here is addiitonal contextual background that may be helpful to you regarding this message: {self.context}"

    start_interactive_chat(initial_text=prompt, on_chat_end=self.upload_note_to_notion)

  context = "The message is from the novel The Death and Life of Great American Cities by Jane Jacobs. This novel is about the importance of learning from traditional urbanism and how it helped shaped beautiful, yet very successful/functional cities across the country. Despite this, modern urban planning tends to throw away most of the important lessons of traditional urban planning and even belittles its practice. Jacobs goes into great detail on many aspects of traditional urban planning and how it contributed to a successful city."
  # recommended_text = None

  def upload_note_to_notion(self, message):
    promptPageSelection = PromptPageSelection()
    selectedPageID = promptPageSelection.promptUserToSelectNotionPage() # handle if None!!! (workspace level)

    self.recommended_text = message.content
    # subprocess.run(self.genCurlCmd(), shell=True)

    url = f'https://api.notion.com/v1/blocks/{selectedPageID}/children'
    headers = {
      'Authorization': f'Bearer {NOTION_API_KEY}',
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28'
    }
    data = {
       "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": self.remove_quotations(self.recommended_text)
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
      print("Patch request successful")
    else:
      print(f"Patch request failed with status code: {response.status_code}")

  @staticmethod
  def remove_quotations(str):
    if str.startswith('"') and str.endswith('"'):
        return str[1:-1]
    return str

  # def genCurlCmd(self):
      # promptPageSelection = PromptPageSelection()
      # selectedPageID = promptPageSelection.promptUserToSelectNotionPage()
  #   return f"""
  #     curl -X PATCH 'https://api.notion.com/v1/blocks/{selectedPageID}/children' \
  #       -H 'Authorization: Bearer {NOTION_API_KEY}' \
  #       -H "Content-Type: application/json" \
  #       -H "Notion-Version: 2022-06-28" \
  #       --data '{
  #         "children": [
  #             {{
  #                 "object": "block",
  #                 "type": "paragraph",
  #                 "paragraph": {{
  #                     "rich_text": [
  #                         {{
  #                             "type": "text",
  #                             "text": {{
  #                                 "content": f'"{self.remove_quotations(self.recommended_text)}"'
  #                             }}
  #                         }}
  #                     ]
  #                 }}
  #             }}
  #         ]
  #     }'
  #     """

if __name__ == "__main__":
    image_file_path = "/Users/mikitosaarna/Projects/notion/scan-photo-to-note/public/photos/note-1.jpeg"
    AddNoteToNotion(image_file_path)
