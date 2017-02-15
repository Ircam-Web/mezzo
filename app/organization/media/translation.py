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

from modeltranslation.translator import translator, register, TranslationOptions

from organization.media.models import *


@register(Media)
class MediaTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(MediaTranscoded)
class MediaTranscodedTranslationOptions(TranslationOptions):

    fields = ()


@register(Playlist)
class PlaylistTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(PlaylistMedia)
class PlaylistMediaTranslationOptions(TranslationOptions):

    fields = ()


@register(MediaCategory)
class MediaCategoryTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(MediaImage)
class MediaImageTranslationOptions(TranslationOptions):

    fields = ()
