import os
import base64
import requests
import sys
from pdf2image import convert_from_path
from dotenv import load_dotenv
from io import BytesIO
import time

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def convert_pdf_to_jpg(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def img_qa(base64_image):
  print("Sending image to be parsed.")
  start = time.time()
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {OPENAI_API_KEY}"
  }

  payload = {
      "model": "gpt-4o",
      "messages": [
          {
              "role": "system",
              "content": [
                  {
                      "type": "text",
                      "text": 
                      "You are an AI system who parses PDF documents by viewing them, and writing out the text that they contain. "
                      "Do not write any additional text, explanatory text, or anything that is not real text from the images shown to you. "
                      "You may also be presented the previous page(s) text to provide you context. "
                      "If you are shown past text and the next page`s image, you should simply continue the previous pages text the way it is written."
                      "You can use special keywords to label certain parts of a PDF like Title, Abstract, Authors, Appendix, and Figure."
                      "These special keywords should be the only time you ever write anything that is not explicitly written in the documents."
                      "As an example, you can use them to specify a string like `Title: Iterated Decomposition Improving Science Q&A By Supervising Reasoning Processes`\n\n"
                      "Finally to recap, your output should be a direct parsing of the PDFs without any additional annotation. You are an AI-PDF parser, do not explain anything, just parse the document."
                  }
              ]
          },
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": "Parse this page of the PDF, exactly as it is written in the PDF."
                  },
                  {
                      "type": "image_url",
                      "image_url": {
                          "url": f"data:image/jpeg;base64,{base64_image}"
                      }
                  }
              ]
          },
      ],
      "max_tokens": 1000
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  end = time.time()
  print("Time to parse:", (end-start))
  return response.json()

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    images = convert_pdf_to_jpg(pdf_path)
    descriptions = []
    for i, image in enumerate(images):
        base64_image = encode_image(image)
        response = img_qa(base64_image)
        descriptions.append(f"Page {i+1}: {response['choices'][0]['message']['content']}")
    print("\n".join(descriptions))

