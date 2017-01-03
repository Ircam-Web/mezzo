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
from organization.network.models import (Person,
                                PersonListBlock,
                                PersonListBlockInline,
                                PageCustomPersonListBlockInline,
                                OrganizationLinked,
                                OrganizationLinkedInline,
                                OrganizationLinkedBlockInline,
                                Organization,
                                PersonActivityTimeSheet)
from organization.pages.models import Page, CustomPage


class PageCustomPersonListForm(forms.ModelForm):

    person_list_block = forms.ModelChoiceField(
        queryset=PersonListBlock.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-list-block-autocomplete')
    )

    class Meta:
        model = PageCustomPersonListBlockInline
        fields = ('person_list_block',)


class PersonListBlockInlineForm(forms.ModelForm):

    person = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        widget=autocomplete.ModelSelect2(url='person-autocomplete')
    )

    class Meta:
        model = PersonListBlockInline
        fields = ('__all__')


class OrganizationLinkedListForm(forms.ModelForm):

    organization_linked = forms.ModelChoiceField(
        queryset=OrganizationLinked.objects.all(),
        widget=autocomplete.ModelSelect2(url='organization-linked-list-autocomplete')
    )

    class Meta:
        model = OrganizationLinkedBlockInline
        fields = ('organization_linked',)


class OrganizationLinkedForm(forms.ModelForm):

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=autocomplete.ModelSelect2(url='organization-linked-autocomplete')
    )

    class Meta:
        model = OrganizationLinkedInline
        fields = ('organization',)


class PersonActivityTimeSheetForm(forms.ModelForm):

    class Meta:
        model = PersonActivityTimeSheet
        fields = ('__all__')
        # PersonActivityTimeSheetviewfields = ['pub_date', 'headline', 'content', 'reporter']
