# -*- coding: utf-8 -*-
import scrapy

from jobsearch.items import JobsearchItem
from scrapy.http import Request
import urllib.request
from scrapy.shell import inspect_response


class JobyingcaiSpider(scrapy.Spider):
    name = 'jobyingcai'
    allowed_domains = ['www.chinahr.com']
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}
    lastpage = 0

    def __init__(self, jobname='爬虫', *args, **kwargs):
        super(JobyingcaiSpider, self).__init__(*args, **kwargs)
        self.jobname = urllib.request.quote(jobname)
        self.target = 0

    def start_requests(self):
        return [Request(
            'http://www.chinahr.com/sou/?orderField=relate&keyword=' + self.jobname + '&city=%E5%85%A8%E5%9B%BD&page=1',
            headers=self.header)]

    def parse(self, response):
        # inspect_response(response, self)
        if self.lastpage == 0:
            self.lastpage = int(response.xpath("//div [@class='quickPage']/span/text()").re(r"\d+")[0])

        for page in range(1, self.lastpage+1):
            url = 'http://www.chinahr.com/sou/?orderField=relate&keyword=' + self.jobname + '&city=%E5%85%A8%E5%9B%BD&page=' + str(page)
            yield Request(url, headers=self.header, dont_filter=True, callback=self.joblist)

    def joblist(self, response):
        postlist = response.xpath("//div [@class='jobList']/@data-url").extract()

        for post in postlist:
            self.target += 1
            yield Request(post, headers=self.header, callback=self.jobdetail)

    def jobdetail(self, response):
        # inspect_response(response, self)

        item = JobsearchItem()
        item['postn_name'] = str(response.xpath("//div [@class='base_info']/div/h1/span/text()").extract())
        item['postn_web'] = str(response.request.url)
        item['postn_area'] = str(response.xpath("//div [@class='job_require']/span [@class='job_loc']/text()").extract())
        item['postn_adds'] = 'null'
        item['postn_salary'] = str(response.xpath("//span [@class='job_price']/text()").extract())
        item['postn_experience'] = str(response.xpath("//span [@class='job_exp']/text()").extract())
        item['postn_edu'] = str(response.xpath("//div [@class='job_require']/span/text()").extract()[3])
        item['postn_numHire'] = 'null'
        item['postn_benifit'] = str(response.xpath("//div [@class='job_fit_tags']/ul/li/text()").extract())
        item['com_name'] = str(response.xpath("//div [@class='company_intro  jpadding mt15']/h4/a/text()").extract())
        item['com_web'] = str(response.xpath("//div [@class='company_intro  jpadding mt15']/h4/a/@href").extract())
        item['com_simInfo'] = str(response.xpath("//div [@class='compny_tag']/span/text()").extract())
        item['post_date'] = str(response.xpath("//p [@class='updatetime']/text()").extract())
        item['resource'] = self.name
        yield item

