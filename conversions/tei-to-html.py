from lxml import etree

# Load TEI XML file
xml_file = etree.parse("tei_xml/tei.xml")
xslt_file = etree.parse("tei_xml/html.xsl")

# Apply the transformation
transform = etree.XSLT(xslt_file)
html_output = transform(xml_file)

# Save the output as an HTML file
with open("index.html", "wb") as f:
    f.write(etree.tostring(html_output, pretty_print=True, method="html"))

print("HTML file generated successfully!")
