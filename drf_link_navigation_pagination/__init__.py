import logging
from pathlib import PurePosixPath
from urllib.parse import unquote
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
    header_number_of_overlap_paths = (
        settings.DRF_LNP_HEADER_NUMBER_OF_OVERLAP_PATHS
        if hasattr(settings, "DRF_LNP_HEADER_NUMBER_OF_OVERLAP_PATHS")
        else "X-Drf-Number-Overlap-Paths"
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
        number_of_overlap_paths = self.request.headers.get(self.header_number_of_overlap_paths)
        number_of_overlap_paths = (
            int(number_of_overlap_paths) if number_of_overlap_paths and str(number_of_overlap_paths).isdigit() else None
        )

        if force_https:
            logger.debug("Forcing HTTPS")
            next_page = _set_https(next_page) if next_page else None
            previous_page = _set_https(previous_page) if previous_page else None
        if new_domain:
            logger.debug("New domain")
            next_page = _get_updated_url(next_page, new_domain) if next_page else None
            previous_page = _get_updated_url(previous_page, new_domain) if previous_page else None
        if number_of_overlap_paths:
            logger.debug("Overlapping paths")
            previous_page = _overlap_path(previous_page, number_of_overlap_paths) if previous_page else None
            next_page = _overlap_path(next_page, number_of_overlap_paths) if next_page else None
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


def _overlap_path(url: str, number_of_overlaps: int) -> str:
    parse_result = urlparse(url)
    path_as_posix = PurePosixPath(unquote(urlparse(url).path))
    if len(path_as_posix.parts) > 1:
        number_of_overlaps += 1
        new_parts = path_as_posix.parts[number_of_overlaps:]
        if len(new_parts) == 0:
            final_path = path_as_posix.parts[0]
        else:
            final_path = path_as_posix.parts[0] + "/".join(new_parts) + path_as_posix.parts[0]
        new_parse_result = parse_result._replace(path=final_path)
        return new_parse_result.geturl()
    return parse_result.geturl()


def _urljoin(*args):
    return "/".join(map(lambda x: str(x).rstrip("/").lstrip("/"), args))
