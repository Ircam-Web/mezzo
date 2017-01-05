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

from django.contrib import admin
from django import forms
from copy import deepcopy
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.network.models import *
from organization.network.forms import *
from organization.pages.models import *
from organization.core.admin import *
from organization.pages.admin import PageImageInline, PageBlockInline, PagePlaylistInline, DynamicContentPageInline, PageRelatedTitleAdmin
from organization.shop.models import PageProductList


class OrganizationAdminInline(StackedDynamicInlineAdmin):

    model = OrganizationLinkedInline
    form = OrganizationLinkedForm


class OrganizationLinkedAdmin(BaseTranslationOrderedModelAdmin):

    inlines = (OrganizationAdminInline,)
    first_fields = ['name',]

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class OrganizationLinkedBlockInlineAdmin(StackedDynamicInlineAdmin):

    model = OrganizationLinkedBlockInline
    form = OrganizationLinkedListForm


class OrganizationPlaylistInline(TabularDynamicInlineAdmin):

    model = OrganizationPlaylist


class OrganizationLinkInline(StackedDynamicInlineAdmin):

    model = OrganizationLink


class OrganizationImageInline(TabularDynamicInlineAdmin):

    model = OrganizationImage


class OrganizationBlockInline(StackedDynamicInlineAdmin):

    model = OrganizationBlock


class OrganizationServiceInline(StackedDynamicInlineAdmin):

    model = OrganizationService


class OrganizationAdmin(BaseTranslationOrderedModelAdmin):

    model = Organization
    inlines = [ OrganizationServiceInline,
                OrganizationPlaylistInline,
                OrganizationImageInline,
                OrganizationBlockInline,
                OrganizationLinkInline,
                OrganizationLinkedBlockInlineAdmin
                 ]
    list_display = ['name', 'type', 'admin_thumb']
    list_filter = ['is_on_map',]
    search_fields = ['name',]
    first_fields = ['name',]



class PageProductListInline(TabularDynamicInlineAdmin):

    model = PageProductList


class DepartmentPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PagePlaylistInline, PageProductListInline, ]


class DepartmentAdmin(BaseTranslationModelAdmin):

    model = Department


class TeamLinkInline(StackedDynamicInlineAdmin):

    model = TeamLink


class TeamAdmin(BaseTranslationModelAdmin):

    model = Team
    search_fields = ['name', 'code']
    list_filter = ['department']
    list_display = ['name', 'department', 'code']
    inlines = [TeamLinkInline,]


class TeamPageAdmin(PageAdmin):

    inlines = [PageImageInline, PageBlockInline, PagePlaylistInline,
                PageProductListInline, PageRelatedTitleAdmin, DynamicContentPageInline]


class PersonAdminBase(BaseTranslationModelAdmin):

    model = Person


class ActivityWeeklyHourVolumeAdmin(BaseTranslationModelAdmin):

    model = ActivityWeeklyHourVolume


class PersonActivityInline(StackedDynamicInlineAdmin):

    model = PersonActivity
    fk_name = 'person'
    filter_horizontal = ['organizations', 'employers', 'teams',
                         'projects', 'supervisors', 'phd_directors', ]
    # fields = ()
    #
    # fields = (('monday_am','monday_pm'), 'weekly_hour_volume')

    # def __init__(self, *args, **kwargs):
    #     super(PersonActivityInline, self).__init__(*args, **kwargs)
    #     # print(self.model._meta.get_fields())
    #     self.fields = self.model._meta.get_fields()
    #     print(self.fields)
    #     # self.fields.append(('monday_am', 'monday_pm'))

class PersonPlaylistInline(TabularDynamicInlineAdmin):

    model = PersonPlaylist


class PersonLinkInline(StackedDynamicInlineAdmin):

    model = PersonLink


class PersonImageInline(TabularDynamicInlineAdmin):

    model = PersonImage


class PersonFileInline(TabularDynamicInlineAdmin):

    model = PersonFile


class PersonBlockInline(StackedDynamicInlineAdmin):

    model = PersonBlock


class PersonAdmin(BaseTranslationOrderedModelAdmin):

    model = Person
    inlines = [PersonImageInline,
               PersonBlockInline,
               PersonPlaylistInline,
               PersonLinkInline,
               PersonFileInline,
               PersonActivityInline,]
    first_fields = ['last_name', 'first_name', 'title', 'gender', 'user']
    search_fields = ['last_name', 'first_name']
    list_display = [ 'last_name', 'first_name', 'register_id', 'external_id', 'email', 'last_weekly_hour_volume', 'gender', 'created']
    list_filter = ['person_title', 'activities__date_from', 'activities__date_to',
                    'activities__is_permanent', 'activities__framework', 'activities__grade',
                    'activities__status', 'activities__teams', 'activities__projects',
                    'activities__weekly_hour_volume', null_filter('register_id'), null_filter('external_id')]

    def last_weekly_hour_volume(self, instance):
        last_activity = instance.activities.first()
        weekly_hour_volume = '-'
        if hasattr(last_activity, 'weekly_hour_volume'):
            if last_activity.weekly_hour_volume.__str__() != 'None':
                weekly_hour_volume = last_activity.weekly_hour_volume.__str__()
        return weekly_hour_volume


class PersonActivityAdmin(BaseTranslationModelAdmin):

    model = PersonActivity
    list_display = ['person', 'get_teams', 'status', 'date_from', 'date_to']
    filter_horizontal = ['organizations', 'employers', 'teams', 'projects',
                         'supervisors', 'phd_directors', ]
    search_fields = ['person__title',]
    list_filter = [ 'date_from', 'date_to',
                    'is_permanent', 'framework', 'grade',
                    'status', 'teams', 'projects']

    def get_teams(self, instance):
        values = []
        for team in instance.teams.all():
            values.append(team.code)
        return ' - '.join(values)


class PersonListBlockInlineAdmin(TabularDynamicInlineAdmin):

    model = PersonListBlockInline
    form = PersonListBlockInlineForm


class PersonListBlockAdmin(admin.ModelAdmin):

    inlines = [PersonListBlockInlineAdmin,]
    list_display = ['title', 'description', 'date_created', 'date_modified']


class ActivityFunctionAdmin(BaseTranslationModelAdmin):

    model = ActivityFunction


class ActivityGradeAdmin(BaseTranslationModelAdmin):

    model = ActivityGrade


class ActivityFrameworkAdmin(BaseTranslationModelAdmin):

    model = ActivityFramework


class ActivityStatusAdmin(BaseTranslationModelAdmin):

    model = ActivityStatus


class TrainingTypeAdmin(BaseTranslationModelAdmin):

    model = TrainingType


class TrainingLevelAdmin(BaseTranslationModelAdmin):

    model = TrainingLevel


class TrainingSpecialityAdmin(BaseTranslationModelAdmin):

    model = TrainingSpeciality


class TrainingTopicAdmin(BaseTranslationModelAdmin):

    model = TrainingTopic


class PersonActivityTimeSheetAdmin(BaseTranslationModelAdmin):
    model = PersonActivityTimeSheet
    list_display = ['person', 'activity', 'year', 'month', 'project', 'work_package', 'percentage',  'accounting', 'validation']
    list_filter = ['activity__person', 'year', 'project']
    def person(self, instance):
        return instance.activity.person

    def work_package(self, instance):
        wk_list = [str(wk.number) for wk in instance.work_packages.all()]
        return ",".join(wk_list)


admin.site.register(OrganizationLinked, OrganizationLinkedAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationType)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(DepartmentPage, DepartmentPageAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamPage, TeamPageAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonListBlock, PersonListBlockAdmin)
admin.site.register(PersonActivity, PersonActivityAdmin)
admin.site.register(ActivityStatus, ActivityStatusAdmin)
admin.site.register(ActivityGrade, ActivityGradeAdmin)
admin.site.register(ActivityFramework, ActivityFrameworkAdmin)
admin.site.register(ActivityFunction, ActivityFunctionAdmin)
admin.site.register(ActivityWeeklyHourVolume, ActivityWeeklyHourVolumeAdmin)
admin.site.register(TrainingType, TrainingTypeAdmin)
admin.site.register(TrainingLevel, TrainingLevelAdmin)
admin.site.register(TrainingTopic, TrainingTopicAdmin)
admin.site.register(TrainingSpeciality, TrainingSpecialityAdmin)
admin.site.register(PersonActivityTimeSheet, PersonActivityTimeSheetAdmin)
