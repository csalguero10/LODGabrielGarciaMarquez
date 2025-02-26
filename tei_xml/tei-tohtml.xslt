<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0">

    <xsl:output method="html" indent="yes"/>

    <!-- Root Template -->
    <xsl:template match="/tei:TEI">
        <html>
            <head>
                <title>
                    <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']"/>
                </title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    h1, h2, h3 { color: #333; }
                    .metadata { background: #f4f4f4; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
                    .content { margin-top: 20px; }
                    .note { font-style: italic; color: #666; }
                    .quote { font-style: italic; color: #444; margin-left: 20px; }
                    .fw { font-weight: bold; text-align: right; display: block; margin-top: 10px; }
                </style>
            </head>
            <body>
                <h1>
                    <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='main']"/>
                </h1>
                <h2>By: <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:author"/></h2>

                <div class="metadata">
                    <h3>Manuscript Information</h3>
                    <p><strong>Alternative Title:</strong> <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@type='alternative']"/></p>
                    <p><strong>Publication Date:</strong> <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:editionStmt/tei:edition/tei:date"/></p>
                    <p><strong>Publisher:</strong> <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher"/></p>
                    <p><strong>Language:</strong> <xsl:value-of select="tei:teiHeader/tei:profileDesc/tei:langUsage/tei:language"/></p>
                    <p><strong>Extent:</strong> <xsl:value-of select="tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:extent"/> pages</p>
                </div>

                <div class="content">
                    <h3>Content</h3>

                    <!-- Extracting Title Page Information -->
                    <h2>Title Page</h2>
                    <h3><xsl:value-of select="tei:text/tei:front/tei:div[@type='titlePage']/tei:head/tei:title"/></h3>
                    
                    <!-- Epigraph -->
                    <xsl:if test="tei:text/tei:front/tei:div/tei:epigraph">
                        <h3>Epigraph</h3>
                        <p class="quote">
                            <xsl:value-of select="tei:text/tei:front/tei:div/tei:epigraph/tei:quote"/>
                            <br/>
                            <em>— <xsl:value-of select="tei:text/tei:front/tei:div/tei:epigraph/tei:l/tei:said"/> </em>
                        </p>
                    </xsl:if>

                    <!-- Extracting Main Text -->
                    <h2>Main Text</h2>
                    <xsl:apply-templates select="tei:text/tei:body/tei:div"/>
                </div>
            </body>
        </html>
    </xsl:template>

    <!-- Template for Main Text -->
    <xsl:template match="tei:div">
        <div>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- Template for Paragraphs -->
    <xsl:template match="tei:p">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <!-- Template for Quotes -->
    <xsl:template match="tei:said">
        <span class="quote">
            "<xsl:apply-templates/>"
        </span>
    </xsl:template>

    <!-- Template for Page Numbers -->
    <xsl:template match="tei:fw">
        <span class="fw">Page <xsl:value-of select="."/></span>
    </xsl:template>

</xsl:stylesheet>
