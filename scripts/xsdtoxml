from lxml import etree

# Ruta de los archivos
xsd_path = "../xsd/eCF47.xsd"
output_xml_path = "../xml/eCF47.xml"

def build_element(element_definitions, element_name):
    """
    Construye un elemento XML basado en su definición en el XSD.
    """
    if element_name not in element_definitions:
        return etree.Element(element_name)

    xml_element = etree.Element(element_name)

    for child_name in element_definitions[element_name]:
        child_element = build_element(element_definitions, child_name)
        xml_element.append(child_element)

    # Solo agregar texto vacío si no tiene hijos
    if not list(xml_element):
        xml_element.text = ""

    return xml_element

def parse_xsd(xsd_path):
    """
    Parsea el XSD y extrae la estructura de elementos y sus relaciones.
    """
    with open(xsd_path, "rb") as f:
        xsd_tree = etree.parse(f)

    root_element = xsd_tree.getroot()
    namespace = {"xs": "http://www.w3.org/2001/XMLSchema"}

    element_definitions = {}

    # Obtener todos los elementos definidos en el esquema
    for element in root_element.findall(".//xs:element", namespace):
        name = element.get("name")
        if name:
            element_definitions[name] = []

            # Si el elemento tiene un tipo complejo, procesar su estructura interna
            complex_type = element.find("xs:complexType", namespace)
            if complex_type is not None:
                sequence = complex_type.find("xs:sequence", namespace)
                if sequence is not None:
                    for sub_element in sequence.findall("xs:element", namespace):
                        sub_name = sub_element.get("name")
                        if sub_name:
                            element_definitions[name].append(sub_name)

    return element_definitions

# Procesar el XSD y obtener la estructura
element_definitions = parse_xsd(xsd_path)

# Crear el XML con la estructura correcta
root_element_name = next(iter(element_definitions.keys()))  # Primer elemento raíz
xml_root = build_element(element_definitions, root_element_name)

# Convertir XML a cadena con pretty print (pero con espacios)
xml_string = etree.tostring(xml_root, pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8")

# Reemplazar doble espacio con tabulación
xml_string = xml_string.replace("  ", "\t")

# Guardar el XML corregido con tabulaciones
with open(output_xml_path, "w", encoding="utf-8") as f:
    f.write(xml_string)

print(f"XML generado correctamente en: {output_xml_path}")
