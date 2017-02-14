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

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.db.models.fields.related import ForeignKey
from mezzanine.conf import settings
from django.core.urlresolvers import reverse
from dal import autocomplete
from organization.network.models import *
from organization.core.views import *
from datetime import date
from organization.network.forms import *
from organization.network.utils import TimesheetXLS
from collections import OrderedDict



class PersonListView(ListView):

    model = Person
    template_name='team/person_list.html'


class PersonDetailView(SlugMixin, DetailView):

    model = Person
    template_name='network/person_detail.html'
    context_object_name = 'person'

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context["related"] = {}
        # Person events : this type is separated from the other because
        # this is not managed by list of person by person in inlines directly
        person_events = self.object.events.all()
        events = [item.event for item in person_events]
        context["related"]["event"] = events
        # All other related models
        person_list_block_inlines = self.object.person_list_block_inlines.all()
        related_instances = []
        # for each person list to which the person belongs to...
        for person_list_block_inline in person_list_block_inlines:
            related_objects = person_list_block_inline.person_list_block._meta.get_all_related_objects()
            for related_object in related_objects:
                if hasattr(person_list_block_inline.person_list_block, related_object.name):
                    # getting relating inlines like ArticlePersonListBlockInline, PageCustomPersonListBlockInline etc...
                    related_inlines = getattr(person_list_block_inline.person_list_block, related_object.name).all()
                    for related_inline in related_inlines:
                        if not isinstance(related_inline, person_list_block_inline.__class__):  #and not isinstance(person_list_block_inline.person_list_block.__class__):
                            fields = related_inline._meta.get_fields()
                            for field in fields:
                                # check if it is a ForeignKey
                                if isinstance(field, ForeignKey) :
                                    instance = getattr(related_inline, field.name)
                                    # get only article, custom page etc...
                                    if not isinstance(instance, person_list_block_inline.person_list_block.__class__) :  #and not isinstance(person_list_block_inline.person_list_block.__class__):
                                        if not instance._meta.model_name in context["related"]:
                                            context["related"][instance._meta.model_name] = []
                                        context["related"][instance._meta.model_name].append(instance)

        context["person_email"] = self.object.email if self.object.email else self.object.slug.replace('-', '.')+" (at) ircam.fr"
        return context


class PersonListBlockAutocompleteView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # if not self.request.is_authenticated():
        #     return PersonListBlock.objects.none()

        qs = PersonListBlock.objects.all()

        title = self.forwarded.get('title', None)

        if title:
            qs = qs.filter(title=title)

        if self.q:
            qs = qs.filter(title__istartswith=self.q)

        return qs


class PersonListView(autocomplete.Select2QuerySetView):

    def get_queryset(self):

        qs = Person.objects.all()

        person_title = self.forwarded.get('person_title', None)

        if person_title:
            qs = qs.filter(person_title=person_title)

        if self.q:
            qs = qs.filter(person_title__istartswith=self.q)

        return qs

class OrganizationListView(ListView):

    model = Organization
    context_object_name = 'organizations'
    template_name='network/organization_list.html'

    def get_queryset(self, **kwargs):
        return self.model.objects.filter(is_on_map=True)

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context['organization_types'] = self.get_queryset().values_list('type__name', 'type__css_class').order_by('type__name').distinct('type__name')
        return context


class OrganizationLinkedListView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = OrganizationLinked.objects.all()
        orga_linked_title = self.forwarded.get('title', None)
        if orga_linked_title:
            qs = qs.filter(title=orga_linked_title)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs


class OrganizationLinkedView(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Organization.objects.all()
        orga_name= self.forwarded.get('name', None)
        if orga_name:
            qs = qs.filter(name=orga_name)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs



class TimesheetAbstractView(LoginRequiredMixin):
    login_url = settings.LOGIN_URL

    class Meta:
        abstract = True


class TimeSheetCreateView(TimesheetAbstractView, CreateView):
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_create.html'
    context_object_name = 'timesheet'
    form_class = PersonActivityTimeSheetForm

    def get_success_url(self):
        print(" self.kwargs['slug']",  self.kwargs['slug'])
        return reverse('organization-network-timesheet-list-view', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        initial = super(TimeSheetCreateView, self).get_initial()
        # get the more recent activity
        initial['activity'] = PersonActivity.objects.filter(person__slug=self.kwargs['slug']).first()
        initial['month'] = self.kwargs['month']
        initial['year'] = self.kwargs['year']
        return initial

    def get_context_data(self, **kwargs):
        context = super(TimeSheetCreateView, self).get_context_data(**kwargs)
        context.update(self.kwargs)
        return context


class PersonActivityTimeSheetListView(TimesheetAbstractView, ListView):
    model = PersonActivityTimeSheet
    template_name='network/person_activity_timesheet/person_activity_timesheet_list.html'
    context_object_name = 'timesheets_by_year'

    def get_queryset(self):
        if 'slug' in self.kwargs:
            timesheets = PersonActivityTimeSheet.objects.filter(activity__person__slug__exact=self.kwargs['slug'])
            t_dict = OrderedDict()
            for timesheet in timesheets:
                year = timesheet.year
                if not year in t_dict:
                    t_dict[year] = {}
                project_slug = timesheet.project.title
                # if new person
                if not project_slug in t_dict[year]:
                    t_dict[year][project_slug] = []
                t_dict[year][project_slug].append(timesheet)
            return t_dict

    def get_context_data(self, **kwargs):
        context = super(PersonActivityTimeSheetListView, self).get_context_data(**kwargs)
        context['current_month'] = date.today().month
        context['current_year'] = date.today().year
        context.update(self.kwargs)
        return context


class PersonActivityTimeSheetExportView(TimesheetAbstractView, View):

    def get(self, *args, **kwargs):
        timesheets = PersonActivityTimeSheet.objects.filter(activity__person__slug__exact=kwargs['slug'], year=kwargs['year'])
        xls = TimesheetXLS(timesheets)
        return xls.write()
