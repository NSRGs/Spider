#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Author: TheCjw<thecjw@qq.com>
# Created on 11:34 2015/10/20

__author__ = "TheCjw"

import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.4; Nexus 7 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl("http://www.wooyun.org/bugs/", callback=self.first_page)

    @config(age=10 * 24 * 60 * 60)
    def first_page(self, response):
        pages_content = response.doc("body > div.content > p").text()
        pages = int(pages_content.split(", ")[1].split(" ")[0])
        for i in range(1, pages + 1):
            self.crawl("http://www.wooyun.org/bugs/page/%d" % i, callback=self.bugs_list)
            
    @config(age=10 * 24 * 60 * 60)
    def bugs_list(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://www.wooyun.org/bugs/wooyun-\d+-\d+$", each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
    
    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        return {
            "title": response.doc("title").text(),
            "content": response.content
        }

