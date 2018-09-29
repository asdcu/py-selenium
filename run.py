#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : run
# @Author   : asd
# @Date     : 2018-09-13 17:29
import os

from lib.page import Page

path = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    p = Page()
    p.open("https://lvwenhan.com/laravel/432.html")
    p.wait(2)
    p.scroll_screen_shot(path=path, name='test3', color=(211, 0, 34))
    p.quit()
