# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from itemadapter import ItemAdapter


class SpiderSteamPipeline:
    def open_spider(self, spider):  # что делать при открытии паука (создаем файлик)
        self.file = open('items.json', 'w')

    def close_spider(self, spider):  # что делать при окончании работы паука (закрываем файлик)
        self.file.close()

    def process_item(self, item, spider): #что делать с полученным item
        # a = dict()
        # a[ItemAdapter(item).asdict()["game_name"]] = ItemAdapter(item).asdict()
        # line = json.dumps(a) + "\n"
        # a[ItemAdapter(item).asdict()["game_name"]] = ItemAdapter(item).asdict()
        # line = json.dumps(a) + "\n"
        # self.file.write(line)
        # return item
        if (int(item["release_date"].split()[2]) > 2000) and item["game_name"] != '':
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file.write(line)
        return item
