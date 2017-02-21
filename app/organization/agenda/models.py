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
from future.builtins import str

from django.utils.translation import ugettext_lazy as _
from mezzanine.core.models import Orderable
from mezzanine.conf import settings
from mezzanine_agenda.models import *
from organization.core.models import *
from organization.network.models import *



class EventBlock(Block):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("block")
        verbose_name_plural = _("blocks")


class EventImage(Image):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "event"


class EventDepartment(models.Model):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='departments', blank=True, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, verbose_name=_('department'), related_name='events', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")


class EventPerson(models.Model):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='persons', blank=True, null=True, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, verbose_name=_('person'), related_name='events', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("persons")


class EventRank(models.Model):

    event = models.OneToOneField(Event, verbose_name=_('event'), related_name='event_rank', blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(verbose_name=_('rank'), blank=True, null=True)

    class Meta:
        verbose_name = _("rank")
        verbose_name_plural = _("ranks")


class EventLink(Link):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("link")
        verbose_name_plural = _("links")


class EventPlaylist(PlaylistRelated):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("playlist")
        verbose_name_plural = _("playlists")
        order_with_respect_to = "event"


class EventPeriod(PeriodDateTime):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='periods', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("period")
        verbose_name_plural = _("periods")


class EventPublicType(Named):

    class Meta:
        verbose_name = _("public type")
        verbose_name_plural = _("public types")


class EventTrainingLevel(Named):

    class Meta:
        verbose_name = _("training level")
        verbose_name_plural = _("training levels")


class EventTraining(models.Model):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='trainings', blank=True, null=True, on_delete=models.SET_NULL)
    language = models.CharField(_('language'), max_length=64, blank=True, null=True, choices=settings.LANGUAGES)
    public_type = models.ForeignKey(EventPublicType, verbose_name=_('public type'), related_name='trainings', blank=True, null=True, on_delete=models.SET_NULL)
    level = models.ForeignKey(EventTrainingLevel, verbose_name=_('level'), related_name='trainings', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("training")
        verbose_name_plural = _("trainings")


class EventRelatedTitle(RelatedTitle):

    event = models.OneToOneField(Event, verbose_name=_('event'), related_name='related_title', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "event"


class DynamicContentEvent(DynamicContent, Orderable):

    event = models.ForeignKey(Event, verbose_name=_('event'), related_name='dynamic_content_event', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Event'


class EventPriceDescription(models.Model):

    event_price = models.OneToOneField(EventPrice, verbose_name=_('event_price_description'), related_name='event_price_description', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = 'Additionnal description'
