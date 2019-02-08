# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from jobsearch.items import JobsearchItem
import urllib.request
from scrapy.shell import inspect_response


class JobliepinSpider(scrapy.Spider):
    name = 'jobliepin'
    allowed_domains = ['www.liepin.com']
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}
    lastpage = 0

    def __init__(self, jobname='爬虫', *args, **kwargs):
        super(JobliepinSpider, self).__init__(*args, **kwargs)
        self.jobname = urllib.request.quote(jobname)
        self.target = 0

    def start_requests(self):
        return [Request('https://www.liepin.com/zhaopin/?key=' + self.jobname + '&d_curPage=2&curPage=0',
                        headers=self.header)]

    def parse(self, response):

        def findLast(url):
            return url[url.find('&curPage=') + 9:]

        if self.lastpage == 0:
            self.lastpage = response.xpath("//div [@class='pagerbar']/a [@class='last']/@href").extract()
            self.lastpage = int(findLast(self.lastpage[0]))

        for page in range(1, self.lastpage + 1):
            url = 'https://www.liepin.com/zhaopin/?key=' + self.jobname + '&d_curPage=' + str(page - 1) \
                  + '&curPage=' + str(page)
            yield Request(url, headers=self.header, dont_filter=True, callback=self.joblist)

    def joblist(self, response):

        # inspect_response(response, self)

        postlist = response.xpath("//div [@class='job-info']/h3/a/@href").extract()
        for post in postlist:
            self.target += 1
            if 'www.liepin.com' not in post:
                post = 'https://www.liepin.com' + post
            yield Request(post, headers=self.header, callback=self.jobdetail)

    def jobdetail(self, response):
        # inspect_response(response, self)

        def comInfo(info):
            company = {'info': 'null', 'addrs': 'null'}
            tem = []
            for i in info:
                if '公司地址' in i:
                    company['addrs'] = i.strip()
                elif '行业' in i:
                    tem.append('行业:' + response.xpath("//ul [@class='new-compintro']/li/a/text()").extract()[0])
                else:
                    if len(i.strip()) > 0:
                        tem.append(i.strip())
            company['info'] = tem
            return company

        item = JobsearchItem()

        companyinfo = comInfo(response.xpath("//ul [@class='new-compintro']/li/text()").extract())
        if 'https://www.liepin.com/job/' in response.request.url:
            item['postn_name'] = str(response.xpath("//div [@class='title-info']/h1/@title").extract())
            item['postn_web'] = str(response.request.url)
            item['postn_area'] = str(response.xpath("//p [@class='basic-infor']/span/a/text()").extract())
            item['postn_adds'] = str(companyinfo['addrs'])
            item['postn_salary'] = str(response.xpath("normalize-space(//p [@class='job-item-title']/text())").extract())
            item['postn_experience'] = str(response.xpath("//div [@class='job-qualifications']/span/text()").extract()[1])
            item['postn_edu'] = str(response.xpath("//div [@class='job-qualifications']/span/text()").extract()[0])
            item['postn_numHire'] = 'null'
            item['postn_benifit'] = str(response.xpath("//div [@class='tag-list']/span/text()").extract())
            item['com_name'] = str(response.xpath("//div [@class='title-info']/h3/a/@title").extract())
            item['com_web'] = str(response.xpath("//div [@class='title-info']/h3/a/@href").extract())
            item['com_simInfo'] = str(companyinfo['info'])
            item['post_date'] = str(response.xpath("normalize-space(//p [@class='basic-infor']/time/text())").extract())

        else:

            item['postn_name'] = str(response.xpath("//div [@class='title-info ']/h1/@title").extract())
            item['postn_web'] = str(response.request.url)
            item['postn_area'] = str(response.xpath("normalize-space(//p [@class='basic-infor']/span/text())").extract())
            item['postn_adds'] = str(companyinfo['addrs'])
            item['postn_salary'] = str(response.xpath("normalize-space(//p [@class='job-main-title']/text())").extract())
            item['postn_experience'] = str(response.xpath("//div [@class='resume clearfix']/span/text()").extract()[1])
            item['postn_edu'] = str(response.xpath("//div [@class='resume clearfix']/span/text()").extract()[0])
            item['postn_numHire'] = 'null'
            item['postn_benifit'] = str(response.xpath("//div [@class='tag-list']/span/text()").extract())
            item['com_name'] = str(response.xpath("//p [@class='company-name']/@title").extract())
            item['com_web'] = str(response.xpath("//div [@class='title-info']/h3/a/@href").extract())
            item['com_simInfo'] = str(companyinfo['info'])
            item['post_date'] = str(response.xpath("normalize-space(//p [@class='basic-infor']/time/text())").extract())
        item['resource'] = self.name
        yield item
