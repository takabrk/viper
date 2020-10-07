#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os,sys,urllib2
from BeautifulSoup.BeautifulSoup import BeautifulSoup,Tag,NavigableString

html = """<!DOCTYPE html>
<html lang="ja">
<head>
</head>
<body></body>
</html>
"""

soup = BeautifulSoup(html)
soup.head.insert(0,Tag(soup,"title"))
soup.title.insert(0,NavigableString("テストページ"))
soup.head.insert(0,Tag(soup,"style"))
soup.head.style.string = """
body{
    background:#000000;
}
.baselayer{
    width:720px;
    height:600px;
    background:#ffffff;
    margin : 0 auto;
}
.test{
   width:100%;
   height:500px;
   margin:0;
   padding:0;
}
footer{
    background-color:#ff0000;
    height:100px;
}
"""

soup.body.insert(0,Tag(soup,"div"))
soup.body.div["class"] = "baselayer"
soup.body.div.insert(0,Tag(soup,"header"))
soup.body.div.header.insert(0,Tag(soup,"a"))
soup.body.div.header.a["href"] = "http://nightmare.osdn.jp"
soup.body.div.header.a["target"] = "_blank"
soup.body.div.header.a.string = "Top"
soup.body.div.insert(1,Tag(soup,"nav"))
soup.body.div.insert(2,Tag(soup,"article"))
soup.body.div.insert(3,Tag(soup,"footer"))
soup.body.div.footer.string = "Copyright@taka"
soup.body.div.article.insert(0,Tag(soup,"p"))
soup.body.div.p["class"] = "test"
soup.body.div.p.insert(0,NavigableString("BeuatifulSoupを活用しています。"))

f= open("test11.html","w")
f.write(soup.prettify())
print soup.prettify()
f.close()