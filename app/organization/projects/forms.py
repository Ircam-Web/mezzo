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

from dal import autocomplete

import dal_queryset_sequence
import dal_select2_queryset_sequence

from django import forms
from django.forms.widgets import HiddenInput
from django.forms import ModelForm
from mezzanine.core.models import Orderable
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import CustomPage
from organization.agenda.models import Event, DynamicContentEvent
from organization.media.models import Playlist
from organization.projects.models import *
from extra_views import InlineFormSet


class DynamicContentProjectForm(autocomplete.FutureModelForm):

    content_object = dal_queryset_sequence.fields.QuerySetSequenceModelField(
        queryset=autocomplete.QuerySetSequence(
            Article.objects.all(),
            CustomPage.objects.all(),
            Event.objects.all()
        ),
        required=False,
        widget=dal_select2_queryset_sequence.widgets.QuerySetSequenceSelect2('dynamic-content-project'),
    )

    class Meta:
        model = DynamicContentProject
        fields = ('content_object',)


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'description', 'keywords', 'website')


class ProjectICTForm(ModelForm):

    class Meta:
        model = Project
        exclude = ('external_id', '_meta_title')


class ProjectICTDataInline(InlineFormSet):

    max_num = 1
    model = ProjectICTData
    exclude = ('validation_status', )


class ProjectSimpleImageInline(InlineFormSet):

    max_num = 3
    model = ProjectSimpleImage
    fields = ('file', 'credits')


class ProjectContactInline(InlineFormSet):

    max_num = 1
    model = ProjectContact
    fields = ('gender', 'person_title', 'first_name', 'last_name', 'address', 'email', 'telephone', 'bio', 'address', 'postal_code', 'city', 'country')


class ProducerForm(ModelForm):

    class Meta:
        model = Organization
        fields = '__all__'


class ProjectResidencyForm(ModelForm):

    class Meta:
        model = ProjectResidency
        fields = '__all__'
