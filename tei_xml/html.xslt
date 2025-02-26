<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">

    <xsl:output method="html" encoding="UTF-8"/>

    <!-- Root Template -->
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
                    .metadata { background: #f4f4f4; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
                    .content { margin-top: 20px; }
                    .note { font-style: italic; color: #666; }
                    .fw { font-weight: bold; text-align: right; display: block; margin-top: 10px; }
                    p { text-indent: 2em; margin-bottom: 1em; }
                </style>
            </head>
            <body>

                <div class="metadata">
                    <h1><xsl:value-of select="tei:teiHeader/tei:sourceDesc/tei:bibl/tei:title[@type='main']"/></h1>
                    <br/>
                    <h3>Transcription and Encoding: </h3>
                        <p><b>Responsible: </b> <xsl:value-of select="//tei:respStmt/tei:persName" /></p>
                        <p><b>Date: </b><xsl:value-of select="//tei:editionStmt/tei:edition/tei:date" /></p>
                        <p><b>Note: </b> <xsl:value-of select="//tei:noteStmt/tei:note" /></p>
                        
                    <h3>Source Description: </h3>
                        <p><b>Title: </b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:title [@type='main']" /></p>
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

                    <!-- Extracting Title Page Information -->
                    <h3><xsl:value-of select="tei:text/tei:front/tei:div[@type='titlePage']/tei:head/tei:title"/></h3>
                    
                    <!-- Epigraph -->
                    <xsl:if test="tei:text/tei:front/tei:div/tei:epigraph">
                        <p class="quote">
                            <xsl:value-of select="tei:text/tei:front/tei:div/tei:epigraph/tei:quote"/>
                            <br/>
                            <em>— <xsl:value-of select="tei:text/tei:front/tei:div/tei:epigraph/tei:l/tei:said"/> </em>
                        </p>
                    </xsl:if>

                    <!-- Extracting Main Text -->
                    <xsl:apply-templates select="tei:text/tei:body/tei:div"/>

                </div>
            </body>
        </html>
    </xsl:template>

    <!-- Template for body and front -->
    <xsl:template match="tei:front | tei:body">
        <xsl:apply-templates select="tei:div | tei:pb | tei:figure"/>
        <xsl:apply-templates select="tei:del"/>
        <xsl:apply-templates select="tei:add"/>
        <xsl:apply-templates select="tei:hi"/>
        <xsl:apply-templates select="tei:unclear"/>
    </xsl:template>

    <!-- Template for div links -->
    <xsl:template match="tei:ref">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="@target"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </a>
    </xsl:template>

    <!-- Template for paragraph -->
    <xsl:template match="tei:p">
        <p>
            <!-- Add class based on rend attribute -->
            <xsl:if test="@rend">
                <xsl:attribute name="class">
                    <xsl:value-of select="@rend"/>
                </xsl:attribute>
            </xsl:if>

            <!-- Apply paragraph content -->
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <!-- Template for Emphasized Text (hi elements) -->
    <xsl:template match="tei:hi">
        <span>
            <!-- Handle @rend as a class -->
            <xsl:if test="@rend">
                <xsl:attribute name="class">
                    <xsl:value-of select="@rend"/>
                </xsl:attribute>
            </xsl:if>
            <!-- Handle @rendition="rectangle" as inline styling -->
            <xsl:if test="@rendition='rectangle'">
                <xsl:attribute name="style">border: 1px solid black; padding: 2px;</xsl:attribute>
            </xsl:if>
        </span>
    </xsl:template>

    <!-- Template to handle the <del> element (deletions) -->
    <xsl:template match="tei:del">
        <del class="deletion">
            <xsl:value-of select="."/>
        </del>
    </xsl:template>

    <!-- Template to handle the <add> element (additions) -->
    <xsl:template match="tei:add">
        <span class="insertion">
            <xsl:value-of select="."/>
        </span>
    </xsl:template>

    <xsl:template match="tei:note">
        <div class="note">
            <!-- Add classes for note type and placement -->
            <xsl:attribute name="class">
                <xsl:text>note </xsl:text>
                <xsl:value-of select="@type"/>
                <xsl:text> </xsl:text>
                <xsl:value-of select="@place"/>
            </xsl:attribute>

            <!-- Process children elements within the note -->
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- Handle unclear text -->
    <xsl:template match="tei:unclear">
        <span class="unclear">
            <xsl:attribute name="title">
                <xsl:value-of select="@reason"/>
            </xsl:attribute>
        </span>
    </xsl:template>

    <!-- Handle gaps (missing or illegible text) -->
    <xsl:template match="tei:gap">
        <span class="gap" title="Texto perdido">
            <xsl:text>[…]</xsl:text>
        </span>
    </xsl:template>

    <!-- Template for quotes -->
    <xsl:template match="tei:said">
        <span class="quote">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- Template for Page Breaks -->
    <xsl:template match="tei:pb">
        <div class="page-break">
            <img src="{@facs}" alt="Page Image" />
        </div>
    </xsl:template>

    <!-- Template for page numbers -->
    <xsl:template match="tei:fw">
        <span class="fw">Page <xsl:value-of select="."/></span>
    </xsl:template>

    <!-- Template for Figures -->
    <xsl:template match="tei:figure">
        <figure>
            <img src="{@facs}" alt="Figure Image" />
            <figcaption>
                <xsl:value-of select="tei:figDesc"/>
            </figcaption>
        </figure>
    </xsl:template>

</xsl:stylesheet>
