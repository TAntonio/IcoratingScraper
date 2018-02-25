# -*- coding: utf-8 -*-
import scrapy

ICO_LIST_XPATH = "//table[contains(@class, 'uk-table')]//tr[@data-href]"
ATTRIBUTES_XPATH = "//div[contains(@class, 'uk-card') and not (.//h3/text()='Bounty')]//table[@class='uk-table']/tbody/tr"
ICO_GENERAL_RATINGS = "//div[contains(./span, 'Investment rating') or contains(./span, 'score')]"
ICO_DETAILED_SOCIAL_LINKS_XPATH = "//div[contains(@class, 'uk-child-width-expand uk-grid-small uk-text-center')]//a[@href]"

BASE_ATTRIBUTES_IGNORE_LIST = ['bonus program', 'description', 'features']
OVERVIEW_PAGE_ATTRIBUTES_IGNORE_LIST = ["ico date", "founded", "website"]  # we will parse this info in detailed info page


class IcoratingSpider(scrapy.Spider):
    name = "icorating"
    allowed_domains = ["icorating.com"]
    start_urls = ['http://icorating.com/ico/?filter=all']

    def parse(self, response):
        ico_list = response.xpath(ICO_LIST_XPATH)
        for ico_item in ico_list:
            ico_url = ico_item.xpath('./@data-href').extract_first()
            yield scrapy.Request(ico_url,
                                 self.parse_ico_item_general_info,
                                 meta={'ico_info': {'ico_url': ico_url}})

    def parse_ico_item_general_info(self, response):
        ico_info = response.meta.get('ico_info')
        ico_name = response.xpath('//h1/text()').extract_first()
        ico_attributes = response.xpath(ATTRIBUTES_XPATH)
        ratings = response.xpath(ICO_GENERAL_RATINGS)

        ico_info['Name'] = ico_name
        self.fill_with_attributes(ico_info, ico_attributes)

        for rating in ratings:
            rating_title = rating.xpath('./span[@class="title"]/text()').extract_first()
            rating_score_name = rating.xpath('./span[@class="name"]/text()').extract_first()
            rating_score_value = rating.xpath('./span[@class="score"]/text()').extract_first()
            if rating_score_value:
                rating_score_value = rating_score_value.split('/')[0]
            ico_info.update({rating_title: rating_score_value or rating_score_name})

        yield scrapy.Request(response.urljoin('details/'),
                             self.parse_ico_item_detailed_info,
                             meta={'ico_info': ico_info})

    def parse_ico_item_detailed_info(self, response):
        ico_info = response.meta.get('ico_info')
        ico_attributes = response.xpath(ATTRIBUTES_XPATH)
        social_items = response.xpath(ICO_DETAILED_SOCIAL_LINKS_XPATH)

        self.fill_with_attributes(ico_info, ico_attributes, from_detailed_info=True)

        for social_item in social_items:
            social_item_name = social_item.xpath('./span/text()').extract_first()
            social_item_link = social_item.xpath('./@href').extract_first()
            ico_info.update({social_item_name.strip(): social_item_link.strip()})
        yield ico_info

    @staticmethod
    def fill_with_attributes(ico_info, ico_attributes, from_detailed_info=False):
        for attr in ico_attributes:
            attr_name = attr.xpath('./td[1]/text()').extract_first()
            attr_value = attr.xpath('./td[2]/p/text()').extract() or attr.xpath('./td[2]/text()').extract()

            if not attr_name or not attr_value:
                continue
            attr_name = attr_name.replace(':', '')
            attr_value = ', '.join([el.strip() for el in attr_value if el.strip()])

            if attr_name.lower() in BASE_ATTRIBUTES_IGNORE_LIST:
                continue

            if from_detailed_info:
                if 'price' in attr_name.lower():
                    attr_value = attr_value.split('=')[1]
            else:
                if attr_name.lower() in OVERVIEW_PAGE_ATTRIBUTES_IGNORE_LIST:
                    continue
            ico_info.update({attr_name.strip(): attr_value})
