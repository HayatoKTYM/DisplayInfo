# -*- coding: utf-8 -*-

"""
Webページに現在のトピックとシステムの知識を表示
"""
__author__ = "Yuto Akagawa"

from csv_processing import CSVProcessing
from get_knowledge import GetKnowledge
import threading
import time
import datetime

csv = CSVProcessing()
gk = GetKnowledge()
csv_path = "../../SotaWozSystem/Server/topic_memory.csv"

def output_html(o1):
    '''
    Webページに現在のトピックとシステムの知識を表示
    '''
    cur_topic = ""
    topic = csv.read(csv_path)
    print topic
    for i, t in enumerate(topic):
        if i == len(topic) - 1:
            cur_topic = t[0]

    # ページの表示
    print >>o1, "<html>"
    print >>o1, "<head>"
    print >>o1, '<meta http-equiv="Content-Type" content="text/html; charset=utf8" />'
    print >>o1, "</head>"
    print >>o1, "<body>"
    print >>o1, "<center>"
    # 現在のトピック
    print >>o1, "<h1>***現在のトピック***</h1>"
    print >>o1, "<h1>" + cur_topic + "</h1>"
    # 現在のトピックについてシステムが保持している知識
    if not cur_topic == "":
        print >>o1, "<table border=\"1\">"
        for info in gk.db[cur_topic].keys():
            for text in gk.db[cur_topic][info]:
                print >>o1, "<tr>"
                print >>o1, "<th>" + info + "</th>"
                print >>o1, "<th>" + text + "</th>"
                print >>o1, "</tr>"
        print >>o1, "</table>"
    print >>o1, "</center>"
    # 3秒に1回ページを更新
    print >>o1, '<meta http-equiv="refresh" content="3" />'
    print >>o1, "</body>"
    print >>o1, "</html>"


"""
Webサーバ
"""
from BaseHTTPServer import *
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        output_html(self.wfile)

time.sleep(1)
HTTPServer(('dm', 8700), MyHandler).serve_forever()
