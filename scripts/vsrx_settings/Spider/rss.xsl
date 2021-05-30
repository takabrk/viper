<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:atom="http://www.w3.org/2005/Atom"
 xmlns:xhtml="http://www.w3.org/1999/xhtml"
 xmlns="http://www.w3.org/1999/xhtml"
 version="1.0">
<xsl:output
  method="xml"
  encoding="utf-8"
  omit-xml-declaration="yes"
  doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
  doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
  indent="yes"
  media-type="application/xhtml+xml"/>
<xsl:template match="/">
	<html xml:lang="ja">
	<head>
		<meta http-equiv="content-style-type" content="text/css" />
		<link rel="stylesheet" type="text/css" href="atom.css" media="all" title="default" />
		<title>Web site Data</title>
	</head>
	<body>
		<div id="maintitle">
			<a href="{atom:feed/atom:link[@rel='alternate']/@href}">
				<xsl:value-of select="atom:feed/atom:title" />
			</a>
			<div id="subT">
				<xsl:value-of select="atom:feed/atom:subtitle" />
			</div>
		</div>
		<xsl:apply-templates select="atom:feed" />
	</body>
	</html>
</xsl:template>
<xsl:template match="atom:feed">
	<div id="wrapper">
		<xsl:apply-templates select="atom:entry" />
	</div>
</xsl:template>
<xsl:template match="atom:entry">
	<div class="contents">
		<div class="subtitle">
			<a href="{atom:link/@href}">
				<xsl:value-of select="atom:title"/>
			</a>
		</div>
		<div class="date">
			<xsl:value-of select="atom:updated"/>
		</div>
		<xsl:copy-of select="atom:content/xhtml:div"/>
	</div>
</xsl:template>
</xsl:stylesheet>
