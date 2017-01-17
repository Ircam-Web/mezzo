# -*- coding: utf-8 -*-
import pandas as pd
import csv
from django.http import HttpResponse
from xlwt import *
import calendar
from organization.network.api import *
import datetime
from collections import defaultdict, OrderedDict
from pprint import pprint


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


def get_nb_half_days_by_period_per_month(date_from, date_to):
    day_list = pd.date_range(date_from, date_to).tolist()

    md_dict = {}
    for i in range(1,13):
        md_dict[i] = {
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

    # for each day of the period
    for day in day_list :
        if day.dayofweek == 0:
            md_dict[day.month]['monday_am'] += 1
            md_dict[day.month]['monday_pm'] += 1
        if day.dayofweek == 1:
            md_dict[day.month]['tuesday_am'] += 1
            md_dict[day.month]['tuesday_pm'] += 1
        if day.dayofweek == 2:
            md_dict[day.month]['wednesday_am'] += 1
            md_dict[day.month]['wednesday_pm'] += 1
        if day.dayofweek == 3:
            md_dict[day.month]['thursday_am'] += 1
            md_dict[day.month]['thursday_pm'] += 1
        if day.dayofweek == 4:
            md_dict[day.month]['friday_am'] += 1
            md_dict[day.month]['friday_pm'] += 1

    return md_dict


class TimesheetXLS2(object):

    def __init__(self, timesheets):
        self.timesheets = timesheets.order_by('activity','project', 'year', 'month')


class TimesheetXLS(object):

    t_dict = OrderedDict()
    first_month_row = 5
    first_month_col = 4
    last_month_col = first_month_col + 13
    project_margin_row = 4
    project_first_row = 6
    project_first_col = 0
    percent_margin = 1
    percent_label = "Percentage of time worked on project"
    percent_label_row = 7
    percent_label_col = 0
    hours_margin = 2
    hours_label = "Productive hours worked on project"
    hours_label_row = 8
    hours_label_col = 0
    wk_margin = 3
    wk_label = "Workpackages to which the person has contributed"
    wk_label_row = 9
    wk_label_col = 0
    accounting_margin = 4
    accounting_label = "Date of accounting by person working on the action"
    accounting_label_col = 0
    validation_margin = 5
    validation_label_row = 0
    validation_label = "Date of validation by the superior"
    validation_label_col = 0
    title_col = 0
    title_row = 0
    title_action_col = 0
    title_action_row = 1
    beneficiary_col = 0
    beneficiary_row = 2
    name_person_col = 0
    name_person_row = 3
    grant_col = 2
    grant_row = 1
    type_personal_col = 2
    type_personal_row = 3


    def __init__(self, timesheets):
        self.timesheets = timesheets.order_by('activity','project', 'year', 'month')
        self.book = Workbook()
        self.grey_pattern = Pattern()
        self.grey_pattern.pattern = Pattern.SOLID_PATTERN
        self.grey_pattern.pattern_fore_colour = Style.colour_map['gray25']
        self.header_style = XFStyle()
        self.header_style.pattern = self.grey_pattern
        self.date_style = XFStyle()
        self.date_style.num_format_str = 'M/D/YY'



    def init_layout(self, sheet, year):
        sheet.write(self.title_row, self.title_col, "TIME RECORDING FOR A HORIZON 2020 ACTION")
        sheet.write(self.title_action_row, self.title_action_col, "Title of the action :")
        sheet.write(self.beneficiary_row, self.beneficiary_col, "Beneficiary's / linked third part's name :")
        sheet.write(self.name_person_row, self.name_person_col, "Name of the person working on the action :")
        sheet.write(self.grant_row, self.grant_col, "Grant Agreement No : ")
        sheet.write(self.type_personal_row, self.type_personal_col, "Type of personnel :")
        row = sheet.row(self.first_month_row)
        for i in range(self.first_month_col, self.last_month_col):
            row.write(i, calendar.month_name[i - self.first_month_col] +"-"+ str(year % 100), self.header_style)

    def format(self):
        self.t_dict = OrderedDict()
        for timesheet in self.timesheets:
            person_slug = timesheet.activity.person.slug
            # if new person
            if not person_slug in self.t_dict:
                self.t_dict[person_slug] = {}
                # caculate for each person leaved days in year
                date_from = datetime.date(timesheet.year, 1, 1)
                date_to = datetime.date(timesheet.year, 12, 31)
                nb_half_days = get_nb_half_days_by_period_per_month(date_from, date_to)
                leave_days = get_leave_days_per_month(date_from, date_to, timesheet.activity.person.external_id)
                worked_hours_by_month = {"test" : "1"}
                # for each month
                for m_key, m_val in nb_half_days.items():
                    # for each week day
                    for nhd_k, nhd_v in m_val.items():
                        if not m_key in worked_hours_by_month:
                            worked_hours_by_month[m_key] = 0
                        half_day_nb_hours = getattr(timesheet.activity, nhd_k)
                        if not half_day_nb_hours is None :
                            # is the person has been present during current m_key month ?
                            if m_key in leave_days :
                                if nhd_k in leave_days[m_key]:
                                    # is the person has been present during current half day nhd_d ?
                                    worked_hours_by_month[m_key] += (nb_half_days[m_key][nhd_k] - leave_days[m_key][nhd_k]) * half_day_nb_hours
                                else :
                                    # if not, count theorical nb oh hours for this half day
                                    worked_hours_by_month[m_key] += nb_half_days[m_key][nhd_k] * half_day_nb_hours
                            # if not, count theorical nb of hours for whole month
                            else :
                                worked_hours_by_month[m_key] += nb_half_days[m_key][nhd_k] * half_day_nb_hours
                        else :
                            # missing data...
                            worked_hours_by_month[m_key] = 0

            # for each percent time worked on a project...
            project_slug = timesheet.project.slug
            if not project_slug in self.t_dict[person_slug]:
                self.t_dict[person_slug][project_slug] = []
            # ...calculate nb of worked hours proportionally
            # the property 'worked_hours' does not exists in the model, it just calculated on the fly
            timesheet.worked_hours = worked_hours_by_month[timesheet.month] * timesheet.percentage
            self.t_dict[person_slug][project_slug].append(timesheet)
        return self.t_dict


    def export(self):
        curr_project = ''
        percent_label_row_index = self.percent_label_row
        hours_label_row_index = self.hours_label_row
        # for each person
        for person_k, person_v in self.t_dict.items():
            # for each project
            project_row_last = (len(person_v) - 1) * self.project_margin_row + self.project_first_row
            for project_k, project_v in person_v.items():
                project_position = list(person_v.keys()).index(project_k)
                project_row_index = self.project_margin_row * project_position + self.project_first_row
                # for each timesheet
                for timesheet in project_v:
                    try :
                        self.sheet = self.book.add_sheet(person_k)
                        self.init_layout(self.sheet, timesheet.year)
                    except:
                        pass

                    # project name
                    try :
                        self.sheet.write(project_row_index, self.project_first_col, timesheet.project.title, self.header_style)
                    except:
                        pass


                    # percent
                    try:
                        self.sheet.write(project_row_index + self.percent_margin, timesheet.month + self.first_month_col, timesheet.percentage)
                    except :
                        pass

                    # nb worked hours
                    try:
                        self.sheet.write(project_row_index + self.hours_margin, timesheet.month + self.first_month_col, timesheet.worked_hours)
                    except :
                        pass


                    # work packages
                    work_packages = [str(wk.number) for wk in timesheet.work_packages.all()]
                    work_packages = ",".join(work_packages)
                    try :
                        self.sheet.write(project_row_index + self.wk_margin, timesheet.month + self.first_month_col, work_packages)
                    except:
                        pass

                    try :
                        self.sheet.write(project_row_index, self.project_first_col + 1, timesheet.project.external_id, self.header_style)
                        self.sheet.write(project_row_index + self.percent_margin, self.percent_label_col, self.percent_label)
                        self.sheet.write(project_row_index + self.hours_margin, self.hours_label_col, self.hours_label)
                        self.sheet.write(project_row_index + self.wk_margin, self.wk_label_col, self.wk_label)
                    except:
                        pass

                    try :
                        # accounting date
                        self.sheet.write(project_row_last + self.accounting_margin, timesheet.month + self.first_month_col, timesheet.accounting, self.date_style)

                        # validation date
                        self.sheet.write(project_row_last + self.validation_margin, timesheet.month + self.first_month_col, timesheet.validation, self.date_style)
                    except:
                        pass



    def write(self):
        self.format()
        self.export()
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        self.book.save(response)
        return response
