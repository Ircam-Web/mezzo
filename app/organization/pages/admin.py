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

from django.contrib import admin
from modeltranslation.admin import TranslationTabularInline
from mezzanine.utils.static import static_lazy as static
from copy import deepcopy
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import Link as MezzanineLink
from organization.pages.models import *
from organization.pages.models import (
    DynamicContentHomeSlider,
    DynamicContentHomeBody,
    Home,
)
from organization.pages.forms import *
from organization.network.forms import *
from organization.network.models import PageCustomPersonListBlockInline
from organization.shop.models import *


class PageBlockInline(StackedDynamicInlineAdmin):

    model = PageBlock


class PageImageInline(TabularDynamicInlineAdmin):

    model = PageImage


class PagePlaylistInline(TabularDynamicInlineAdmin):

    model = PagePlaylist


class PageLinkInline(StackedDynamicInlineAdmin):

    model = PageLink


class LinkImageInline(StackedDynamicInlineAdmin):

    model = LinkImage


class LinkImageAdmin(LinkAdmin):

    inlines = [LinkImageInline,]


class PersonListBlockAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = PageCustomPersonListBlockInline
    exclude = ("title", "description")
    # form = PageCustomPersonListForm


class PageProductListInline(TabularDynamicInlineAdmin):

    model = PageProductList


class DynamicContentPageInline(TabularDynamicInlineAdmin):

    model = DynamicContentPage
    form = DynamicContentPageForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class PageRelatedTitleAdmin(TranslationTabularInline):

    model = PageRelatedTitle


class CustomPageAdmin(PageAdmin):

    inlines = [PageBlockInline,
            PageImageInline,
            PagePlaylistInline,
            PageLinkInline,
            PersonListBlockAutocompleteInlineAdmin,
            PageProductListInline,
            PageRelatedTitleAdmin,
            DynamicContentPageInline
            ]


class DynamicContentHomeSliderInline(TabularDynamicInlineAdmin):

    model = DynamicContentHomeSlider
    form = DynamicContentHomeSliderForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class DynamicContentHomeBodyInline(TabularDynamicInlineAdmin):

    model = DynamicContentHomeBody
    form = DynamicContentHomeBodyForm


class DynamicContentHomeMediaInline(TabularDynamicInlineAdmin):

    model = DynamicContentHomeMedia
    form = DynamicContentHomeMediaForm


class HomeImageInline(TabularDynamicInlineAdmin):

    model = HomeImage


class HomeAdminDisplayable(BaseTranslationModelAdmin):

    inlines = [ HomeImageInline,
                DynamicContentHomeSliderInline,
                DynamicContentHomeMediaInline,
                DynamicContentHomeBodyInline,
                ]


admin.site.register(CustomPage, CustomPageAdmin)
admin.site.register(Home, HomeAdminDisplayable)
admin.site.unregister(MezzanineLink)
admin.site.register(MezzanineLink, LinkImageAdmin)
