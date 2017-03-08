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
    url("^calls/detail/(?P<slug>.*)/$", ProjectCallDetailView.as_view(), name='organization-call-detail'),

    url("^calls/detail/(?P<slug>.*)/projects/submission/$", ProjectICTCreateView.as_view(), name='organization-project-create'),
    url("^calls/detail/(?P<call_slug>.*)/projects/detail/(?P<slug>.*)/$", ProjectICTDetailView.as_view(), name='organization-project-detail'),
    url("^calls/detail/(?P<call_slug>.*)/projects/lists/$", ProjectICTListView.as_view(), name='organization-project-list'),

    url("^calls/detail/(?P<slug>.*)/producers/submission/$", ProducerCreateView.as_view(), name='organization-producer-create'),
    url("^calls/detail/(?P<call_slug>.*)/producers/detail/(?P<slug>.*)/$", ProducerDetailView.as_view(), name='organization-producer-detail'),
    url("^calls/detail/(?P<call_slug>.*)/producers/lists/$", ProducerListView.as_view(), name='organization-producer-list'),

    url("^calls/detail/(?P<slug>.*)/residencies/submission/$", ProjectResidencyCreateView.as_view(), name='organization-residency-create'),
    url("^calls/detail/(?P<call_slug>.*)/residencies/detail/(?P<slug>.*)/$", ProjectResidencyDetailView.as_view(), name='organization-residency-detail'),
    url("^calls/detail/(?P<call_slug>.*)/residencies/lists/$", ProjectResidencyListView.as_view(), name='organization-residency-list'),


]
