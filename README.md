# MyselfObjects
# 个人网站

## 各模块功能：
### CRM:
- 实现了不同角色管理，不同的角色有不同的权限，每个角色可以做的事情可以动态配置
- 细致的权限管理，可以将权限控制到是否允许一个按键可以点击的级别
- 实现了动态菜单管理，用户页面上显示的菜单都是动态生成的
- 自己重写了大部分django admin,几乎可以实现django admin所有功能，且很多地方做了优化
注：此项目依然在开发中，必然还有很多bug,会陆续添加新的功能。

### 图片模块：
- 实现爬取某一网站的全部图片（参考项目：Scrapy-PIC）
- 实现了不用类别的图片分开展示
- 同一类别的图片展示缩略图
- 图片详细界面实现滚动播放原始图片

###视频模块：
-同样实现视频的分类处理
-实现爬取某一网站的视频文件

##基本使用
###requirements
-python3.7+
-django 2.1+
###使用
-python manage.py runserver 0.0.0.0:8000
username: czk@126.com password: meiyoumima


###使用中的bug可加此群汇报 qq: python开发交流群 255012808

##以下为一些项目截图

####项目入口

image

####客户页面及在kingadmin里的配置

image

####学员注册页

image

####kingadmin配置页

image
