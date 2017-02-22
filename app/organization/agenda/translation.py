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

from modeltranslation.translator import translator, register, TranslationOptions

from organization.agenda.models import *


@register(EventBlock)
class EventBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(EventImage)
class EventImageTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPlaylist)
class EventPlaylistTranslationOptions(TranslationOptions):

    fields = ()


@register(EventDepartment)
class EventDepartmentTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPerson)
class EventPersonTranslationOptions(TranslationOptions):

    fields = ()


@register(EventLink)
class EventLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(EventPeriod)
class EventPeriodTranslationOptions(TranslationOptions):

    fields = ()


@register(EventTraining)
class EventTrainingTranslationOptions(TranslationOptions):

    fields = ()


@register(EventTrainingLevel)
class EventTrainingLevelTranslationOptions(TranslationOptions):

    fields = ('name',)


@register(EventPublicType)
class EventPublicTypeTranslationOptions(TranslationOptions):

    fields = ('name',)


@register(EventRelatedTitle)
class EventRelatedTitleTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(DynamicContentEvent)
class DynamicContentEventTranslationOptions(TranslationOptions):

    fields = ()


@register(EventPriceDescription)
class EventPriceDescriptionTranslationOptions(TranslationOptions):

    fields = ('description', )


@register(EventPrice)
class EventPriceTranslationOptions(TranslationOptions):

    fields = ()
