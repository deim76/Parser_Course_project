# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from course_project.settings import mongo_client

class CourseProjectPipeline(object):
    def process_item(self, item, spider):
        print(item._values.get('id_start'))

        data_base = mongo_client[spider.name]
        collection = data_base['friends']
        collection.insert(item)

        return item
