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

from __future__ import unicode_literals

import os
import re
import pwd
import time
import urllib
import string
import datetime
import mimetypes
from geopy.geocoders import GoogleV3 as GoogleMaps
from geopy.exc import GeocoderQueryError

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

from organization.core.models import *
from organization.media.models import *
from organization.pages.models import CustomPage

from organization.network.validators import *

# from .nationalities.fields import NationalityField

# Hack to have these strings translated
mr = _('Mr')
mrs = _('Ms')

GENDER_CHOICES = [
    ('male', _('male')),
    ('female', _('female')),
]

PERSON_LIST_STYLE_CHOICES = [
    ('square', _('square')),
    ('circle', _('circle')),
]

TITLE_CHOICES = [
    ('Dr', _('Dr')),
    ('Prof', _('Prof')),
    ('Prof Dr', _('Prof Dr')),
]

PATTERN_CHOICES = [
    ('pattern-bg--circles', _('circles')),
    ('pattern-bg--squares', _('squares')),
    ('pattern-bg--stripes', _('stripes')),
    ('pattern-bg--triangles', _('triangles')),
]

ALIGNMENT_CHOICES = (('left', _('left')), ('left', _('left')), ('right', _('right')))

CSS_COLOR_CHOICES = [
    ('orange', _('orange')),
    ('blue', _('blue')),
    ('green', _('green')),
]

CSS_BANNER_CHOICES = [
    ('fsxxl', 'fsxxl'),
    ('fsxxxl', 'fsxxxl'),
]

BOX_SIZE_CHOICES = [
    (3, 3),
    (6, 6),
]


class Organization(Named, Address, URL, AdminThumbRelatedMixin, Orderable):
    """(Organization description)"""

    mappable_location = models.CharField(max_length=128, blank=True, null=True, help_text="This address will be used to calculate latitude and longitude. Leave blank and set Latitude and Longitude to specify the location yourself, or leave all three blank to auto-fill from the Location field.")
    lat = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Latitude", help_text="Calculated automatically if mappable location is set.")
    lon = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True, verbose_name="Longitude", help_text="Calculated automatically if mappable location is set.")
    type = models.ForeignKey('OrganizationType', verbose_name=_('organization type'), blank=True, null=True, on_delete=models.SET_NULL)
    initials = models.CharField(_('initials'), max_length=128, blank=True, null=True)
    is_on_map = models.BooleanField(_('is on map'), default=False, blank=True)
    is_host = models.BooleanField(_('is host'), default=False, blank=True)
    telephone = models.CharField(_('telephone'), max_length=64, blank=True, null=True)
    opening_times = models.TextField(_('opening times'), blank=True)
    subway_access = models.TextField(_('subway access'), blank=True)
    bio = models.TextField(_('bio'), blank=True)
    admin_thumb_type = 'logo'

    class Meta:
        verbose_name = _('organization')
        ordering = ['name',]

    def clean(self):
        """
        Validate set/validate mappable_location, longitude and latitude.
        """
        super(Organization, self).clean()

        if self.lat and not self.lon:
            raise ValidationError("Longitude required if specifying latitude.")

        if self.lon and not self.lat:
            raise ValidationError("Latitude required if specifying longitude.")

        if not (self.lat and self.lon) and not self.mappable_location:
            if self.address:
                self.mappable_location = self.address.replace("\n"," ").replace('\r', ' ') + ", " + self.postal_code + " " + self.city

        if self.mappable_location and not (self.lat and self.lon): #location should always override lat/long if set
            g = GoogleMaps(domain=settings.EVENT_GOOGLE_MAPS_DOMAIN)
            try:
                mappable_location, (lat, lon) = g.geocode(self.mappable_location)
            except GeocoderQueryError as e:
                raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
            except ValueError as e:
                raise ValidationError("The mappable location you specified could not be found on {service}: \"{error}\" Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.".format(service="Google Maps", error=e.message))
            except TypeError as e:
                raise ValidationError("The mappable location you specified could not be found. Try changing the mappable location, removing any business names, or leaving mappable location blank and using coordinates from getlatlon.com.")
            self.mappable_location = mappable_location
            self.lat = lat
            self.lon = lon

    def save(self, **kwargs):
        self.clean()
        super(Organization, self).save()


class OrganizationLinkedBlockInline(Titled, Orderable):
    organization_linked = models.ForeignKey('OrganizationLinked', verbose_name=_('organization list'), related_name='organization_linked_block_inline_list', blank=True, null=True)
    organization_main = models.ForeignKey('Organization', verbose_name=_('organization'), related_name='organization_linked_block', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationLinked(Titled):

    class Meta:
        verbose_name = _('Organization Linked')

    def __str__(self):
        return self.title


class OrganizationLinkedInline(Titled, Orderable):

    organization_list = models.ForeignKey('OrganizationLinked', verbose_name=_('organization linked'), related_name='organization_linked_inline_linked', blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey('Organization', verbose_name=_('organization'), related_name='organization_linked_inline_from', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationPlaylist(PlaylistRelated):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationLink(Link):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationImage(Image):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationBlock(Block):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class OrganizationService(Named, URL, Orderable):

    organization = models.ForeignKey(Organization, verbose_name=_('organization'), related_name='services', blank=True, null=True, on_delete=models.SET_NULL)
    image = FileField(_("Image"), max_length=1024, format="Image", upload_to="images")
    css_color = models.CharField(_('css color'), max_length=64, blank=True, null=True, choices=CSS_COLOR_CHOICES)
    css_banner_type = models.CharField(_('css banner type'), max_length=64, blank=True, null=True, choices=CSS_BANNER_CHOICES)
    box_size = models.IntegerField(_('box size'), default=3, choices=BOX_SIZE_CHOICES)


class OrganizationType(Named):
    """(OrganizationType description)"""

    css_class = models.CharField(_('class css'), max_length=64, blank=True, null=True,  help_text="Determine color on map.")

    class Meta:
        verbose_name = _('organization type')
        ordering = ['name',]


class Department(Named):
    """(Department description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'), related_name="departments")

    class Meta:
        verbose_name = _('department')
        ordering = ['name',]

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        return self.name


class DepartmentPage(Page, SubTitled, RichText):
    """(Department description)"""

    department = models.ForeignKey('Department', verbose_name=_('department'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)
    weaving_css_class = models.CharField(_('background pattern'), choices=PATTERN_CHOICES, max_length=64, blank=True)

    class Meta:
        verbose_name = _('department page')


class Team(Named, URL):
    """(Team description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'), related_name="teams", blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('Department', verbose_name=_('department'), related_name="teams", blank=True, null=True, on_delete=models.SET_NULL)
    code = models.CharField(_('code'), max_length=64, blank=True, null=True)
    is_legacy = models.BooleanField(_('is legacy'), default=False)
    parent = models.ForeignKey('Team', verbose_name=_('parent team'), related_name="children", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('team')
        ordering = ['name',]

    def __str__(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join((self.department.organization.name, self.department.name, self.name))
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name

    @property
    def short(self):
        if self.organization:
            return ' - '.join((self.organization.name, self.name))
        elif self.department:
            if self.department.organization:
                return ' - '.join((self.department.organization.name, self.name))
            else:
                return ' - '.join((self.department.name, self.name))
        return self.name


class TeamPage(Page, SubTitled, RichText):
    """(Team description)"""

    team = models.ForeignKey('Team', verbose_name=_('team'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('team page')


class TeamLink(Link):

    team = models.ForeignKey(Team, verbose_name=_('team'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class Person(Displayable, AdminThumbMixin):
    """(Person description)"""

    user = models.OneToOneField(User, verbose_name=_('user'), blank=True, null=True, on_delete=models.SET_NULL)
    person_title = models.CharField(_('title'), max_length=16, choices=TITLE_CHOICES, blank=True)
    gender = models.CharField(_('gender'), max_length=16, choices=GENDER_CHOICES, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    telephone = models.CharField(_('telephone'), max_length=64, blank=True, null=True)
    register_id = models.CharField(_('register ID'), blank=True, null=True, max_length=128)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    bio = RichTextField(_('biography'), blank=True)
    external_id = models.CharField(_('external ID'), blank=True, null=True, max_length=128)

    class Meta:
        verbose_name = _('person')
        ordering = ['last_name',]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-network-person-detail", kwargs={'slug': self.slug})

    def set_names(self):
        names = self.title.split(' ')
        if len(names) == 1:
            self.first_name = ''
            self.last_name = names[0]
        elif len(names) == 2:
            self.first_name = names[0]
            self.last_name = names[1]
        else:
            self.first_name = names[0]
            self.last_name = ' '.join(names[1:])

    def save(self, *args, **kwargs):
        super(Person, self).save(args, kwargs)
        for activity in self.activities.all():
            update_activity(activity)


class PersonPlaylist(PlaylistRelated):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class PersonLink(Link):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class PersonImage(Image):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class PersonFile(File):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class PersonBlock(Block):

    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class PageCustomPersonListBlockInline(Titled):

    page = models.ForeignKey(CustomPage, verbose_name=_('Page'), related_name='page_custom_person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)
    person_list_block = models.ForeignKey("PersonListBlock", related_name='page_custom_person_list_block_inlines', verbose_name=_('Person List Block'), blank=True, null=True)

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonListBlock(Titled, Dated):

    style = models.CharField(_('style'), max_length=16, choices=PERSON_LIST_STYLE_CHOICES)

    class Meta:
        verbose_name = _('Person List')

    def __str__(self):
        return self.title


class PersonListBlockInline(models.Model):

    person_list_block = models.ForeignKey(PersonListBlock, verbose_name=_('Person List Block'), related_name='person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, verbose_name=_('Person'), related_name='person_list_block_inlines', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Person autocomplete')


class ActivityStatus(Named):

    order = models.IntegerField(_('order number'), default=100)
    display = models.BooleanField(_('display on team page'), blank=True, default=True)
    parent = models.ForeignKey('ActivityStatus', verbose_name=_('parent'), related_name='children', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('status')
        ordering = ['order']


class ActivityGrade(Named):

    class Meta:
        verbose_name = _('grade')
        verbose_name_plural = _('grades')


class ActivityFramework(Named):

    class Meta:
        verbose_name = _('framework')
        verbose_name_plural = _('frameworks')

class ActivityFunction(Named):

    class Meta:
        verbose_name = _('function')
        verbose_name_plural = _('functions')

class BudgetCode(Named):

    class Meta:
        verbose_name = _('budget code')
        verbose_name_plural = _('budget codes')

class RecordPiece(Named):

    class Meta:
        verbose_name = _('record piece')
        verbose_name_plural = _('record pieces')

class TrainingType(Named):

    class Meta:
        verbose_name = _('training type')
        verbose_name_plural = _('training types')

class TrainingLevel(Named):

    class Meta:
        verbose_name = _('training level')
        verbose_name_plural = _('training levels')

class TrainingTopic(Named):

    class Meta:
        verbose_name = _('training topic')
        verbose_name_plural = _('training topics')

class TrainingSpeciality(Named):

    class Meta:
        verbose_name = _('training speciality')
        verbose_name_plural = _('training specialities')

class UMR(Named):

    class Meta:
        verbose_name = _('UMR')


class ActivityWeeklyHourVolume(Titled):

    monday_am = models.FloatField(_('monday AM'), validators=[validate_positive])
    monday_pm = models.FloatField(_('monday PM'), validators=[validate_positive])
    tuesday_am = models.FloatField(_('tuesday AM'), validators=[validate_positive])
    tuesday_pm = models.FloatField(_('tuesday PM'), validators=[validate_positive])
    wednesday_am = models.FloatField(_('wednesday AM'), validators=[validate_positive])
    wednesday_pm = models.FloatField(_('wednesday PM'), validators=[validate_positive])
    thursday_am = models.FloatField(_('thursday AM'), validators=[validate_positive])
    thursday_pm = models.FloatField(_('thursday PM'), validators=[validate_positive])
    friday_am = models.FloatField(_('friday AM'), validators=[validate_positive])
    friday_pm = models.FloatField(_('friday PM'), validators=[validate_positive])

    class Meta:
        verbose_name = _('Activity Weekly Hour Volume')
        verbose_name_plural = _('Activity Weekly Hour Volumes')


class PersonActivity(Period):
    """(Activity description)"""

    person = models.ForeignKey('Person', verbose_name=_('person'), related_name='activities')

    weeks = models.IntegerField(_('number of weeks'), blank=True, null=True)
    status = models.ForeignKey(ActivityStatus, verbose_name=_('status'), blank=True, null=True, related_name='activities', on_delete=models.SET_NULL)
    is_permanent = models.BooleanField(_('permanent'), default=False)
    framework = models.ForeignKey(ActivityFramework, verbose_name=_('framework'), blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.ForeignKey(ActivityGrade, verbose_name=_('grade'), blank=True, null=True, on_delete=models.SET_NULL)
    function = models.ForeignKey(ActivityFunction, verbose_name=_('function'), blank=True, null=True, on_delete=models.SET_NULL)

    organizations = models.ManyToManyField(Organization, verbose_name=_('organizations (attachment or subscribed)'), related_name='project_activities', blank=True)
    employers = models.ManyToManyField(Organization, verbose_name=_('employers'), related_name='employer_project_activities', blank=True)
    umr = models.ForeignKey(UMR, verbose_name=_('UMR'), blank=True, null=True, on_delete=models.SET_NULL)
    teams = models.ManyToManyField('Team', verbose_name=_('teams'), related_name='team_activities', blank=True)
    team_text = models.CharField(_('other team text'), blank=True, null=True, max_length=256)

    projects = models.ManyToManyField('organization-projects.Project', verbose_name=_('projects'), related_name='activities', blank=True)
    rd_quota_float = models.FloatField(_('R&D quota (float)'), blank=True, null=True)
    rd_quota_text = models.CharField(_('R&D quota (text)'), blank=True, null=True, max_length=128)
    rd_program = models.TextField(_('R&D program'), blank=True)
    budget_code = models.ForeignKey(BudgetCode, blank=True, null=True, on_delete=models.SET_NULL)

    supervisors = models.ManyToManyField('Person', verbose_name=_('supervisors'), related_name='supervisor_activities', blank=True)

    phd_doctoral_school = models.ForeignKey(Organization, verbose_name=_('doctoral school'), blank=True, null=True, on_delete=models.SET_NULL)
    phd_directors = models.ManyToManyField('Person', verbose_name=_('PhD directors'), related_name='phd_director_activities', blank=True)
    phd_defense_date = models.DateField(_('PhD defense date'), blank=True, null=True)
    phd_title = models.TextField(_('PhD title'), blank=True)
    phd_post_doctoral_situation =  models.CharField(_('post-doctoral situation'), blank=True, max_length=256)
    hdr = models.BooleanField(_('HDR'), default=False)

    training_type = models.ForeignKey(TrainingType, verbose_name=_('training type'), blank=True, null=True, on_delete=models.SET_NULL)
    training_level = models.ForeignKey(TrainingLevel, verbose_name=_('training level'), blank=True, null=True, on_delete=models.SET_NULL)
    training_topic = models.ForeignKey(TrainingTopic, verbose_name=_('training topic'), blank=True, null=True, on_delete=models.SET_NULL)
    training_speciality = models.ForeignKey(TrainingSpeciality, verbose_name=_('training speciality'), blank=True, null=True, on_delete=models.SET_NULL)
    training_title = models.TextField(_('Training title'), blank=True)

    record_piece = models.ForeignKey(RecordPiece, blank=True, null=True, on_delete=models.SET_NULL)

    date_added = models.DateTimeField(_('add date'), auto_now_add=True)
    date_modified = models.DateTimeField(_('modification date'), auto_now=True)
    date_modified_manual = models.DateTimeField(_('manual modification date'), blank=True, null=True)

    comments = models.TextField(_('comments'), blank=True)
    external_id = models.CharField(_('external ID'), blank=True, null=True, max_length=128)

    weekly_hour_volume = models.ForeignKey('ActivityWeeklyHourVolume', blank=True, null=True, on_delete=models.SET_NULL)

    monday_am = models.FloatField(_('monday AM'), validators=[validate_positive], blank=True, null=True)
    monday_pm = models.FloatField(_('monday PM'), validators=[validate_positive], blank=True, null=True)
    tuesday_am = models.FloatField(_('tuesday AM'), validators=[validate_positive], blank=True, null=True)
    tuesday_pm = models.FloatField(_('tuesday PM'), validators=[validate_positive], blank=True, null=True)
    wednesday_am = models.FloatField(_('wednesday AM'), validators=[validate_positive], blank=True, null=True)
    wednesday_pm = models.FloatField(_('wednesday PM'), validators=[validate_positive], blank=True, null=True)
    thursday_am = models.FloatField(_('thursday AM'), validators=[validate_positive], blank=True, null=True)
    thursday_pm = models.FloatField(_('thursday PM'), validators=[validate_positive], blank=True, null=True)
    friday_am = models.FloatField(_('friday AM'), validators=[validate_positive], blank=True, null=True)
    friday_pm = models.FloatField(_('friday PM'), validators=[validate_positive], blank=True, null=True)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ['-date_from',]

    def __str__(self):
        if self.status:
            return ' - '.join((self.status.name, str(self.date_from), str(self.date_to)))
        else:
            return ' - '.join((str(self.date_from), str(self.date_to)))

    def save(self, *args, **kwargs):
        super(PersonActivity, self).save(args, kwargs)
        update_activity(self)



class PersonActivityTimeSheet(models.Model):

    activity = models.ForeignKey('PersonActivity', verbose_name=_('activity'), related_name='timesheets')
    project = models.ForeignKey('organization-projects.Project', verbose_name=_('project'), related_name='timesheets')
    work_packages = models.ManyToManyField('organization-projects.ProjectWorkPackage', verbose_name=_('work package'), related_name='timesheets', blank=True)
    percentage = models.FloatField(_('% of work time on the project'), validators=[validate_positive])
    month = models.IntegerField(_('month'))
    year = models.IntegerField(_('year'))
    accounting = models.DateField(default=timezone.now(), blank=True)
    validation = models.DateField(default=timezone.now(), blank=True)

    @property
    def date(self):
        pass

    class Meta:
        verbose_name = _('activity timesheet')
        verbose_name_plural = _('activity timesheets')
        ordering = ['month',]


class PersonActivityVacation(Period):

    activity = models.ForeignKey('PersonActivity', verbose_name=_('activity'))


def update_activity(a):
    if a.weekly_hour_volume :
        # caution : if 0 return False
        # caution : 'None' is not empty
        if not a.monday_am.__str__() != 'None' and \
        not a.monday_pm.__str__() != 'None' and \
        not a.tuesday_am.__str__() != 'None' and \
        not a.tuesday_pm.__str__() != 'None' and \
        not a.wednesday_am.__str__() != 'None' and \
        not a.wednesday_pm.__str__() != 'None' and \
        not a.thursday_am.__str__() != 'None' and \
        not a.thursday_pm.__str__() != 'None' and \
        not a.friday_am.__str__() != 'None' and \
        not a.friday_pm.__str__() != 'None' :
            a.monday_am = a.weekly_hour_volume.monday_am
            a.monday_pm = a.weekly_hour_volume.monday_pm
            a.tuesday_am = a.weekly_hour_volume.tuesday_am
            a.tuesday_pm = a.weekly_hour_volume.tuesday_pm
            a.wednesday_am = a.weekly_hour_volume.wednesday_am
            a.wednesday_pm = a.weekly_hour_volume.wednesday_pm
            a.thursday_am = a.weekly_hour_volume.thursday_am
            a.thursday_pm = a.weekly_hour_volume.thursday_pm
            a.friday_am = a.weekly_hour_volume.friday_am
            a.friday_pm = a.weekly_hour_volume.friday_pm
            a.save()
