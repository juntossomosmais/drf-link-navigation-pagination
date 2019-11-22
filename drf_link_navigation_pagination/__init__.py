from typing import Optional
from urllib.parse import urlparse

from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


def _eval_str_as_boolean(value: str):
    return str(value).lower() in ("true", "1", "t", "y")


class LinkNavigationPagination(LimitOffsetPagination):
    header_change_domain = (
        settings.DRF_LNP_HEADER_CHANGE_DOMAIN_NAME
        if hasattr(settings, "DRF_LNP_HEADER_CHANGE_DOMAIN_NAME")
        else "X-Drf-Change-Domain"
    )
    use_https = _eval_str_as_boolean(settings.DRF_LNP_USE_HTTPS) if hasattr(settings, "DRF_LNP_USE_HTTPS") else True

    def get_paginated_response(self, data, *args, **kwargs):
        response_from_super = super().get_paginated_response(data)

        next_page = response_from_super.data["next"]
        previous_page = response_from_super.data["previous"]
        new_domain = self.request.headers.get(self.header_change_domain)

        if new_domain:
            response_from_super.data["next"] = _update_url_otherwise_none(next_page, new_domain, self.use_https)
            response_from_super.data["previous"] = _update_url_otherwise_none(previous_page, new_domain, self.use_https)

        return response_from_super


def _get_updated_url(url: str, domain: str, use_https: bool) -> str:
    parse_result = urlparse(url)
    # See more about _replace method here: https://docs.python.org/3/library/urllib.parse.html#url-parsing
    new_parse_result = parse_result._replace(netloc=domain, scheme="https" if use_https else "http")
    return new_parse_result.geturl()


def _update_url_otherwise_none(url: str, domain: str, use_https: bool) -> Optional[str]:
    return _get_updated_url(url, domain, use_https) if url else None
