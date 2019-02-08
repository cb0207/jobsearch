# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from jobsearch.items import JobsearchItem
from scrapy.shell import inspect_response
from itertools import chain
import urllib.request

# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess

class JobzhipinSpider(scrapy.Spider):
    name = 'jobzhipin'
    allowed_domains = ['www.zhipin.com']
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}
    page = 0

    def __init__(self, jobname='爬虫', *args, **kwargs):
        super(JobzhipinSpider, self).__init__(*args, **kwargs)
        self.jobname = urllib.request.quote(jobname)
        self.start_urls = ['https://www.zhipin.com/c100010000/h_100010000/?query=' + self.jobname + '&page=1000']
        self.target = 0

    def parse(self, response):
        # inspect_response(response, self)
        if self.page == 0:
            self.page = int(response.xpath("//a [@class='cur']/text()").extract()[1])

        for page in range(1, self.page+1):
            url = 'https://www.zhipin.com/c100010000/h_100010000/?query=' + self.jobname + '&page=' + str(page)
            yield Request(url, dont_filter=True, headers=self.header, callback=self.joblist)

    def joblist(self, response):
        postlist = response.xpath("//div [@class='job-primary']/div/h3/a/@href").extract()

        for post in postlist:
            self.target += 1
            yield Request(url='https://www.zhipin.com' + post, headers=self.header, callback=self.jobDetail)

    def jobDetail(self, response):
        # inspect_response(response, self)

        def postInfo(info):
            post = {'city': 'null', 'experience': 'null', 'edu': 'null'}
            for i in info:
                if '城市' in i:
                    post['city'] = getIt(i.strip())
                elif '经验' in i:
                    post['experience'] = getIt(i.strip())
                else:
                    post['edu'] = getIt(i.strip())
            return post

        def getIt(info):
            return info[info.find('：') + 1:]

        def comInfor(*info):
            info = list(chain.from_iterable(info))
            company = {'info': 'null', 'web': 'null'}
            tem = []
            for i in info:
                if ('http' or 'www' or 'com') in i:
                    company['web'] = i
                else:
                    tem.append(i)
            company['info'] = tem
            return company

        item = JobsearchItem()

        post = postInfo(
            response.xpath("//div [@class='job-primary detail-box']/div [@class='info-primary']/p/text()").extract())
        company = comInfor(
            response.xpath("//div [@class='info-company']/p/text()").extract(),
            response.xpath("//div [@class='info-company']/p/a/text()").extract()
        )

        item['postn_name'] = str(response.xpath(
            "//div [@class='job-primary detail-box']/div [@class='info-primary']/div [@class='name']/h1/text()").extract())
        item['postn_web'] = str(response.request.url)
        item['postn_area'] = str(post['city'])
        item['postn_adds'] = str(response.xpath("//div [@class='location-address']/text()").extract())
        item['postn_salary'] = str(response.xpath(
            "normalize-space(//div [@class='job-primary detail-box']/div [@class='info-primary']/div [@class='name']/span/text())").extract())
        item['postn_experience'] = str(post['experience'])
        item['postn_edu'] = str(post['edu'])
        item['postn_numHire'] = 'null'
        item['postn_benifit'] = str(response.xpath(
            "//div [@class='detail-content']/div [@class='job-sec']/div [@class='job-tags']/span/text()").extract())
        item['com_name'] = str(response.xpath("//div [@class='info-company']/h3/a/text()").extract())
        item['com_web'] = str(company['web'])
        item['com_simInfo'] = str(company['info'])
        item['post_date'] = str(response.xpath("//div [@class='job-author']/span/text()").re(r"发布于(.*)"))
        item['resource'] = self.name
        yield item

# if __name__ =="__main__":
#
#     process=CrawlerProcess({"user-agent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/52.0.2743.116Safari/537.36Edge/15.15063"})
#     process.crawl(JobzhipinSpider)
#     process.start()
