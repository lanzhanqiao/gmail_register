# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter


class GoogleregisterPipeline:

    def process_item(self, item, spider):
        print("mysql消费")
        print(item)
        # mydb = mysql.connector.connect(
        #     host="127.0.0.1",
        #     user="root",
        #     passwd="123456",
        #     database="scrapy",
        #     port=3306
        # )
        # mycursor = mydb.cursor()
        # values = (
        #     item['first_name'],
        #     item['last_name'],
        #     item['email'],
        #     item['password']
        # )
        # sql = "insert into gmail_info (first_name, last_name, email, password) VALUES (%s,%s,%s,%s)"
        # mycursor.execute(sql, values)
        # mydb.commit()
        return item
