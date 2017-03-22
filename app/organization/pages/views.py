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
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dal import autocomplete
from dal_select2_queryset_sequence.views import Select2QuerySetSequenceView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import settings
from organization.pages.models import CustomPage
from organization.core.views import SlugMixin, autocomplete_result_formatting
from organization.magazine.models import Article, Topic, Brief
from organization.pages.models import Home
from organization.agenda.models import Event
from organization.media.models import Playlist, Media
from organization.network.models import Person
from django.shortcuts import redirect


class HomeView(SlugMixin, ListView):

    model = Home
    template_name = 'index.html'
    briefs = Brief.objects.all() # with .published, order by isn't working anymore
    context_object_name = 'home'

    def get_queryset(self, **kwargs):
        homes = self.model.objects.published()
        if homes:
            return homes.latest("publish_date")
        return None

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['briefs'] = self.briefs
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.get_queryset():
            page = CustomPage.objects.first()
            return redirect(reverse_lazy('page', kwargs={'slug': page.slug}))
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)


class DynamicContentHomeSliderView(Select2QuerySetSequenceView):

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        persons = Person.objects.published()
        medias = Media.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            persons = persons.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events, persons, medias)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class DynamicContentHomeBodyView(Select2QuerySetSequenceView):

    paginate_by = settings.DAL_MAX_RESULTS

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()
        briefs = Brief.objects.all()
        medias = Media.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)
            briefs = briefs.filter(title__icontains=self.q)
            medias = medias.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, briefs, events, medias)

        if self.q:
            # This would apply the filter on all the querysets
            qs = qs.filter(title__icontains=self.q)

        # This will limit each queryset so that they show an equal number
        # of results.
        qs = self.mixup_querysets(qs)

        return qs


    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results


class DynamicContentHomeMediaView(Select2QuerySetSequenceView):

    def get_queryset(self):

        playlists = Playlist.objects.all()

        if self.q:
            playlists = playlists.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(playlists,)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)
        return qs


class NewsletterView(TemplateView):

    template_name = "pages/newsletter.html"


class DynamicContentPageView(Select2QuerySetSequenceView):

    def get_queryset(self):

        articles = Article.objects.all()
        custompage = CustomPage.objects.all()
        events = Event.objects.all()

        if self.q:
            articles = articles.filter(title__icontains=self.q)
            custompage = custompage.filter(title__icontains=self.q)
            events = events.filter(title__icontains=self.q)

        qs = autocomplete.QuerySetSequence(articles, custompage, events)

        if self.q:
            qs = qs.filter(title__icontains=self.q)

        qs = self.mixup_querysets(qs)

        return qs

    def get_results(self, context):
        results = autocomplete_result_formatting(self, context)
        return results
