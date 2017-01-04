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

from organization.projects.models import *


@register(Project)
class ProjectTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(ProjectPlaylist)
class ProjectPlaylistTranslationOptions(TranslationOptions):

    pass


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):

    pass


@register(ProjectFile)
class ProjectFileTranslationOptions(TranslationOptions):

    pass


@register(ProjectBlock)
class ProjectBlockTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content')


@register(ProjectBlogPage)
class ProjectBlogPageTranslationOptions(TranslationOptions):

    fields = ('title', 'description', 'content', 'login_required_content')


@register(ProjectLink)
class ProjectLinkTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(ProjectProgram)
class ProjectProgramTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectProgramType)
class ProjectProgramTypeTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectTopic)
class ProjectTopicTranslationOptions(TranslationOptions):

    fields = ('name', 'description')


@register(ProjectTopicPage)
class ProjectTopicPageTranslationOptions(TranslationOptions):

    fields = ('sub_title',)


@register(ProjectDemo)
class ProjectDemoTranslationOptions(TranslationOptions):

    fields = ('title', 'description',)


@register(ProjectWorkPackage)
class ProjectWorkPackageTranslationOptions(TranslationOptions):

    pass


@register(ProjectRelatedTitle)
class ProjectRelatedTitleTranslationOptions(TranslationOptions):

    fields = ('title',)


@register(DynamicContentProject)
class DynamicContentProjectTranslationOptions(TranslationOptions):

    fields = ()
