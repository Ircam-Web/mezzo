# Figgo API consumption

import requests
import time
from django.conf import settings
from datetime import date, timedelta
import dateutil.parser
from pprint import pprint

WEEK_DAYS = {
    1:'monday',
    2:'tuesday',
    3:'wednesday',
    4:'thursday',
    5:'friday'
}

def figgo_request(method):
    """generic method to call Figgo API"""
    return requests.get(settings.FIGGO_API_URL_PROD+method, headers={'Authorization': settings.FIGGO_API_HEADER_AUTH})


def get_active_persons():
    r_p_active = figgo_request('api/users?fields=id,lastname,firstname')
    r_p_active = r_p_active.json()
    return r_p_active['data'] if 'data' in r_p_active else {}


def get_inactive_persons():
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.isoformat()
    r_p_inactive = figgo_request('api/users?dtContractEnd=until,'+yesterday+',null&fields=id,lastname,firstname')
    r_p_inactive = r_p_inactive.json()
    return r_p_inactive['data'] if 'data' in r_p_inactive else {}


def get_leave_periods(date_from, date_to, person_external_id):
    leave_periods = figgo_request('api/leaves?date=between,'+str(date_from)+','+str(date_to)+'&fields=owner.name,owner.login,owner.mail,owner.matricule,duration,name,date,status,leaveScope&owner.id='+str(person_external_id))
    leave_periods = leave_periods.json()

    return leave_periods['data'] if 'data' in leave_periods else {}


def get_leave_days(date_from, date_to, person_external_id):
    """Calculate the number of validated leaving days.
    It takes in account half days.
    Return a dictionary of half days not worked in a week.
    Example :
    {
      "wednesday_am": 2,
      "monday_pm": 1,
      "friday_am": 2,
      "thursday_am": 3,
    }
    """
    leave_periods = get_leave_periods(date_from, date_to, person_external_id)
    days_dict = {}
    for leave_period in leave_periods:
        # if leave period has been validated
        if leave_period['status'] == 1:
            day_week = dateutil.parser.parse(leave_period['date']).isoweekday()
            # morning or evening
            if leave_period['leaveScope'] == 'PM' or leave_period['leaveScope'] == 'AM':
                key = WEEK_DAYS[day_week]+"_"+leave_period['leaveScope'].lower()
                days_dict = increment_day(key, days_dict)
            # whole day = morning + evening
            if leave_period['leaveScope'] == 'ALL':
                key_am = WEEK_DAYS[day_week]+"_am"
                days_dict = increment_day(key_am, days_dict)
                key_pm = WEEK_DAYS[day_week]+"_pm"
                days_dict = increment_day(key_pm, days_dict)
    return days_dict


def get_leave_days_per_month(date_from, date_to, person_external_id):
    """Calculate the number of validated leaving days.
    It takes in account half days.
    Return a dictionary of half days not worked in a week.
    Example :
    {
      "wednesday_am": 2,
      "monday_pm": 1,
      "friday_am": 2,
      "thursday_am": 3,
    }
    """
    leave_periods = get_leave_periods(date_from, date_to, person_external_id)
    days_dict = {}
    for leave_period in leave_periods:
        leave_date = dateutil.parser.parse(leave_period['date'])
        month_key = leave_date.month
        # if leave period has been validated
        if leave_period['status'] == 1:
            day_week = dateutil.parser.parse(leave_period['date']).isoweekday()
            # morning or evening
            if leave_period['leaveScope'] == 'PM' or leave_period['leaveScope'] == 'AM':
                day_key = WEEK_DAYS[day_week]+"_"+leave_period['leaveScope'].lower()
                days_dict = increment_day_per_month(month_key, day_key, days_dict)
            # whole day = morning + evening
            if leave_period['leaveScope'] == 'ALL':
                key_am = WEEK_DAYS[day_week]+"_am"
                days_dict = increment_day_per_month(month_key, key_am, days_dict)
                key_pm = WEEK_DAYS[day_week]+"_pm"
                days_dict = increment_day_per_month(month_key, key_pm, days_dict)
    return days_dict


def increment_day_per_month(month_key, day_key, dt):
    if month_key in dt:
        if day_key in dt[month_key]:
            dt[month_key][day_key] += 1
        else :
            dt[month_key][day_key] = 1
    else :
        dt[month_key] = {}
        dt[month_key][day_key] = 1
    return dt


def increment_day(key, dt):
    if key in dt:
        dt[key] += 1
    else :
        dt[key] = 1
