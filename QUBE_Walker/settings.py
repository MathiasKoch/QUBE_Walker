# -*- coding: utf-8 -*-

# Settings for QUBE_Walker project
#
# See in the bottom of this file for the Scrapy specific setttings!
#


# Name of the bot
BOT_NAME = 'QUBE_Walker'

# Enabled spider modules (Currently only one is existing, so no reasong to mess with this)
SPIDER_MODULES = ['QUBE_Walker.spiders']
NEWSPIDER_MODULE = 'QUBE_Walker.spiders'

# Log level in the terminal. Can be: [Lowest severity] (DEBUG, INFO, WARNING, ERROR, CRITICAL) [Highest severity]
LOG_LEVEL = 'INFO'

# HTTP identification on the user-agent (This is what is seen by the IT administrators, as the computer accessing QUBE)
USER_AGENT = 'QUBE_Walker (BY MATKO)'

# Authentification for QUBE (DOMAIN\\USERNAME) !!! DOMAIN must be included !!!
QUBE_USER = 'DE-PROD\\MATKO'
QUBE_PASS = ''

# Settings of the GraphWiz graph being exported by the QUBE_Walker
DOT_GRAPH_TYPE = 'digraph'				# Graph type (digraph for arrows between nodes, graph for lines)
DOT_MARGIN = '0.15'						# Margin around text inside figure
DOT_SPLINES = 'polyline'				# Shaping of edge lines between nodes
DOT_RANKSEP = '5'						# Vertical separation of levels in graph
DOT_NODESEP = '0.9'						# Horizontal separation of nodes in same level

DOT_GRAPH_COLORS = ["#F0E8CD", "#FFFFB0", "#CFECCF", "#CCECEF", "#DDD4E8", "#F98CB6", "#7589BF", "#48B5A3", "#85CA5D", "#FCA985", "#6FB7D6", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]


OUTPUT_PATH = 'graphs/'					# Relative to walk.py OR full absolute path only
OUTPUT_NAME = '%T'						# Use %T to include OUTPUT_TIME_FORMAT
OUTPUT_TIME_FORMAT = '%d-%m___%H-%M'	# For full list of formats, see http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/ 

HIGHLIGHT_CHANGES = True				# Highlight changes since last run in the graph (Not implemented yet)
EXPORT_LIST_OF_CHANGES = True			# Exports an excel list of changes since last run (Not fully implemented yet)
SAVE_ONLY_ON_CHANGES = True				# Enable to only save new outputs if a change in QUBE structure has occurred since last saved run

NUMBER_OF_GRAPHS_TO_SAVE = 10			# Number of graphs to save, before starting to delete the oldest when a new one comes in (-1 = infinite)

SAVE_PDF = True                         # Export a PDF file of the structure (Not fully implemented yet)


QUBE_AREAS = ['Governance and Compliance', 'Core processes', 'Support Processes']                    # Choose areas to export (Governance and Compliance, Core Processes, Support Processes)
#QUBE_AREAS = ['Governance and Compliance', 'Support Processes']                    # Choose areas to export (Governance and Compliance, Core Processes, Support Processes)


#
#		Scrappy specific settings starting here
#
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#



# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# Uncomment to put a custom request header on the http requests made from QUBE_Walker
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}


# Enable or disable downloader middlewares
# Leave NTLM Authentification enabled to allow authenticating against QUBE (Sharepoint)
DOWNLOADER_MIDDLEWARES = {
    'QUBE_Walker.middlewares.NTLM_Middleware': 1,
}

# Configure item pipelines
# Uncomment the appropriate line of the file types you want to output (JSON, XML, GRAPH = SVG)
# NOTE: 
#	QUBE_Walker.pipelines.GraphExportPipeline must be enabled in order to highlight changes in QUBE structure
ITEM_PIPELINES = {
    #'QUBE_Walker.pipelines.JsonExportPipeline': 300,
    #'QUBE_Walker.pipelines.XmlExportPipeline': 400,
    'QUBE_Walker.pipelines.GraphExportPipeline': 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
