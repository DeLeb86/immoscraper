# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import json,os
import pandas as pd
from time import sleep
#from pymongo import MongoClient


class ImmoelizaPipeline:
    def process_item(self, item, spider):
        """
        actions performed after the crawling is done.
        data cleaning, data post processing.
        removing duplicates and removing unusable entries (no price, no postal code)

        Args:
            spider (ImmowebscraperSpider): the spider itself
        """
        item.transform()
        item.pop("js")
        #item.pop("html_elems")
        return item
    
    def close_spider(self, spider):
        """
        actions performed after the crawling is done.
        data cleaning, data post processing.
        removing duplicates and removing unusable entries (no price, no postal code)

        Args:
            spider (ImmowebscraperSpider): the spider itself
        """
        print("SPIDER FINISHED!!! ------ Post processing data")
        sleep(20)
        try:
            df=pd.read_json("data/output.json",orient="columns")
        except:
            df=pd.read_json("data/output.json")
        df.dropna(subset=["Price","PostalCode"],inplace=True)
        df.drop(df[df["PostalCode"]>10000].index,inplace=True)
        df.to_json("data/final_dataset.json")
        
