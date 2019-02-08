# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest, cookies
import re
import json
from jobsearch.items import JobsearchItem
import urllib.request
from scrapy.shell import inspect_response


class JoblagouSpider(scrapy.Spider):
    name = 'jobLagou'
    allowed_domains = ['lagou.com']
    # start_urls = ['https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=']
    cookies = cookies.CookieJar()
    result = []
    ttlpage = 0

    # custom_settings = {
    #    "LOG_FILE": "/Users/cb/Downloads/Project/Project_crawler job/Project/Error Log/lagou.txt"
    # }

    def __init__(self, jobname='爬虫', *args, **kwargs):
        super(JoblagouSpider, self).__init__(*args, **kwargs)
        self.postdata = {'first': 'true', 'pn': '1', 'kd': jobname}
        self.jobname = urllib.request.quote(jobname)
        self.header = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  'Connection': 'keep-alive',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'Cookie': 'JSESSIONID=;SEARCH_ID=;user_trace_token=',
                  'Host': 'www.lagou.com',
                  'Referer': 'https://www.lagou.com/jobs/list_' + self.jobname + '?labelWords=&fromSearch=true&suginput=',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                  'X-Anit-Forge-Code': '0',
                  'X-Anit-Forge-Token': 'None',
                  'X-Requested-With': 'XMLHttpRequest'}
        self.target = 0

    def start_requests(self):

        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                  'Connection': 'keep-alive',
                  'Host': 'www.lagou.com',
                  'Upgrade-Insecure-Request': '1',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'}

        return [Request("https://www.lagou.com/jobs/list_" + self.jobname + "?labelWords=&fromSearch=true&suginput=",
                        headers=header, meta={'cookiejar': 1, 'dont_merge_cookies': True}, callback=self.parse)]

    def parse(self, response):
        # inspect_response(response, self)
        cookie1 = response.headers.getlist('Set-Cookie')
        # print(cookie1)
        self.cookies.extract_cookies(response, response.request)
        jsessionPat = (r'JSESSIONID=(.*?);')
        searchPat = (r'SEARCH_ID=(.*?);')
        usertoken = (r'LGRID=(.*?);')
        jsess = re.compile(jsessionPat).findall(str(cookie1))
        search = re.compile(searchPat).findall(str(cookie1))
        utoken = re.compile(usertoken).findall(str(cookie1))
        self.header['Cookie'] = 'JSESSIONID=%s;SEARCH_ID=%s;LGRID=%s' % (jsess[0], search[0], utoken[0])
        return [FormRequest(url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
                            meta={'cookiejar': self.cookies.jar, 'dont_merge_cookies': True},
                            headers=self.header,
                            formdata=self.postdata,
                            callback=self.searchlist)]

    def searchlist(self, response):
        # inspect_response(response, self)
        if self.ttlpage == 0:
            # try:
            api = json.loads(response.text)
            ttResult = api['content']['positionResult']['totalCount']
            pagesize = api['content']['positionResult']['resultSize']
            self.ttlpage = ttResult % pagesize
            # except KeyError:
                # inspect_response(response, self)

        for page in range(1, self.ttlpage + 1):
            self.postdata['pn'] = str(page)
            yield FormRequest(url='https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false',
                              meta={'cookiejar': response.meta['cookiejar'], 'dont_merge_cookies': True},
                              headers=self.header,
                              formdata=self.postdata,
                              dont_filter=True,
                              callback=self.joblist)

    def joblist(self, response):
        # inspect_response(response, self)
        api = json.loads(response.text)

        if api['success']:
            result = api['content']['positionResult']['result']
            for post in result:
                self.target += 1
                yield Request(url='https://www.lagou.com/jobs/' + str(post['positionId']) + '.html',
                              meta={'cookiejar': response.meta['cookiejar'], 'dont_merge_cookies': True, "post": post},
                              headers=self.header,
                              callback=self.jobdetail)
        else:
            # inspect_response(response, self)
            reRequest = response.request.copy()
            reRequest.dont_filter = True
            yield reRequest

    def jobdetail(self, response):
        # inspect_response(response, self)
        if response.status == 200:
            benifit = []
            item = JobsearchItem()
            item['postn_name'] = str(response.meta['post']['positionName'])
            item['postn_web'] = str('https://www.lagou.com/jobs/' + str(response.meta['post']['positionId']) + '.html')
            item['postn_area'] = str(response.meta['post']['city'])
            tem = response.xpath("//div [@class='work_addr']/a/text()").extract()
            tem.remove(tem[-1])
            item['postn_salary'] = str(response.meta['post']['salary'])
            item['postn_experience'] = str(response.meta['post']['workYear'])
            item['postn_edu'] = str(response.meta['post']['education'])
            item['postn_numHire'] = 'Null'
            benifit.extend(response.meta['post']['companyLabelList'])
            benifit.append(response.meta['post']['positionAdvantage'])
            item['postn_benifit'] = str(benifit)
            item['com_name'] = str(response.meta['post']['companyFullName'])
            item['com_web'] = str(response.xpath("//i [@class='icon-glyph-home']/following-sibling::a/@href").extract())
            item['com_simInfo'] = str(response.meta['post']['industryField'])
            item['post_date'] = str(response.meta['post']['formatCreateTime'])
            item['resource'] = self.name
            yield item
        elif response.status == 302:
            # inspect_response(response, self)
            reRequest = response.request.copy()
            reRequest.dont_filter = True
            yield reRequest
            # yield Request(url='https://www.lagou.com/jobs/' + str(response.meta['post']['positionId']) + '.html',
            #               meta={'cookiejar': response.meta['cookiejar'], 'dont_merge_cookies': True,
            #                     "post": response.meta['post']},
            #               headers=self.header,
            #               callback=self.jobdetail,
            #               dont_filter=True)


if __name__ == '__main__':

    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"})
    process.crawl(JoblagouSpider)
    process.start()
