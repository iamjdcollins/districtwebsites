from django.http.response import HttpResponseRedirectBase
from django.utils.deprecation import MiddlewareMixin

from ..models import Site


class CurrentSite(MiddlewareMixin):
    """
    Middleware that sets `site` attribute to request object. If the domain is
    not the canonical domain for the site a redirect will happen.
    """

    def process_request(self, request):
        request.site = Site.objects.get_current(request)
        if request.site.__class__.__base__ == HttpResponseRedirectBase:
            return request.site
