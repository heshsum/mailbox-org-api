# mailbox-api-client

## Motivation and purpose
A library to access the mailbox.org Business API.  
The goal is to provide a comprehensive library that can easily be used to integrate the business features at mailbox.org.

## Usage
Basic usage is fairly straightforward: 

```python
from mailboxOrgAPI import APIClient

username = 'foo'
password = 'bar'

# Initializing
api_connection = APIClient.APIClient()

# Testing with hello.world
api_connection.hello_world()

# Creating a new API session
api_connection.auth(username, password)

# Testing the session with hello.innerworld
api_connection.hello_innerworld()

# Closing the session
api_connection.deauth()
``` 

The implemented functions follow the naming scheme of the API, but with underscores instead of points (e.g. `mail_add()` for of `mail.add`).

## API documentation
mailbox.org provides API documentation here: [https://api.mailbox.org](https://api.mailbox.org)
