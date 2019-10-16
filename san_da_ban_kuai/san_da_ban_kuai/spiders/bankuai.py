# -*- coding: utf-8 -*-
import json

import scrapy


class BankuaiSpider(scrapy.Spider):
    name = 'bankuai'
    allowed_domains = ['stock.jiangjuncj.com']
    start_urls = ['http://stock.jiangjuncj.com/stock/exponent/query']
    zscodes = ["sz399001", "sh000001", "sz399006"]
    index = 0

    headers = {
        # "Accept": "application/json, text/plain, */*",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "Connection": "keep-alive",
        # "Content-Length": "21",
        "Content-Type": "application/json;charset=UTF-8",
        "Host": "stock.jiangjuncj.com",
        "Origin": "http://www.jiangjuncj.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }

    def start_requests(self):
        form_data = {
            "zscode": self.zscodes[self.index]
        }
        yield scrapy.Request(self.start_urls[0], method="POST", body=json.dumps(form_data), headers=self.headers, callback=self.parse)

    def parse(self, response):
        content = json.loads(response.body)["model"]
        if content:
            name = content["name"]
            settlement = content["settlement"]
            changepercent = content["changepercent"]
            print("name:%s , settlement:%s , changepercent: %s" % (name, settlement, changepercent))
            if self.index < 2:
                self.index += 1
                print(self.index)

                body = {
                     "zscode": self.zscodes[self.index]
                }
                yield scrapy.Request(self.start_urls[0], method="POST", body=json.dumps(body), headers=self.headers, callback=self.parse)
        else:
            print(response.body)
            print("响应中没有数据！")