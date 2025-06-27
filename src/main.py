from hackthebox import HTBClient
from dotenv import load_dotenv
import os 


load_dotenv()

ACCESS_TOKEN = os.getenv("HTB_ACCESS_TOKEN")


print("Welcome to the Hack The Box Machine Notifier!")

client = HTBClient(app_token=ACCESS_TOKEN)
print(client.get_all_vpn_servers())
print(client.do_request("GET", "https://www.hackthebox.com/api/v4/machine/paginated/?per_page=20"))

requests.get("https://www.hackthebox.com/api/v4/machine/paginated/?per_page=20", headers={'Authorization': 'Bearer ' +ACCESS_TOKEN})

