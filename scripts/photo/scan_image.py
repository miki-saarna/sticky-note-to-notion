from PIL import Image
import pytesseract
from rebase_photo import encode_image_base64_url
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI()

def image_text_extraction_OCR(image_path):
    try:
        image = Image.open(image_path)

        text = pytesseract.image_to_string(image) # pytesseract OCR

        print("Extracted Text:")
        print(text)

    except Exception as e:
        print(f"An error occurred: {e}")

class ScanImageWithChatGPT:
  def __init__(self, image_file_path):
    self.image_text = self.image_text_extraction_gpt4_vision(image_file_path)

  context = "The message is from the novel The Death and Life of Great American Cities by Jane Jacobs. This novel is about the importance of learning from traditional urbanism and how it helped shaped beautiful, yet very successful/functional cities across the country. Despite this, modern urban planning tends to throw away most of the important lessons of traditional urban planning and even belittles its practice. Jacobs goes into great detail on many aspects of traditional urban planning and how it contributed to a successful city."

  def image_text_extraction_gpt4_vision(self, image_file_path):
    base64_image = encode_image_base64_url(image_file_path)
    response = client.chat.completions.create(
      model="gpt-4-vision-preview",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What does the text contained within this image say?"},
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
