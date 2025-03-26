Esta implementación está basada en el documento [Firmado de e-CF](https://dgii.gov.do/cicloContribuyente/facturacion/comprobantesFiscalesElectronicosE-CF/Documentacin%20sobre%20eCF/Instructivos%20sobre%20Facturaci%C3%B3n%20Electr%C3%B3nica/Firmado%20de%20e-CF.pdf), página 17.

Se realizaron varios cambios adicionales a la clase XmlSigner.php para que se ajustara a lo esperado por el servicio web (api).

El script fue probado en la versión php 8.2.28 (web) pero considero que funciona con versiones superiores, siempre y cuando, la librería las soporte.
