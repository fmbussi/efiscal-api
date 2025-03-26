# Certificado

Si estás trabajando en una distribución Linux puede que al tratar de utilizar el certificado aparezca un error similar a este en la línea de comando o simplemente, el script no funciona y no muestra error:

```diff
PKCS7 Encrypted data: pbeWithSHA1And40BitRC2-CBC, Iteration 1024
	Error outputting keys and certificates
	40F712096C740000:error:0308010C:digital envelope routines:inner_evp_generic_fetch:unsupported:../crypto/evp/evp_fetch.c:386:Global default library context, Algorithm (RC2-40-CBC : 0), Properties ()
```

Esto se debe a que algunos certificados utilizan algoritmos considerados obsoletos o no compatibles con OpenSSL v3. 
 
La solución podría ser comprar un nuevo certificado pero no hay garantías de que ese certificado no tenga también un algoritmo obsoleto o migrar a otro algoritmo pero eso es cuestionable.

Por el momento, se sugiere una solución combinada: comprar un nuevo certificado cuando el actual venza y configurar OpenSSL v3 en modo legacy hasta conseguir un certificado válido.

```bash
# Confirma la versión instalada.
openssl version
```

```bash
# Accede al archivo de configuración.
sudo vim /etc/ssl/openssl.cnf
```

```ini
# Busca las siguientes líneas y confirma que queden igual que estas.
[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

```bash
# Reinicia el servicio.
sudo systemctl restart openssl
```

Si estas trabajando con php, también tendrás que reiniciar el servicio. Si es php-fpm, el comando de reinicio es diferente.

```bash
# Reinicia el servicio.
sudo systemctl restart apache2
```

Esta solución fue probada en Ubuntu 24.04 LTS

Por si acaso, el servicio web de la facturación electrónica no permite certificados autofirmados.
