# jobsearch
scrapy框架多爬虫模式，爬取51job，拉钩，直聘，猎聘，大街，中华英才网


框架简介：
一个爬虫对应一个网站，以jobname变量传入搜索内容

Commandline 使用方法:
1. scrapy crawl + 爬虫名 + 职位搜索： scrapy crawl job51 jobname='爬虫'
   使用对应爬虫对职位进行爬取

2. scrapy mycrawl + 职位搜索：scrapy mycrawl jobnamw='爬虫'
   使用所有爬虫，对职位进行爬取
   
