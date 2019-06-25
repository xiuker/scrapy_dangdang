# -*- coding: utf-8 -*-
import scrapy,time
from dangdang.items import DangdangItem

class PythonbookSpider(scrapy.Spider):
    name = 'pythonbook'
    allowed_domains = ['search.dangdang.com']
    start_urls = ['http://search.dangdang.com/?key=python&page_index=1']
    p = 1
    def parse(self, response):
        lilist = response.css('ul.bigimg li')
        #print(lilist)
        for li in lilist:
            item = DangdangItem()
            title = li.css('a::attr(title)').extract_first()
            if len(title) > 32:
                item['title'] = title[:32]
            else:
                item['title'] = title
            item['author'] = li.css('p.search_book_author span a::text').extract_first()
            item['price'] = li.css('p.price span::text').extract_first()
            item['comment_num'] = li.css('p.search_star_line a::text').extract_first()[:-3]
            item['detail'] = li.css('p.detail::text').extract_first()
            if li.css('a img::attr(data-original)').extract_first():
                item['picurl'] = li.css('a img::attr(data-original)').extract_first()
            else:
                item['picurl'] = li.css('a img::attr(src)').extract_first()
            item['picurl'] = item['picurl'].replace('_b_','_w_')
            yield item
            #print(item)
        time.sleep(3)
        self.p += 1
        if self.p < 6:
            next_url = 'http://search.dangdang.com/?key=python&page_index='+str(self.p)
            url = response.urljoin(next_url)
            yield scrapy.Request(url=url,callback=self.parse)






