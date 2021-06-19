#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
load_numbers.py
Created By takamitu hamada
version :  20180402
License      :  BSD License
Web site URL :  http://valkyrieviper.space
"""
import re,os,datetime,locale,sys,random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bs4 import BeautifulSoup
day = datetime.datetime.today()
num = 20
class numbers_list(object):
#Base URL
    def __init__(self):
        pass
    def set_list(self):
        sl = (["00"+str(i*2)+"1" for i in range(5)]
        + ["0"+str(i*2)+"1" for i in range(5,50)]
        + ["10"+str(i*2)+"1" for i in range(5)]
        + ["1"+str(i*2)+"1" for i in range(5,50)]
        + ["20"+str(i*2)+"1" for i in range(5)]
        + ["2"+str(i*2)+"1" for i in range(5,50)]
        + ["30"+str(i*2)+"1" for i in range(5)]
        + ["3"+str(i*2)+"1" for i in range(5,50)]
        + ["40"+str(i*2)+"1" for i in range(5)]
        + ["4"+str(i*2)+"1" for i in range(5,50)]
        + ["50"+str(i*2)+"1" for i in range(5)]
        + ["5"+str(i*2)+"1" for i in range(5,50)])
        #print(sl)
        return sl

#Numbers3
    def set_list2(self):
        sl2 = (["num3-20170"+str(i) for i in range(1,10)]
        + ["num3-2017"+str(i) for i in range(10,13)]
        + ["num3-20180"+str(i) for i in range(1,10)]
        + ["num3-2018"+str(i) for i in range(10,13)]
        )
        #print(sl2)
        return sl2
    def make_list3(self,url):
        try:
            rla = []
            rlb = []
            rlc = []
            rld = []
            rle = []
            soup = BeautifulSoup(open(url),"html.parser")
            for table in soup("table"):
                for tbody in table("tbody"):
                    for tr in tbody("tr"):
                        for th in tr("th"):
                            rla.append(th.renderContents())
                        for td in tr("td"):
                            rlb.append(td.renderContents())
            ml3 = [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46,49,52,55,58,61]
            for i in [ml3[i] for i in range(num)]:
                rlc.append(rlb[i])
            for i in rlc:
                i = re.sub("r'<.*?>'","",i)
                rld.append(int(i))
            for i in rla:
                i = re.sub("\xe7\xac\xac","",i)
                i = re.sub("\xe5\x9b\x9e","",i)
                rle.append(int(i))
        except:rle,rld
        list3 = zip(rle,rld)
        #print(list3)
        return list3
    def new_make_list3(self,url):
        try:
            rla = []
            rlb = []
            rlc = []
            rld = []
            rle = []
            soup = BeautifulSoup(open(url),"html.parser")
            for table in soup("table"):
                for thead in table("thead"):
                    for th in thead("th"):
                        rla.append(th.renderContents())
            #print(rla)
            rlaa = []
            nml3 = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41]
            for i in [nml3[i] for i in range(num)]:
                rlaa.append(rla[i])
            for i in rlaa:
                i = re.sub("\xe7\xac\xac","",i)
                i = re.sub("\xe5\x9b\x9e","",i)
                rle.append(int(i))
            #print(rle)
            for table in soup("table"):
                for tbody in table("tbody"):
                    for td in tbody("td"):
                        rlb.append(td.renderContents())
            nml32 = [1,14,27,40,53,66,79,92,105,118,131,144,157,170,183,196,209,222,235,248,261]
            for i in [nml32[i] for i in range(num)]:
                rlc.append(rlb[i])
            for i in rlc:
                p = re.compile(r'<.*?>')
                rld.append(int(p.sub("",i)))
        except:rle,rld
        list3 = zip(rle,rld)
        #print(list3)
        return list3
    def make_list3_total(self):
        list3 = []
        for i in ["num"+i for i in self.set_list()]:
            list3 += self.make_list3("numbers/data/"+i+".html")
        for i in self.set_list2():
            list3 += self.new_make_list3("numbers/data/"+i+".html")
        list3 += self.new_make_list3("numbers/data/numbers3.html")
        list3.sort(cmp=lambda x,y:cmp(x[0],y[0]),reverse=True)
        #list3.sort(key=lambda x:x[0],reverse=True)
        #print(list3)
        return list3

#Numbers4
    def set_list3(self):
        sl3 = (["num4-20170"+str(i) for i in range(1,10)]
        + ["num4-2017"+str(i) for i in range(10,13)]
        + ["num4-20180"+str(i) for i in range(1,10)]
        + ["num4-2018"+str(i) for i in range(10,13)]
        )
        #print(sl3)
        return sl3
    def make_list4(self,url):
        try:
            rla = []
            rlb = []
            rlc = []
            rld = []
            rle = []
            soup = BeautifulSoup(open(url),"html.parser")
            for table in soup("table"):
                for tbody in table("tbody"):
                    for tr in tbody("tr"):
                        for th in tr("th"):
                            rla.append(th.renderContents())
                        for td in tr("td"):
                            rlb.append(td.renderContents())
            ml4 = [2,5,8,11,14,17,20,23,26,29,32,35,38,41,44,47,50,53,56,59,61]
            for i in [ml4[i] for i in range(num)]:
                rlc.append(rlb[i])
            for i in rlc:
                i = re.sub("r'<.*?>'","",i)
                rld.append(int(i))
            for i in rla:
                i = re.sub("\xe7\xac\xac","",i)
                i = re.sub("\xe5\x9b\x9e","",i)
                rle.append(int(i))
        except:rle,rld
        list4 = zip(rle,rld)
        #print(list4)
        return list4
    def new_make_list4(self,url):
        try:
            rla = []
            rlb = []
            rlc = []
            rld = []
            rle = []
            soup = BeautifulSoup(open(url),"html.parser")
            for table in soup("table"):
                for thead in table("thead"):
                    for th in thead("th"):
                        rla.append(th.renderContents())
            rlaa = []
            nml4 = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,42]
            for i in [nml4[i] for i in range(num)]:
                rlaa.append(rla[i])
            for i in rlaa:
                i = re.sub("\xe7\xac\xac","",i)
                i = re.sub("\xe5\x9b\x9e","",i)
                rle.append(int(i))
            for table in soup("table"):
                for tbody in table("tbody"):
                    for td in tbody("td"):
                        rlb.append(td.renderContents())
            nml42 = [1,12,23,34,45,56,67,78,89,100,111,122,133,144,155,166,177,188,199,210,221]
            for i in [nml42[i] for i in range(num)]:
                rlc.append(rlb[i])
            for i in rlc:
                p = re.compile(r'<.*?>')
                rld.append(int(p.sub("",i)))
        except:rle,rld
        list4 = zip(rle,rld)
        #print(list4)
        return list4
    def make_list4_total(self):
        list4 = []
        for i in ["num"+i for i in self.set_list()]:
            list4 += self.make_list4("numbers/data/"+i+".html")
        for i in self.set_list3():
            list4 += self.new_make_list4("numbers/data/"+i+".html")
        list4 += self.new_make_list4("numbers/data/numbers4.html")
        list4 = sorted(set(list4))
        list4.sort(cmp=lambda x,y:cmp(x[0],y[0]),reverse=True)
        #list4.sort(key=lambda x:x[0],reverse=True)
        #print(list4)
        return list4
    def write_file(self):
        f = open("numbers/numbers_list.py","w")
        f.write("#!/usr/bin/env python\n")
        f.write("#-*- coding:utf-8 -*-\n")
        f.write("year = %s\n" % (day.year))
        f.write("month = %s\n" % (day.month))
        f.write("day = %s\n" % (day.day))
        f.write("#ナンバーズ3の第1回から最新回までの当選数字\n")
        f.write("list3 = ")
        f.write(str(list3) + "\n\n")
        f.write("#ナンバーズ4の第1回から最新回までの当選数字\n")
        f.write("list4 = ")
        f.write(str(list4) + "\n\n")
        f.close()

if __name__ == "__main__":
    nl = numbers_list()
    list3 = nl.make_list3_total()
    list4 = nl.make_list4_total()
    nl.write_file()
    print("Finish")




