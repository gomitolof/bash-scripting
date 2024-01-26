# OpenSSL is an open source implementation of the SSL and TLS protocols.

# https://docs.python.org/3/library/ssl.html
# This module provides access to Transport Layer Security (often known as “Secure Sockets Layer”) encryption and peer authentication
# facilities for network sockets, both client-side and server-side. This module uses the OpenSSL library.

# https://www.pyopenssl.org/en/latest/
# pyOpenSSL is a rather thin wrapper around (a subset of) the OpenSSL library. With thin wrapper we mean that a lot of the object methods
# do nothing more than calling a corresponding function in the OpenSSL library.

import ssl
import socket
from OpenSSL import crypto
from prettytable import PrettyTable
from cryptography.hazmat.primitives import serialization

def read_certificate(hostname, port=443):
    # create a default SSL context to provide a set of default parameters and configuration options for secure connections via SSL/TLS
    # Returns SSLContext object.
    context = ssl.create_default_context()
    # Encapsulate a socket with an SSL/TLS security level with the secure context to establish a secure connection via SSL or TLS, as is the
    # case with HTTPS.
    # AF_INET is an address family used to designate the type of addresses that your socket can communicate with (in this case, IPv4 addresses)
    # Returns SSLContext.sslsocket_class
    sock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)

    sock.connect((hostname, port))

    # returns the X.509 certificate of the server to which the SSL/TLS socket is connected
    cert_bin = sock.getpeercert(binary_form=True)
    cert_txt = sock.getpeercert()
                
    # Load a certificate (X509) from the string cert_bin encoded with the type crypto.FILETYPE_ASN1.
    # The format used by FILETYPE_ASN1 is also sometimes referred to as DER (binary).
    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_bin)
    return cert_txt, x509.get_pubkey().to_cryptography_key()

def print_certificate(certificate, url):
    print("\n------------------------------------------------ %s SSL Certificate ------------------------------------------------" % (url))
    for key, value in certificate.items():
        myTable = PrettyTable(["Attribute", "Value"]) 
        values1 = []
        if isinstance(value, tuple):
            print("\n" + key)
            values3 = []
            for item_1 in value:
                if isinstance(item_1, tuple):
                    values2 = []
                    for item_2 in item_1:
                        if isinstance(item_2, tuple):
                            values = []
                            for item_3 in item_2:
                                values.append(item_3)
                            myTable.add_row(values)
                        else:
                            values2.append(item_2)
                        if len(values2) == 2:
                            myTable.add_row(values2)
                else:
                    values3 = [key, item_1]
                    myTable.add_row(values3)
        else:
            values1 = [key,value]
            myTable.add_row(values1)

        print(myTable)
        print()

def get_public_key(cert_path):
    # Carica il certificato SSL
    with open(cert_path, 'rb') as cert_file:
        cert_data = cert_file.read()
    
    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_data)
    
    # Estrai la chiave pubblica
    public_key = x509.get_pubkey().to_cryptography_key()
    
    return public_key

if __name__ == "__main__":
    url = input('Insert an url: ')
    # url = "www.facebook.com"
    ssl_port = 443  # SSL default port is 443

    cert_txt, pub_key = read_certificate(url, ssl_port)
    if cert_txt and pub_key:
        print_certificate(cert_txt, url)
        # encoding – The Encoding that will be used to serialize the certificate request.
        public_key_text = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print(public_key_text.decode('utf-8'))

