# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Ircam
# Copyright (c) 2016-2017 Guillaume Pellerin
# Copyright (c) 2016-2017 Emilie Zawadzki

# This file is part of mezzanine-organization.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import csv
import logging
import datetime
import math
import datetimerange
from optparse import make_option
import xlrd
from itertools import takewhile
from re import findall
import dateutil.parser
# from string import split
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Q

from organization.core.models import *
from organization.network.models import *
from organization.projects.models import *


class Logger:

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def info(self, prefix, message):
        self.logger.info(' ' + prefix + ' : ' + message)

    def error(self, prefix, message):
        self.logger.error(prefix + ' : ' + message)


def get_instance(model, field, value):
    models = model.objects.filter(field=value)
    if models:
        return models[0]
    else:
        model = model()
        model.field = value
        return model


class IrcamXLS:

    register_id_row = 4
    register_id_col = 3
    period_row = 6
    period_col = 2
    first_project_row = 14
    first_project_col = 2
    first_month_row = 11
    first_month_col = 3
    first_percent_row = 13
    first_percent_col = 3
    nb_of_month = 12
    nb_max_of_project = 10

    def __init__(self, file):
        self.book = xlrd.open_workbook(file)
        self.sheets = self.book.sheets()


class IrcamTimeSheet(object):

    def __init__(self, person, date_from, date_to):
        self.person = person
        self.date_from = date_from
        self.date_to = date_to

    def set_person_activity_timesheet(self,
                                    activity,
                                    project,
                                    percentage,
                                    month,
                                    year):
        """ Set for a year percentage worked by month
        on a project
        """
        pats = PersonActivityTimeSheet.objects.get_or_create(activity = activity,
                                                    project = project,
                                                    percentage = percentage,
                                                    month = month,
                                                    year = year
                                                    )


    def set_work_package(self, person_activity_timesheet):
        """ set contract id of the project """

class Command(BaseCommand):
    help = """Import Person data from IRCAM's legacy XLS management file.
              python manage.py import-ircam-timesheet-xls -s /srv/backup/TemplateInputTimeSheet2015-16.xlsx
    """

    option_list = BaseCommand.option_list + (
          make_option('-d', '--dry-run',
            action='store_true',
            dest='dry-run',
            help='Do NOT write anything'),
          make_option('-f', '--force',
            action='store_true',
            dest='force',
            help='Force overwrite data'),
          make_option('-s', '--source',
            dest='source_file',
            help='define the XLS source file'),
          make_option('-l', '--log',
            dest='log',
            help='define log file'),
    )

    def handle(self, *args, **kwargs):
        self.logger = Logger(kwargs.get('log'))
        self.pattern = kwargs.get('pattern')
        self.source_file = os.path.abspath(kwargs.get('source_file'))
        self.dry_run =  kwargs.get('dry-run')
        self.force = kwargs.get('force')

        xls = IrcamXLS(self.source_file)
        for sheet in xls.sheets:
            person_register_id = sheet.cell_value(xls.register_id_row, xls.register_id_col)
            persons = Person.objects.filter(register_id=int(person_register_id))
            processing_counter = 0
            # database not enough clear, possible multiple entries for some persons
            # iterating over one person
            for person in persons:
                period_str = sheet.cell_value(xls.period_row, xls.period_col)
                periods = findall(r'\d{1,2}/\d{1,2}/\d{4}', period_str)
                print("periods", periods, person, period_str)
                date_from = dateutil.parser.parse(periods[0])
                date_to = dateutil.parser.parse(periods[1])
                print("date_from", type(date_from), "date_to", type(date_to))
                curr_range_date = datetimerange.DateTimeRange(date_from, date_to)
                curr_year = date_to.year

                self.logger.info('Processing', '******************* PERSON : ' + str(person.id) + ' | '+person.title + " *******************" )
                its = IrcamTimeSheet(person, date_from, date_to)

                # iterating on each month
                for col_index in range(xls.first_percent_col, xls.first_percent_col + xls.nb_of_month):

                    # condition to determine the end of projects list
                    end_project_list_row = 0

                    # get month
                    month = int(sheet.cell_value(xls.first_month_row, col_index))

                    # calculate the current date
                    curr_date = datetime.date(curr_year, month, 1)

                    self.logger.info('Processing', 'year : ' + str(curr_year) + " | month : " + str(month) + " | " + str(curr_date))

                    # find the right activities corresponding to the current month / year
                    activities = person.activities.all()
                    activity = None
                    if not activities:
                        self.logger.info('Not Found', 'activity for person : ' + str(person.id) + " - " + person.title + " for period : " + period_str)
                    else :
                        # find the right
                        for curr_activity in activities :
                            activity_date_range = datetimerange.DateTimeRange(datetime.datetime.combine(curr_activity.date_from, datetime.datetime.min.time()), datetime.datetime.combine(curr_activity.date_to, datetime.datetime.min.time()))
                            if curr_range_date.is_intersection(activity_date_range):
                                activity = curr_activity

                    if not activity:
                        self.logger.info('Not Found', 'No activity correponds to period : '+ str(curr_year) +" "+str(month))
                    else :
                        # for each activities
                        # for activity in activities :
                        # iterating over projects cells
                        self.logger.info('Processing', 'activity : ' + str(activity.id) + ' | ' + activity.__str__())
                        project_row_index = xls.first_project_row
                        while sheet.cell_value(project_row_index, xls.first_project_col) != "Total final":

                            # get percent
                            percent = sheet.cell_value(project_row_index, col_index) if sheet.cell_value(project_row_index, col_index) else 0

                            # try to find project
                            project_id_str = sheet.cell_value(project_row_index, xls.first_project_col - 1)
                            if isinstance(project_id_str, float) :
                                # by default, numbers are retrived as float
                                project_id_str = str(int(project_id_str))

                            # processing projects
                            if end_project_list_row == 0:
                                # check if project exists
                                print("project_id_str", project_id_str, project_row_index, xls.first_project_col - 1)
                                project, is_created = Project.objects.get_or_create(external_id=str(project_id_str))
                                if is_created:
                                    project.title = sheet.cell_value(project_row_index, xls.first_project_col)
                                    project.external_id = project_id_str
                                    project.save()
                                # project = Project.objects.filter(external_id__icontains=project_id_str).first()
                                if project :
                                    # save timesheet without work packages
                                    its.set_person_activity_timesheet(activity, project, percent, month, curr_year)
                                    processing_counter += 1
                                    self.logger.info('Processing', 'project : ' + str(project.id) + " | " + str(project.external_id) + " | " + project.title + " | percent : " + str(percent))
                                else :
                                    self.logger.info('Not Found', 'project : ' + project_id_str)

                            # increment index
                            project_row_index += 1

                        # processing work package
                        work_package_row_index = project_row_index + 1
                        print("WK", sheet.cell_value(work_package_row_index, xls.first_project_col))
                        while sheet.cell_value(work_package_row_index, xls.first_project_col) != "Date entrée":

                            # get project
                            project_external_id = int(sheet.cell_value(work_package_row_index, xls.first_project_col - 1))
                            print("project_external_id", project_external_id)
                            project = Project.objects.get(external_id=str(project_external_id))

                            # check if project exists
                            if project:

                                # list all work package
                                print(work_package_row_index, col_index)
                                wk_p_str = sheet.cell_value(work_package_row_index, col_index)
                                if wk_p_str :
                                    self.logger.info('Processing', 'work packages : ' + str(wk_p_str) + " | project" + project.external_id + " - " + project.title)
                                    wk_p_list = ""
                                    if isinstance(wk_p_str, str):
                                        wk_p_list = wk_p_str.split(",")
                                    elif isinstance(wk_p_str, float):
                                        i, d = divmod(wk_p_str, 1)
                                        wk_p_list = (int(i), int(d))
                                        print("wk_p_list", wk_p_list, wk_p_str)
                                    # link work packages to timesheet
                                    for wk_p_num in wk_p_list:
                                        wk_p_num = str(wk_p_num)

                                        # create or get ProjectWorkPackage
                                        wk_obj, wk_created = ProjectWorkPackage.objects.get_or_create(title="wk_"+wk_p_num, number=wk_p_num, project=project)
                                        pat = PersonActivityTimeSheet.objects.filter(activity=activity, project=project, month=month, year=curr_year)

                                        # for each PersonActivityTimeSheet link work package
                                        for timesheet in pat:
                                            timesheet.work_packages.add(wk_obj)
                                            timesheet.save()


                            # increment index
                            work_package_row_index += 1

                        # processing accounting and validation date
                        dates_row_index = work_package_row_index
                        date_accounting_str = sheet.cell_value(dates_row_index, col_index)
                        date_accounting = xlrd.xldate.xldate_as_datetime(date_accounting_str, 1) if date_accounting_str else None
                        date_validation_str = sheet.cell_value(dates_row_index + 1, col_index)
                        date_validation = xlrd.xldate.xldate_as_datetime(date_validation_str, 1) if date_validation_str else None

                        # get all timesheets, function of the activity, month and year
                        pats = PersonActivityTimeSheet.objects.filter(activity=activity, month=month, year=curr_year)
                        for pat in pats :
                            pat.accounting = date_accounting
                            pat.validation = date_validation
                            pat.save()

                self.logger.info('Processing', '_________________________ Number of record : ' + str(processing_counter) + ' _________________________')
