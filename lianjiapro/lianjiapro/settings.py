# -*- coding: utf-8 -*-

# Scrapy settings for lianjiapro project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lianjiapro'

SPIDER_MODULES = ['lianjiapro.spiders']
NEWSPIDER_MODULE = 'lianjiapro.spiders'

# DEFAULT_REQUEST_HEADERS = {
#     'Host': 'nj.lianjia.com',
#     'Referer': 'https://nj.lianjia.com/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=sousuo',
#     'pgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36Accept-Encoding: gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     'Connection': 'keep-alive'
# }
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'lianjiapro (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
ITEM_PIPELINES = {
   'lianjiapro.pipelines.lianjiaproPipeline': 10,
}
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lianjiapro.middlewares.LianjiaproSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Retry many times since proxies often fail
RETRY_TIMES = 5
# Retry on most error codes since proxies fail for different reasons
# RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    'lianjiapro.middlewares.RandomUserAgentMiddleware': 543,           #将在middlewares.py中定义了RandomUserAgentMiddlware类添加到这里;
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,   #需要将scrapy默认的置为None不调用
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'scrapy.pipelines.images.ImagesPipeline': 300,
    # 'lianjiapro.middlewares.ProxyMiddleWare': 100,
    # 'scrapy_proxies.RandomProxy': 100,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None
}

RANDOM_UA_TYPE = "random"
# # Proxy list containing entries like
# # http://host1:port
# # http://username:password@host2:port
# # http://host3:port
# # 这是存放代理IP列表的位置
# PROXY_LIST = Proxies().list
#
# #代理模式
# # 0 = Every requests have different proxy
# # 1 = Take only one proxy from the list and assign it to every requests
# # 2 = Put a custom proxy to use in the settings
# PROXY_MODE = 0
#
# #如果使用模式2，将下面解除注释：
# #CUSTOM_PROXY = "http://host1:port"