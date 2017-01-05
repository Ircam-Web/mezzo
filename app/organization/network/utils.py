# -*- coding: utf-8 -*-
import pandas as pd

def get_nb_half_days_by_period(date_from, date_to):
    day_list = pd.date_range(date_from, date_to).tolist()
    day_dict = {
      "monday_am": 0,
      "monday_pm": 0,
      "tuesday_am": 0,
      "tuesday_pm": 0,
      "wednesday_am": 0,
      "wednesday_pm": 0,
      "thursday_am": 0,
      "thursday_pm": 0,
      "friday_am": 0,
      "friday_pm": 0,
    }
    for day in day_list :
        if day.dayofweek == 0:
            day_dict['monday_am'] += 1
            day_dict['monday_pm'] += 1
        if day.dayofweek == 1:
            day_dict['tuesday_am'] += 1
            day_dict['tuesday_pm'] += 1
        if day.dayofweek == 2:
            day_dict['wednesday_am'] += 1
            day_dict['wednesday_pm'] += 1
        if day.dayofweek == 3:
            day_dict['thursday_am'] += 1
            day_dict['thursday_pm'] += 1
        if day.dayofweek == 4:
            day_dict['friday_am'] += 1
            day_dict['friday_pm'] += 1

    return day_dict
