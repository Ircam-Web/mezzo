from django.shortcuts import render

from organization.projects.models import *
from organization.core.views import *


class ProjectListView(ListView):

    model = Project
    template_name='projects/project_list.html'


class ProjectDetailView(SlugMixin, DetailView):

    model = Project
    template_name='projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        project = self.get_object()
        department = None

        if project.lead_team:
            if project.lead_team.department:
                department = project.lead_team.department
        else:
            for team in project.teams.all():
                if team.department:
                    department = team.department
                    break

        context['department'] = department
        return context
