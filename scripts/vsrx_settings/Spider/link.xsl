<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:xhtml="http://www.w3.org/1999/xhtml"
version="1.0">
<xsl:output
  method="html"
  encoding="utf-8"
  omit-xml-declaration="yes"
  doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
  doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
  indent="yes"
  media-type="application/xhtml+xml"/>
<xsl:template match="/">
  <xsl:apply-templates />
</xsl:template>
<xsl:template match="data">
<html lang="ja">
<head>
	<title><xsl:value-of select="./site-title/@title"/></title>
	<meta charset="utf-8" />
	<meta http-equiv="X-UA-Compatible" content="chrome=1" />
	<meta name="keywords" content="Bookmartks" />
	<meta name="auther" content="takamitu hamada" />
	<link rel="stylesheet" href="../Spider/core.css" type="text/css" />
	<link rel="stylesheet" href="../CSS/moon.css" type="text/css" />
	<style type="text/css">
		h1{
			-webkit-animation-duration:3s;
			-webkit-animation-name:fadeOutInOutSwirl;
			-moz-animation-duration:3s;
			-moz-animation-name:fadeOutInOutSwirl;
		}
		
		h2{
			-webkit-animation-delay:2500ms;
			-webkit-animation-duration:3s;
			-webkit-animation-name:fadeOutInOutSwirl2;
			-moz-animation-delay:2500ms;
			-moz-animation-duration:3s;
			-moz-animation-name:fadeOutInOutSwirl2;
		}
	</style>
</head>
<body>
	<header>
		<nav>
			<ul class="menu">
				<li><a href="../index.html">Top</a></li>
			</ul>
		</nav>
	</header>
	<div class="baselayer" id="main">
		<article class="spider_index">
  <h1><xsl:value-of select="./h1-title/@title"/></h1>
  <div class="fly">
    <xsl:apply-templates />
  </div>
		</article>
	</div>
</body>
<script type="text/javascript" src="../Spider/spider.js"></script>
<script type="text/javascript">
		spider("").load(function(){
			stroll.bind("#main ul");
		});
</script>
</html>
</xsl:template>
<xsl:template match="h2-item">
  <h2><xsl:value-of select="./@title"/></h2>
  <ul>
    <xsl:apply-templates/>
  </ul>
</xsl:template>
<xsl:template match="item">
    <li>
    <a>
      <xsl:attribute name="href">
	<xsl:value-of select="./title/@url" />
      </xsl:attribute>
      <xsl:attribute name="target">_blank</xsl:attribute>
      <xsl:value-of select="./title"/>
    </a>
    </li>
</xsl:template>
</xsl:stylesheet>
