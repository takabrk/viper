#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
numbers.py
Copyright@ takamitu_hamada
version :  20210304
License      :  BSD License
"""
from numbers_list import *
from loto_list import *
import random,sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append(os.pardir)
#Numbers3
#numbers3クラス
class numbers3(object):
    def __init__(self):
#過去の当選数字全て
        self.full_num3 = [i[1] for i in list3]

#ミニ当選数字と当選回数
        self.full_mini = [i%100 for i in self.full_num3]
        self.full_mini_count = list(zip(self.full_mini,[self.full_mini.count(i) for i in self.full_mini]))

#過去240回のミニ当選数字
        self.mini_240 = [self.full_mini[i] for i in range(240)]
        self.mini_240_count = list(zip(self.mini_240,[self.mini_240.count(i) for i in self.mini_240]))
        self.dic_mini_full = sorted(set(zip([i for i in range(100)],[self.mini_240.count(i) for i in [i for i in range(100)]])))

#ストレート当選数字と当選回数
        self.nums3full = list(zip(self.full_num3,[self.full_num3.count(i) for i in self.full_num3]))

#過去240回のストレート当選数字
        self.num31020 = [self.full_num3[i] for i in range(240)]
        self.num31020_count = list(zip(self.num31020,[self.num31020.count(i) for i in self.num31020]))

#Filter G
        self.g_num = 20
        self.g_num2 = 40
#各位が特定回数以上出現していない場合に削除するフィルタ
#過去240回の各桁数列
        self.num1 = [self.num31020[i]/100 for i in range(240)]
        self.num2 = [self.num31020[i]%100/10 for i in range(240)]
        self.num3 = [self.num31020[i]%100%10 for i in range(240)]

        self.unm100 = zip([0,1,2,3,4,5,6,7,8,9],[self.num1.index(0),self.num1.index(1),self.num1.index(2),self.num1.index(3),self.num1.index(4),self.num1.index(5),self.num1.index(6),self.num1.index(7),self.num1.index(8),self.num1.index(9)])
        self.unm10 = zip([0,1,2,3,4,5,6,7,8,9],[self.num2.index(0),self.num2.index(1),self.num2.index(2),self.num2.index(3),self.num2.index(4),self.num2.index(5),self.num2.index(6),self.num2.index(7),self.num2.index(8),self.num2.index(9)])

        self.gga = [i[0] for i in self.unm100 if i[1] >= self.g_num]
        self.ggb = [i[0] for i in self.unm10 if i[1] >= self.g_num2]

        self.g1 = [i*100+j for i in self.gga for j in range(100)]
        self.g2 = [i*10+j for i in self.ggb for j in range(10)]

#Group 1
        self.group1 = [[0,1,10,11],[2,3,12,13],[4,5,14,15],[6,7,16,17],[8,9,18,19],
[20,21,30,31],[22,23,32,33],[24,25,34,35],[26,27,36,37],[28,29,38,39],
[40,41,50,51],[42,43,52,53],[44,45,54,55],[46,47,56,57],[48,49,58,59],
[60,61,70,71],[62,63,72,73],[64,65,74,75],[66,67,76,77],[68,69,78,79],
[80,81,90,91],[82,83,92,93],[84,85,94,95],[86,87,96,97],[88,89,98,99]]

#Group 2
        self.group2 = [[0,1,2,3,4,10,11,12,13,14,20,21,22,23,24,30,31,32,33,34],
[5,6,7,8,9,15,16,17,18,19,25,26,27,28,29,35,36,37,38,39],
[40,41,42,43,44,50,51,52,53,54,60,61,62,63,64,70,71,72,73,74],
[45,46,47,48,49,50,55,56,57,58,59,65,66,67,68,69,75,76,77,78,79],
[80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]]

#Group 3
        self.group3 = [[0],
[1,10],
[2,11,20],
[3,12,21,30],
[4,13,22,31,40],
[5,14,23,32,41,50],
[6,15,24,33,42,51,60],
[7,16,25,34,43,52,61,70],
[8,17,26,35,44,53,62,71,80],
[9,18,27,36,45,54,63,72,81,90],
[19,28,37,46,55,64,73,82,91],
[29,38,47,56,65,74,83,92],
[39,48,57,66,75,84,93],
[49,58,67,76,85,94],
[59,68,77,86,95],
[69,78,87,96],
[79,88,97],
[89,98],
[99]]
        self.group3b = [[0],
[1,10,100],
[2,11,20,101,110,200],
[3,12,21,30,102,111,120,201,210,300],
[4,13,22,31,40,103,112,121,130,202,211,220,301,310,400],
[5,14,23,32,41,50,104,113,122,131,140,203,212,221,230,302,311,320,401,410,500],
[6,15,24,33,42,51,60,105,114,123,132,141,150,204,213,222,231,240,303,312,321,330,402,411,420,501,510,600],
[7,16,25,34,43,52,61,70,106,115,124,133,142,151,160,205,214,223,232,241,250,304,313,322,331,340,403,412,421,430,502,511,520,601,610,700],
[8,17,26,35,44,53,62,71,80,107,116,125,134,143,152,161,170,206,215,224,233,242,251,260,305,314,323,332,341,350,404,413,422,431,440,503,512,521,530,602,611,620,701,710,800],
[9,18,27,36,45,54,63,72,81,90,108,117,126,135,144,153,162,171,180,207,216,225,234,243,252,261,270,306,315,324,333,342,351,360,405,414,423,432,441,450,504,513,522,531,540,603,612,621,630,702,711,720,801,810,900],
[19,28,37,46,55,64,73,82,91,109,118,127,136,145,154,163,172,181,190,208,217,226,235,244,253,262,271,280,307,316,325,334,343,352,361,370,406,415,424,442,451,460,505,514,523,532,541,550,604,613,622,631,640,703,712,721,730,802,811,820,901,910],
[29,38,47,56,65,74,83,92,119,128,137,146,155,164,173,182,191,209,218,227,236,245,254,263,272,281,290,308,317,326,335,344,353,362,371,380,407,416,425,443,452,461,470,506,515,524,533,542,551,560,605,614,623,632,641,650,704,713,722,731,740,803,812,821,830,902,911,920],
[39,48,57,66,75,84,93,129,138,147,156,165,174,183,192,219,228,237,246,255,264,273,282,291,309,318,327,336,345,354,363,372,381,390,408,417,426,444,453,462,471,480,507,516,525,534,543,552,561,570,606,615,624,633,642,651,660,705,714,723,732,741,750,804,813,822,831,840,903,912,921,930],
[49,58,67,76,85,94,139,148,157,166,175,184,193,229,238,247,256,265,274,283,292,319,328,337,346,355,364,373,382,391,409,418,427,445,454,463,472,481,490,508,517,526,535,544,553,562,571,580,607,616,625,634,643,652,661,670,706,715,724,733,742,751,760,805,814,823,832,841,850,904,913,922,931,940],
[59,68,77,86,95,149,158,167,176,185,194,239,248,257,266,275,284,293,329,338,347,356,365,374,383,392,419,428,446,455,464,473,482,491,509,518,527,536,545,554,563,572,581,590,608,617,626,635,644,653,662,671,680,707,716,725,734,743,752,761,770,806,815,824,833,842,851,860,905,914,923,932,941,950],
[69,78,87,96,159,168,177,186,195,249,258,267,276,285,294,339,348,357,366,375,384,393,429,447,456,465,474,483,492,519,528,537,546,555,564,573,582,591,609,618,627,636,645,654,663,672,681,690,708,717,726,735,744,753,762,771,780,807,816,825,834,843,852,861,870,906,915,924,933,942,951,960],
[79,88,97,169,178,187,196,259,268,277,286,295,349,358,367,376,385,394,448,457,466,475,484,493,529,538,547,556,565,574,583,592,619,628,637,646,655,664,673,682,691,709,718,727,736,745,754,763,772,781,790,808,817,826,835,844,853,862,871,880,907,916,925,934,943,952,961,970],
[89,98,179,188,197,269,278,287,296,359,368,377,386,395,449,458,467,476,485,494,539,548,557,566,575,584,593,629,638,647,656,665,674,683,692,719,728,737,746,755,764,773,782,791,809,818,827,836,845,854,863,872,881,890,908,917,926,935,944,953,562,971,980],
[99,189,198,279,288,297369,378,387,396,459,468,477,486,495,549,558,567,576,585,594,639,648,657,666,675,684,693,729,738,747,756,765,774,783,792,819,828,837,846,855,864,873,882,891,909,918,927,936,945,954,963,972,981,990],
[199,199,289,298,379,388,397,469,478,487,496,559,568,577,586,595,649,658,667,676,685,694,739,748,757,766,775,784,793,829,838,847,856,865,874,883,892,919,928,937,946,955,964,973,982,991],
[299,389,398,479,488,497,569,578,587,596,659,668,677,686,695,749,758,767,776,785,794,839,848,857,866,875,884,893,929,938,947,956,965,974,983,992],
[399,489,498,579,588,597,669,678,687,696,759,768,777,786,795,849,858,867,876,885,894,939,948,957,966,975,984,993],
[499,589,598,679,688,697,769,778,787,796,859,868,877,886,895,949,958,967,976,985,994],
[599,689,698,779,788,797,869,878,887,896,959,968,977,986,995],
[699,789,798,879,888,897,969,978,987,996],
[799,889,898,979,988,997],
[899,989,998],
[999]]
#当選回数が多い、31までのミニ数字
        self.group3c = [9,14,2,18,0,22,26,17,21,8,4,7,31,19,28,1]
#Group 4　ゴロ合わせ
        self.group4 = [7,9,10,14,17,23,24,28,29,41,43,44,45,50,64,70,72,76,81,83,84,90,93,
109,110,119,141,139,148,168,175,178,181,184,193,
235,251,252,253,291,296,298,
318,324,326,333,343,348,354,369,374,375,382,387,383,389,392,396,398,
410,420,461,463,489,490,491,493,
510,534,538,539,546,549,551,553,556,564,567,573,579,584,585,588,589,590,593,594,596,
610,631,634,640,648,653,674,681,693,696,
710,718,725,735,753,756,765,773,775,790,
804,810,813,814,815,818,819,820,824,827,828,831,833,838,840,845,848,851,867,870,871,873,874,875,881,883,890,891,893,
894,
910,919,925,931,933,935,961,962,963,965,969]

#Group 5
        self.group5 = [[i for i in range(100)],
[100+i for i in range(100)],
[200+i for i in range(100)],
[300+i for i in range(100)],
[400+i for i in range(100)],
[500+i for i in range(100)],
[600+i for i in range(100)],
[700+i for i in range(100)],
[800+i for i in range(100)],
[900+i for i in range(100)]]

#Group 6
        self.group6 = [[12,13,14,15,16,17,18,19,23,24,25,26,27,28,29,34,35,36,37,38,39,45,46,47,48,49,56,57,58,59,67,68,69,78,79,89],
[1,2,3,4,5,6,7,8,9,11,22,33,44,55,66,77,88,99],
[123,124,125,126,127,128,129,134,135,
136,137,138,139,145,146,147,148,149,156,157,158,159,167,168,169,
178,179,189,],
[112,113,114,115,116,117,118,119,122,133,144,155,166,177,188,199],
[234,235,236,237,238,239,245,246,247,248,249,
256,257,258,259,267,268,269,278,279,289],
[223,224,225,226,227,228,229,233,244,255,266,277,288,299],
[345,346,347,348,349,356,357,358,359,367,368,369,378,379,389],
[334,335,336,337,338,339,344,355,366,377,388,399],
[456,457,458,459,467,468,469,478,479,489],
[445,446,447,448,449,455,466,477,488,499],
[567,568,569,578,579,589],
[556,557,558,559,566,577,588,599],
[678,679,689],
[667,668,669,677,688,699],
[789],
[778,779,788,799],
[889,899]]

#全ストレート番号
    def make_straight(self):
        rs3 = [i for i in xrange(1000)]
        return rs3
#全ボックス番号
    def make_box(self,rs3):
        rs3a = [i/100 for i in rs3]
        rs3b = [i%100/10 for i in rs3]
        rs3c = [i%100%10 for i in rs3]
        rs3d = [sorted([rs3a[i],rs3b[i],rs3c[i]]) for i in range(len(rs3))]
        rs3 = [i[0]*100+i[1]*10+i[2] for i in rs3d]
        return rs3
#過去特定回数に出現したストレート数字
    def make_numbers3(self,num):
        rs3 = [self.full_num3[i] for i in range(num)]
        return rs3
#過去特定回数に出現したミニ数字
    def make_numbersmini(self,num):
        self.e = [self.full_num3[i]%100 for i in range(num)]
        return self

#当選回数が多いボックス数字
    def make_n3box_many(self):
        rs3 = sorted(set([89,24,349,157,59,278,169,138,127,459,368,247,234,189,18,279,129,679,589,568,458,14,369,23,389,139,126,237,358,49,379,28,468,178,268,19,137,147,469,179,36,168,135,79,45,57,167,346,245,68,47,16,478,378,37,269,259,579,678,58,26,457,367,124,128,136,236,257,489,479,29,15,159,345,789,289,246,123,69,17,146,347,249,145,66,78,567,35,359,148,248,238,258,67,569,578,267,158,06,34]))
        return rs3

#ナンバーズ3ミニ
#makeMiniNumber
#100までの数列を作成
    def makeMiniNumber1(self):
        e = [i for i in range(100)]
        return e
#当選数字の中で出現回数の多い順より特定数個抽出
    def makeMiniNumber2(self,num,e):
        mini_240_counta = sorted(set(zip(e,[self.full_mini.count(i) for i in e])))
        mini_240_counta.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)
        e = [mini_240_counta[i][0] for i in range(num)]
        return e
#Group1から３において当選数字が含まれるグループを削除
    def makeMiniNumber3(self,e):
        xx =[self.full_mini[i] for i in range(21)]
        xy = []
        for i in xx:
            for j in self.group1:
                try:
                    if not(j.index(i)):
                        xy.append(j)
                except:pass
        xy1 = sorted(set([i[j] for i in xy for j in range(len(i))]))
        print(xy1)
        xz=[]
        for i in xx:
            for j in self.group2:
                try:
                    if not(j.index(i)):
                        xz.append(j)
                except:pass
        xz1 = sorted(set([i[j] for i in xz for j in range(len(i))]))
        print(xz1)
        xzza=[]
        for i in xx:
            for j in self.group3:
                try:
                    if not(j.index(i)):
                        xzza.append(j)
                except:pass
        xzza1 = sorted(set([i[j] for i in xzza for j in range(len(i))]))
        print(xzza1)
        #xyz = sorted(set(xy1+xz1+xzza1))
        xyz = sorted(set(xzza1))
        for i in xyz:
            try:
                e.remove(i)
            except:e
        return e
#数式をかける
    def numbersMini_math_effect(self,sin_arg,e):
        nmme = [abs(int(i*math.sin(sin_arg)+i*math.cos(sin_arg))) for i in e]
        return nmme
#当選日付と同じミニ当選数字を削除
    def deldaymini(self,e):
        ddm = [i for i in e if (i == int(year)/100) or (i == int(year)%100) or (i == int(month)) or (i == int(day))]
        for i in ddm:
            try:e.remove(i)
            except:e
        return e
#過去100回のミニの出現回数が特定回以上なら削除
    def delupmini(self,num,e):
        ls = [i for i in range(100)]
        gls = [[self.full_mini[i] for i in range(100)].count(j) for j in ls]
        dic_ls = zip(ls,gls)
        dic_lsa = [i for i,j in dic_ls if j >= num]
        for i in dic_lsa:
            try:e.remove(i)
            except:e
        return e
#十の位と一の位の合計値が過去特定回数の十の位と一の位の合計値と同じなら削除
    def delsummini(self,num,e):
        dsm = [i for i in [k for k in range(100)] for j in range(num) if i/10+i%10 == self.num2[j]+self.num3[j]]
        for j in dsm:
            try:e.remove(i)
            except:e
        return e
#過去特定回数のミニ当選数字を削除
    def delstmini(self,num,e):
        for i in [self.full_mini[j] for j in range(num)]:
            try:e.remove(i)
            except:e
        return e
#過去特定回数のミニ当選数字の十の位と一の位を逆にしたものを削除
    def delboxmini(self,num,e):
        dbm = [i%10*10+i/10 for i in [self.full_mini[j] for j in range(num)]]
        for i in dbm:
            try:e.remove(i)
            except:e
        return e
#Use Filter G for mini
    def useGmini(self,e):
        ugm2 = [i%100 for i in self.g2]
        ugmm = [i for i in [k for k in range(100)] for j in ugm2 if i == j]
        for i in ugmm:
            try:e.remove(i)
            except:e
        return e
#過去特定回数以上出現していないミニの当選数字を削除
    def delbeforemini(self,num,e):
        full_mini = [i%100 for i in self.full_num3]
        nf_mini = sorted(set([full_mini[i] for i in range(len(self.full_num3)-1) if full_mini.index(full_mini[i]) >= num]))
        dbm = [i for i in e for j in nf_mini if i == j]
        for i in dbm:
            try:e.remove(i)
            except:e
        return e
#0〜31までの数字を削除
    def del031(self,e):
        for i in range(31):
            try:
                e.remove(i)
            except:e
        return e
#ナンバーズ3ストレート・ボックス・セット
#makeNumber
#1000までの数列を作成
    def makeNumber1(self):
        return [i for i in range(1000)]
#ミニの予想数字をベースに３桁の数字を作成
    def makeNumber2(self,e):
        return [i*100+j for i in [k/100 for k in sorted(set([self.full_num3[m] for m in range(20)]))] for j in e]

#過去の当選数字のボックス数字の中で出現回数の多い順より特定数個抽出
    def makeNumber3(self,num,rs3):
        num31020_counta = sorted(set(zip(rs3,[self.make_box(self.full_num3).count(i) for i in rs3])))
        num31020_counta.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)
        rs3 = [num31020_counta[i][0] for i in range(num)]
        return rs3
#当選数字を３桁の組みに分けて、それらの数字の出現回数の上位の組み合わせで数字を作成
    def makeNumber4(self,num):
        gm1 = [self.full_num3[i]/10 for i in range(num)]
        gm2 = [self.full_num3[i]%100 for i in range(num)]
        gm3 = [self.full_num3[i]/100+self.full_num3[i]%100%10 for i in range(num)]
        gm1c = sorted(set(zip(gm1,[gm1.count(i) for i in gm1])))
        gm2c = sorted(set(zip(gm2,[gm2.count(i) for i in gm2])))
        gm3c = sorted(set(zip(gm3,[gm3.count(i) for i in gm3])))
        gm1c.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)
        gm2c.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)
        gm3c.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)
        gm1a = [i*100+gm1c[j][0] for i in range(10) for j in range(1)]
        gm2a = [i*100+gm2c[j][0] for i in range(10) for j in range(1)]
        gm3a = [i*100+gm3c[j][0] for i in range(10) for j in range(1)]
        rs = gm1a+gm2a+gm3a
        return rs
#数式をかける
    def numbers3_math_effect(self,sin_arg,rs3):
        n3me = [abs(int(i*math.sin(sin_arg)+i*math.cos(sin_arg))) for i in rs3]
        return n3me
#過去特定回数のストレート数字を削除
    def delst(self,num,rs3):
        for i in [self.full_num3[j] for j in range(num)]:
            try:rs3.remove(i)
            except:rs3
        return rs3
#過去特定回数のボックスの当選数字を削除
    def delbox(self,reverse_num,rs3):
        num_a = [self.full_num3[i]/100 for i in range(reverse_num)]
        num_b = [self.full_num3[i]%100/10 for i in range(reverse_num)]
        num_c = [self.full_num3[i]%100%10 for i in range(reverse_num)]

        reverse1 = [(num_a[i]*100+num_c[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse2 = [(num_b[i]*100+num_a[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse3 = [(num_b[i]*100+num_c[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse4 = [(num_c[i]*100+num_b[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse5 = [(num_c[i]*100+num_a[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_n3 = reverse1+reverse2+reverse3+reverse4+reverse5
        reverse_n3 = sorted(set(reverse_n3))
        for i in reverse_n3:
            try:rs3.remove(i)
            except:rs3
        return rs3
#過去特定回数のミニ当選数字をベースにしたストレート数字を削除
    def delst4mini(self,num,rs3):
        stdsm = [i*100+j for i in range(10) for j in [self.full_mini[k] for k in range(num)]]
        for i in stdsm:
            try:rs3.remove(i)
            except:rs3
        return rs3
#各桁の合計値が過去特定回数の各桁の合計値と同じなら削除
    def delsum(self,num,rs3):
        ds = [i for i in range(1000) for j in range(num) if (i/100+i%100/10+i%100%10) == (self.num1[j]+self.num2[j]+self.num3[j])]
        for i in ds:
            try:rs3.remove(i)
            except:rs3
        return rs3
#合計値特定の範囲以外の数字を削除
    def delsumrange(self,low,high,rs3):
        ds = [i for i in range(1000) if ((i/100+i%100/10+i%100%10) < low or (i/100+i%100/10+i%100%10) > high)]
        for i in ds:
            try:rs3.remove(i)
            except:rs3
        return rs3
#過去1度も出現していない数字を削除
    def delzero(self,rs3):
        box = sorted(set(self.make_box(self.make_straight())))
        fullbox = sorted(set(self.make_box(self.full_num3)))
        dic_3b = sorted(set(zip(box,[fullbox.count(i) for i in box])))
        dz3 = [i for i in rs3 for j in dic_3b if j[1] == 0 and i == j[0]]
        for i in dz3:
            try:rs3.remove(i)
            except:rs3
        return rs3
#Use Filter G
    def useG(self,rs3):
        ug = [i for i in [k for k in range(1000)] for j in self.g1 if i == j]
        for i in ug:
            try:rs3.remove(i)
            except:rs3
        return rs3
#ゾロ目を削除
    def delzoro3(self,rs3):
        zoro3 = [i*100+i*10+i for i in range(10)]
        for i in zoro3:
            try:rs3.remove(i)
            except:rs3
        return rs3
#過去特定回数以上出現していない当選数字を削除
    def delbefore(self,num,rs3):
        nf = sorted(set([i for i in self.full_num3 if self.full_num3.index(i) >= num]))
        dbm = [i for i in rs3 for j in nf if i == j]
        dbm2 = self.make_box(dbm)
        for i in dbm2:
            try:rs3.remove(i)
            except:rs3
        return rs3
#パターンに当てはまらない数字を削除
    def delpattern(self,array,rs3):
        pattern = [i for i in array]
        for i in pattern:
            for j in rs3:
                try:
                    if j/10 != i or j%100 != i:
                        rs3.remove(j)
                except:rs3
        return rs3
#Today
    def today_numbers3(self,rs3):
        today1 = [786,517,113,697,468,174,181,498,927,289,509,249,644,816,983,802,
621,586,58,721,151]
        today1a = set(sorted(self.make_box(today1)))
        for i in today1a:
            try:
                rs3.remove(i)
            except:rs3
        return rs3
#特定回数の百の桁と十の桁の組み合わせを削除
    def del100plus10(self,rs3):
        num100 = set(sorted([self.full_num3[i]/100 for i in range(10)]))
        num10 = set(sorted([self.full_num3[i]%100/10 for i in range(10)]))
        num100plus10 = set(sorted([i*100+j*10+k for i in num100 for j in num10 for k in range(10)]))
        #print(num100)
        #print(num10)
        #print(num100plus10)
        for i in num100plus10:
            try:
                rs3.remove(i)
            except:rs3
        return rs3

#Numbers 4
#Numbers4クラス
class numbers4(object):
    def __init__(self):
#過去のストレート当選数字
        self.full_num34 = [i[1] for i in list4]

#過去全てのストレート数字と当選回数
        self.nfc100 = list(zip(self.full_num34,[self.full_num34.count(i) for i in self.full_num34]))

#過去240回の各桁数列
        self.nums4240 = [self.full_num34[i] for i in range(240)]
        self.num1a = [self.nums4240[i]/1000 for i in range(240)]
        self.num2a = [self.nums4240[i]%1000/100 for i in range(240)]
        self.num3a = [self.nums4240[i]%1000%100/10 for i in range(240)]
        self.num4a = [self.nums4240[i]%1000%100%10 for i in range(240)]

#Filter G
        self.g_num4 = 20
#各位が特定回以上出現していない場合に削除するフィルタ
        self.una1000 = [(0,self.num1a.index(0)),(1,self.num1a.index(1)),(2,self.num1a.index(2)),(3,self.num1a.index(3)),(4,self.num1a.index(4)),(5,self.num1a.index(5)),(6,self.num1a.index(6)),(7,self.num1a.index(7)),(8,self.num1a.index(8)),(9,self.num1a.index(9))]
        self.unr1000 = [(0,float(self.una1000[0][1])/100),(1,float(self.una1000[1][1])/100),(2,float(self.una1000[2][1])/100),(3,float(self.una1000[3][1])/100),(4,float(self.una1000[4][1])/100),(5,float(self.una1000[5][1])/100),(6,float(self.una1000[6][1])/100),(7,float(self.una1000[7][1])/100),(8,float(self.una1000[8][1])/100),(9,float(self.una1000[9][1])/100)]
        self.ggd = [i[0] for i in self.una1000 if i[1] >= self.g_num4]
        self.ga = [i*1000+j for i in self.ggd for j in range(1000)]

#全ストレート番号
    def make_straight(self):
        rs = [i for i in range(10000)]
        return rs

#3000未満の数字を除外したベース数字
    def make_straight_under3000(self):
        rs = [i for i in range(3000,10000)]
        return rs

#全ボックス番号
    def make_box(self,rs):
        rsa = [i/1000 for i in rs]
        rsb = [i%1000/100 for i in rs]
        rsc = [i%1000%100/10 for i in rs]
        rsd = [i%1000%100%10 for i in rs]
        rse = [sorted([rsa[i],rsb[i],rsc[i],rsd[i]]) for i in range(len(rs))]
        rs = [i[0]*1000+i[1]*100+i[2]*10+i[3] for i in rse]
        return rs
#過去特定回数に出現したストレート数字
    def make_numbers4(self,num):
        rs = [self.full_num34[i] for i in range(num)]
        return rs
#過去の全ての回数の当選数字のボックス数字の中で出現回数の多い順より特定数個抽出
    def makeNumber(self,num,rs):
        nfc100aa = sorted(set(zip(rs,[self.make_box(self.full_num34).count(i) for i in rs])))
        nfc100aa.sort(cmp=lambda x,y:cmp(x[1],y[1]),reverse=True)
        rs = [nfc100aa[i][0] for i in range(num)]
        return rs

#過去のストレート数字を削除
    def delst(self,rs):
        for i in self.full_num34:
            try:
                rs.remove(i)
            except:pass
        return rs
#ボックスの当選数字を削除
    def delbox(self,reverse_num,rs):
        num_a = [self.full_num34[i]/1000 for i in range(reverse_num)]
        num_b = [self.full_num34[i]%1000/100 for i in range(reverse_num)]
        num_c = [self.full_num34[i]%1000%100/10 for i in range(reverse_num)]
        num_d = [self.full_num34[i]%1000%100%10 for i in range(reverse_num)]

        reverse_a = [(num_a[i]*1000+num_b[i]*100+num_d[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse_b = [(num_a[i]*1000+num_c[i]*100+num_b[i]*10+num_d[i]) for i in range(reverse_num)]
        reverse_c = [(num_a[i]*1000+num_c[i]*100+num_d[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_d = [(num_a[i]*1000+num_d[i]*100+num_b[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse_e = [(num_a[i]*1000+num_d[i]*100+num_c[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_f = [(num_b[i]*1000+num_a[i]*100+num_c[i]*10+num_d[i]) for i in range(reverse_num)]
        reverse_g = [(num_b[i]*1000+num_a[i]*100+num_d[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse_h = [(num_b[i]*1000+num_d[i]*100+num_a[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse_i = [(num_b[i]*1000+num_d[i]*100+num_c[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse_j = [(num_b[i]*1000+num_c[i]*100+num_a[i]*10+num_d[i]) for i in range(reverse_num)]
        reverse_k = [(num_b[i]*1000+num_c[i]*100+num_d[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse_l = [(num_c[i]*1000+num_a[i]*100+num_b[i]*10+num_d[i]) for i in range(reverse_num)]
        reverse_m = [(num_c[i]*1000+num_a[i]*100+num_d[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_n = [(num_c[i]*1000+num_b[i]*100+num_a[i]*10+num_d[i]) for i in range(reverse_num)]
        reverse_o = [(num_c[i]*1000+num_b[i]*100+num_d[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse_p = [(num_c[i]*1000+num_d[i]*100+num_a[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_q = [(num_c[i]*1000+num_d[i]*100+num_b[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse_r = [(num_d[i]*1000+num_a[i]*100+num_b[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse_s = [(num_d[i]*1000+num_a[i]*100+num_c[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_t = [(num_d[i]*1000+num_b[i]*100+num_a[i]*10+num_c[i]) for i in range(reverse_num)]
        reverse_u = [(num_d[i]*1000+num_b[i]*100+num_c[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse_v = [(num_d[i]*1000+num_c[i]*100+num_a[i]*10+num_b[i]) for i in range(reverse_num)]
        reverse_w = [(num_d[i]*1000+num_c[i]*100+num_b[i]*10+num_a[i]) for i in range(reverse_num)]
        reverse_n4 = reverse_a+reverse_b+reverse_c+reverse_d+reverse_e+reverse_f+reverse_g+reverse_h+reverse_i+reverse_j+reverse_k+reverse_l+reverse_m+reverse_n+reverse_o+reverse_p+reverse_q+reverse_r+reverse_s+reverse_t+reverse_u+reverse_v+reverse_w

        for i in reverse_n4:
            try:rs.remove(i)
            except:rs
        return rs
#過去5回の千の位が同じ数字の列を削除
    def del1000(self):
        d1000a = [i for i in range(10)]
        d1000b = [self.num1a[i] for i in range(5)]
        for i in d1000b:
            try:d1000a.remove(i)
            except:d1000a
        return d1000a

#Use Filter G2
    def useG2(self,rs):
        ug2 = [i for i in [k for k in range(10000)] for j in self.ga if i == j]
        for i in ug2:
            try:rs.remove(i)
            except:rs
        return rs
#各桁の合計が同じ数字を削除
    def delsum4(self,num,rs):
        ds4 = [i for i in range(10000) for j in range(num) if (i/1000+i%1000/100+i%1000%100/10+i%1000%100%10) == (self.num1a[j]+self.num2a[j]+self.num3a[j]+self.num4a[j])]
        for i in ds4:
            try:rs.remove(i)
            except:rs
        return rs
#合計値が特定範囲以外の数字を削除
    def delsumrange(self,low,high,rs):
        ds4 = [i for i in range(10000) if (i/1000+i%1000/100+i%1000%100/10+i%1000%100%10) < low or (i/1000+i%1000/100+i%1000%100/10+i%1000%100%10) > high]
        for i in ds4:
            try:rs.remove(i)
            except:rs
        return rs
#過去1度も出現していない数字を削除
    def delzero(self,rs):
        st = sorted(set(self.make_straight()))
        fullst = sorted(set(self.full_num34))
        dic_4b = sorted(set(zip(st,[fullst.count(i) for i in st])))
        dz4 = [i for i in rs for j in dic_4b if j[1] == 0 and i == j[0]]
        for i in dz4:
            try:rs.remove(i)
            except:rs
        return rs
#ゾロ目を削除
    def delzoro4(self,rs):
        for i in [i*1000+i*100+i*10+i for i in range(10)]:
            try:rs.remove(i)
            except:rs
        return rs
#トリプルの数字を削除
    def deltriple(self,rs):
        rs3z = []
        for i in range(10):
            for j in range(10):
                try:
                    rs3z.append(i*1000+i*100+i*10+j)
                    rs3z.append(j*1000+i*100+i*10+i)
                    rs3z.append(i*1000+j*100+i*10+i)
                    rs3z.append(i*1000+i*100+j*10+i)
                except:pass
        rs3z = set(sorted(rs3z))
        for i in rs3z:
            try:
                rs.remove(i)
            except:pass
        return rs
#ダブルの数字を削除
    def deldouble(self,rs):
        d4 = []
        for i in range(10):
            for j in range(10):
                try:
                    d4.append(i*1000+i*100+j*10+j)
                    d4.append(i*1000+j*100+i*10+j)
                    d4.append(i*1000+j*100+j*10+i)
                    d4.append(j*1000+i*100+i*10+j)
                    d4.append(j*1000+i*100+j*10+i)
                    d4.append(j*1000+j*100+i*10+i)
                except:pass
        d4 = set(sorted(d4))
        for i in d4:
            try:
                rs.remove(i)
            except:pass
        return rs
#過去特定回数以上出現していない当選数字を削除
    def delbefore(self,num,rs):
        nf = sorted(set([i for i in self.full_num34 if self.full_num34.index(i) >= num]))
        dbm = [i for i in rs for j in nf if i == j]
        dbm2 = self.make_box(dbm)
        for i in dbm2:
            try:rs.remove(i)
            except:rs
        return rs

#過去に出た当選番号の下2桁のを削除
    def dellow2(self,num,rs):
        num43_a = [i%100 for i in self.full_num34]
        num43 = sorted(num43_a[0:num])
        for i in rs:
            for j in num43:
                try:
                    if j == i%100:
                        rs.remove(i)
                except:pass
        return rs

#過去に出た当選番号の下3桁のを削除
    def dellow3(self,num,rs):
        num43_a = [i%1000 for i in self.full_num34]
        num43 = sorted(num43_a[0:num])
        for i in rs:
            for j in num43:
                try:
                    if j == i%1000:
                        rs.remove(i)
                except:pass
        return rs

#ナンバーズ予想スクリプト
class allnumbers(object):
    def __init__(self):
#Numbers3予想
        n3=numbers3()
#mini
        ee = n3.makeMiniNumber1()
        n3.del031(ee)
        ee = ee+n3.group3c
        n3.delstmini(39,ee)
        n3.delbeforemini(200,ee)
        #n3.makeMiniNumber3(ee)
        e = ee
        #e = sorted(set([random.choice(ee) for i in range(20)]))
        n3a = sorted(set(zip(e,[n3.full_mini.count(i) for i in e])))
#straight
        rs3 = n3.makeNumber2(e)
        #rs3 = n3.make_n3box_many()
        n3.delst(240,rs3)
        #n3.del100plus10(rs3)
        rs3 = sorted(set(n3.make_box(rs3)))
        n3.delbox(40,rs3)
        n3.delzoro3(rs3)
        #rs3 = set(sorted([random.choice(rs3) for i in range(10)]))
        n3b = sorted(set(zip(rs3,[n3.make_box(n3.full_num3).count(i) for i in rs3])))
#Numbers4予想
        n4 = numbers4()
        rs = n4.make_straight_under3000()
        rs = n4.make_straight()
        n4.delst(rs)
        n4.dellow2(50,rs)
        n4.dellow3(500,rs)
        rs = sorted(set(n4.make_box(rs)))
        n4.delbox(240,rs)
        n4.delzoro4(rs)
        n4.deltriple(rs)
        n4.deldouble(rs)
        #rs = set(sorted([random.choice(rs) for i in range(200)]))
        n4a = sorted(set(zip(rs,[n4.make_box(n4.full_num34).count(i) for i in rs])))

#File writing
        sssmini = str([format(i[0],'02') for i in n3a])
        #print(str([i[0] for i in n3a]) + "\n")
        sss3 = str([format(i[0],'03') for i in n3b])
        print(str(sss3)+"\n")
        #print(str(rs3)+"\n")
        sss4 = str([format(i[0],'04') for i in n4a])
        print(str(sss4) + "\n")
        #print(str(rs)+"\n")
        with open("numbers.txt","w") as f:
#ミニ予想数字
            f.write("◇ミニ予想数字\n"+ str([i[0] for i in n3a]) + "\n"+str(len([i[0] for i in n3a]))+"個\n")
            #f.write("◇ミニ予想数字\n"+ sssmini + "\n"+str(len([i[0] for i in n3a]))+"個\n")
            #f.write("◇ミニ予想数字 "+ str(n3a) + "\n")
#Numbers3予想数字
            f.write("◇ナンバーズ3予想数字\n"+sss3+"\n"+str(len([i[0] for i in n3b]))+"個\n")
            #f.write("◇ナンバーズ3予想数字"+str(n3b)+"\n")
            #f.write("◇ナンバーズ3予想数字\n"+str(rs3)+"\n")
            #f.write("◇ナンバーズ3予想数字\n"+ str([i for i in n3b]) + "\n"+str(len([i[0] for i in n3b]))+"個\n")
#Numbers4予想数字
            #f.write("◇ナンバーズ4予想数字\n"+str(rs)+"\n")
            #f.write("◇ナンバーズ4予想数字\n"+ str([i for i in n4a]) + "\n"+str(len([i[0] for i in n4a]))+"個\n")
            f.write("◇ナンバーズ4予想数字\n"+ sss4 + "\n" + str(len([i[0] for i in n4a])) + "個\n")
            #f.write("◇ナンバーズ4予想数字 " + str(n4a) + "\n")
            #f.write("◇ナンバーズ3の過去240回の当選数字(当選数字の横の数字は当選回数)\n" + str(n3.num31020_count) + "\n")
            #f.write("◇ナンバーズ4過去240回の当選数字\n" + str(n4.nfc100) + "\n")
            #f.write("◇ミニ過去240回の当選数字(予想数字の横の値は当選回数)\n" + str(n3.mini_240_count) + "\n")
            #f.write("◇0～99までの数字のミニ過去240回の当選状況(予想数字の横の値は過去240回の当選回数)\n" + str(n3.dic_mini_full) + "\n")
            f.close()
            print("Finish")

#ロト class
class loto(object):
    def __init__(self):
        pass
    def six(self):
        loto_base = [i for i in range(1,44)]
        yn = len(loto6)
        la = [loto6[i][0] for i in range(yn)]
        lb = [loto6[i][1] for i in range(yn)]
        lc = [loto6[i][2] for i in range(yn)]
        ld = [loto6[i][3] for i in range(yn)]
        le = [loto6[i][4] for i in range(yn)]
        lf = [loto6[i][5] for i in range(yn)]
        la1,lb1,lc1,ld1,le1,lf1=loto_base,loto_base,loto_base,loto_base,loto_base,loto_base
        for k in la:
              try:
                  la1.remove(k)
              except:
                  pass
        for k in lb:
              try:
                  lb1.remove(k)
              except:
                  pass
        for k in lc:
              try:
                  lc1.remove(k)
              except:
                  pass
        for k in ld:
              try:
                  ld1.remove(k)
              except:
                  pass
        for k in le:
              try:
                  le1.remove(k)
              except:
                  pass
        for k in lf:
              try:
                  lf1.remove(k)
              except:
                  pass
        lss = sorted(set(la+lb+lc+ld+le+lf))
        for j in lss:
            try:
                lss.remove(j)
            except:
                lss
        for  j2 in deleteloto6:
            try:
                lss.remove(j2)
            except:
                lss
        #print(lss)
        lss2 = sorted(set(la1+lb1+lc1+lc1+ld1+le1))
        for j3 in lss:
            try:
                lss.remove(j3)
            except:
                lss
        for  j4 in deleteloto6:
            try:
                lss2.remove(j4)
            except:
                lss2
        #print(lss2)
        loto_e = []
        while len(loto_e) < 6:
            la2 = random.randrange(1,44)
            lb2 = random.randrange(1,44)
            lc2 = random.randrange(1,44)
            ld2 = random.randrange(1,44)
            le2 = random.randrange(1,44)
            lf2 = random.randrange(1,44)
            if(la2 == la[0] and la2 == la[1]):
                la2 = random.choice(la)
            if(lb2 == lb[0] and lb2 == lb[1]):
                lb2 = random.choice(lb)
            if(lc2 == lc[0] and lc2 == lc[1]):
                lc2 = random.choice(lc)
            #if(ld2 == ld[0] and ld2 == ld[1]):
            #    ld2 = random.choice(ld)
            #if(le2 == le[0] and le2 == le[1]):
            #    le2 = random.choice(le)
            #if(lf2 == lf[0] and lf2 == lf[1]):
            #    lf2 = random.choice(lf)
            loto_e = sorted(set([la2,lb2,lc2,ld2,le2,lf2]))
        print(loto_e)
        return loto_e
    def mini(self):
        miniloto_base = [i for i in range(1,32)]
        ynmini = len(lotomini)
        la = [lotomini[i][0] for i in range(ynmini)]
        lb = [lotomini[i][1] for i in range(ynmini)]
        lc = [lotomini[i][2] for i in range(ynmini)]
        ld = [lotomini[i][3] for i in range(ynmini)]
        le = [lotomini[i][4] for i in range(ynmini)]
        la1,lb1,lc1,ld1,le1=miniloto_base,miniloto_base,miniloto_base,miniloto_base,miniloto_base
        for k in la:
              try:
                  la1.remove(k)
              except:
                  pass
        for k in lb:
              try:
                  lb1.remove(k)
              except:
                  pass
        for k in lc:
              try:
                  lc1.remove(k)
              except:
                  pass
        for k in ld:
              try:
                  ld1.remove(k)
              except:
                  pass
        for k in le:
              try:
                  le1.remove(k)
              except:
                  pass
        ltt = sorted(set(la+lb+lc+ld+le))
        for j in bonus:
              try:
                  ltt.remove(j)
              except:
                  ltt
        for j2 in deleteminiloto:
              try:
                  ltt.remove(j2)
              except:
                  ltt
        ltt2 = sorted(set(la1+lb1+lc1+ld1+le1))
        for j3 in bonus:
              try:
                  ltt2.remove(j3)
              except:
                  ltt2
        for j4 in ltt2:
              try:
                  ltt2.remove(j4)
              except:
                  ltt2
        mini_e = []
        while len(mini_e) < 5:
            la2 = random.choice(ltt)
            lb2 = random.choice(ltt2)
            lc2 = continuation2[0]
            ld2 = continuation2[1]
            le2 = continuation2[2]
            if(la2 == la[0] and la2 == la[1]):
                la2 = random.choice(la)
            if(lb2 == lb[0] and lb2 == lb[1]):
                lb2 = random.choice(lb)
            if(lc2 == lc[0] and lc2 == lc[1]):
                lc2 = random.choice(lc)
            if(ld2 == ld[0] and ld2 == ld[1]):
                ld2 = random.choice(ld)
            if(le2 == le[0] and le2 == le[1]):
                le2 = random.choice(le)
            mini_e =sorted(set([la2,lb2,lc2,ld2,le2]))
        print(mini_e)
        return mini_e

class allloto(object):
    def __init__(self):
        lx=loto()
#File writing
        fl = open("loto.txt","w")
        fl.write("◇ロト予想数字\n")
        fl.write(str(lx.six()) + "\n")
        fl.write("◇ミニロト予想数字\n")
        fl.write(str(lx.mini()) + "\n")
        fl.close()
        print("Finish")

if __name__ == "__main__":
    allnumbers()
    allloto()
