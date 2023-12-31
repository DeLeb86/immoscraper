# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import json,os
import pandas as pd
#from pymongo import MongoClient


class ImmoelizaPipeline:
    #def open_spider(self,spider):
    #    self.db=MongoClient("localhost").get_database("immoeliza")
    def process_item(self, item, spider):
        item.transform()
        for field in item.fields:
            item.setdefault(field,None)
        item.pop("js")
        item.pop("html_elems")
        #self.db["properties"].insert_one(ItemAdapter(item).asdict())
        return item
    
    def close_spider(self, spider):
        print("SPIDER FINISHED!!!")
        #js=json.load(open("output.json"))
        
