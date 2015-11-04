# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class QunarPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='', db='spider', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item_bak(self, item, spider):
        pass
    
    def process_item(self, item, spider):
        try:
            self.cursor.execute("""SELECT * FROM qn_region WHERE name = %s""",(item['city']))
            lines = self.cursor.fetchall()
            if lines:
                city_id = lines[0][0]
                self.cursor.execute("""INSERT INTO qn_scenic(city_id,title,tel,olink,addr,introduce,lysj,jtzn,ts,otime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (city_id, item['title'], item['tel'], item['olink'], item['addr'], item['introduce'], item['lysj'], item['jtzn'], item['ts'], item['otime']))
                self.conn.commit()
            else:
                print "所属城市不存在"
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item