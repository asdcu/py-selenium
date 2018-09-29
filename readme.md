# 基于python封装的selenium操作

包含

- 页面相关属性
- 窗口、iframe、tab相关操作
- 截图、滚动截图
- cookie
- 元素查找、点击

demo

```
p = Page()
```

- 打开页面

```
p.open("https://sspai.com/post/26536")
```

- 退出

```
p.quit()  # 在发生异常时,捕获并退出浏览器
```

- 获取网页标题

```
print(p.title)
```

- cookie操作

```
# 获取cookie
print(page.cookies)

# 使用cookie打开页面
page.open(login_url)  # 登录的url
page.del_cookies()
page.add_cookies(cookies=cookie)
page.open(home_url)
```

- 元素查找、点击、输入

```
page.find_element(selector=('xpath','//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/span'))

page.find_elements(selector=('xpath','//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/span'))

page.click(selector=('xpath','//*[@id="app"]/div[2]/div[2]/div[2]/div[1]/span'))

page.send(password_selector, '123456')
```

- 截图

```
# 保存路径为当前路径
path = os.path.abspath(os.path.dirname(__file__))
p.screen_shot(path=path, name='test')
```

- 滚动截图

```
p.open("https://lvwenhan.com/laravel/432.html")
p.wait(2)
p.scroll_screen_shot(path=path, name='test3', color=(211, 0, 34))
```

![普通截图](http://oxp2ww2bs.bkt.clouddn.com/test.png)
![带水印截图](http://oxp2ww2bs.bkt.clouddn.com/test2.png)
![滚动截图](http://oxp2ww2bs.bkt.clouddn.com/test3.png)

