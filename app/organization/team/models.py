from __future__ import unicode_literals

import os
import re
import pwd
import time
import urllib
import string
import datetime
import mimetypes

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.contrib.auth.models import User

from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from mezzanine.galleries.models import BaseGallery

from organization.core.models import *
from organization.magazine.models import Article

from django_countries.fields import CountryField
# from .nationalities.fields import NationalityField


# Hack to have these strings translated
mr = _('Mr')
mrs = _('Ms')

GENDER_CHOICES = [
    ('male', _('male')),
    ('female', _('female')),
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


class Address(models.Model):
    """(Address description)"""

    address = models.TextField(_('address'), blank=True)
    postal_code = models.CharField(_('postal code'), max_length=16, blank=True)
    country = CountryField(_('country'))

    def __str__(self):
        return ' '.join((self.address, self.postal_code))

        class Meta:
            abstract = True


class Organization(Slugged, Description, Address, Photo):
    """(Organization description)"""

    type = models.ForeignKey('OrganizationType', verbose_name=_('organization type'), blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(_('website'), max_length=512, blank=True)
    is_on_map = models.BooleanField(_('is on map'), default=True)

    class Meta:
        verbose_name = _('organization')


class OrganizationType(Named):
    """(OrganizationType description)"""

    class Meta:
        verbose_name = _('organization type')


class Department(Page, SubTitle, RichText, Photo):
    """(Department description)"""

    organization = models.ForeignKey('Organization', verbose_name=_('organization'))
    url = models.URLField(_('URL'), max_length=512, blank=True)
    weaving_css_class = models.CharField(_('background pattern'), choices=PATTERN_CHOICES, max_length=64, blank=True)
    articles_related = models.ManyToManyField(Article, verbose_name=_('Related articles'), blank=True)

    class Meta:
        verbose_name = _('department')


class Team(Page, SubTitle, RichText, Photo):
    """(Team description)"""

    # department = models.ForeignKey('Department', verbose_name=_('department'), related_name="teams", blank=True, null=True, on_delete=models.SET_NULL)
    partner_organizations = models.ManyToManyField(Organization, verbose_name=_('partner organizations'), blank=True)
    partner_teams = models.ManyToManyField('Team', verbose_name=_('partner teams'), blank=True)

    class Meta:
        verbose_name = _('team')


class Person(Displayable, AdminThumbMixin, Photo):
    """(Person description)"""

    user = models.ForeignKey(User, verbose_name=_('user'), blank=True, null=True, on_delete=models.SET_NULL)
    person_title = models.CharField(_('title'), max_length=16, choices=TITLE_CHOICES, blank=True)
    gender = models.CharField(_('gender'), max_length=16, choices=GENDER_CHOICES, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    birthday = models.DateField(_('birthday'), blank=True, null=True)
    bio = RichTextField(_('biography'), blank=True)

    class Meta:
        verbose_name = _('person')
        ordering = ['last_name',]

    def __str__(self):
        return ' '.join((self.first_name, self.last_name))

    # def get_absolute_url(self):
    #     return reverse("festival-artist-detail", kwargs={'slug': self.slug})

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

    def clean(self):
        super(Person, self).clean()
        self.set_names()

    def save(self, *args, **kwargs):
        self.set_names()
        super(Person, self).save(*args, **kwargs)


class TeamLink(Link):

    team = models.ForeignKey(Team, verbose_name=_('links'))

    def __str__(self):
        return self.url


class PersonActivity(Description, Period, RichText):
    """(Activity description)"""

    person = models.ForeignKey('Person', verbose_name=_('person'))
    team = models.ForeignKey('Team', verbose_name=_('team'))
    role = models.CharField(_('role'), blank=True, max_length=512)

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')

    def __unicode__(self):
        return ' - '.join((self.person, self.role, self.date_begin, self.date_end))


class PersonLink(Link):
    """A person can have many links."""

    person = models.ForeignKey('Person', verbose_name=_('person'))

    class Meta:
        verbose_name = _('person link')

    def __str__(self):
        return self.url
