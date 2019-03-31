BOT_NAME = 'cartoon'

SPIDER_MODULES = ['cartoon.spiders']
NEWSPIDER_MODULE = 'cartoon.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cartoon (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'cartoon.pipelines.ComicImgDownloadPipeline': 1,
}

IMAGES_STORE = 'D:/火影忍者'

COOKIES_ENABLED = False

DOWNLOAD_DELAY = 0.25    # 250 ms of delay

