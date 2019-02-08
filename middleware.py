# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from jobsearch.settings import UAPool
import sqlite3
import random
from scrapy.dupefilters import RFPDupeFilter
from pybloom import ScalableBloomFilter
import hashlib
from w3lib.url import canonicalize_url

class JobsearchSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JobsearchDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class JobseaerchIPProxy(HttpProxyMiddleware):
#
#     def __init__(self, ip=''):
#         con = sqlite3.connect('/Users/cb/Downloads/IPProxyPool/data/proxy.db')
#         cur = con.cursor()
#         cur.execute("select * from proxys where types=0 and score>=6")
#         res = cur.fetchall()
#         self.httplist = [str(x[1]) + ':' + str(x[2]) for x in res if x[4] != 1]
#         self.httpslist = [str(x[1]) + ':' + str(x[2]) for x in res if x[4] != 0]
#         con.close()
#
#     def process_request(self, request, spider):
#         '''
#         ip proxy handling,
#         :param request:
#         :param spider:
#         :return:
#         '''
#         # execptSpider = ['jobdajie']#,'jobzhipin'
#         # if spider.name not in execptSpider:
#         if request.url[0:5] == 'https':
#             self.thisip = 'https://' + random.choice(self.httpslist)
#         else:
#             self.thisip = 'http://' +random.choice(self.httplist)
#         print('当前使用ip是: ' + self.thisip)
#         request.meta['proxy'] = self.thisip
#
#
#
#
#
#     # def process_response(self, request, response, spider):
#     #
#     #     if response.status == 400 or 403:
#     #         self.iplist.remove(self.thisip)
#     #
#     #     return response


class JobsearchUserAgent(UserAgentMiddleware):

    def __init__(self, ua=''):
        self.user_agent = ua

    def process_request(self, request, spider):
        '''
        user agent handling
        :param request:
        :param spider:
        :return:
        '''
        self.user_agent = random.choice(UAPool)
        # print('当前使用的user-agent:' + self.user_agent)
        request.headers['User-Agent'] = self.user_agent
        # print(request.headers)


class URLBloomFilter(RFPDupeFilter):

    def __init__(self, path=None, debug=False):
        self.urls_sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        fp = hashlib.sha1()
        fp.update(canonicalize_url(request.url).encode('utf-8'))
        url_sha1 = fp.hexdigest()
        if url_sha1 in self.urls_sbf:
            return True
        else:
            self.urls_sbf.add(url_sha1)
