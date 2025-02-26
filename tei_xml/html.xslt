<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <!-- Template for the root element -->
    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']" /></title>
                <style>
                    body {
                    font-family: 'Montserrat', Arial, sans-serif;
                    margin: 20px;
                    background-color: #ffe4e1; 
                    }
                    
                    .metadata {
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                    }
                    .right-indent {
                    margin-left: 20em;
                    }
                </style>
            </head>
            
            <body>
                <div class="metadata">
                    <h1><xsl:value-of select="//tei:titleStmt/tei:title[@type='main']"/></h1>
                    <h2>by <xsl:value-of select="//tei:titleStmt/tei:author" /></h2>
                    
                    <h3>Alternative Title</h3>
                    <p><xsl:value-of select="//tei:titleStmt/tei:title[@type='alternative']" /></p>
                    
                    <h3>Transcription and Encoding</h3>
                    <p><xsl:value-of select="//tei:respStmt/tei:persName" /></p>
                    
                    <h3>Edition Information</h3>
                    <p>
                        <b>Edition:</b><xsl:value-of select="//tei:editionStmt/tei:edition/@n" />
                    </p>
                    <p>
                        <b>Date:</b> <xsl:value-of select="//tei:editionStmt/tei:edition/tei:date" />
                    </p>
                    <p>
                        <b>Note:</b> <xsl:value-of select="//tei:editionStmt/tei:edition/tei:note" />
                    </p>
                    
                    <h3>Publication Information</h3>
                    <p><b>Publisher:</b> <xsl:value-of select="//tei:publicationStmt/tei:distributor" /></p>
                    <p><b>Location:</b> <xsl:value-of select="//tei:publicationStmt/tei:address/tei:addrLine" /></p>
                    <p><b>Availability:</b> <xsl:value-of select="//tei:publicationStmt/tei:availability" /></p>
                    
                    <h3>Project Source</h3>
                    <p><xsl:value-of select="//tei:noteStmt/tei:note"/> </p>
                    
                    <h3>Original Manuscript Description</h3>
                    <p><b>Title:</b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:title" /></p>
                    <p><b>Author: </b><xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:author" /></p>
                    <p><b>Date:</b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:date" /></p>
                    <p><b>Publication Place:</b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:pubPlace" /></p>
                    <p><b>Language:</b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:lang" /></p>
                    <p><b>Extent:</b> <xsl:value-of select="//tei:sourceDesc/tei:bibl/tei:extent" /></p>
                    <p><b>Adnnotations: </b><xsl:value-of select="//sourceDesc/tei:bibl/tei:note"/> </p>
                    
                    <h3>Digitized Manuscript Description</h3>
                    <p><b>Holder institution:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:institution" /></p>
                    <p><b>Repository:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:repository" /></p>
                    <p><b>Collection:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:collection" /></p>
                    <p><b>Identifier:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno" /></p>
                    <p><b>Language:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msContents/tei:textLang" /></p>
                    <p><b>Title:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msContents/tei:titlePage/tei:docTitle/tei:titlePart" /></p>
                    <p><b>Author:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msContents/tei:msItem/tei:author" /></p>
                    <p><b>Phisical Description:</b> <xsl:value-of select="//tei:sourceDesc/tei:msDesc/tei:msContents/tei:physDesc" /></p>
                    
                    <h3>Encoding Description</h3>
                    <p><b>Project Description:</b> <xsl:value-of select="//tei:encodingDesc/tei:projectDesc" /></p>
                    <p><b>Editorial Declaration:</b> <xsl:value-of select="//tei:encodingDesc/tei:editorialDecl" /></p>
                    <p><b>Revision Description:</b> <xsl:value-of select="//tei:encodingDesc/tei:revisionDesc" /></p>
                    
                </div>
                
                <div>
                    <h3>Handnotes</h3> #control which oter functions can we us as where, or if to fileter
                    <ul>
                        <xsl:for-each select="//tei:profileDesc/tei:handNotes/tei:note">
                            <li>
                                <strong>Hand:</strong> <xsl:value-of select="tei:handNote/@hand" />
                                <br />
                                <strong>Content:</strong> <xsl:value-of select="tei:handNote" />
                            </li>
                        </xsl:for-each>
                    </ul>
                </div>
                
                <xsl:apply-templates select="tei:TEI/tei:text/tei:body"/>
                
                
            </body>
        </html>
    </xsl:template>
    
    <!-- Template to match body -->
    <xsl:template match="tei:body">
        <xsl:apply-templates select="tei:div"/>
    </xsl:template>
    
    <!-- Template to match image -->
    <xsl:template match="tei:div[@type='verso']">
        <div class="verso" data-number="{@n}">
            <xsl:apply-templates select="tei:head | tei:pb | tei:figure | tei:figDesc"/>
        </div>
    </xsl:template>
    
    <!-- Template to match head elements -->
    <xsl:template match="tei:head [@type='main-authorial']">
        <h2>
            <xsl:value-of select="."/>
        </h2>
    </xsl:template>

    <xsl:template match="tei:head [@type='authorial']">
        <h3>
            <xsl:value-of select="."/>
        </h3>
    </xsl:template>
    
    <xsl:template match="tei:p">
        <p>
            <xsl:apply-templates select="tei:lb | tei:hi | tei:q | text()"/>
        </p>
    </xsl:template>
    
    <xsl:template match="tei:lb">
        <br/>
    </xsl:template>
    
    <xsl:template match="tei:hi">
        <xsl:element name="{local-name()}">
            <xsl:attribute name="class">
                <xsl:value-of select="@rend"/>
            </xsl:attribute>
            <xsl:apply-templates select="."/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="tei:q">
        <blockquote>
            <xsl:attribute name="cite">
                <xsl:value-of select="@who"/>
            </xsl:attribute>
            <xsl:apply-templates select="."/>
        </blockquote>
    </xsl:template>
    
    <xsl:template match="tei:figure">
        <figure>
            <img>
                <xsl:attribute name="src">
                    <xsl:value-of select="tei:graphic/@url"/>
                </xsl:attribute>
            </img>
            <figcaption>
                <xsl:value-of select="tei:figDesc"/>
            </figcaption>
        </figure>
    </xsl:template>
    
    <xsl:template match="tei:note">
        <aside>
            <xsl:apply-templates select="tei:p"/>
        </aside>
    </xsl:template>
    
</xsl:stylesheet>