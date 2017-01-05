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
from organization.network.utils import get_nb_half_days_by_period

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
