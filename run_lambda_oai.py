from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.environ["LAMBDA_API_KEY"]
openai_api_base = "https://api.lambdalabs.com/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

print(client.models.list())
