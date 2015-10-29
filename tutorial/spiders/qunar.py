# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QunarItem

class QunarSpider(scrapy.Spider):
    name = "qunar"
    allowed_domains = ["qunar.com"]
    #allowed_domains = ["localhost"]
    start_urls = (
        'http://travel.qunar.com/place/',
        #'http://localhost/qunar_index.html',
        #"http://localhost/qunar_xiamen.htm",
        #"http://localhost/qunar_gugong.htm",
        #"http://localhost/qunar_tiananmen.htm",
    )

    def parse(self, response):
        nodes = response.xpath('//div[@class="list current"]/div[@class="contbox current"]/dl/dd/div/ul/li/a')
        for node in nodes:
             city = node.xpath('text()').extract()[0]
             url  = node.xpath('@href').extract()[0]+'-jingdian'
             yield scrapy.Request(url, callback=self.parse_page, meta={'city': city})

    def parse_page(self, response):
        last_page = response.xpath('//div[@class="b_paging"]/a')
        if last_page:
            if last_page[-1].xpath('text()').extract()[0].encode('utf-8') == '下一页':
                max_p = int(last_page[-2].xpath('text()').extract()[0].encode('utf-8'))+1
                urls = [response.url]
                urls.extend([response.url +'-1-' + str(p) for p in range(2, max_p)])
                for url in urls:
                    yield scrapy.Request(url, callback=self.parse_item, meta={'city': response.meta['city']})

    def parse_item(self, response):
        nodes = response.xpath('//ul[@class="list_item clrfix"]/li/a')
        for node in nodes:
            url = node.xpath('@href').extract()[0]
            yield scrapy.Request(url, callback=self.parse_info, meta={'city': response.meta['city']})

    def parse_info(self, response):
        item = QunarItem()
        #景区名字
        titlep = response.xpath('//div[@class="b_title clrfix"]/h1/text()').extract()
        if titlep:
            item['title'] = titlep[0].encode('utf-8')
        else:
            item['title'] = ''
        #景区介绍
        introducep = response.xpath('//div[@class="e_db_content_box"]').extract()
        item['introduce'] = '<br>'.join(introducep).encode('utf-8')
        #td_l = response.xpath('//div[@class="e_summary_list clrfix"]/table/tbody/tr/td[@class="td_l"]/dl/dd/span/text()').extract()   
        # scrapy 不认识 tbody标签^_^!
        td_l = response.xpath('//td[@class="td_l"]/dl/dd/span/text()').extract()    
        #景区地址
        if td_l:
            
            item['addr'] = td_l[0].encode('utf-8')
            
            #    item['addr'] = ''
            #景区电话
            if len(td_l)>1:
                item['tel'] = td_l[1].encode('utf-8')
            else:
                item['tel'] = ''
        else:
            item['addr'] = ''
            item['tel'] = ''
        
        #景区官网
        olinkp = response.xpath('//dl/dd[@class="m_desc_isurl"]/a/text()').extract()
        if olinkp:
            item['olink'] = olinkp[0].encode('utf-8')
        else:
            item['olink']  = ''
        #开放时间
        otimep = response.xpath('//td[@class="td_r"]/dl[@class="m_desc_right_col"]/dd/span').extract()
        if otimep:
            item['otime'] = otimep[0].encode('utf-8')
        else:
            item['otime'] = ''
        #旅游时节
        lysj = response.xpath('//div[@id="lysj"]/div[@class="e_db_content_box e_db_content_dont_indent"]/p/text()').extract()
        if lysj:
            item['lysj'] = lysj[0].encode('utf-8')
        else:
            item['lysj'] = ''
        #交通指南
        jtznp = response.xpath('//div[@id="jtzn"]/div[@class="e_db_content_box e_db_content_dont_indent"]/p').extract()
        item['jtzn'] = ''.join(jtznp).encode('utf-8')
        #小贴士
        tsp = response.xpath('//div[@id="ts"]/div[@class="e_db_content_box e_db_content_dont_indent"]/p/text()').extract()
        item['ts'] = '<br>'.join(tsp).encode('utf-8')
        #城市
        #response.meta['city'] = '北京'
        item['city'] = response.meta['city']

        return item