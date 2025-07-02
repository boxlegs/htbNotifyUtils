from hackthebox import HTBClient
from dotenv import load_dotenv
import os 
import datetime
import pytz
from python_ntfy import NtfyClient
import argparse


load_dotenv()

ACCESS_TOKEN = os.getenv("HTB_ACCESS_TOKEN")
TIMEZONE = os.getenv("TIMEZONE")

print("Welcome to the Hack The Box Machine Notifier!")

client = HTBClient(app_token=ACCESS_TOKEN)
data = client.do_request("season/machines")
machines = data['data']

# Just loop through

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', help="ntfy server URL. If not supplied, https://ntfy.sh is used by default.")
args = parser.parse_args()

ntfy_url = args.url.strip() if args.url else "https://ntfy.sh/"


for machine in machines:
    if not machine['unknown']:
        release_time = datetime.datetime.fromisoformat(machine['release_time'])
        now = datetime.datetime.now(pytz.timezone(TIMEZONE))
        
        if abs(now - release_time) <= datetime.timedelta(hours=24) and machine['is_released']:
            client = NtfyClient('newbox', ntfy_url)
            client.send(f"\nA new machine has been released on HTB.\n\n**Name:** {machine['name']}\n**Difficulty:** {machine['difficulty_text']}\n**OS:** {machine['os']}\n\n Get to it!", f"New Machine {machine['name']} Just Dropped!", priority=client.MessagePriority.HIGH, tags=['package'], format_as_markdown=True)

