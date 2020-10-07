#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
kyotei.py
Copyright@ takamitu hamada
version :  20190728
License      :  BSD License
Web site URL :  http://vsrx.site
"""
import sqlite3,os,sys,csv
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

argvs = sys.argv
#kyotei class
class kyotei(object):
    def __init__(self):
        try:
            klist1 = [int(argvs[1]),int(argvs[2]),int(argvs[3]),int(argvs[4]),int(argvs[5]),int(argvs[6])]
            kdata = self.db2list()
            kk1a = ""
            kks = self.k_sym(kdata,klist1)
            for i in kks:
                kk1a += str(i[0])+","+str(i[1])+"/"
            kk2a = [i[1] for i in kks]
            kk3a = kk2a[0]-kk2a[-1]
            kk3b = kk1a + " difference : " + str(kk3a)
            print(kk3b)
        except:
            print("failed")
#db_open method
    def db_open(self):
        con = sqlite3.connect("kyotei.sqlite")
        try:
            sql = """
            create table 競艇(
                登録番号 integer,
                選手 varchar(20),
                勝率 integer,
                ２連率 integer,
                モーター２連率 integer,
            );
            """
            con.execute(sql)
        except:pass
        con.executemany(u"insert into 'main'.'競艇'('登録番号','選手','勝率','２連率','モーター２連率') values(?1,?2,?3,?4,?5)",
unicode(kdata,"utf-8"))
        c = con.execute(u"select * from 競艇")
        wdb = ""
        for i in c:
            wdb += "%s,%s,%s,%s,%s" % (i[0],i[1],i[2],i[3],i[4])
        con.close()
        return wdb
#db2list method
    def db2list(self):
        con = sqlite3.connect("kyotei.sqlite")
        c = con.cursor()
        c.execute("select * from 競艇")
        kdata = []
        for i in c:
            kdata.append(i)
        wdb2 = [list(i) for i in kdata]
        wdb3 = [(i[0],i[1].encode("utf_8"),i[2],i[3],i[4]) for i in wdb2]
        return wdb3
#k_sym method
    def k_sym(self,kdata,klist):
        kdata2 = []
        for i in klist:
            for j in kdata:
                try:
                    if i == j[0]:
                        kdata2.append(j)
                except:kdata2
        kdata3 = kdata4 = kdata5 = kdata2
        kdata2a = zip([i[1] for i in kdata2],[7,6,5,4,3,2])
        kdata3.sort(cmp=lambda x,y:cmp(x[2],y[2]),reverse=True)
        kdata7 = zip([i[1] for i in kdata3],[10,9,8,7,6,5])
        kdata4.sort(cmp=lambda x,y:cmp(x[3],y[3]),reverse=True)
        kdata8 = zip([i[1] for i in kdata4],[10,9,8,7,6,5])
        kdata5.sort(cmp=lambda x,y:cmp(x[4],y[4]),reverse=True)
        kdata9 = zip([i[1] for i in kdata5],[6,5,4,3,2,1])
        kdata7a = [list(i) for i in kdata7]
        kdata8a = [list(i) for i in kdata8]
        kdata9a = [list(i) for i in kdata9]
        kdata11a = []
        for i in kdata7a:
            for j in kdata8a:
                if i[0] == j[0]:
                    try:
                        i[1] = i[1]+j[1]
                        kdata11a.append([i[0],i[1]])
                    except:pass
        kdata11b = []
        for i in kdata11a:
            for j in kdata9a:
                if i[0] == j[0]:
                    try:
                        i[1] = i[1]+j[1]
                        kdata11b.append([i[0],i[1]])
                    except:pass
        kdata11c = []
        for i in kdata11b:
            for j in kdata2a:
                if i[0] == j[0]:
                    try:
                        i[1] = i[1]+j[1]
                        kdata11c.append([i[0],i[1]])
                    except:pass
        kdata11c.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse = True)
        return kdata11c

if __name__ == "__main__":
    k = kyotei()
