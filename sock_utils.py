#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - sock-utils.py
Grupo: 11
Números de aluno: 50384, 52172, 51596
"""
# Zona para fazer imports
import socket as s

def create_tcp_server_socket(address, port, queue_size):

	sock=s.socket(s.AF_INET, s.SOCK_STREAM)

	sock.bind((address,port))
	sock.listen(queue_size)
	return sock


def create_tcp_client_socket(address, port):
	
	sock=s.socket(s.AF_INET,s.SOCK_STREAM)
	
	sock.connect((address,port))
	
	return sock

def receive_all(socket, length):
	
	sock=s.socket(s.AF_INET,s.SOCK_STREAM)
	msg= conn_sock.recv(length)
	
	return sock
	