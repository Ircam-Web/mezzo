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

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationTabularInline
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin
from mezzanine_agenda.models import Event, EventCategory
from mezzanine_agenda.admin import *
from organization.core.models import *
from organization.agenda.models import *
from organization.agenda.forms import *


class EventBlockInline(StackedDynamicInlineAdmin):

    model = EventBlock


class EventImageInline(TabularDynamicInlineAdmin):

    model = EventImage


class EventPlaylistInline(TabularDynamicInlineAdmin):

    model = EventPlaylist


class EventDepartmentInline(TabularDynamicInlineAdmin):

    model = EventDepartment


class EventPersonInline(TabularDynamicInlineAdmin):

    model = EventPerson


class EventLinkInline(TabularDynamicInlineAdmin):

    model = EventLink


class EventTrainingInline(StackedDynamicInlineAdmin):

    model = EventTraining


class EventPeriodInline(TabularDynamicInlineAdmin):

    model = EventPeriod


class EventRelatedTitleAdmin(TranslationTabularInline):

    model = EventRelatedTitle


class EventPriceDescriptionAdmin(TranslationTabularInline):

    model = EventPriceDescription


class CustomEventPriceAdmin(BaseTranslationModelAdmin):

    inlines = [EventPriceDescriptionAdmin,]


class DynamicContentEventInline(TabularDynamicInlineAdmin):

    model = DynamicContentEvent
    form = DynamicContentEventForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class CustomEventCategoryAdmin(BaseTranslationModelAdmin):

    pass


class EventPublicTypeAdmin(BaseTranslationModelAdmin):

    model = EventPublicType


class EventTrainingLevelAdmin(BaseTranslationModelAdmin):

    model = EventTrainingLevel



admin.site.unregister(EventPrice)
admin.site.unregister(EventCategory)
admin.site.register(EventPublicType, EventPublicTypeAdmin)
admin.site.register(EventTrainingLevel, EventTrainingLevelAdmin)
admin.site.register(EventCategory, CustomEventCategoryAdmin)
admin.site.register(EventPrice, CustomEventPriceAdmin)
