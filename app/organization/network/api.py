# Figgo API consumption

import requests
from django.conf import settings
from datetime import date, timedelta


def get_active_person():
    r_p_active = requests.get(settings.FIGGO_API_URL_PROD+'api/users?fields=id,lastname,firstname',
    headers={'Authorization': settings.FIGGO_API_HEADER_AUTH})
    return r_p_active.json()

def get_inactive_person():
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.isoformat()
    r_p_inactive = requests.get(settings.FIGGO_API_URL_PROD+'api/users?dtContractEnd=until,'+yesterday+',null&fields=id,lastname,firstname',
    headers={'Authorization': settings.FIGGO_API_HEADER_AUTH})
    return r_p_inactive.json()
