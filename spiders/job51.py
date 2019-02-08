# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from jobsearch.items import JobsearchItem
from scrapy.http import Request, Response
from scrapy import signals
import re
import urllib.request
from scrapy.shell import inspect_response

class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['51job.com']
    # start_urls = ['https://search.51job.com/list/%252C,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,1.html']
    lastpage = 0

    def __init__(self, jobname='爬虫', *args, **kwargs):
        super(Job51Spider, self).__init__(*args, **kwargs)
        self.jobname = urllib.request.quote(jobname)
        self.jobname = urllib.request.quote(self.jobname)
        self.start_urls = ['https://search.51job.com/list/%252C,000000,0000,00,9,99,' + self.jobname + ',2,1.html']
        self.target = 0

    def parse(self, response):
        # inspect_response(response, self)
        if self.lastpage == 0:
            self.lastpage = int(response.xpath("//span [@class='td']/text()").re(r'\d+')[0])

        for page in range(1, self.lastpage+1):
            nexturl = "https://search.51job.com/list/%252C,000000,0000,00,9,99," + self.jobname + ",2," + str(page) + ".html"
            yield Request(nexturl, dont_filter=True, callback=self.joblist)

    def joblist(self, response):
        positList = response.xpath("//p [@class='t1 ']/span/a/@href ").extract()
        for posit in positList:
            self.target += 1
            yield Request(posit, callback=self.jobdetail)

    def jobdetail(self, response):
        # inspect_response(response, self)
        item = JobsearchItem()

        def postInfo(info):
            post = {'experience': 'null', 'edu': 'null', 'numhire': 'null', 'postdate': 'null'}
            for i in info:
                if '发布' in i:
                    post['postdate'] = i.strip()
                elif '经验' in i:
                    post['experience'] = i.strip()
                elif '招' in i:
                    post['numhire'] = i.strip()
                else:
                    post['edu'] = i.strip()
            return post

        postInfom = postInfo(response.xpath("//p [@class='msg ltype']/text()").extract()[1:])
        item['postn_name'] = str(response.xpath("//h1/@title").extract())
        item['postn_web'] = str(response.url)
        item['postn_area'] = str(response.xpath("//p [@class='msg ltype']/text()").extract()[0].strip())
        item['com_name'] = str(response.xpath("//p [@class='cname']/a/@title").extract())
        item['com_web'] = str(response.xpath("//p [@class='cname']/a/@href").extract())
        item['com_simInfo'] = str(response.xpath("//div [@class='com_tag']/p/@title").extract())
        item['post_date'] = str(postInfom['postdate'])
        item['postn_adds'] = str(response.xpath("//div [@class='bmsg inbox']/p//text()").extract()[2].strip())
        item['postn_salary'] = str(response.xpath("//strong/text()").extract()[1])
        item['postn_experience'] = str(postInfom['experience'])
        item['postn_edu'] = str(postInfom['edu'])
        item['postn_numHire'] = str(postInfom['numhire'])
        item['postn_benifit'] = str(response.xpath("//div [@class='t1']/span/text()").extract())
        item['resource'] = self.name
        yield item

        @classmethod
        def from_crawler(cls, crawler, *args, **kwargs):
            spider = super(Job51Spider, cls).from_crawler(crawler, *args, **kwargs)
            crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
            return spider

        def spider_closed(self, spider):
            spider.logger.info('Spider closed: %s', spider.name)








