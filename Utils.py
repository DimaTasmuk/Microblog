# -*- coding: UTF-8 -*-
import math

from mongoengine import QuerySet

from app import app


class Pagination(object):

    def __init__(self, items, page) -> None:
        super().__init__()
        self.items = items
        self.page_size = app.config['POSTS_PER_PAGE']
        self.page = page

        if isinstance(items, QuerySet):
            self.total = items.count()
        else:
            self.total = len(items)

    @property
    def pages(self):
        return int(math.ceil(self.total / float(self.page_size)))

    def has_next(self):
        return self.page < self.pages

    def has_prev(self):
        return self.page > 1

    def next_num(self):
        return self.page + 1

    def prev_num(self):
        return self.page - 1

    def paginate(self):
        skips = self.page_size * (self.page - 1)
        return self.items.skip(skips).limit(self.page_size)
