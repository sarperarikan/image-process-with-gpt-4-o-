import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_description(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Bu görselleri görme engelli kullanıcılar için tüm ayrıntılarıyla detaylı şekilde betimleyebilir ve görsel ile ilgili görme engelli kullanıcının zihninde tüm ayrıntılarıyla bir biçim oluşturabilir. Betimlemede yalın ve anlaşılır bir dil kullanır.  "
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("error", {"message": "Betimleme yapılamadı."})}
