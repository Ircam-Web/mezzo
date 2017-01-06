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
import datetime
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from mezzanine.core.models import RichText, Displayable, Slugged, Orderable

from organization.core.models import *
from organization.pages.models import *
from organization.network.models import *


PROJECT_TYPE_CHOICES = [
    ('internal', _('internal')),
    ('external', _('external')),
]

ACCESS_CHOICES = [
    ('public', _('public')),
    ('shared', _('shared')),
    ('private', _('private')),
]


class Project(Displayable, Period, RichText):
    """(Project description)"""

    type = models.CharField(_('type'), max_length=128, choices=PROJECT_TYPE_CHOICES)
    external_id = models.CharField(_('external ID'), blank=True, null=True, max_length=128)
    program = models.ForeignKey('ProjectProgram', verbose_name=_('project program'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    program_type = models.ForeignKey('ProjectProgramType', verbose_name=_('project program type'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    call = models.ForeignKey('ProjectCall', verbose_name=_('project call'), related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    lead_team = models.ForeignKey('organization-network.Team', verbose_name=_('lead team'), related_name='leader_projects', blank=True, null=True)
    lead_organization = models.ForeignKey('organization-network.Organization', verbose_name=_('lead organization'), related_name='leader_projects', blank=True, null=True)
    teams = models.ManyToManyField('organization-network.Team', verbose_name=_('teams'), related_name='partner_projects', blank=True)
    organizations = models.ManyToManyField('organization-network.Organization', verbose_name=_('organizations'), blank=True)
    website = models.URLField(_('website'), max_length=512, blank=True)
    topic = models.ForeignKey('ProjectTopic', verbose_name=_('topic'), related_name='projects', blank=True, null=True)
    referring_person = models.ManyToManyField('organization-network.Person', verbose_name=_('Referring Person'), related_name='projects_referring_person', blank=True)
    manager =  models.ManyToManyField('organization-network.Person', verbose_name=_('Manager'), related_name='projects_manager', blank=True, null=True)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _("projects")
        ordering = ['-date_from', '-date_to']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-project-detail", kwargs={"slug": self.slug})

    def project_status(self):
        if self.date_from and self.date_to:
            if datetime.date.today() >= self.date_from and datetime.date.today() <= self.date_to:
                return _('in progress')
            elif datetime.date.today() < self.date_from and datetime.date.today() < self.date_to:
                return _('pending')
            elif datetime.date.today() > self.date_to and datetime.date.today() > self.date_to:
                return _('completed')
        else:
            return _('pending')


class ProjectTopic(Named):

    parent = models.ForeignKey('ProjectTopic', verbose_name=_('parent topic'), related_name='topics', blank=True, null=True)

    class Meta:
        verbose_name = _('project topic')
        verbose_name_plural = _("project topics")
        ordering = ['name',]

    def __str__(self):
        if self.parent:
            return ' - '.join((self.parent.name, self.name))
        else:
            return self.name


class ProjectProgram(Named):

    class Meta:
        verbose_name = _('program')
        verbose_name_plural = _("programs")
        ordering = ['name',]


class ProjectProgramType(Named):

    class Meta:
        verbose_name = _('program type')
        verbose_name_plural = _("program types")
        ordering = ['name',]


class ProjectCall(Named):

    class Meta:
        verbose_name = _('project call')
        verbose_name_plural = _("project calls")
        ordering = ['name',]


class ProjectWorkPackage(Titled, Period):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='work_packages')
    number = models.IntegerField(_('number'))
    lead_organization = models.ForeignKey('organization-network.Organization', verbose_name=_('lead organization'), related_name='leader_work_packages', blank=True, null=True)

    class Meta:
        verbose_name = _('work package')
        verbose_name_plural = _("work packages")
        ordering = ['number',]


class ProjectPlaylist(PlaylistRelated):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectLink(Link):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='links', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectImage(Image):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectFile(File):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='files', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectBlock(Block):


    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='blocks', blank=True, null=True, on_delete=models.SET_NULL)


class ProjectTopicPage(Page, SubTitled):

    project_topic = models.ForeignKey('ProjectTopic', verbose_name=_('project topic'), related_name="pages", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('project topic page')
        verbose_name_plural = _("project topic pages")


class ProjectDemo(Displayable, RichText, URL):

    project = models.ForeignKey('Project', verbose_name=_('project'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    authors = models.ManyToManyField(Person, verbose_name=_('authors'), related_name='demos', blank=True)
    repository = models.ForeignKey('Repository', verbose_name=_('repository'), related_name='demos', blank=True, null=True, on_delete=models.SET_NULL)
    build_commands = models.TextField(_('build commands'), blank=True)
    directory = models.CharField(_('directory'), max_length=256, blank=True, null=True, help_text='Relative directory in repository')

    class Meta:
        verbose_name = _('project demo')
        verbose_name_plural = _("project demos")

    def get_absolute_url(self):
        return reverse("organization-project-demo-detail", kwargs={"slug": self.slug})

    @property
    def relative_url(self):
        path = self.repository.directory.replace(settings.MEDIA_ROOT, '')
        return settings.MEDIA_URL + path + os.sep + self.directory + '/index.html'

    def build(self):
        os.chdir(self.repository.directory)
        for command in self.build_commands.split('\n'):
            os.system(command)

    def save(self, *args, **kwargs):
        super(ProjectDemo, self).save(args, kwargs)
        if self.repository:
            self.build()


class Repository(Named):

    system = models.ForeignKey('RepositorySystem', verbose_name=_('system'), related_name='repositories')
    access = models.CharField(_('access'), max_length=64, choices=ACCESS_CHOICES, default='private')
    branch = models.CharField(_('branch'), max_length=32, default='master')
    url = models.CharField(_('URL'), max_length=256, help_text='http(s) or ssh')

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _("repositories")

    def save(self, *args, **kwargs):
        super(Repository, self).save(args, kwargs)
        os.path.exists(self.directory)
        if not os.path.exists(self.directory):
            self.clone()
        self.checkout()

    @property
    def directory(self):
        dir_name = self.url.split('/')[-1].split('.')[0]
        return settings.PROJECT_DEMOS_DIR + dir_name

    def clone(self):
        os.chdir(settings.PROJECT_DEMOS_DIR)
        os.system(' '.join((self.system.clone_command, self.url)))

    def pull(self):
        os.chdir(self.directory)
        os.system(' '.join((self.system.pull_command, self.branch)))

    def checkout(self):
        os.chdir(self.directory)
        os.system(' '.join((self.system.checkout_command, self.branch)))


class RepositorySystem(Named):

    clone_command = models.CharField(_('clone command'), max_length=256)
    pull_command = models.CharField(_('pull command'), max_length=256)
    checkout_command = models.CharField(_('checkout command'), max_length=256)
    branch_command = models.CharField(_('branch command'), max_length=256)

    class Meta:
        verbose_name = _('repository system')
        verbose_name_plural = _("repository systems")


class ProjectRelatedTitle(RelatedTitle):

    project = models.OneToOneField(Project, verbose_name=_('project'), related_name='related_title', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("related title")
        order_with_respect_to = "project"


class DynamicContentProject(DynamicContent, Orderable):

    project = models.ForeignKey(Project, verbose_name=_('project'), related_name='dynamic_content_project', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Dynamic Content Project'
