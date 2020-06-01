import socket                                                                                                                                                              
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('localhost',5432))
    s.close()
except socket.error as ex:
    print("Connection failed with errno {0}: {1}".format(ex.errno, ex.strerror)) 