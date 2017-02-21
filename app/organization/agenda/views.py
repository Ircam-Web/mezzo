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

from datetime import datetime
from django.views.generic.base import TemplateView
from mezzanine.conf import settings
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from organization.magazine.models import Article
from organization.pages.models import CustomPage
from mezzanine_agenda.models import Event
from mezzanine_agenda.views import EventListView
from organization.core.views import autocomplete_result_formatting
from django.db.models import Q


class ConfirmationView(TemplateView):

    template_name = "agenda/confirmation.html"

    def get_context_data(self, **kwargs):
        context = super(ConfirmationView, self).get_context_data(**kwargs)
        context['confirmation_url'] = settings.EVENT_CONFIRMATION_URL % kwargs['transaction_id']
        return context


class DynamicContentEventView(Select2QuerySetSequenceView):

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


class CustomEventListView(EventListView):
    past_events = []
    paginate_by = settings.EVENT_PER_PAGE

    def get_queryset(self, tag=None):
        qs = super(CustomEventListView, self).get_queryset(tag=None)
        qs = qs.order_by("event_rank__rank", "start") # loosing start ordering. Had to regive it.
        self.past_events = Event.objects.filter(Q(start__lt=datetime.now()) | Q(end__lt=datetime.now())).order_by("start")
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(CustomEventListView, self).get_context_data(**kwargs)
        context['past_events'] = self.past_events
        return context
