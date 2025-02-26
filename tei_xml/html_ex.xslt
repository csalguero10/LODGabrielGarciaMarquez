<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">

    <!-- Template for the root element -->
    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select="//tei:titleStmt/tei:title[@type='main']" /></title>
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
                    <h1><xsl:value-of select="//tei:titleStmt/tei:title[@type='main']" /></h1>
                    <h2>by <xsl:value-of select="//tei:titleStmt/tei:author" /></h2>
                    
                    <h3>Alternative Title</h3>
                        <p><xsl:value-of select="//tei:titleStmt/tei:title[@type='alternative']" /></p>
                    
                    <h3>Encoded by</h3>
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

                    <h3>Extent</h3>
                    <p><xsl:value-of select="//tei:extent/tei:measure[@unit='pages']" /></p>

                    <h3>Publication Information</h3>
                    <p><b>Publisher:</b> <xsl:value-of select="//tei:publicationStmt/tei:publisher" /></p>
                    <p><b>Location:</b> <xsl:value-of select="//tei:publicationStmt/tei:address/tei:addrLine" /></p>

                    <h3>Source Description</h3>
                    <p><b>Title:</b> <xsl:value-of select="//tei:sourceDesc/tei:biblStruct/tei:monogr/tei:title" /></p>
                    <p><b>Author: </b><xsl:value-of select="//tei:sourceDesc/tei:biblStruct/tei:monogr/tei:author" /></p>
                    <p><b>Publication Year:</b> <xsl:value-of select="//tei:sourceDesc/tei:biblStruct/tei:monogr/tei:imprint/tei:date" /></p>
                    <p><b>Language:</b><xsl:value-of select="//tei:profileDesc/tei:langUsage/tei:language" /></p>

                    <h3>Project Description</h3>
                    <p><xsl:value-of select="//tei:encodingDesc/tei:projectDesc/tei:p" /></p>

                    <h3>Editorial Declaration</h3>
                    <p><xsl:value-of select="//tei:encodingDesc/tei:editorialDecl/tei:p" /></p>
                </div>
                
                <div>
                    <h3>List of Characters</h3>
                    <ul>
                        <xsl:for-each select="//tei:profileDesc/tei:particDesc/tei:listPerson/tei:person">
                            <li>
                                <strong>Name:</strong> <xsl:value-of select="tei:persName/tei:forename" /> <xsl:value-of select="tei:persName/tei:surname" />
                                <br />
                                <strong>Nickname:</strong> <xsl:value-of select="tei:persName/tei:addName[@type='nickname']" />
                                <br />
                                <strong>Occupation:</strong> <xsl:value-of select="tei:occupation" />
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
    <xsl:template match="tei:div[@type='image']">
        <div class="image" data-number="{@n}">
        <xsl:apply-templates select="tei:head | tei:p | tei:figure | tei:note"/>
        </div>
    </xsl:template>

    <!-- Template to match head elements -->
    <xsl:template match="tei:head">
        <h2>
        <xsl:value-of select="."/>
        </h2>
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

