# -*- coding: utf-8 -*-

# Scrapy settings for jobsearch project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jobsearch'
COMMANDS_MODULE='jobsearch.mycmd'

SPIDER_MODULES = ['jobsearch.spiders']
NEWSPIDER_MODULE = 'jobsearch.spiders'

# BloomFilter
# DUPEFILTER_CLASS = 'jobsearch.middlewares.URLBloomFilter'


# 使用scrapy_redis的调度器
SCHEDULER = "Amazing_SpiderMan.myscrapy.scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_CLASS = 'Amazing_SpiderMan.myscrapy.scrapy_redis.queue.SpiderPriorityQueue'


# 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
SCHEDULER_PERSIST = True
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
# # 去重队列的信息
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0

REDIRECT_ENABLED = False

# HTTPERROR_ALLOWED_CODES = [302, 403, 429]

RETRY_TIMES = 20

RETRY_HTTP_CODES = [403, 429, 302, 301]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 7
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False
COOKIES_DEBUG = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'jobsearch.middlewares.JobsearchSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'jobsearch.middlewares.JobsearchDownloaderMiddleware': 543,
    # 'jobsearch.middlewares.JobseaerchIPProxy': 125,
    'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.IPProxy.IPProxyMiddleware': 125,
    'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.UserAgent.UserAgent': 1,
}
IPPROXY_ENABLED = True

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#     # 'Amazing_SpiderMan.myscrapy.extensions.StatsInflux.StatsInfluxdb': 300,
#     # 'scrapy.extensions.telnet.TelnetConsole': 0,
# }

# Configure extensions
# InfluxDB Setting
# INFLUX_ENABLED = True
# INFLUX_NAME = 'scrapy'



# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'jobsearch.pipelines.JobSearchMysqlPipeline': 301,
   #  'Amazing_SpiderMan.myscrapy.pipelines.MongoPipeline.MongoPipeline': 300,
      'Amazing_SpiderMan.myscrapy.pipelines.MysqlPipeline.MysqlPipeline': 300,
   #  'jobsearch.pipelines.JobSearchMongoPipeline': 300,
   #  'scrapy_redis.pipelines.RedisPipeline': 300,
}
# MYSQL host
MYSQL_URI = 'localhost'
MYSQL_PORT = 3306
#
# # MYSQL database
MYSQL_DATABASE = 'scrapy'
#
# # MYSQL table
MYSQL_TABLE = 'job'
#
# # MYSQL use
MYSQL_USER = 'root'
#
# # MYSQL password
MYSQL_PASS = '10ily1314'

# # # mongo host
# MONGO_URI = 'mongodb://127.0.0.1:27017'
# # MONGO_URI = 'mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019'
# #
# # # replicaset
# # REPLICASET = 'repset'
# #
# # # mongo database
# MONGO_DATABASE = 'test'
# # # mongo collection
# MONGO_COLLECTION = 'testdb'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


