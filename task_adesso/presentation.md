# CREAZIONE DI UN CERTIFICATO

Facebook crea chiave priv e pub, mette nel certificato la chiave pubblica, mette i vari campi (commonName, subjectAlternativeName, etc...)
tiene la chiave privata segreta, firma il certificato con la chiave privata. Questa certificato non è ancora valido, è una richiesta e si
chiama CSR (Certificate Signing Request). Lo spediamo alla Subordinate Certification Authority (SubCA), controllano i vari parametri, se
tutto ok firmano il certificato con la loro chiave privata e spediscono a facebook il nuovo certifiato firmato da loro. Quindi il certificate
ha due firme, una di facebook e una di digicert. Facebook lo installa nei server, e quando il client fa la richiesta a un server facebook,
il certificato viene spedito al client. Il browser ha una lista di SubCAs trustati di default installati, e conosce la loro chiave pubblica,
e anche quella di facebook (nel certificato). Quindi riesce a fare il validation dell'issuer SubCA (digicert), e lucchetto verde viene
mostrato.

# CAMPI DI UN CERTIFICATO

subject commonName most important because it is used to recognize one identity on the web. It is the certificate owner

issuer: chi ha rilasciato il certificato a facebook (e.g., digicert) Subordinate Certification Authority (SubCA)
versione del certificato

serialNumber identifica ogni certificato (importante)

notBefore: data rilascio del certificato

notAfter: data di scadenza del certificato

subjectAltName: non obbligatorio, ma certi browser lo vogliono obbligatorio. Lista di nomi DNS, indirizzi ip, o altri User
Principal Name (UPN) attribute is an internet communication standard for user accounts (è l'hostname della macchina). Ce ne sono
tanti perché il certificato vale per tutti i dominii presenti (1 certificato per diversi dominii)

OCSP (Online Certificate Status Protocol) protocollo nuovo che affianca le CRL. Alcuni certificati possono essere revocati, un utente
controlla le Certificate Revocation List che contengono una lista di serial number di certificati revocati. Quando apro facebook, controllo
le CRL, e se c'è l'indirizzo di facebook allora l'utente non lo trusta. OCSP è più leggero, CRL sono una lista di serial numbers di certificati
quindi sono pesanti. OCSP è un protocollo che permette al client di richiedere alle subCA se un dato certificato è valido o meno.

caIssuer (Certificate Authority Issuer), certificato della subCA ovvero chi ha rilasciato il certificato a facebook.

crlDistributionPoints mostra lista di CRL (certification revocation list). Uno in HTTP e l'altro è in Lightweight Directory Access Protocol,
apribile solo da windows.

Il certificato TLS viene usato per l'autenticazione client/server durante lo stabilimento di una connessione TLS (handshake) e vengono
scambiate delle ephimeral keys per crittografare le sessioni. Certificati usati per l'autenticazione, e poi le chiavi di sessione vengono
usate per scambiarsi informazioni.

openssl x509 -inform der -in SwissSign_RSA_TLS_OV_ICA_2021_-_1.ca -outform pem -out SwissSign_RSA_TLS_OV_ICA_2021_-_1.pem
openssl x509 -in ./SwissSign_RSA_TLS_OV_ICA_2021_-_1.ca -noout -text

tipologia di certificati:

certificati server (e.g., chiedi a facebook te li fornisce e client verifica l'autenticità del server)
certificati client (usati dal server per autenticare il client)
certificati client-server (usati da server ma che può essere anche client)
wildcard certificate (possono essere rilasciati sia client che server, esempio *.facebook.com nel commonName-SubjectAlternativeName)