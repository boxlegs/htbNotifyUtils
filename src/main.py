from hackthebox import HTBClient
from dotenv import load_dotenv
import requests
import os 


load_dotenv()

ACCESS_TOKEN = os.getenv("HTB_ACCESS_TOKEN")


print("Welcome to the Hack The Box Machine Notifier!")

client = HTBClient(app_token=ACCESS_TOKEN)
print(client.do_request("machine/list/retired/paginated"))
