# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 11
Números de aluno: 50384, 52172, 51596
"""

# zona para fazer importação
import sys,socket as s
#import pickle as p,struct
from sock_utils import create_tcp_client_socket

# definição da classe server 

class server:
    """
    Classe para abstrair uma ligação a um servidor TCP. Implementa métodos
    para estabelecer a ligação, para envio de um comando e receção da resposta,
    e para terminar a ligação
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.sock = None

    def getAddress(self):
        return self.address

    def getPort(self):
        return self.port
    
    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização do
        objeto.
        """
        self.sock = create_tcp_client_socket(self.address, self.port)
        #self.sock.connect((self.address, self.port))

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna a
        resposta recebida pela mesma socket.
        """
        self.sock.sendall(data.encode())
        resposta = self.sock.recv(1024)

        ##PICKLE##
        # dataObj = p.dumps(data,-1) # enviar lista serializado com pickle
        # dataObj_size = struct.pack('!i',len(dataObj))

        # self.sock.sendall(dataObj_size)
        # self.sock.sendall(dataObj)

        #receber dados servidor
        # resp_size = self.sock.recv(1024)
        # size = struck.unpack('!i',resp_size)[0]

        # resp_bytes = self.sock.recv(size)
        # resposta = p.loads(resp_bytes)

        return resposta.decode()
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        self.sock.close()
        exit()
