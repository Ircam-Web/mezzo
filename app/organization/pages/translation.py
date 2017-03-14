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
from mezzanine.pages.models import Page, RichText
from mezzanine.pages.translation import TranslatedRichText
from organization.pages.models import *


@register(Home)
class HomeTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentHomeSlider)
class DynamicContentHomeSliderTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentHomeBody)
class DynamicContentHomeBodyTranslationOptions(TranslationOptions):

    pass


@register(DynamicContentHomeMedia)
class DynamicContentHomeMediaTranslationOptions(TranslationOptions):

    pass


@register(CustomPage)
class CustomPageTranslationOptions(TranslationOptions):

    fields = ('sub_title', 'content')


@register(PageBlock)
class PageBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(PageImage)
class PageImageTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(PagePlaylist)
class PagePlaylistTranslationOptions(TranslationOptions):

    pass


@register(PageLink)
class PageLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(DynamicContentPage)
class DynamicContentPageTranslationOptions(TranslationOptions):

    pass


@register(LinkImage)
class LinkImageTranslationOptions(TranslationOptions):

    pass


@register(PageRelatedTitle)
class PageRelatedTitleTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(HomeImage)
class HomeImageTranslationOptions(TranslationOptions):

    fields = ()
