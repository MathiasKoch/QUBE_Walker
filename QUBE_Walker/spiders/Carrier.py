from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy
import settings
import re


class CarrierItem(scrapy.Item):
	varName = scrapy.Field()
	parentVarName = scrapy.Field()
	parentName = scrapy.Field()
	name = scrapy.Field()
	guid = scrapy.Field()
	href = scrapy.Field()
	color = scrapy.Field()
	level = scrapy.Field()
	type = scrapy.Field()

color_cnt = 0


def parse_script(raw_script):
	global color_cnt
	pattern = re.compile(r'var (.*?).?=.*?name:\"(.*?)\".*?guid:.?\"(.*?)\".*?level:.?([0-9])')

	items = []
	selected_areas = []
	ss = ''.join(raw_script)

	for a in settings.QUBE_AREAS:
		pattern_a = re.compile(r'var (.*?).?=.*?name:\"' + a + '\"')
		for (varName) in re.findall(pattern_a, ss):
			selected_areas.append(varName)

	for (varName, name, guid, level) in re.findall(pattern, ss):
		selected = False
		for a in selected_areas:
			if a in varName.encode('utf-8'):
				selected = True
				break
			else:
				selected = False

		if selected:
			item = CarrierItem()
			item['varName'] = varName.encode('utf-8')
			item['name'] = name.encode('utf-8')
			item['guid'] = guid.encode('utf-8')
			item['level'] = level.encode('utf-8')
			matching = re.search(r'(.*?)\.children\.add\(%s\)' % re.escape(varName), ss, re.M | re.I)
			if matching:
				item['parentVarName'] = matching.group(1).encode('utf-8')
				matching2 = re.search(r'var (%s).?=.*?name:\"(.*?)\"' % re.escape(item['parentVarName']), ss, re.M | re.I)
				if matching2:
					item['parentName'] = matching2.group(1).encode('utf-8')
				else:
					item['parentName'] = ""
			else:
				item['parentVarName'] = 0
			matching_gm = re.search(r'guid:.?\"%s\".*?(milestone|gate):.?true' % re.escape(guid), ss, re.M | re.I)
			if matching_gm:
				item['type'] = matching_gm.group(1).encode('utf-8')
			else:
				item['type'] = 'node'

			if item['level'] == "1" and color_cnt != 0:
				color_cnt += 1

			item['color'] = settings.DOT_GRAPH_COLORS[color_cnt]
			items.append(item)
	return items


class CarrierSpider(Spider):
	http_user = settings.QUBE_USER
	http_pass = settings.QUBE_PASS
	name = 'QUBE'
	allowed_domains = ['apps/qms/']
	start_urls = ["http://apps/qms/SitePages/Process%20Landscape.aspx"]

	def parse(self, response):
		base_url = "http://apps/qms/SitePages/Process%20Landscape.aspx"
		sites = Selector(response).xpath('//script/text()').extract()
		full_script = filter(lambda x: 'var selectedTermFieldId' in x, sites)
		items = parse_script(full_script)
		for i in items:
			i['href'] = base_url + "?selectedTerm=" + i['guid']
			yield i
			item = CarrierItem()
			item['parentVarName'] = i['varName']
			item['parentName'] = i['name']
			item['level'] = str(int(i['level']) + 1)
			item['type'] = 'area'
			item['color'] = i['color']
			request = scrapy.Request(base_url + "?selectedTerm=" + i['guid'], dont_filter=True, callback=self.parse_areas)
			request.meta['item'] = item
			yield request

	def parse_areas(self, response):
		item = response.meta['item']
		areas = Selector(response).xpath('//div[@id="MSO_ContentTable"]//div[@id="WebPartWPQ4"]//table[contains(@class,"ms-listviewtable")]//td[contains(@class, "ms-vb-title")]/div[contains(@class, "ms-vb")]')
		for a in areas:
			ret = item
			ret['name'] = ''.join(a.xpath('./a/text()').extract()).encode('utf-8')
			ret['href'] = 'http://apps' + ''.join(a.xpath('./a/@href').extract()).encode('utf-8')
			yield ret
