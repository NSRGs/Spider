#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-16 05:47:25
# Project: wooyun6



import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    }

    @every(minutes=60)
    def on_start(self):
        for i in range(1,10000):
            self.crawl('http://www.wooyun.org/bugs/page/' + str(i), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://www.wooyun.org/bugs/wooyun-\d+-\d+$", each.attr.href):
                self.crawl(each.attr.href, priority = 9,callback=self.detail_page)

    @config(priority=9)
    def detail_page(self, response):
        return {
           "link": response.url,
            "漏洞标题": response.doc('.wybug_title').text().replace('\t\t',' ').replace(u"\u6f0f\u6d1e\u6807\u9898\uff1a "," "),
            "漏洞类型": response.doc(".wybug_type").text().replace('\t\t',' ').replace(u"\u6f0f\u6d1e\u7c7b\u578b\uff1a "," "),
            "危害等级":response.doc(".wybug_level").text().replace('\t\t',' ').replace(u"\u5371\u5bb3\u7b49\u7ea7\uff1a"," "),
            "漏洞状态":response.doc(".wybug_status").text().replace('\t',' ').replace(u"\u6f0f\u6d1e\u72b6\u6001\uff1a\r\n"," "),
            "公开时间": response.doc('.wybug_open_date').text().replace('\t\t',' ').replace(u"\u516c\u5f00\u65f6\u95f4\uff1a "," "),
            "相关厂商": response.doc(".wybug_corp").text().replace('\t\t',' ').replace(u"\u76f8\u5173\u5382\u5546\uff1a"," "),
            "公开状态": response.doc(".wybug_open_status").text().replace('\t\t',' ').replace('\t',' '),
            "简要描述": response.doc(".wybug_description").text().replace('\t\t',' ').replace('\t',' '),
            "详细说明": response.doc(".wybug_detail > p").text().replace('\t\t',' ').replace('\t',' '),
            "厂商回应": response.doc(".wybug_result").text().replace('\t\t',' ').replace('\t',' '),
            "ALL": response.doc(".content").text().replace('\t\t',' ').replace('\t',' '),



}

