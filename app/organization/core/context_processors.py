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

from django.conf import settings # import the settings file
from datetime import datetime, date
from organization.pages.models import Page
from organization.network.models import Organization, OrganizationLinkedInline

def settings(request):
    date_now = datetime.now()
    # SEASON
    current_season = int(date_now.year) - 1 if datetime(date_now.year, 1,1) <= date_now and date_now <= datetime(date_now.year, 7, 31) else date_now.year
    current_season_styled = str(current_season)[-2:]+"."+str(current_season+1)[-2:]

    # NEWSLETTER
    newsletter_page = Page.objects.filter(slug="newsletter")
    newsletter_subscribing_url = ""
    if newsletter_page:
        newsletter_subscribing_url = newsletter_page.first().get_absolute_url()

    # HOST ORGANIZATIONS
    host_org = Organization.objects.filter(is_host=True).first()
    organization_lists = []

    for orga_linked_block in host_org.organization_linked_block.all():
        organizations = []
        for orga_list in OrganizationLinkedInline.objects.filter(organization_list_id=orga_linked_block.organization_linked_id):
            organizations.append(orga_list.organization)
        organization_lists.append(organizations)

    linked_org_content = organization_lists[0] if len(organization_lists) > 0 else None
    linked_org_footer = organization_lists[1] if len(organization_lists) > 1 else None
    linked_org_footer_2 = organization_lists[2] if len(organization_lists) > 2 else None

    research_slug = "recherche"

    return {'current_season': current_season,
            'current_season_styled': current_season_styled,
            'newsletter_subscribing_url': newsletter_subscribing_url,
            'host_organization': host_org,
            'linked_organization_content' : linked_org_content,
            'linked_organization_footer' : linked_org_footer,
            'linked_organization_footer_2' : linked_org_footer_2,
            'research_slug' : research_slug
            }
