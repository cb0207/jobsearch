# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, cookies
import json
from jobsearch.items import JobsearchItem
import urllib.request
from scrapy.shell import inspect_response

import re


class JobdajieSpider(scrapy.Spider):

    name = 'jobdajie'
    allowed_domains = ['dajie.com']
    # start_urls = ['http://so.dajie.com/']
    cookie = cookies.CookieJar()

    ttlpage = 0

    def __init__(self, jobname='爬虫', *args, **kwargs):
        super(JobdajieSpider, self).__init__(*args, **kwargs)
        self.jobname = urllib.request.quote(jobname)
        self.header = {"Accept": 'application/json, text/javascript, */*; q=0.01',
                  "Accept-Encoding": 'gzip, deflate, br',
                  "Accept-Language": 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  "Connection": 'keep-alive',
                  "Cookie": "DJ_RF=%s; DJ_EU=%s; DJ_UVID=%s; SO_COOKIE_V2=%s",
                  "Host": 'so.dajie.com',
                  "Referer": 'https://so.dajie.com/job/search?keyword=' + self.jobname + '&from=job',
                  "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                  "X-Requested-With": 'XMLHttpRequest'}
        self.target = 0

    def start_requests(self):
        header1 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Connection': 'keep-alive',
                   'Host': 'so.dajie.com',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}
        return [Request('https://so.dajie.com/job/search?keyword=' + self.jobname + '&from=job',
                        headers=header1,
                        meta={'cookiejar': 1, 'dont_merge_cookies': True},
                        callback=self.parse)]

    def parse(self, response):
        cookie1 = response.headers.getlist('Set-Cookie')
        self.cookie.extract_cookies(response, response.request)
        djeu_pat = "DJ_EU=(.*?);"
        djrf_pat = "DJ_RF=(.*?);"
        djevid_pat = "DJ_UVID=(.*?);"
        cov2_pat = "SO_COOKIE_V2=(.*?);"
        djeu = re.compile(djeu_pat).findall(str(cookie1))
        djrf = re.compile(djrf_pat).findall(str(cookie1))
        djevid = re.compile(djevid_pat).findall(str(cookie1))
        cov2 = re.compile(cov2_pat).findall(str(cookie1))
        self.header['Cookie'] = "DJ_RF=%s; DJ_EU=%s; DJ_UVID=%s; SO_COOKIE_V2=%s" % (djrf[0], djeu[0], djevid[0], cov2[0])

        return [Request(
            'https://so.dajie.com/job/ajax/search/filter?keyword=' + self.jobname + '&order=0&city=&recruitType=&salary=&experience=&page=1&positionFunction=&_CSRFToken=&ajax=1',
            headers=self.header,
            meta={'dont_merge_cookies': True},
            callback=self.searchlist)]

    def searchlist(self, response):
        if self.ttlpage == 0:
            api = json.loads(response.text)
            self.ttlpage = api['data']['totalPage']

        for page in range(1, self.ttlpage + 1):
            url = 'https://so.dajie.com/job/ajax/search/filter?keyword=' + self.jobname + '&order=0&city=&recruitType=&salary=&experience=&page=' + str(
                page) + '&positionFunction=&_CSRFToken=&ajax=1'

            yield Request(url=url,
                          headers=self.header,
                          meta={'dont_merge_cookies': True},
                          dont_filter=True,
                          callback=self.joblist)

    def joblist(self, response):
        # inspect_response(response, self)
        api = json.loads(response.text)
        result = api['data']['list']

        header2 = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Connection': 'keep-alive',
                   'Host': 'job.dajie.com',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}

        for post in result:
            self.target += 1
            yield Request(url='https:' + post['jobHref'],
                          headers=header2,
                          meta={'dont_merge_cookies': True, 'post': post},
                          callback=self.jobdetail)

    def jobdetail(self, response):
        # inspect_response(response, self)
        item = JobsearchItem()
        item['postn_name'] = str(response.meta['post']['jobName'])
        item['postn_web'] = str('https:' + response.meta['post']['jobHref'])
        item['postn_area'] = str(response.meta['post']['pubCity'])
        item['postn_adds'] = str(response.xpath("//div [@class='ads-msg']/span/text()").extract())
        item['postn_salary'] = str(response.meta['post']['salary'])
        if 'pubEx' in response.meta['post'].keys():
            item['postn_experience'] = str(response.meta['post']['pubEx'])
        else:
            item['postn_experience'] = 'null'

        if 'pubEdu' in response.meta['post'].keys():
            item['postn_edu'] = str(response.meta['post']['pubEdu'])
        else:
            item['postn_edu'] = 'null'

        item['postn_numHire'] = str(response.xpath("//li [@class='recruiting']/span/text()").re("(\d+)\xa0人"))
        item['postn_benifit'] = str(response.xpath("//div [@class='job-msg-bottom']/ul/li/text()").extract())
        item['com_name'] = str(response.meta['post']['compName'])
        item['com_web'] = 'null'
        if 'industryName' in response.meta['post'].keys():
            item['com_simInfo'] = str(response.meta['post']['industryName'])
        else:
            item['com_simInfo'] = 'null'

        item['post_date'] = 'null'
        item['resource'] = self.name
        yield item

if __name__ == '__main__':

    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"})
    process.crawl(JobdajieSpider)
    process.start()
