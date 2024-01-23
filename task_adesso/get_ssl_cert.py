# https://docs.python.org/3/library/ssl.html

# This module provides access to Transport Layer Security (often known as “Secure Sockets Layer”) encryption and peer authentication
# facilities for network sockets, both client-side and server-side. This module uses the OpenSSL library.

import ssl
import socket

from prettytable import PrettyTable 

def read_certificate(hostname, porta=443):
    # create a default SSL context to provide a set of default parameters and configuration options for secure connections via SSL/TLS
    # Returns SSLContext object.
    context = ssl.create_default_context()
    # Encapsulate a socket with an SSL/TLS security level with the secure context to establish a secure connection via SSL or TLS, as is the
    # case with HTTPS.
    # AF_INET is an address family used to designate the type of addresses that your socket can communicate with (in this case, IPv4 addresses)
    # Returns SSLContext.sslsocket_class
    secSocket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)

    secSocket.connect((hostname, porta))
    # returns the X.509 certificate of the server to which the SSL/TLS socket is connected
    certificato = secSocket.getpeercert()

    return certificato

def print_certificate(certificate, url):
    print("\n------------------------------------------------ %s SSL Certificate ------------------------------------------------" % (url))
    for chiave, valore in certificate.items():
        myTable = PrettyTable(["Attribute", "Value"]) 
        values1 = []
        if isinstance(valore, tuple):
            print("\n" + chiave)
            values3 = []
            for item_1 in valore:
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
                    values3 = [chiave, item_1]
                    myTable.add_row(values3)
        else:
            values1 = [chiave,valore]
            myTable.add_row(values1)

        print(myTable)
        print()

if __name__ == "__main__":
    # sito_web = input('Insert an url: ')
    url = "www.facebook.com"
    porta_ssl = 443  # SSL default port is 443

    certificate = read_certificate(url, porta_ssl)
    print_certificate(certificate, url)

    