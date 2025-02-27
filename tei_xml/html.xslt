<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">

    <xsl:output method="html" encoding="UTF-8"/>

    <xsl:template match="/tei:TEI">
        <html lang="es">
            <head>
                <meta charset="UTF-8"/>
                <title>
                    <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']"/>
                </title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    h1, h2, h3 { color: #333; }
                    .unclear { background-color: yellow; }
                    .metadata { background:rgb(244, 244, 244); padding: 30px; border-radius: 5px; margin-bottom: 20px; }
                    .content { margin-top: 20px; }
                    .gap { color: red; font-weight: bold; }
                    .quote { font-style: italic; }
                    .note { font-style: italic; color: #666; }
                    .page-break { margin: 20px 0; text-align: center; }
                    .spaced { display: inline-block; width: 100%; margin-top: 10px; }
                    .figure { font-style: italic; color:rgb(38, 107, 46) }
                </style>
            </head>
            <body>

                <div class="metadata">
                    <h1><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']"/></h1>
                    <h2><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='subtitle']"/></h2>
                    <br/>
                    <h3>Transcription and Encoding: </h3>
                    <p><b>Responsible: </b> <xsl:value-of select="//tei:respStmt/tei:persName" /></p>
                    <p><b>Date: </b><xsl:value-of select="//tei:editionStmt/tei:edition/tei:date" /></p>
                    
                    <h3>Source Description: </h3>
                    <p><b>Title: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:title[@type='main']" /></p>
                    <p><b>Alternative Title: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:title[@type='alternative']" /></p>
                    <p><b>Author: </b><xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:author" /></p>
                    <p><b>Date: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:date" /></p>
                    <p><b>Place: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:pubPlace" /></p>
                    <p><b>Extent: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:extent" /></p>
                    <p><b>Language: </b><xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language"/></p>
                    <p><b>Note: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:note" /></p>

                    <h3>Publication Information: </h3>
                    <p><b>Publisher: </b> <xsl:value-of select="//tei:publicationStmt/tei:publisher" /></p>
                    <p><b>Location: </b> <xsl:value-of select="//tei:publicationStmt/tei:address/tei:addrLine" /></p>
                    <p><b>Collection: </b> <xsl:value-of select="//tei:msDesc/tei:msIdentifier/tei:collection" /></p>
                    <p><b>Availability: </b> <xsl:value-of select="//tei:publicationStmt/tei:availability" /></p>

                    <p><b>Project Description: </b> <xsl:value-of select="//tei:encodingDesc/tei:projectDesc" /></p>
                    
                    <h3>Handnotes from the original source: </h3>
                    <ul>
                        <xsl:for-each select="tei:teiHeader/tei:profileDesc/tei:handNotes/tei:handNote">
                            <li>
                                <b>Hand ID: </b> <xsl:value-of select="@xml:id"/> - 
                                <b>Medium: </b> <xsl:value-of select="@medium"/>
                            </li>
                        </xsl:for-each>
                    </ul>
                </div>

                <div class="content">
                    <!-- Extracting Main Text -->
                    <xsl:apply-templates select="tei:text"/>
                </div>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="tei:title | tei:name">
        <h3>
            <xsl:apply-templates/>
        </h3>
    </xsl:template>

    <xsl:template match="tei:div">
        <div class="spaced">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="tei:figure">
        <div class="figure">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="tei:pb">
        <div class="page-break spaced">
            <xsl:if test="@facs">
                <img src="https://hrc.contentdm.oclc.org/digital/collection/p15878coll51/{@facs}" alt="Page Image"/>
            </xsl:if>
        </div>
    </xsl:template>

    <xsl:template match="tei:fw">
        <span class="folio spaced" style="float:right; font-weight:bold;">
            Página <xsl:value-of select="."/>

        </span>
    </xsl:template>

    <xsl:template match="tei:quote">
        <span class="quote spaced">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="tei:epigraph">
        <blockquote>    
            <xsl:apply-templates/>
        </blockquote>
    </xsl:template>

    <xsl:template match="tei:lb">
        <br/>
    </xsl:template> 

    <xsl:template match="tei:del">
        <del title="Deletion">
            <xsl:apply-templates/>
        </del>
    </xsl:template>

    <xsl:template match="tei:add">
        <ins title="Insertion">
            <xsl:apply-templates/>
        </ins>
    </xsl:template>

    <xsl:template match="tei:unclear">
        <span class="unclear" title="Unclear text">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="tei:gap">
        <span class="gap" title="Text impossible to transcribe">[…]</span>
    </xsl:template>

    <xsl:template match="tei:note">
        <span class="note spaced" title="Note">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="tei:ref">
        <a href="{ @target }">
            <xsl:apply-templates/>
        </a>
    </xsl:template>

    <xsl:template match="tei:p">
        <p>
            <xsl:if test="@rend='first-line-indent'">
                <xsl:attribute name="style">text-indent: 1em;</xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <!-- Template for Emphasized Text (hi elements) -->
    <xsl:template match="tei:hi">
        <span>
            <xsl:choose>
                <xsl:when test="@rend='caps'">
                    <xsl:attribute name="style">text-transform: uppercase;</xsl:attribute>
                </xsl:when>
                <xsl:when test="@rend">
                    <xsl:attribute name="class">
                        <xsl:value-of select="@rend"/>
                    </xsl:attribute>
                </xsl:when>
            </xsl:choose>
            <xsl:apply-templates/>
        </span>
    </xsl:template>
</xsl:stylesheet>
