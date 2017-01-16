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

from django.test import SimpleTestCase
import datetime
from organization.network.utils import get_nb_half_days_by_period, get_nb_half_days_by_period_per_month
from organization.network.api import get_leave_days_per_month

#
# To run tests without database :
# python manage.py test organization.network.tests.[method_name] --settings='organization.core.no_db_settings'
#

class NbOfHalfDaysInPeriodTestCase(SimpleTestCase):

    def setUp(self):
        self.date_from = datetime.date(2016,12,1)
        self.date_to = datetime.date(2016,12,31)

    def test_nbhalf_half_days(self):

        expected = {
          "monday_am": 4,
          "monday_pm": 4,
          "tuesday_am": 4,
          "tuesday_pm": 4,
          "wednesday_am": 4,
          "wednesday_pm": 4,
          "thursday_am": 5,
          "thursday_pm": 5,
          "friday_am": 5,
          "friday_pm": 5,
        }

        result = get_nb_half_days_by_period(self.date_from, self.date_to)
        self.assertEquals(result, expected)


class NbOfHalfDaysInPeriodPerMonthTestCase(SimpleTestCase):

    def setUp(self):
        self.date_from = datetime.date(2015,1,1)
        self.date_to = datetime.date(2015,12,31)

    def test_nbhalf_half_days(self):

        expected = {
           1:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           2:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           3:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           4:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           5:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           6:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           7:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           8:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           9:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           10:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           11:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           },
           12:{
              'friday_pm':52,
              'tuesday_am':52,
              'thursday_pm':53,
              'monday_pm':52,
              'tuesday_pm':52,
              'wednesday_am':52,
              'thursday_am':53,
              'wednesday_pm':52,
              'friday_am':52,
              'monday_am':52
           }
        }

        result = get_nb_half_days_by_period_per_month(self.date_from, self.date_to)
        self.assertEquals(result, expected)


class NbOfLeaveDaysPerMonthTestCase(SimpleTestCase):

    def setUp(self):
        self.date_from = datetime.date(2015,1,1)
        self.date_to = datetime.date(2015,12,31)
        self.external_id = 97

    def test_nb_leave_days(self):

        expected = {
           1:{
              'wednesday_am':1,
              'monday_am':2,
              'friday_am':1,
              'thursday_am':1,
              'tuesday_pm':1,
              'wednesday_pm':1,
              'friday_pm':2,
              'tuesday_am':1,
              'monday_pm':2,
              'thursday_pm':1
           },
           6:{
              'monday_pm':1
           },
           7:{
              'wednesday_am':3,
              'monday_am':2,
              'friday_am':2,
              'thursday_am':3,
              'tuesday_pm':2,
              'wednesday_pm':3,
              'friday_pm':2,
              'tuesday_am':2,
              'monday_pm':2,
              'thursday_pm':3
           },
           8:{
              'wednesday_am':2,
              'monday_am':3,
              'friday_am':2,
              'thursday_am':2,
              'tuesday_pm':3,
              'wednesday_pm':2,
              'friday_pm':2,
              'tuesday_am':3,
              'monday_pm':4,
              'thursday_pm':2
           },
           9:{
              'wednesday_am':1,
              'friday_am':1,
              'thursday_am':1,
              'tuesday_pm':1,
              'wednesday_pm':1,
              'tuesday_am':1,
              'friday_pm':1,
              'thursday_pm':1
           },
           10:{
              'thursday_pm':1
           },
           11:{
              'wednesday_am':1,
              'monday_am':1,
              'tuesday_pm':1,
              'wednesday_pm':1,
              'friday_pm':1,
              'tuesday_am':1,
              'monday_pm':1
           },
           12:{
              'wednesday_am':2,
              'monday_am':1,
              'thursday_am':2,
              'tuesday_pm':2,
              'wednesday_pm':2,
              'tuesday_am':2,
              'monday_pm':2,
              'thursday_pm':2
           }
        }

        result = get_leave_days_per_month(self.date_from, self.date_to, self.external_id)
        self.assertEquals(result, expected)
