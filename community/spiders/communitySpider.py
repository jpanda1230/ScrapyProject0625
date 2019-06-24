import scrapy

from community.items import CommunityItem
from datetime import datetime
import re
import json
from json import JSONEncoder
from collections import OrderedDict

urlPath = ''


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class EventsSpider(scrapy.Spider):
    name = "communityCrawler"

    def start_requests(self):
        yield scrapy.Request("http://rubinmuseum.org/events?category=14", self.parse_clien)

    def parse_clien(self, response):
        eventLinks = response.xpath('//div[@class="title"]/a/@href').extract()
        for linkForEachEvent in eventLinks:
            self.urlPath = str(linkForEachEvent)
            yield scrapy.Request(str(linkForEachEvent), self.parse_page )

    def parse_page(self, response):

        checkEvent = response.xpath('//h3[@class="subheader"]/text()').extract()[0]
        if checkEvent.find(",") < 1:
            print("No Match")
        else:

            item = CommunityItem()
            #item['title'] = response.xpath('h1[@class="header"]/text()').extract()
            item['title'] = str(response.xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/h1/text()').extract()).replace("\"","")
            print(item['title'])

            #df =response.xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/h3/text()').extract()[0].strip()
            df = response.xpath('//h3[@class="subheader"]/text()').extract()[0]
            print('********',df)
            _date = df.split(',')
            items = _date[1].split('.')
            _date_year = 2000 + int(items[2])
            _date_month = int(items[0])
            _date_day = int(items[1])
            x = datetime(_date_year, _date_month, _date_day)
            df = x.strftime("%m/%d/%Y")
            print(x.strftime("%m/%d/%Y"))
            item['datefrom'] = df.rstrip("\n")

            time_st = response.xpath('/html/body/div[2]/div/div[2]/div[2]/div[1]/div[2]/h3/text()[2]').extract()[0]
            tempst = time_st.split("-")
            time_st = tempst[0].strip()
            prog = re.compile('\b((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))')

            if prog.match(time_st):
                st = time_st
            elif len(time_st) == 7:
                st = '0' + time_st
            else:
                st = time_st
                #st = datetime.strptime(time_st,'\b((1[0-2]|0?[1-9]):([0-5][0-9]) ([AaPp][Mm]))')
            print(st)
            item['starttime'] = st

            item['eventwebsite'] = (self.urlPath)
            print(self.urlPath)

            item['description'] = re.sub('[^A-Za-z0-9-. ]+', '',response.xpath('//div[@class="row description"]/div//p//text()').extract()[0])
            item['id'] = '7057'
            item['location'] = "NewYork"
            item['address'] = response.xpath('//*[@id="footer"]/div[2]/div/div/div/div[1]/address/span[1]/text()').extract()
            item['organization'] = response.xpath('//*[@id="footer"]/div[2]/div/div/div/div[1]/h4/text()').extract()
            item['city'] = response.xpath('//*[@id="footer"]/div[2]/div/div/div/div[1]/address/span[2]/text()').extract()
            item['state'] = "NY"

            def replace_all(text, dic):
                for i, j in dic.items():
                    text = text.replace(i, j)
                return text

            path = 'outTest.json'
            od = OrderedDict([("\n", ""), ("\"", ""), ("   ", ""), ("[", ""), ("]", "")])
            with open(path, '+a') as outfile:
                #json.dumps(outfile.write("%r\n" %((str(item).replace("\n", "")).replace("\"","")).replace("   ","")))
                json.dumps(outfile.write("%r\n" %replace_all(str(item), od)))
            print(item)
            yield item
