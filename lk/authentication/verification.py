import requests
import clearbit
import json
from .config.config import clearbit_token, hunter_token


def verify(email):
    
    # Registering clearbit token 
    clearbit.key = clearbit_token

    # Verifying email
    r = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_token}')
    content = json.loads(r.content)
    
    verified_email = False

    # If score is more than 70 email is verified
    if r.status_code == 200 and content['data']['score'] > 70:
        print('fhfhfjgjghj')
        verified_email = True
    
    # Trying to get some additional info from clearbit(first and last name)
    try:
        response = clearbit.Enrichment.find(email=email, stream=True)
        first_name = response['person']['name']['givenName']
        last_name = response['person']['name']['familyName']
    
    except Exception as e:
        last_name = 'unknown'
        first_name = email.split('@')[0]
    
    return first_name, last_name, verified_email
