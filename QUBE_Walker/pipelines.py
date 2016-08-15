# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import XmlItemExporter, JsonItemExporter
import pydot
import settings
import os
import heapq
import time


class JsonExportPipeline(object):
	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('%s_nodes.jl' % spider.name, 'w+b')
		self.files[spider] = file
		self.exporter = JsonItemExporter(file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item


class XmlExportPipeline(object):
	def __init__(self):
		self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		file = open('%s_products.xml' % spider.name, 'w+b')
		self.files[spider] = file
		self.exporter = XmlItemExporter(file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		file = self.files.pop(spider)
		file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item


def files_in_tree_age(rootfolder, count=1, extension=".svg", oldest=True):
	if oldest:
		return heapq.nsmallest(count,
						(os.path.join(dirname, filename)
						for dirname, dirnames, filenames in os.walk(rootfolder)
						for filename in filenames
						if filename.endswith(extension)),
						key=lambda fn: os.stat(fn).st_mtime)
	else:
		return heapq.nlargest(count,
						(os.path.join(dirname, filename)
						for dirname, dirnames, filenames in os.walk(rootfolder)
						for filename in filenames
						if filename.endswith(extension)),
						key=lambda fn: os.stat(fn).st_mtime)


class GraphExportPipeline(object):
	def __init__(self):
		self.graph = {}
		self.old_graph = {}
		self.old_graph_list = list()
		self.new_graph_list = list()

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		graph = pydot.Dot(graph_type=settings.DOT_GRAPH_TYPE, size='100000, 32')
		graph.set_node_defaults(margin=settings.DOT_MARGIN)
		graph.set_graph_defaults(splines=settings.DOT_SPLINES)
		graph.set_graph_defaults(ranksep=settings.DOT_RANKSEP)
		graph.set_graph_defaults(nodesep=settings.DOT_NODESEP)
		self.graph[spider] = graph

		if settings.HIGHLIGHT_CHANGES or settings.EXPORT_LIST_OF_CHANGES:
			path = settings.OUTPUT_PATH
			if settings.OUTPUT_PATH.endswith("/"):
				path = path[:-1]

			if os.path.isdir(path) and os.path.exists(path):
				old_graph_ = files_in_tree_age(path, 1, '.dot', False)
				if len(old_graph_) > 0:
					if time.gmtime() > time.strptime(old_graph_[0].replace(path + '\\', '').replace('.dot', ''), settings.OUTPUT_TIME_FORMAT):
						self.old_graph[spider] = pydot.graph_from_dot_file(old_graph_[0])
						self.old_graph_list = self.old_graph[spider].get_node_list()

	def spider_closed(self, spider):
		graph = self.graph.pop(spider)

		path = settings.OUTPUT_PATH
		if settings.OUTPUT_PATH.endswith("/"):
			path = path[:-1]

		if not os.path.isdir(path) and not os.path.exists(path):
			os.makedirs(path)

		if settings.NUMBER_OF_GRAPHS_TO_SAVE != -1:
			l = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name)) and name.endswith(".svg")]) + 1
			if l > settings.NUMBER_OF_GRAPHS_TO_SAVE:
				rmlist = files_in_tree_age(path, l - settings.NUMBER_OF_GRAPHS_TO_SAVE, '.svg', True)
				for f in rmlist:
					os.remove(f)
					os.remove(f.replace('.svg', '.dot'))
					os.remove(f.replace('.svg', '.pdf'))

		name = settings.OUTPUT_NAME.replace('%T', time.strftime(settings.OUTPUT_TIME_FORMAT)) + '.svg'
		graph.write_svg(os.path.join(path, name))

		if settings.EXPORT_LIST_OF_CHANGES or settings.HIGHLIGHT_CHANGES:
			name = settings.OUTPUT_NAME.replace('%T', time.strftime(settings.OUTPUT_TIME_FORMAT)) + '.dot'
			graph.write_dot(os.path.join(path, name))
			if settings.EXPORT_LIST_OF_CHANGES:
				# Save the self.old_graph_list in some excel/csv format
				print("============== Saving changelog list ==============")
				print("Items removed in new graph:")
				print([node.get_name() for node in self.old_graph_list])
				print("Items added in new graph:")
				print([node.get_name() for node in self.new_graph_list])

		if settings.SAVE_PDF:
			name_pdf = settings.OUTPUT_NAME.replace('%T', time.strftime(settings.OUTPUT_TIME_FORMAT)) + '.pdf'
			graph.write_pdf(os.path.join(path, name_pdf))

	def process_item(self, item, spider):
		graph = self.graph.get(spider)

		if item['type'] == 'node' and item['parentVarName'] != 0:
			node = pydot.Node(name=item['varName'], label="\"" + item['name'] + "\"", style="filled",
								fillcolor=item['color'], href="\"" + item['href'] + "\"", comment="\"" + item['guid'] + "\"")
		elif item['type'] == 'milestone' and item['parentVarName'] != 0:
			node = pydot.Node(name=item['varName'], label="\"" + item['name'] + "\"", shape="triangle", style="filled",
								fillcolor=item['color'], href="\"" + item['href'] + "\"", comment="\"" + item['guid'] + "\"")
		elif item['type'] == 'gate' and item['parentVarName'] != 0:
			node = pydot.Node(name=item['varName'], label="\"" + item['name'] + "\"", shape="diamond", style="filled",
								fillcolor=item['color'], href="\"" + item['href'] + "\"", comment="\"" + item['guid'] + "\"")
		elif item['type'] == 'area':
			node = pydot.Node(name="\"" + item['name'] + "\"", label="\"" + item['name'] + "\"", shape="box",
								href="\"" + item['href'] + "\"")
		else:
			return

		graph.add_node(node)
		edge = pydot.Edge(item['parentVarName'], node)
		graph.add_edge(edge)

		node_new = True

		if settings.EXPORT_LIST_OF_CHANGES or settings.HIGHLIGHT_CHANGES:
			for node_element in self.old_graph_list:
				if item['href'] in node_element.to_string():
					self.old_graph_list.remove(node_element)

			# At this point self.old_graph_list contains only elements that exists in the old graph, but not in the new.

			if len(self.old_graph) > 0:
				old_graph_ = self.old_graph.get(spider).get_node_list()
				for node_element in old_graph_:
					if item['href'] in node_element.to_string():
						node_new = False

				if node_new:
					self.new_graph_list.append(node)

			# At this point self.old_graph_list contains all elements that exists in the old graph, but not in the new.
			# As well as all the elements that exists in the new, but not in the old!

		if settings.HIGHLIGHT_CHANGES and node_new:
			# Do something to change the nodes appearance!
			if node_new:
				print("New node! %s" % node.get_name())

		return item