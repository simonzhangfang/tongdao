#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'ghost'

import tornado.web
from app.helper import BaseTemplateRequestHandler, has_pet_cache, set_pet_cache, BaseApiRequestHandler
from app.libs import router
from app.models.home import Pet
from settings import logger


@router.Route('/home')
class HomeHandler(BaseTemplateRequestHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        uid = self.session['uid']
        # 如果尚未领取,重定向领取列表
        if not has_pet_cache(uid) and not Pet.findone(uid=uid):
            return self.redirect('/pets')

        # 设置领养的缓存
        set_pet_cache(uid)
        # 获取领取用户信息
        pet_info = Pet.get_info(uid)
        if not pet_info:
            return  self.redirect('/pets')
        self.render('home.html', pet_info=pet_info)


@router.Route('/pets')
class BabiesHandler(BaseTemplateRequestHandler):
    """
    领养列表
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # 渲染列表页面
        self.render("pets.html")


@router.Route('/pet/?P<ptype>.*')
class BabiesHandler(BaseTemplateRequestHandler):
    """
    领养接口,领养成功重定向个人页
    """
    @tornado.web.authenticated
    def get(self, ptype):

        uid = self.session['uid']
        # 如果领取了,重定向个人页
        if has_pet_cache(uid) or Pet.findone(uid=uid):
            return self.redirect('/home')

        # 领养
        pet = Pet(type=ptype, uid=uid)
        try:
            row = pet.insert()
            logger.info('insert pet success {}'.format(row))
            set_pet_cache(uid)
        except Exception, e:
            self.set_status(500)
            logger.error('insert pet error {}'.format(e))
            return self.redirect('/pets')
        self.redirect('/home')

@router.Route('/api/v1/keep')
class KeepHandler(BaseApiRequestHandler):

    @tornado.web.authenticated
    def get(self, type):
        type_ = self.get_argument('type_', None)
        if not type_:
            return self.render('/error')


