# Figgo API consumption

import requests
from django.conf import settings
from datetime import date, timedelta


def figgo_request(method):
    """generic method to call Figgo API"""
    return requests.get(settings.FIGGO_API_URL_PROD+method, headers={'Authorization': settings.FIGGO_API_HEADER_AUTH})


def get_active_persons():
    r_p_active = figgo_request('api/users?fields=id,lastname,firstname')
    r_p_active = r_p_active.json()
    return r_p_active['data']


def get_inactive_persons():
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.isoformat()
    r_p_inactive = figgo_request('api/users?dtContractEnd=until,'+yesterday+',null&fields=id,lastname,firstname')
    r_p_inactive = r_p_inactive.json()
    return r_p_inactive['data']


def get_leave_periods(date_from, date_to, person_external_id):
    leave_periods = figgo_request('api/leaves?date=between,'+date_from+','+date_to+'&fields=owner.name,owner.login,owner.mail,owner.matricule,name,date,status,leaveScope&owner.id='+str(person_external_id))
    leave_periods = leave_periods.json()
    return leave_periods['data']


def get_leave_days(date_from, date_to, person_external_id):
    """Calculate the number of validated leaving days.
    It takes in account half days.
    Return float value
    """
    leave_periods = get_leave_periods(date_from, date_to, person_external_id)
    days = 0
    for leave_period in leave_periods:
        if leave_period['status'] == 1:
            if leave_period['leaveScope'] == 'PM' or leave_period['leaveScope'] == 'AM':
                days += 0.5
            if leave_period['leaveScope'] == 'ALL':
                days += 1
    return days
