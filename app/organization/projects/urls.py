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

import django.views.i18n
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import permission_required
from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from organization.projects.views import *

urlpatterns = [
    url("^dynamic-content-project/$",  permission_required('project.can_edit')(DynamicContentProjectView.as_view()), name='dynamic-content-project'),

    url("^projects/detail/(?P<slug>.*)/$", ProjectDetailView.as_view(), name='organization-project-detail'),
    url("^projects/demo/(?P<slug>.*)/$", ProjectDemoDetailView.as_view(), name='organization-project-demo-detail'),
    url("^projects/blog/(?P<slug>.*)/$", ProjectBlogPageView.as_view(), name='organization-project-blogpage-detail'),

    url("^calls/list/$", ProjectCallListView.as_view(), name='organization-call-list'),
    url("^calls/(?P<slug>.*)/detail/$", ProjectCallDetailView.as_view(), name='organization-call-detail'),

    url("^calls/(?P<slug>.*)/detail/projects/submission/$", ProjectCallDetailView.as_view().as_view(), name='organization-project-submission'), #HACK
    url("^calls/(?P<slug>.*)/detail/projects/create/$", ProjectICTCreateView.as_view(), name='organization-project-create'),
    url("^calls/(?P<slug>.*)/detail/projects/validation/$", ProjectICTValidationView.as_view(), name='organization-project-validation'),

    url("^calls/(?P<call_slug>.*)/projects/detail/(?P<slug>.*)/$", ProjectICTDetailView.as_view(), name='organization-project-detail'),
    url("^calls/(?P<call_slug>.*)/projects/list/$", ProjectICTListView.as_view(), name='organization-project-list'),

    url("^producers/submission/$", ProducerCreateView.as_view(), name='organization-producer-create'),
    url("^producers/(?P<slug>.*)/detail/$", ProducerDetailView.as_view(), name='organization-producer-detail'),
    url("^producers/list/$", ProducerListView.as_view(), name='organization-producer-list'),

    url("^calls/(?P<slug>.*)/residencies/submission/$", ProjectResidencyCreateView.as_view(), name='organization-residency-create'),
    url("^calls/(?P<call_slug>.*)/residencies/(?P<slug>.*)/detail/$", ProjectResidencyDetailView.as_view(), name='organization-residency-detail'),
    url("^calls/(?P<call_slug>.*)/residencies/list/$", ProjectResidencyListView.as_view(), name='organization-residency-list'),


]
