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

from copy import deepcopy
from django.contrib import admin
from mezzanine.core.admin import *
from organization.media.models import *
from organization.media.forms import *


class MediaTranscodedAdmin(TabularDynamicInlineAdmin):

    model = MediaTranscoded


class MediaImageInline(TabularDynamicInlineAdmin):

    model = MediaImage

    
class MediaAdmin(BaseTranslationModelAdmin):

    model = Media
    inlines = (MediaTranscodedAdmin, MediaImageInline)
    list_display = ['title',]


class PlaylistMediaInline(TabularDynamicInlineAdmin):

    model = PlaylistMedia
    form = PlaylistMediaForm


class PlaylistAdmin(BaseTranslationModelAdmin):

    model = Playlist
    inlines = (PlaylistMediaInline,)


class MediaCategoryAdmin(BaseTranslationModelAdmin):

    model = MediaCategory






admin.site.register(Media, MediaAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)
