# -*- coding: utf-8 -*-

"""
MySQLデータベースから知識を獲得
"""
__author__ = "Yuto Akagawa"

import random
import sys
import MySQLdb

class GetKnowledge:
    def __init__(self, host="ds", db_name="woz2017", user="root"):
        self.db = self.get_db(host, db_name, user)

    def get_db(self, host="ds", db_name="woz2017", user="root"):
        '''
        MySQLから発話内容を一括取得
        :return: db (dict)
        '''
        # コネクションの確立
        connector = MySQLdb.connect(host=host, db=db_name, user=user, passwd="", charset="utf8")
        cursor  = connector.cursor()  # カーソル(概念)を作成

        db = {}
        cursor.execute('select * from genre')
        genres = cursor.fetchall()
        # e.g. genres = ((1, 1, 'romance'), (2, 2, 'action'), (3, 3, 'SF'), (4, 4, 'horror'))
        for genre in genres:
            genre_id = genre[1]
            genre_name = genre[2].encode('utf-8')
            cursor.execute('select * from topic where genre_id={}'.format(genre_id))
            topics = cursor.fetchall()
            # e.g. topics = ((1, 1, '美女と野獣'), (2, 2, 'ララランド'), (3, 3, 'ピーチガール'))
            for topic in topics:
                topic_id = topic[2]
                topic_name = topic[3].encode('utf-8')
                db[topic_name] = {}
                db[topic_name]['genre'] = [genre_name]
                for message in ['abstract', 'director', 'actor', 'review', 'evaluation']:
                    cursor.execute('select * from {} where topic_id={}'.format(message, topic_id))
                    fields = cursor.fetchall()
                    text_list = []
                    for field in fields:
                        text = field[2].encode('utf-8')
                        text_list.append(text)
                    db[topic_name][message] = text_list

        cursor.close()
        connector.close()
        return db

if __name__ == '__main__':
    gk = GetKnowledge()
    print(gk.db["美女と野獣"]["actor"][0])
