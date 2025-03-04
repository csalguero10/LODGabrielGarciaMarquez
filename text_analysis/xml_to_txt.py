import xml.etree.ElementTree as ET
import os

def xml_to_txt(input_xml_file, output_txt_file):
    # Verificar si el archivo XML existe
    if not os.path.exists(input_xml_file):
        print(f"Error: El archivo {input_xml_file} no existe.")
        return

    try:
        tree = ET.parse(input_xml_file)
        root = tree.getroot()

        with open(output_txt_file, 'w', encoding='utf-8') as txt_file:
            for element in root.iter():
                if element.text and element.text.strip():
                    print(f"Extrayendo: {element.text.strip()}")  # Depuración
                    txt_file.write(element.text.strip() + ' ')

        print(f"✅ Archivo convertido con éxito: {output_txt_file}")

    except ET.ParseError as e:
        print(f"Error de XML: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Uso
input_xml_file = 'tei_xml/tei.xml'
output_txt_file = 'text_analysis/tei.txt'
xml_to_txt(input_xml_file, output_txt_file)

