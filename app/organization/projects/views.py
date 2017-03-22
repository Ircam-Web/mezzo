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
from django.views.generic.detail import SingleObjectMixin
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from mezzanine_agenda.models import Event
from mezzanine.conf import settings
from organization.projects.models import *
from organization.projects.forms import *
from organization.network.forms import *
from organization.core.views import *
from organization.magazine.views import Article
from organization.pages.models import CustomPage


class ProjectMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        self.object = self.get_object()
        if not isinstance(self.object, Project):
            self.project = self.object.project
        else:
            self.project = self.object

        department = None

        if self.project.lead_team:
            if self.project.lead_team.department:
                department = self.project.lead_team.department
        else:
            for team in self.project.teams.all():
                if team.department:
                    department = team.department
                    break

        context['department'] = department
        if self.project.topic and self.project.topic.parent:
            context['page'] = self.project.topic.parent.pages.all().first()
        elif self.project.topic:
            context['page'] = self.project.topic.pages.all().first()

        return context


class ProjectDetailView(SlugMixin, ProjectMixin, DetailView):

    model = Project
    template_name='projects/project_detail.html'


class ProjectICTDetailView(SlugMixin, ProjectMixin, DetailView):

    model = Project
    template_name='projects/project_ict_detail.html'


class ProjectListView(ListView):

    model = Project
    template_name='projects/project_list.html'


class DynamicContentProjectView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class ProjectDemoDetailView(SlugMixin, ProjectMixin, DetailView):

    model = ProjectDemo
    template_name='projects/project_demo_detail.html'


class ProjectBlogPageView(SlugMixin, ProjectMixin, DetailView):

    model = ProjectBlogPage
    template_name='projects/project_blogpage_detail.html'


class ProjectICTDetailView(SlugMixin,DetailView):

    model = Project
    template_name='projects/project_ict_detail.html'


class ProjectCallMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ProjectCallMixin, self).get_context_data(**kwargs)
        self.call = ProjectCall.objects.get(slug=self.kwargs['slug'])
        context['call'] = self.call
        return context


class ProjectICTSubmissionView(ProjectCallMixin, TemplateView):

    model = Project
    template_name='projects/project_ict_submission.html'



class ProjectICTCreateView(ProjectCallMixin, CreateWithInlinesView):

    model = Project
    form_class = ProjectForm
    template_name='projects/project_ict_create.html'
    inlines = [ProjectPublicDataInline, ProjectPrivateDataInline, ProjectUserImageInline, ProjectContactInline,]
    topic = 'ICT'


    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.call = ProjectCall.objects.get(slug=self.kwargs['slug'])
        self.object.call = self.call
        self.object.topic, c = ProjectTopic.objects.get_or_create(name='ICT')
        self.object.save()
        return super(ProjectICTCreateView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('organization-project-validation', kwargs={'slug':self.call.slug})


class ProjectICTValidationView(ProjectCallMixin, TemplateView):

    model = Project
    template_name='projects/project_ict_validation.html'


class ProjectICTListView(ListView):

    model = Project
    template_name='projects/project_ict_list.html'


class ProjectCallDetailView(SlugMixin, DetailView):

    model = ProjectCall
    template_name='projects/project_call_detail.html'


class ProjectCallListView(ListView):

    model = ProjectCall
    template_name='projects/project_call_list.html'


class ProducerDetailView(SlugMixin, DetailView):

    model = Organization
    template_name='projects/project_producer_detail.html'


class ProducerListView(ListView):

    model = Organization
    template_name='projects/project_producer_list.html'

    def get_queryset(self):
        type, c = OrganizationType.objects.get_or_create(name='Producer')
        qs = Organization.objects.filter(type=type)
        return qs


class ProducerCreateView(CreateWithInlinesView):

    model = Organization
    form_class = OrganizationForm
    template_name='projects/project_producer_create.html'
    inlines = [OrganizationContactInline, OrganizationUserImageInline]

    def forms_valid(self, form, inlines):
        self.object = form.save()
        self.object.type, c = OrganizationType.objects.get_or_create(name='Producer')
        self.object.save()
        return super(ProducerCreateView, self).forms_valid(form, inlines)

    def get_success_url(self):
        return reverse_lazy('organization-producer-detail', kwargs={'slug':self.slug})


class ProjectResidencyDetailView(SlugMixin, DetailView):

    model = ProjectResidency
    template_name='projects/project_residency_detail.html'


class ProjectResidencyListView(ListView):

    model = ProjectResidency
    template_name='projects/project_residency_list.html'


class ProjectResidencyCreateView(CreateWithInlinesView):

    model = ProjectResidency
    form_class = ProjectResidencyForm
    template_name='projects/project_residency_create.html'
    inlines = []
