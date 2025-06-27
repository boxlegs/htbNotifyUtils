# htb-machine-notifier
Cheeky PoC for polling new machine/challenge releases with support for ntfy notifications.


### Endpoints of Interest
It seems that the API endpoints have changed somewhat since current tools (such as [pyhackthebox](https://pypi.org/project/PyHackTheBox/)) were updated. For example, the current machine listing endpoints are different, thus `get_machines()` for example no longer works.

I decided to boot up burpsuite to see where they've run off to. Here are some interesting ones - note that some of these may not have changed:

```sh
machine/list/retired/paginated # Retired boxes, paginated
machine/paginated # Gets machines? Not sure how this is different from machine/list
machine/recommended
machine/active # Get active machine details
season/machines # The current seasonal machines
```