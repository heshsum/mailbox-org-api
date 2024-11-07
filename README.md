# mailbox-api-client
A library to access the mailbox.org Business API.

## Motivation and purpose 
The goal is to provide a comprehensive library that can easily be used to integrate the business features at mailbox.org.

## Installation 
```python
pip install git+https://github.com/heshsum/mailbox-api-client
```

## Usage
Basic usage is fairly straightforward:

```python
from mailbox_org_api import APIClient

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

## Here be dragons
1. I'm not a programmer. I'm not very good at this. Be aware of my incompetence.
2. Implementation is not complete. Not all functions of the API have been implemented
3. Type hinting is available for most functions, but not all of them.  
E.g. `mail_add()` accepts kwargs due to the number of available attributes. 
In that case type errors will be returned if wrong types are provided.

## API documentation
mailbox.org provides API documentation here: [https://api.mailbox.org](https://api.mailbox.org)
