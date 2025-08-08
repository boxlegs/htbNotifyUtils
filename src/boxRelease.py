from hackthebox import HTBClient
from dotenv import load_dotenv
import os 
import datetime
import pytz
from python_ntfy import NtfyClient
import argparse

API_BASE = "https://labs.hackthebox.com/api/v4/"

load_dotenv()

def main():
    
    # Parse args and env vars
    ACCESS_TOKEN = os.getenv("HTB_ACCESS_TOKEN")
    TIMEZONE = os.getenv("TIMEZONE")

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="ntfy server URL. If not supplied, https://ntfy.sh is used by default.")
    parser.add_argument('-t', '--topic', help="ntfy server topic slug. If not supplied, 'newbox' is used by default.")
    args = parser.parse_args()

    ntfy_url = args.url.strip() if args.url else "https://ntfy.sh/"
    ntfy_topic = args.topic.strip() if args.topic else "newbox" 
    ntfy_client = NtfyClient(ntfy_topic, ntfy_url)

    # Check token exists and is valid
    if ACCESS_TOKEN is None:
        print("Please set the ACCESS_TOKEN environment variable.")
        exit(1)
        
    try:   
        htb_client = HTBClient(app_token=ACCESS_TOKEN, api_base=API_BASE)
        data = htb_client.do_request("season/machines")
    except Exception as e:
        print(ntfy_client.send(f"Your HTB access token has expired, or API endpoints have changed.", "FATAL ERROR", tags=["warning"], priority=ntfy_client.MessagePriority.HIGH))
        print("Error: ACCESS_TOKEN has likely expired.")
        exit(1)
        
    # Iterate through active machiens
    machines = data['data']
    for machine in machines:
        if not machine['unknown']:
            release_time = datetime.datetime.fromisoformat(machine['release_time'])
            now = datetime.datetime.now(pytz.timezone(TIMEZONE))
            
            if abs(now - release_time) <= datetime.timedelta(hours=24) and machine['is_released']:
                ntfy_client = NtfyClient('newbox', ntfy_url)
                ntfy_client.send(f"\nA new machine has been released on HTB.\n\n**Name:** "
                                 f"{machine['name']}\n**Difficulty:** {machine['difficulty_text']}\n"
                                 f"**OS:** {machine['os']}\n\n Get to it!",
                                 f"New Machine {machine['name']} Just Dropped!", 
                                priority=ntfy_client.MessagePriority.HIGH, 
                                tags=['package'], 
                                format_as_markdown=True)


if __name__ == "__main__":
    main()