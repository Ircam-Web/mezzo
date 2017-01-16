# -*- coding: utf-8 -*-
import pandas as pd
import csv
from django.http import HttpResponse
from xlwt import Workbook
import calendar
from organization.network.api import *
import datetime



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

    md_dict = {}
    for i in range(1,13):
        md_dict[i] = day_dict
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



class TimesheetXLS(object):

    first_month_row = 5
    first_month_col = 4
    last_month_col = first_month_col + 13
    project_margin_row = 6
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
    wk_label = "Workpackages to which the person has contributed"
    wk_label_row = 9
    wk_label_col = 0
    accounting_label = "Date of accounting by person working on the action"
    accounting_label_col = 0
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
    work_package_margin = 3
    accounting_margin = 3
    validation_margin = 4

    def __init__(self, timesheets):
        self.timesheets = timesheets.order_by('activity','project', 'month')
        self.book = Workbook()

    def init_layout(self, sheet, year):
        sheet.write(self.title_row, self.title_col, "TIME RECORDING FOR A HORIZON 2020 ACTION")
        sheet.write(self.title_action_row, self.title_action_col, "Title of the action :")
        sheet.write(self.beneficiary_row, self.beneficiary_col, "Beneficiary's / linked third part's name :")
        sheet.write(self.name_person_row, self.name_person_col, "Name of the person working on the action :")
        sheet.write(self.grant_row, self.grant_col, "Grant Agreement No : ")
        sheet.write(self.type_personal_row, self.type_personal_col, "Type of personnel :")
        row = sheet.row(self.first_month_row)
        for i in range(self.first_month_col, self.last_month_col):
            row.write(i, calendar.month_name[i - self.first_month_col] +"-"+ str(year % 100))

    def export(self):
        curr_project = ''
        project_row_index = self.project_first_row
        percent_label_row_index = self.percent_label_row
        hours_label_row_index = self.hours_label_row
        wk_label_row_index = self.wk_label_row

        for timesheet in self.timesheets:
            print("TIME SHEET", timesheet.id)
            try :
                self.sheet = self.book.add_sheet(timesheet.activity.person.slug)
                self.init_layout(self.sheet, timesheet.year)

                # calculate nb of worked hours
                date_from = datetime.date(timesheet.year, 1, 1)
                date_to = datetime.date(timesheet.year, 12, 31)
                nb_half_days = get_nb_half_days_by_period_per_month(date_from, date_to)
                leave_days = get_leave_days_per_month(date_from, date_to, timesheet.activity.person.external_id)
                # substract none worked half days
                # print(nb_half_days)
                # print("****************************")
                # print(leave_days)
                # print("****************************")
                for m_key, m_val in nb_half_days.items():
                    if m_key in leave_days :
                        for nhd_k, nhd_v in m_val.items():
                            if nhd_k in leave_days[m_key]:
                                print(m_key, nhd_k, leave_days[m_key][nhd_k], nb_half_days[m_key][nhd_k])
                                nb_half_days[m_key][nhd_k] = nhd_v - leave_days[m_key][nhd_k]
                                print(m_key, nhd_k, nb_half_days[m_key][nhd_k])
                print(nb_half_days)
            except:
                pass

            if curr_project == '':
                curr_project = timesheet.project
            elif curr_project != timesheet.project:
                curr_project = timesheet.project
                project_row_index += self.project_margin_row
                percent_label_row_index += self.project_margin_row
                hours_label_row_index += self.project_margin_row
                wk_label_row_index += self.project_margin_row

            # percent
            self.sheet.write(project_row_index + self.percent_margin, timesheet.month + self.first_month_col, timesheet.percentage)



            # multiplying by nb of theoretical worked hours
            #
            # theo_worked_hours =
            # timesheet.activity.monday_am =

            # multiplying by percent

            # work packages
            work_packages = [str(wk.number) for wk in timesheet.work_packages.all()]
            work_packages = ",".join(work_packages)
            self.sheet.write(project_row_index + self.work_package_margin, timesheet.month + self.first_month_col, work_packages)

            try :
                self.sheet.write(project_row_index, self.project_first_col, timesheet.project.__str__())
                self.sheet.write(project_row_index, self.project_first_col + 1, timesheet.project.external_id)
                self.sheet.write(percent_label_row_index, self.percent_label_col, self.percent_label)
                self.sheet.write(hours_label_row_index, self.hours_label_col, self.hours_label)
                self.sheet.write(wk_label_row_index, self.wk_label_col, self.wk_label)
            except:
                pass

            # check were is the lower cell
            if wk_label_row_index > self.validation_label_row:
                self.validation_label_row = wk_label_row_index
            elif wk_label_row_index == self.validation_label_row:
                try :
                    # accounting date
                    self.sheet.write(self.validation_label_row + 1, timesheet.month + self.first_month_col, timesheet.accounting)

                    # validation date
                    self.sheet.write(self.validation_label_row + 2, timesheet.month + self.first_month_col, timesheet.validation)
                except:
                    pass



    def write(self):
        self.export()
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=users.xls'
        self.book.save(response)
        return response
