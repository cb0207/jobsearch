# jobsearch
scrapy框架多爬虫模式，爬取51job，拉钩，直聘，猎聘，大街，中华英才网


# 框架简介：
一个爬虫对应一个网站，以jobname变量传入搜索关键字。可以单独启动某个网站的搜索，也可以同时启动全部爬虫进行搜索。

特点：该项目会应用IP代理，redis+bloomfilter 进行去重爬取

# 控制台使用方法:
需要先启动ip代理池，redis数据库

1. scrapy crawl + 爬虫名 + 职位搜索： scrapy crawl job51 jobname='爬虫'
   使用对应爬虫对职位进行爬取

2. scrapy mycrawl + 职位搜索：scrapy mycrawl jobnamw='爬虫'
   使用所有爬虫，对职位进行爬取
   

# 配置settings：
设置中会出现'Amazing_SpiderMan.'的功能模块，属于一个我自己维护的一个爬虫帮助工具，会在另外的项目中进行详细介绍以及更新。

1. DOWNLOADER_MIDDLEWARES：下载中间件
    
    * IP代理设置：
      'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.IPProxy.IPProxyMiddleware': 125
    * UserAgent代理设置：
      'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.UserAgent.UserAgent': 1

2. ITEM_PIPELINES：数据储存件

   * mysql数据库，该插件使用ORM方式将数据入库：
      'Amazing_SpiderMan.myscrapy.pipelines.MysqlPipeline.MysqlPipeline': 300
   * 数据库对应相关设置：

      MYSQL_URI = 'localhost'
      
      MYSQL_PORT = 3306

      MYSQL_DATABASE = 'scrapy'

      MYSQL_TABLE = 'job'

      MYSQL_USER = 'root'

      MYSQL_PASS = '10ily1314'
      
3. Redis + bloomfilter: 去重列队

   SCHEDULER = 'Amazing_SpiderMan.myscrapy.scrapy_redis.scheduler.Scheduler'
   
   SCHEDULER_QUEUE_CLASS = 'Amazing_SpiderMan.myscrapy.scrapy_redis.queue.SpiderPriorityQueue'

   SCHEDULER_PERSIST = True
   
   REDIS_HOST = '127.0.0.1'
   
   REDIS_PORT = 6379

   FILTER_URL = None
   
   FILTER_HOST = 'localhost'
   
   FILTER_PORT = 6379
   
   FILTER_DB = 0
