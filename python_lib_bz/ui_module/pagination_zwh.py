#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math
import urlparse
import urllib

from ui_module import my_ui_module


def update_querystring(url, **kwargs):
    base_url = urlparse.urlsplit(url)
    query_args = urlparse.parse_qs(base_url.query)
    query_args.update(kwargs)
    for arg_name, arg_value in kwargs.iteritems():
        if arg_value is None:
            if arg_name in query_args:
                del query_args[arg_name]

    query_string = urllib.urlencode(query_args, True)
    return urlparse.urlunsplit((base_url.scheme, base_url.netloc,
                                base_url.path, query_string, base_url.fragment))


class pagination_zwh(my_ui_module.HtmlUIModule):

    def render(self, page, page_size, results_count):
        pages = int(math.ceil(results_count / page_size)) if results_count else 0

        def get_page_url(page):
            if page < 1:
                page = None
            return update_querystring(self.request.uri, page=page)

        next = page + 1 if page < pages else None
        previous = page - 1 if page > 1 else None

        def iter_pages(left_edge=2, left_current=2, right_current=5, right_edge=2):
            last = 0
            for num in xrange(1, pages + 1):
                if num <= left_edge or \
                   (num > page - left_current - 1 and
                    num < page + right_current) or \
                   num > pages - right_edge:
                    if last + 1 != num:
                        yield None
                    yield num
                    last = num

        return self.render_string('pagination_zwh.html', page=page, pages=pages, next=next,
                                  previous=previous, get_page_url=get_page_url, iter_pages=iter_pages)
