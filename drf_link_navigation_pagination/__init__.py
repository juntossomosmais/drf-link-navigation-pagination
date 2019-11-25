import logging
from urllib.parse import urlparse

from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination

logger = logging.getLogger("drf_link_navigation_pagination")


def _eval_str_as_boolean(value: str):
    return str(value).lower() in ("true", "1", "t", "y")


class LinkNavigationPagination(LimitOffsetPagination):
    header_change_domain = (
        settings.DRF_LNP_HEADER_CHANGE_DOMAIN_NAME
        if hasattr(settings, "DRF_LNP_HEADER_CHANGE_DOMAIN_NAME")
        else "X-Drf-Change-Domain"
    )
    header_add_request_path = (
        settings.DRF_LNP_HEADER_ADD_REQUEST
        if hasattr(settings, "DRF_LNP_HEADER_ADD_REQUEST")
        else "X-Drf-Add-Request-Path"
    )
    header_use_https = (
        settings.DRF_LNP_HEADER_USE_HTTPS if hasattr(settings, "DRF_LNP_HEADER_FORCE_HTTPS") else "X-Drf-Force-Https"
    )

    def get_paginated_response(self, data, *args, **kwargs):
        logger.debug("Getting answer from super")
        response_from_super = super().get_paginated_response(data)

        next_page = response_from_super.data["next"]
        previous_page = response_from_super.data["previous"]
        new_domain = self.request.headers.get(self.header_change_domain)
        request_path = self.request.headers.get(self.header_add_request_path)
        force_https = self.request.headers.get(self.header_use_https)
        force_https = _eval_str_as_boolean(force_https) if force_https is not None else False

        if force_https:
            logger.debug("Forcing HTTPS")
            next_page = _set_https(next_page) if next_page else None
            previous_page = _set_https(previous_page) if previous_page else None
        if new_domain:
            logger.debug("New domain")
            next_page = _get_updated_url(next_page, new_domain) if next_page else None
            previous_page = _get_updated_url(previous_page, new_domain) if previous_page else None
        if request_path:
            logger.debug("Adding request path")
            next_page = _add_request_path(next_page, request_path) if next_page else None
            previous_page = _add_request_path(previous_page, request_path) if previous_page else None

        response_from_super.data["next"] = next_page
        response_from_super.data["previous"] = previous_page

        return response_from_super


def _set_https(url: str) -> str:
    parse_result = urlparse(url)
    new_parse_result = parse_result._replace(scheme="https")
    return new_parse_result.geturl()


def _get_updated_url(url: str, domain: str) -> str:
    parse_result = urlparse(url)
    new_parse_result = parse_result._replace(netloc=domain)
    return new_parse_result.geturl()


def _add_request_path(url: str, request_path: str) -> str:
    parse_result = urlparse(url)
    final_path = _urljoin(request_path, parse_result.path)
    new_parse_result = parse_result._replace(path=final_path)
    return new_parse_result.geturl()


def _urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip("/").lstrip("/"), args))
