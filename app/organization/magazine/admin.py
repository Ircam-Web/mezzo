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
from django import forms
from copy import deepcopy
from modeltranslation.admin import TranslationTabularInline
from mezzanine.core.admin import *
from mezzanine.pages.admin import PageAdmin
from organization.magazine.models import *
from organization.magazine.forms import *


class ArticleImageInline(TabularDynamicInlineAdmin):

    model = ArticleImage


class ArticlePlaylistInline(TabularDynamicInlineAdmin):

    model = ArticlePlaylist


class ArticleAdmin(admin.ModelAdmin):

    model = Article


class ArticlePersonAutocompleteInlineAdmin(TabularDynamicInlineAdmin):

    model = ArticlePersonListBlockInline
    # form = ArticlePersonListForm
    exclude = ("title", "description")


class DynamicContentArticleInline(TabularDynamicInlineAdmin):

    model = DynamicContentArticle
    form = DynamicContentArticleForm

    class Media:
        js = (
            static("mezzanine/js/admin/dynamic_inline.js"),
        )


class ArticleRelatedTitleAdmin(TranslationTabularInline):

    model = ArticleRelatedTitle


class ArticleAdminDisplayable(DisplayableAdmin):

    fieldsets = deepcopy(ArticleAdmin.fieldsets)
    exclude = ('related_posts',)
    filter_horizontal = ['categories',]
    inlines = [ArticleImageInline,
              ArticlePersonAutocompleteInlineAdmin,
              ArticleRelatedTitleAdmin,
              DynamicContentArticleInline,
              ArticlePlaylistInline]


class BriefAdmin(admin.ModelAdmin): #OrderableTabularInline

    model = Brief


class BriefAdminDisplayable(BaseTranslationModelAdmin,): #, OrderableAdmin

    list_display = ('title', 'external_content', 'content_object', )
    form = BriefForm
    fieldsets = deepcopy(BriefAdmin.fieldsets)
    exclude = ("short_url", "keywords", "description", "slug", )


admin.site.register(Article, ArticleAdminDisplayable)
admin.site.register(Brief, BriefAdminDisplayable)
admin.site.register(Topic, PageAdmin)
