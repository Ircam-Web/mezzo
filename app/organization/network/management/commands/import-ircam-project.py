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
import re
import logging
import datetime
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


def format_message(project):
    message = str(project.id) + " | "
    message += project.title + " | "
    message += project.external_id if project.external_id else "None"
    return message


class IrcamXLS:

    sheet_id = 0
    project_table_1_first_row = 12
    project_table_1_last_row = 25
    project_table_2_first_row = 34
    project_table_2_last_row = 90
    nb_col_max = 9
    nb_col_min = 0
    avoid_col = 3

    def __init__(self, file):
        self.book = xlrd.open_workbook(file)
        self.sheet = self.book.sheet_by_index(self.sheet_id)


class IrcamProjects(object):

    def __init__(self, project_name):
        project, is_created = Project.objects.get_or_create(title=project_name)
        self.project = project
        self.is_created = is_created
        if self.is_created:
            self.project.title = project_name


    def set_external_id(self, external_id):
        if external_id and self.project.external_id is None:
            if isinstance(external_id, float):
                external_id = str(int(external_id))
            external_id = re.sub(r'((\s)*(-)(\s)*)|(\s)', '-', external_id)
            self.project.external_id = external_id


    def set_call_project(self, call):
        if call and self.project.call is None:
            project_call, is_created = ProjectCall.objects.get_or_create(name__icontains=call)
            if is_created:
                project_call.name = call
                project_call.save()
            self.project.call = project_call


    def set_date_from(self, date_from):
        if date_from and self.project.date_from is None:
            self.project.date_from = date_from


    def set_date_to(self, date_to):
        if date_to and self.project.date_to is None:
            self.project.date_to = date_to


    def set_lead_organization(self, lead_organization):
        if lead_organization and self.project.lead_organization is None:
            lo, is_created = Organization.objects.get_or_create(name=lead_organization)
            self.project.lead_organization = lo


    def set_referring_person(self, referring_person):
        if referring_person and self.project.referring_person is None:
            referring_person_list = re.split(r'\s*/\s*', referring_person, 1)
            for rp in referring_person_list:
                rp_whole_name = re.split(r'\s*', rp, 1)
                last_name = max(rp_whole_name, key=len)
                initial_first_name = min(rp_whole_name, key=len)
                initial_first_name = re.sub(r'\.', '', initial_first_name)
                persons = Person.objects.filter(last_name__icontains=last_name)
                for person in persons:
                    if person.first_name[0] == initial_first_name:
                        self.project.referring_person.add(person)


    def set_teams(self, lead_teams):
        if lead_teams and self.project.lead_team is None:
            lead_teams_list = re.split(r'\s*,\s*', lead_teams, 1)
            for lt in lead_teams_list:
                t, is_created = Team.objects.get_or_create(code__icontains=lt)
                if is_created:
                    t.title = lt
                    t.save()
                self.project.teams.add(t)


    def set_manager(self, manager):
        if manager and self.project.manager is None :
            manager_whole_name = re.split(r'\s*', manager, 1)
            last_name = max(manager_whole_name, key=len)
            initial_first_name = min(manager_whole_name, key=len)
            initial_first_name = re.sub(r'\.', '', initial_first_name)
            persons = Person.objects.filter(last_name__icontains=last_name)
            for person in persons:
                if person.first_name[0] == initial_first_name:
                    self.project.manager.add(person)


    def save_project(self):
        self.project.save()


class Command(BaseCommand):
    help = """Import Person data from IRCAM's legacy XLS management file.
              python manage.py import-ircam-project -s /srv/backup/projects_rd_jan17.xlsx
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

        # Table 1
        for row_index in range(xls.project_table_1_first_row, xls.project_table_1_last_row):
            ip = IrcamProjects(xls.sheet.cell_value(row_index, 0))
            ip.set_external_id(xls.sheet.cell_value(row_index, 1))
            ip.set_call_project(xls.sheet.cell_value(row_index, 2))
            ip.set_date_from(xlrd.xldate.xldate_as_datetime(xls.sheet.cell_value(row_index, 4), 1))
            ip.set_date_to(xlrd.xldate.xldate_as_datetime(xls.sheet.cell_value(row_index, 5), 1))
            ip.set_lead_organization(xls.sheet.cell_value(row_index, 6))
            ip.set_referring_person(xls.sheet.cell_value(row_index, 7))
            ip.set_teams(xls.sheet.cell_value(row_index, 8))
            ip.set_manager(xls.sheet.cell_value(row_index, 9))
            ip.save_project()

            self.logger.info('Project', format_message(ip.project))


        # Table 2
        for row_index in range(xls.project_table_2_first_row, xls.project_table_2_last_row):

            ip = IrcamProjects(xls.sheet.cell_value(row_index, 0))
            ip.set_external_id(xls.sheet.cell_value(row_index, 1))
            ip.set_call_project(xls.sheet.cell_value(row_index, 2))
            ip.set_date_from(xlrd.xldate.xldate_as_datetime(xls.sheet.cell_value(row_index, 4), 1))
            ip.set_date_to(xlrd.xldate.xldate_as_datetime(xls.sheet.cell_value(row_index, 5), 1))
            ip.set_lead_organization(xls.sheet.cell_value(row_index, 6))
            ip.set_referring_person(xls.sheet.cell_value(row_index, 7))
            ip.set_teams(xls.sheet.cell_value(row_index, 8))
            ip.set_manager(xls.sheet.cell_value(row_index, 9))
            ip.save_project()

            self.logger.info('Project', format_message(ip.project))
