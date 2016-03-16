#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app.helper import BaseRequestHandler
from app.libs import router


@router.Route('/')
class IndexHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")