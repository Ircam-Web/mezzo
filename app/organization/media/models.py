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

from pyquery import PyQuery as pq

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.managers import SearchableManager
from mezzanine.core.models import RichText, Displayable, Slugged
from mezzanine.core.fields import RichTextField, OrderField, FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from organization.core.models import *
from mezzanine_agenda.models import Event
from django.conf import settings
import requests


MEDIA_BASE_URL = getattr(settings, 'MEDIA_BASE_URL', 'http://medias.ircam.fr/embed/media/')

PLAYLIST_TYPE_CHOICES = [
    ('audio', _('audio')),
    ('video', _('video')),
]

class Media(Displayable):
    """Media"""

    external_id = models.CharField(_('media id'), max_length=128)
    poster_url = models.URLField(_('poster'), max_length=1024, blank=True)
    category = models.ForeignKey('MediaCategory', verbose_name=_('category'), related_name='medias', blank=True, null=True, on_delete=models.SET_NULL)

    # objects = SearchableManager()
    # search_fields = ("title",)

    class Meta:
        verbose_name = "media"
        verbose_name_plural = "medias"
        ordering = ('created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("organization-media-detail", kwargs={"type": self.type, "slug": self.slug})

    @property
    def uri(self):
        return MEDIA_BASE_URL + self.external_id

    def get_html(self):
        r = requests.get(self.uri)
        return r.content

    @property
    def type(self):
        for transcoded in self.transcoded.all():
            if 'video' in transcoded.mime_type:
                return 'video'
            if 'audio' in transcoded.mime_type:
                return 'audio'


def create_media(instance, created, raw, **kwargs):
    # Ignore fixtures and saves for existing courses.

    if not created or raw:
        return

    q = pq(instance.get_html())
    sources = q('source')

    video = q('video')
    if len(video):
        if 'poster' in video[0].attrib.keys():
            instance.poster_url = video[0].attrib['poster']

    for source in sources:
        mime_type = source.attrib['type']
        transcoded = MediaTranscoded(media=instance, mime_type=mime_type)
        transcoded.url = source.attrib['src']
        transcoded.save()

    instance.save()

models.signals.post_save.connect(create_media, sender=Media, dispatch_uid='create_media')


class MediaTranscoded(models.Model):

    media = models.ForeignKey('Media', verbose_name=_('media'), related_name='transcoded')
    file = FileField(_("file"), max_length=1024, upload_to="uploads/media/", blank=True, null=True)
    url = models.URLField(_('URL'), max_length=1024, blank=True)
    mime_type = models.CharField(_('mime type'), max_length=64)

    preferred_mime_type = ['video/webm', 'audio/ogg']

    class Meta:
        verbose_name = "media file"
        verbose_name_plural = "media files"

    def __str__(self):
        return self.url


class MediaImage(Image):

    media = models.ForeignKey(Media, verbose_name=_('media'), related_name='images', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
        order_with_respect_to = "media"


class MediaCategory(Slugged, Description):
    """Media Category"""

    class Meta:
        verbose_name = _('media category')
        verbose_name_plural = _('media categories')

    def count(self):
        return self.medias.published().count()+1


class Playlist(Displayable):
    """Playlist"""

    type = models.CharField(_('type'), max_length=32, choices=PLAYLIST_TYPE_CHOICES)

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlists')

    def __str__(self):
        return ' '.join((self.title, '(' + self.type + ')'))

    def get_absolute_url(self):
        return reverse("organization-playlist-detail", kwargs={"slug": self.slug})


class PlaylistMedia(models.Model):
    """Playlist media"""

    playlist = models.ForeignKey(Playlist, verbose_name=_('playlist'), related_name='medias', blank=True, null=True, on_delete=models.SET_NULL)
    media = models.ForeignKey(Media, verbose_name=_('media'), related_name='playlists', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('media')
        verbose_name_plural = _('medias')


class PlaylistRelated(models.Model):
    """Playlist inline"""

    playlist = models.ForeignKey(Playlist, verbose_name=_('playlist'), related_name='playlist_related', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('playlist')
        verbose_name_plural = _('playlists')
