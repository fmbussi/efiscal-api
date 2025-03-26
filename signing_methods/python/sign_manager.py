import base64

from signxml import XMLSigner, methods
from lxml import etree
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# Configuración directa en variables
CERT_STORE_PATH = "certificado_valido_y_autorizado.p12"  # Ruta del certificado .p12
PASSWORD = "123456"  # Contraseña del certificado
XML_FILE_PATH = "semilla.xml"  # Archivo XML a firmar

class SignManager:
    def __init__(self, cert_store_path: str, password: str):
        self.password = password
        self.cert_store_path = cert_store_path
        self.cert, self.private_key = self.load_certificate()

    def load_certificate(self):
        """Carga el certificado .p12 usando cryptography."""
        try:
            with open(self.cert_store_path, "rb") as file:
                cert_store = file.read()
        except FileNotFoundError:
            print("Error: No se pudo leer el archivo del certificado")
            exit(1)

        private_key, certificate, additional_certificates = load_key_and_certificates(
            cert_store, self.password.encode(), default_backend()
        )

        # Convertir clave privada a formato PEM
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()

        # Convertir certificado a formato PEM
        cert_pem = certificate.public_bytes(serialization.Encoding.PEM).decode()

        return cert_pem, private_key_pem

    def sign(self, xml: str) -> str:
        """Firma el XML y devuelve el XML firmado."""
        try:
            # Parsear XML con eliminación de espacios innecesarios
            parser = etree.XMLParser(remove_blank_text=True) # Equivalente a preserveWhiteSpace=False
            xml_tree = etree.fromstring(xml.encode(), parser=parser)

            # Crear el firmador
            signer = XMLSigner(
                method=methods.enveloped, 
                digest_algorithm="sha256", 
                signature_algorithm="rsa-sha256", 
                c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#" # Excluye namespaces redundantes
            )

            # Firmar XML (Aquí se calcula Signature Value)
            signed_xml = signer.sign(
                xml_tree, 
                key=self.private_key, 
                cert=self.cert
            )

            # Obtener el Signature Value si necesitas modificarlo
            """signature_value_element = signed_xml.find(".//{http://www.w3.org/2000/09/xmldsig#}SignatureValue")
            if signature_value_element is not None:
                signature_value = signature_value_element.text
                print(f"Signature Value Calculado: {signature_value}")"""

            return etree.tostring(signed_xml, pretty_print=True).decode()
        except Exception as e:
            print(f"Error al firmar el XML: {str(e)}")
            exit(1)

# Cargar XML desde archivo
try:
    with open(XML_FILE_PATH, "r", encoding="utf-8") as xml_file:
        xml_content = xml_file.read()
except FileNotFoundError:
    print("Error: No se pudo leer el archivo XML")
    exit(1)

# Firmar el XML
sign_manager = SignManager(CERT_STORE_PATH, PASSWORD)
signed_xml = sign_manager.sign(xml_content)

# Guardar XML firmado
with open("signed_output.xml", "w", encoding="utf-8") as output_file:
    output_file.write(signed_xml)

print("XML firmado exitosamente. Guardado en signed_output.xml")
