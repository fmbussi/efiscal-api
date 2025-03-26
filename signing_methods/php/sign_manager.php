<?php

namespace Dgii\Lib;

include './libs/xmldsig/Exception/CertificateException.php';
include './libs/xmldsig/Exception/XmlSignatureValidatorException.php';
include './libs/xmldsig/Exception/XmlSignerException.php';
include './libs/xmldsig/PrivateKeyStore.php';
include './libs/xmldsig/Algorithm.php';
include './libs/xmldsig/CryptoSignerInterface.php';
include './libs/xmldsig/CryptoSigner.php';
include './libs/xmldsig/X509Reader.php';
include './libs/xmldsig/XmlReader.php';
include './libs/xmldsig/XmlSigner.php';

use Selective\XmlDSig\PrivateKeyStore;
use Selective\XmlDSig\Algorithm;
use Selective\XmlDSig\CryptoSigner;
use Selective\XmlDSig\XmlSigner;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['cert_store']) && isset($_POST['password']) && isset($_FILES['xml_file'])) {
        $cert_store = $_FILES['cert_store']['tmp_name'];
        $password = $_POST['password'];
        $xml_file = file_get_contents($_FILES['xml_file']['tmp_name']);

        try {
            $signManager = new SignManager();
            $signedXml = $signManager->sign($cert_store, $password, $xml_file);

            header('Content-Type: application/xml');
            header('Content-Disposition: attachment; filename="signed_output.xml"');
            echo $signedXml;
        } catch (Exception $e) {
            http_response_code(400);
            echo "Error al firmar el XML: " . $e->getMessage();
        }
    } else {
        http_response_code(400);
        echo "Faltan parámetros necesarios: Certificado, contraseña o archivo XML.";
    }
} else {
    echo '<form method="POST" enctype="multipart/form-data">
            <label for="cert_store">Archivo del Certificado (P12):</label>
            <input type="file" name="cert_store" required><br>
            <label for="password">Contraseña del Certificado:</label>
            <input type="password" name="password" required><br>
            <label for="xml_file">Archivo XML:</label>
            <input type="file" name="xml_file" required><br>
            <input type="submit" value="Firmar XML">
          </form>';
}

final class SignManager
{
    /**
    * The constructor.
    *
    * @param string $cert_store contenido del archivo p12
    * @param string $password contraseña para acceder a la información contenida en el certificado
    * @param string $xml contenido del archivo xml
    */
    public function sign(string $cert_store, string $password, string $xml): string
    {
        if (!$cert_store = file_get_contents($cert_store)) {
            echo "Error: No fue posible leer el archivo.\n";
            exit;
        }

        if (!openssl_pkcs12_read($cert_store , $certs, $password)) {
            echo "Error: No fue posible leer el contenido del certificado.\n" . openssl_error_string();
            exit;
        }

        $pem_file_contents = $certs['cert'] . $certs['pkey'];

        $privateKeyStore = new PrivateKeyStore();

        $privateKeyStore->loadFromPem($pem_file_contents, $password);

        $privateKeyStore->addCertificatesFromX509Pem($pem_file_contents);

        $algorithm = new Algorithm(Algorithm::METHOD_SHA256);

        $cryptoSigner = new CryptoSigner($privateKeyStore, $algorithm);

        $xmlSigner = new XmlSigner($cryptoSigner);

        $xmlSigner->setReferenceUri('');

        $signedXml = $xmlSigner->signXml($xml);

        return $signedXml;
    }
}
?>
