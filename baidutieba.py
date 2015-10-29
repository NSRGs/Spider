#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-10-25 07:24:44
# Project: baidutieba1

import re
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
            "headers": {


        }
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://tieba.baidu.com/f?kw=%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6%E6%88%90%E9%83%BD%E5%AD%A6%E9%99%A2&ie=utf-8&pn=0', callback=self.theme_page)
        
    @config(age=10 * 24 * 60 * 60)
    def theme_page(self, response):
        ThemePages = response.doc(".red_text").text().split(" ")[0]
        for x in range(0,int(ThemePages),50):
            self.crawl('http://tieba.baidu.com/f?kw=%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E5%A4%A7%E5%AD%A6%E6%88%90%E9%83%BD%E5%AD%A6%E9%99%A2&ie=utf-8&pn=' + str(x), callback=self.tiezi_page)
        

    @config(age=10 * 24 * 60 * 60)
    def tiezi_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match(".+/p/+\d", each.attr.href):
                self.crawl(each.attr.href, callback=self.tieziPages_page)
                
                
    @config(age=10 * 24 * 60 * 60)
    def tieziPages_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://tieba.baidu.com/p/+\d+\?pn=", each.attr.href):
                tiezipages = response.doc(".thread_theme_5 .red").text().split(" ")[1]
                for c in range(1,int(tiezipages) + 1):
                    self.crawl(each.attr.href.split("=")[0] + "=" + str(c), callback=self.detail_page)
        
    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('.clearfix > .text-overflow').text(),
            "xcontent": response.doc(".content").text(),
            "tie_time": response.doc(".d_post_content_firstfloor .post-tail-wrap > .tail-info").text(),
        }
