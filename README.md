# General Spider

制作人: 张浩铭

参与者: 张浩铭

时间: 2018.07

版本号: v1.0

### 1: 使用环境要求

1.1: Python 3 所有版本 (Python 3.7不稳定 不推荐。推荐使用3.6以及之前的版本)

1.2: Scrapy 1.5.1(pip install scrapy) 此插件安装经常报错, 若无法安装请移步 https://pypi.org/project/Scrapy/ 下载后使用命令 pip install xxxx.whl

### 2: 使用方法

2.1: cd /genspider/genspider  (on bash)

2.2: python3 entry.py  (on bash) 运行此脚本会有操作提示，按照提示输入单个或多个网址即可爬取对应内容

### 3: 文件构造

3.1: /genspider

​     out.json        ->    输出文件（若不存在，在脚本运行时会默认生成，若存在，自动append）

​     scrapy.cfg      ->    scrapy配置文件，无需修改

​     使用说明.txt     ->    使用说明，即本文件

3.2: /genspider/genspider

​     __init__.py     ->    无需修改

​     entry.py        ->    爬虫启动脚本 使用方法见2.2

​     items.py        ->    爬虫field脚本，简而言之为爬虫爬取的内容暂时储存地

​     middlewares.py  ->    爬虫中间件，无需修改

​     pipelines.py    ->    pipeline 即输出相关，修改可以更改输出的类型等

​     rotateuseragent.py -> 更改用户代理脚本，无需修改

​     settings.py     ->    scrapy设置，可设置等待时间，是否遵循robots.txt等，具体参见scrapy官方文档

3.3: /genspider/genspider/spiders

​     __init__.py     ->    无需修改

​     genSpider.py    ->    爬虫本体，所有和爬虫相关的函数都在里面，切记返回items给pipelines，否则没输出

### 4: 完成情况

​     已经可以爬取大多数网页的新闻列表以及列表中第一页的所有信息。
​     需要完成的还有：

​	每个网站的翻页脚本或写法都大抵不相同，此爬虫无法做到翻页。

​	网站列表名(news_list_names)，网站内容列表名(news_content_list_names)并未涵盖所有情况或者不够智能，亟待更新。

​	无法爬取a标签中带换行的页面。

​	新闻具体内容中，有些网址的导航栏的结构也是 ul li 无法过滤，导致可能会有一些垃圾信息。

​	待续...