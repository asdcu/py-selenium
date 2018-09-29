#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : page
# @Author   : asd
# @Date     : 2018-09-13 17:34
import math
import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageDraw, ImageFont


class Page(object):
    browser_name = 'chrome'

    def __init__(self, selenium_server=None, max_size=False, **kwargs):
        self.size = kwargs.get('size', (1920, 1080))  # resize window
        browser = getattr(DesiredCapabilities, self.browser_name.upper(), DesiredCapabilities.CHROME)
        if selenium_server:
            self.driver = webdriver.Remote(command_executor=selenium_server, desired_capabilities=browser)
        else:
            self.driver = webdriver.Chrome()
        self.driver.set_window_size(self.size[0], self.size[1])
        if max_size:
            self.driver.maximize_window()

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, item):
        return getattr(self, item, None)

    @property
    def sid(self):
        """get unique session id"""
        return self.driver.session_id

    @property
    def title(self):
        """get current title"""
        return self.driver.title

    @property
    def current_window(self):
        """get current window handle"""
        return self.driver.current_window_handle

    @property
    def current_url(self):
        """get current href"""
        return self.driver.current_url

    @property
    def page_source(self):
        """get page source"""
        return self.driver.page_source

    @property
    def cookies(self):
        """get the browser cookie"""
        return self.driver.get_cookies()

    def clean_cookies(self):
        """clear browser cookie"""
        self.driver.delete_all_cookies()

    def add_cookies(self, cookies, domain=None):
        """add cookie,selenium need to get new page before set cookie,
        because this action is related to the cookie domain"""
        if type(cookies) is list:
            for c in cookies:
                if "name" in c and "value" in c:
                    domain = domain if domain else c.get('domain', None)
                    if domain:
                        self.driver.add_cookie(
                            {'name': c["name"], 'value': c["value"], 'domain': domain})
                    else:
                        self.driver.add_cookie(
                            {'name': c["name"], 'value': c["value"]})
        elif type(cookies) is dict:
            for k, v in cookies.items():
                if domain:
                    self.driver.add_cookie(
                        {'name': k, 'value': v, 'domain': domain})
                else:
                    self.driver.add_cookie(
                        {'name': k, 'value': v})
        elif type(cookies) is str:
            for c in cookies.split("; "):
                if domain:
                    self.driver.add_cookie(
                        {'name': c.split('=')[0], 'value': c.split('=')[1], 'domain': domain})
                else:
                    self.driver.add_cookie(
                        {'name': c.split('=')[0], 'value': c.split('=')[1]})

    def window(self, partial_url='', partial_title=''):
        """
        switch window，if window's num <=2,no parameters required，
        switch to the outside window.If window's num >2,parameters required
        :param partial_url:
        :param partial_title:
        :return:
        """
        all_windows = self.driver.window_handles
        if len(all_windows) == 1:
            self.driver.switch_to.window(all_windows[-1])
        elif len(all_windows) == 2:
            other_window = all_windows[1 - all_windows.index(self.current_window)]
            self.driver.switch_to.window(other_window)
        else:
            for window in all_windows:
                self.driver.switch_to.window(window)
                if partial_url in self.driver.current_window_handle or partial_title in self.driver.title:
                    break

    def open(self, url):
        """create a new browser window"""
        self.driver.get(url)

    def new_tab(self, url):
        """create a new tab window"""
        js = "window.open('%s')" % url
        self.driver.execute_script(js)
        # switch to the last on window
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self.driver.current_window_handle

    def refresh(self):
        """browser refresh"""
        self.refresh()

    def back(self):
        """action back"""
        self.driver.back()

    def forward(self):
        """action forward"""
        self.driver.forward()

    def close(self):
        """close, it's same to the quit when window's num is just one"""
        self.driver.close()

    def quit(self):
        """quit browser"""
        self.driver.quit()

    @staticmethod
    def wait(second=1):
        """sleeping, default 1 second"""
        time.sleep(second)

    def alert(self, action=1):
        """dismiss pop-up windows"""
        try:
            if action == 1:
                self.driver.switch_to.alert().accept()
            else:
                self.driver.switch_to.alert().dismiss()
        except NoAlertPresentException:
            pass

    def no_alert_or_click_alert(self):
        """
        capture whether the browser has a pop-up window,if there is a pop-up window and click to confirm,
        it is usually used when you login without using cookie that you are not logged in.
        :return:
        """
        ret = False
        try:
            self.driver.switch_to.alert().accept()
            ret = True
        except NoAlertPresentException:
            pass
        finally:
            return ret

    def frame(self, id_or_name=None):
        """
        switch frame
        :param id_or_name: switch back to the default frame if it is none
        :return:
        """
        if id_or_name == 0 or id_or_name:
            self.driver.switch_to.frame(id_or_name)
        else:
            self.driver.switch_to.default_content()

    def script(self, src):
        """
        execute javascript
        :param src: injection javascript code
        :return:
        """
        return self.driver.execute_script(src)

    def click(self, selector):
        el = self.find_element(selector)
        el.click()  # forced click error when could not be found
        self.wait()

    def find_element(self, selector, timeout=3):
        """
        element positioning method and content list
        supported function：id, xpath, class_name, css_selector, link_text, name, partial_link_text, tag_name
        :param selector:
        >> loc = ('id', 'su')
        >> page.find_element(loc)
        :param timeout
        :return: element or None
        """
        try:
            WebDriverWait(self.driver, timeout, 0.5).until(
                EC.presence_of_element_located(selector)
            )
            element = self.driver.find_element(by=selector[0], value=selector[1])
            return element
        except NoSuchElementException as e:
            return None
        except TimeoutException as e:
            return None

    def find_elements(self, selector, timeout=3):
        """
        element positioning method and content list
        supported function：id, xpath, class_name, css_selector, link_text, name, partial_link_text, tag_name
        :param selector:
        >> loc = ('id', 'su')
        >> page.find_element(loc)
        :param timeout
        :return: element or None
        """
        try:
            WebDriverWait(self.driver, timeout, 0.5).until(
                EC.presence_of_element_located(selector)
            )
            elements = self.driver.find_elements(by=selector[0], value=selector[1])
            return elements
        except NoSuchElementException as e:
            return None
        except TimeoutException as e:
            return None

    def send(self, selector, value=""):
        """
        enter text, clear the text box and then enter again
        :param selector:
        :param value:
        :return:
        """
        el = self.find_elements(selector)
        el.clear()
        el.send_keys(value)

    def screen_shot(self, selector=None, path='./screenshots', name='test', before=None):
        """
        screen_shot
        :param selector: element selector
        :param path: screenShot file saved path
        :param name: screenShot file's name
        :param before: preamble function before screen shot
        :return:
        """
        if not os.path.exists(path):
            # recursive created
            os.makedirs(path)
        file = os.path.join(path, str(name) + ".png")
        if before and type(before) is function:
            before()
        # screen shot
        if selector:
            # screen shot specified element
            WebDriverWait(self.driver, 5).until(lambda x: x.find_element(by=selector[0], value=selector[1]))
            el = self.driver.find_element(by=selector[0], value=selector[1])
            self.driver.get_screenshot_as_file(file)
            left = el.location['x']
            top = el.location['y']
            right = el.location['x'] + el.size['width']
            bottom = el.location['y'] + el.size['height']
            img = Image.open(file)
            img = img.crop((left, top, right, bottom))
            if len(img.split()) == 4:
                r, g, b, a = img.split()
                img = Image.merge("RGB", (r, g, b))
            img.save(file)
        else:
            # screen shot full screen
            self.driver.get_screenshot_as_file(file)
        return file

    def screen_shot_with_watermark(self, path='./screenshots', name="test", before=None, gap=(20, 20),
                                   color=(155, 155, 155, 180)):
        if not os.path.exists(path):
            os.makedirs(path)
        file = os.path.join(path, str(name) + ".png")
        if before and type(before) is function:
            before()
        self.driver.get_screenshot_as_file(file)
        img = Image.open(file)
        # add watermark
        font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SIMHEI.TTF'), 20)
        img_with_watermark = self._add_text_to_image(img,
                                                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                     font=font, gap=gap, color=color)
        img_with_watermark.save(file)
        return file

    @staticmethod
    def _add_text_to_image(image, text, font=None, gap=(20, 20), color=(155, 155, 155, 180)):
        """
        add watermark into image
        :param image: pillow image
        :param text:
        :param font:
        :param gap:
        :param color:
        :return:
        """
        rgba_image = image.convert("RGBA")
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        text_size_x, text_size_y = image_draw.textsize(text, font=font)
        # set text position
        text_xy = (rgba_image.size[0] - text_size_x - gap[0], rgba_image.size[1] - text_size_y - gap[1])
        # set text color and alpha
        image_draw.text(text_xy, text, font=font, fill=color)
        image_draw_text = Image.alpha_composite(rgba_image, text_overlay)
        return image_draw_text

    def scroll_screen_shot(self, path, name, top=0, bottom=0, with_watermark=True, gap=(20, 20),
                           color=(155, 155, 155, 180)):
        """
        scroll screen shot with water mark or not
        :param path:
        :param name:
        :param top:
        :param bottom:
        :param with_watermark:
        :param gap:
        :param color:
        :return:
        """
        # get dom actual height
        dom_height = self.script("return Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);")
        # get visual window height
        client_height = self.script("""
            return (function getClientHeight(){     
                var clientHeight=0;     
                if(document.body.clientHeight&&document.documentElement.clientHeight){     
                    var clientHeight=(document.body.clientHeight<document.documentElement.clientHeight)?document.body.
                    clientHeight:document.documentElement.clientHeight;             
                }else{     
                    var clientHeight=(document.body.clientHeight>document.documentElement.clientHeight)?document.body.
                    clientHeight:document.documentElement.clientHeight;         
                }     
                return clientHeight;     
            })();
        """)
        # calculate how much scrolling pic
        num = math.ceil(dom_height / client_height)
        # location to store scroll temporary files
        if not os.path.exists(os.path.join('/tmp', 'scroll_tmp')):
            os.makedirs(os.path.join('/tmp', 'scroll_tmp'))
        files, ims = [], []
        # pseudo random, maybe unique under multi-threading environment circumstances
        now = str(int(time.time())) + str(random.random())[2:8]
        last_height = 0
        if num == 1:
            if with_watermark:
                return self.screen_shot_with_watermark(path, name=name, gap=gap, color=color)
            else:
                return self.screen_shot(path=path, name=name)
        else:
            for i in range(num):
                if i != num - 1:
                    # the last pic
                    self.script("document.documentElement.scrollTop={}".format(
                        i * (float(client_height) - float(top) - float(bottom))))
                else:
                    self.script("document.documentElement.scrollTop={}".format(dom_height))
                    last_height = dom_height - 2 * float(top) - i * (float(client_height) - float(top) - float(bottom))
                self.wait(1)
                file_tmp = now + "_{i}x{h}".format(i=i, h=client_height)
                file = self.screen_shot(path=os.path.join('/tmp', 'scroll_tmp'), name=file_tmp)
                files.append(file)
                ims.append(Image.open(file))
        # merge
        current_height = 0
        res = Image.new(ims[0].mode, (ims[0].size[0], dom_height - (num - 1) * (top + bottom)))
        for key, value in enumerate(ims):
            if key == 0:
                value = value.crop((0, 0, value.size[0], value.size[1] - bottom))
                if len(value.split()) == 4:
                    r, g, b, a = value.split()
                    value = Image.merge("RGB", (r, g, b))
                res.paste(value, box=(0, 0))
                current_height = value.size[1] - bottom
            elif key == len(ims) - 1:
                value = value.crop((0, value.size[1] - last_height, value.size[0], value.size[1]))
                if len(value.split()) == 4:
                    r, g, b, a = value.split()
                    value = Image.merge("RGB", (r, g, b))
                res.paste(value, box=(0, current_height))
            else:
                value = value.crop((0, top, value.size[0], value.size[1] - bottom))
                if len(value.split()) == 4:
                    r, g, b, a = value.split()
                    value = Image.merge("RGB", (r, g, b))
                res.paste(value, box=(0, current_height))
                current_height += value.size[1] - top - bottom

        if not os.path.exists(path):
            os.makedirs(path)

        # add watermark or not
        if with_watermark:
            font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SIMHEI.TTF'), 20)
            img_with_watermark = self._add_text_to_image(res,
                                                         time.strftime("%Y-%m-%d %H:%M:%S",
                                                                       time.localtime(time.time())),
                                                         font=font, gap=gap, color=color)
            img_with_watermark.save(os.path.join(path, name + ".png"))
        else:
            res.save(os.path.join(path, name + ".png"))

        # delete temporary file
        for item in files:
            os.remove(item)

        return os.path.join(path, name + ".png")
