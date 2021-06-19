#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
download_data.py
Created By takamitu hamada
version :  20180402
License      :  BSD License
Web site URL :  http://valkyrieviper.space
"""
import urllib2,re,os,datetime,locale,sys,random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

day = datetime.datetime.today()
num = 20
class download_data(object):
#Base URL
    def __init__(self):
        self.url_base = "http://www.mizuhobank.co.jp/takarakuji/numbers/"
        self.url_base_new = "https://www.mizuhobank.co.jp/retail/takarakuji/numbers/"
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.132 Safari/537.36')]
#downloaded HTML
    def download_html(self):
        if not os.path.isdir("numbers/data"):
            os.chdir("numbers")
            os.mkdir("data")
            os.chdir("data")
        else:
            os.chdir("numbers/data")
#        nnum =(["num"+i for i in self.set_list()]
#        + self.set_list2()
        nnum =(self.set_list2()
        + self.set_list3())
        print(nnum)
        for i in nnum:
            try:
                html = self.opener.open(self.url_base+"backnumber/%s.html" % (i))
                print self.url_base+"backnumber/%s.html" % (i)
                with open(i+".html","w") as lf:
                    lf.write(html.read())
                lf.close()
            except Exception,e:pass
            try:
                html2 = self.opener.open(self.url_base_new+"numbers3/index.html")
                html3 = self.opener.open(self.url_base_new+"numbers4/index.html")
                with open("numbers3.html","w") as lf2:
                    lf2.write(html2.read())
                lf2.close()
                with open("numbers4.html","w") as lf3:
                    lf3.write(html3.read())
                lf3.close()
            except Exception,e:pass
        os.chdir("../")
        return sorted(set([i for i in os.listdir("data")]))
#    def set_list(self):
#        sl = (["00"+str(i*2)+"1" for i in range(5)]
#        + ["0"+str(i*2)+"1" for i in range(5,50)]
#        + ["10"+str(i*2)+"1" for i in range(5)]
#        + ["1"+str(i*2)+"1" for i in range(5,50)]
#        + ["20"+str(i*2)+"1" for i in range(5)]
#        + ["2"+str(i*2)+"1" for i in range(5,50)]
#        + ["30"+str(i*2)+"1" for i in range(5)]
#        + ["3"+str(i*2)+"1" for i in range(5,50)]
#        + ["40"+str(i*2)+"1" for i in range(5)]
#        + ["4"+str(i*2)+"1" for i in range(5,50)])
#        return sl
    def set_list2(self):
        sl2 = (["num3-20170"+str(i) for i in range(1,10)]
        + ["num3-2017"+str(i) for i in range(10,13)]
        + ["num3-20180"+str(i) for i in range(1,10)]
        )
        return sl2
    def set_list3(self):
        sl3 = (["num4-20170"+str(i) for i in range(1,10)]
        + ["num4-2017"+str(i) for i in range(10,13)]
        + ["num4-20180"+str(i) for i in range(1,10)]
        )
        return sl3


if __name__ == "__main__":
    dd = download_data()
    dd.download_html()
    print("Finish")


