from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from course_project import settings
from course_project.spiders.vk import VkSpider

if __name__=='__main__':
    cr_settings=Settings()
    cr_settings.setmodule(settings)
    process=CrawlerProcess(settings=cr_settings)
    process.crawl(VkSpider)
    process.start()