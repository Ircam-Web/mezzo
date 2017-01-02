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

from organization.network.models import *


@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):

    fields = ('description', 'opening_times', 'subway_access', 'bio')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(DepartmentPage)
class DepartmentPageTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content',)


@register(Team)
class TeamTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(TeamPage)
class TeamPageTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content',)


@register(TeamLink)
class TeamLinkTranslationOptions(TranslationOptions):

    fields = ()


@register(Person)
class PersonTranslationOptions(TranslationOptions):

    fields = ('description','bio',)


@register(PersonActivity)
class PersonActivityTranslationOptions(TranslationOptions):

    fields = ('comments',)


@register(PersonPlaylist)
class PersonPlaylistTranslationOptions(TranslationOptions):

    pass


@register(PersonLink)
class PersonLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(PersonImage)
class PersonImageTranslationOptions(TranslationOptions):

    pass


@register(PersonFile)
class PersonFileTranslationOptions(TranslationOptions):

    pass


@register(PersonBlock)
class PersonBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(OrganizationPlaylist)
class OrganizationTranslationOptions(TranslationOptions):

    pass


@register(OrganizationLink)
class OrganizationLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(OrganizationImage)
class OrganizationImageTranslationOptions(TranslationOptions):

    pass


@register(OrganizationBlock)
class OrganizationBlockTranslationOptions(TranslationOptions):

    pass


@register(OrganizationService)
class OrganizationServiceTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(PersonListBlock)
class PersonListBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'description')


@register(PersonListBlockInline)
class PersonListBlockInlineTranslationOptions(TranslationOptions):

    pass


@register(PageCustomPersonListBlockInline)
class PageCustomPersonListBlockInlineTranslationOptions(TranslationOptions):

    pass


@register(ActivityGrade)
class ActivityGradeTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(ActivityFunction)
class ActivityFunctionTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(ActivityFramework)
class ActivityFrameworkTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(ActivityStatus)
class ActivityStatusTranslationOptions(TranslationOptions):

    fields = ['name', 'description',]


@register(TrainingTopic)
class TrainingTopicTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingType)
class TrainingTypeTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingLevel)
class TrainingLevelTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(TrainingSpeciality)
class TrainingSpecialityTranslationOptions(TranslationOptions):

    fields = ['name', 'description']


@register(OrganizationLinked)
class OrganizationLinkedTranslationOptions(TranslationOptions):

    fields = []


@register(OrganizationLinkedInline)
class OrganizationLinkedInlineTranslationOptions(TranslationOptions):

    fields = []


@register(OrganizationLinkedBlockInline)
class OrganizationLinkedBlockInlineTranslationOptions(TranslationOptions):

    fields = []


@register(ActivityWeeklyHourVolume)
class ActivityWeeklyHourVolumeTranslationOptions(TranslationOptions):

    fields = []


@register(PersonActivityTimeSheet)
class PersonActivityTimeSheetTranslationOptions(TranslationOptions):

    fields = []
