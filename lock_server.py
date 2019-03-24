#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 11
Números de aluno: 50384, 52172, 51596
"""

# Zona para fazer importação

import sys, sock_utils, time
import socket as s


class resource_lock:
    def __init__(self):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.status = 0
        self.lock_num = 0
        self.client_id = 0
        self.time_limit = 0

    def get_status(self):
        """
        Retorna o valor da variável status
        """
        return self.status

    def get_lock_num(self):
        """
        Retorna o valor da variável lock_num
        """
        return self.lock_num

    def get_client_id(self):
        """
        Retorna o valor da variável client_id
        """
        return self.client_id

    def get_time_limit(self):
        """
        Retorna o valor da variável time_limit
        """
        return self.time_limit


    def lock(self, client_id, time_limit):
        """
        Bloqueia o recurso se este não estiver bloqueado ou inativo, ou mantém o bloqueio
        se o recurso estiver bloqueado pelo cliente client_id. Neste caso renova
        o bloqueio do recurso até time_limit.
        Retorna True se bloqueou o recurso ou False caso contrário.
        """

        if self.status == 0 or client_id == self.get_client_id():
            self.status = 1
            self.client_id = client_id
            self.time_limit = time.time() + time_limit
            self.lock_num += 1
            return True
        else:
            return False



    def urelease(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.status = 0
        self.client_id = 0
        self.time_limit = 0
        return True

    def release(self, client_id):
        """
        Liberta o recurso se este foi bloqueado pelo cliente client_id,
        retornando True nesse caso. Caso contrário retorna False.
        """
        if self.client_id == client_id:
            self.status = 0
            self.client_id = 0
            self.time_limit = 0
            return 'OK'
        else:
            return 'NOK'

    def test(self):
        """
        Retorna o estado de bloqueio do recurso ou inativo, caso o recurso se 
        encontre inativo.
        """
        if self.status == 0:
            return 'UNLOCKED'
        elif self.status == 1:
            return 'LOCKED'
        else:
            return 'DISABLED'

    def stat(self):
        """
        Retorna o número de vezes que este recurso já foi bloqueado em k.
        """
        return self.lock_num

    def disable(self):
        """
        Coloca o recurso inativo/indisponível incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.status = 2

    def __repr__(self):
        """
        Representação do recurso
        """
        return 'Resource condition:' + '\nstatus:' + str(self.status) + '\nclient id:' + str(self.client_id) + '\nnum of locks:' +str(self.lock_num) + '\nlock time:' + str(self.time_limit) + '\n'




###############################################################################

class lock_pool:
    def __init__(self, N, K, Y, T):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe.
        Define K, o número máximo de bloqueios permitidos para cada recurso. Ao 
        atingir K, o recurso fica indisponível/inativo.
        Define Y, o número máximo permitido de recursos bloqueados num dado 
        momento. Ao atingir Y, não é possível realizar mais bloqueios até que um 
        recurso seja libertado.
		Define T, o tempo máximo de concessão de bloqueio.
        """
        self.res = [resource_lock() for i in range(N)]
        self.num_res = N
        self.max_K_locks = K
        self.max_Y_locks = Y
        self.max_T_locks = T

    def get_resources(self):
        """
        Retorna o array com todos os recursos
        """
        return self.res

    def get_num_res(self):
        """
        Retorna o valor de N, o número de recursos existentes.
        """
        return self.num_res

    def get_max_K_locks(self):
        """
        Retorna o valor de K, o número máximo de bloqueios permitidos para cada recurso.
        """
        return self.max_K_locks

    def get_max_Y_locks(self):
        """
        Retorna o valor de Y, o número máximo permitido de recursos bloqueados num dado
        momento.
        """
        return self.max_Y_locks

    def get_max_T_locks(self):
        """
        Retorna o valor de T, o tempo máximo de concessão de bloqueio.
        """
        return self.max_T_locks

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão do bloqueio. Liberta os recursos caso o seu tempo de
        concessão tenha expirado.
        """
        for i in self.get_resources():
            if i.get_status() != 0 and time.time() > i.get_time_limit():
                print('-> resource '+str(self.get_resources().index(i)+1)+' released, due to time limit')
                i.urelease()




    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, até ao
        instante time_limit.
        O bloqueio do recurso só é possível se o recurso estiver ativo, não 
        bloqueado ou bloqueado para o próprio requerente, e Y ainda não foi 
        excedido. É aconselhável implementar um método __try_lock__ para
        verificar estas condições.
        Retorna True em caso de sucesso e False caso contrário.
        """

        if resource_id <= self.get_num_res() and resource_id > 0:
            if self.stat_y() < self.get_max_Y_locks() and self.get_resources()[resource_id-1].lock(client_id, time_limit):
                self.verify_max_K_locks()
                return 'OK'
            else:
                return 'NOK'
        else:
            return 'UNKOWN RESOURCE'



    def verify_max_K_locks(self):
        """
        Assegura que cada recurso é desactivado assim que atingir K bloqueios
        """
        for i in self.get_resources():
            if i.stat() >= self.get_max_K_locks():
                i.disable()


    def release(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        True em caso de sucesso e False caso contrário.
        """
        if resource_id <= self.get_num_res() and resource_id > 0:
            return self.get_resources()[resource_id-1].release(client_id)
        else:
            return 'UNKOWN RESOURCE'


    def test(self,resource_id):
        """
        Retorna True se o recurso resource_id estiver desbloqueado e False caso
        esteja bloqueado ou inativo.
        """
        if resource_id <= self.get_num_res() and resource_id > 0:
            if self.get_resources()[resource_id-1].get_status() == 0:
                return 'UNLOCKED'
            elif self.get_resources()[resource_id-1].get_status() == 1:
                return 'LOCKED'
            else:
                return 'DISABLE'
        else:
             return 'UNKOWN RESOURCE'

    def stat(self,resource_id):
        """
        Retorna o número de vezes que o recurso resource_id já foi bloqueado, dos 
        K bloqueios permitidos.
        """
        if resource_id <= self.get_num_res() and resource_id > 0:
            return self.get_resources()[resource_id-1].stat()
        else:
             return 'UNKOWN RESOURCE'



    def stat_y(self):
        """
        Retorna o número de recursos bloqueados num dado momento de Y permitidos.
        """
        num = 0
        for i in self.get_resources():
            if i.get_status() == 1:
                num += 1
        return num

    def stat_n(self):
        """
        Retorna o número de recursos disponíneis em N.
        """
        n = 0
        for i in self.get_resources():
            if i.get_status() == 0:
                n += 1
        return n

		
    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print.
        """
        data = ''
        for i in self.get_resources():
            if(i.test() == 'LOCKED' or i.test() == 'DISABLE'):
                res_id_client = str(i.get_client_id())
                data = data + '\nid_client: ' + res_id_client+' -> '+str(self.get_resources().index(i)+1) + ' -> ' + time.ctime(i.get_time_limit())



        return '\nAvailable resources: ' + str(self.stat_n()) + '\n\n' + 'Locked Resources:' + data


        #
        # Acrescentar na output uma linha por cada recurso bloqueado, da forma:
        # recurso <número do recurso> bloqueado pelo cliente <id do cliente> até
        # <instante limite da concessão do bloqueio>
        #
        # Caso o recurso não esteja bloqueado a linha é simplesmente da forma:
        # recurso <número do recurso> desbloqueado
        # Caso o recurso não esteja inativo a linha é simplesmente da forma:
        # recurso <número do recurso> inativo
        #

###############################################################################


# código do programa principal


try:
    if len(sys.argv) > 1:
        HOST = ''
        PORT = sys.argv[1]
        num_res = sys.argv[2]
        max_lock_per_resource = sys.argv[3]
        max_lock_resources = sys.argv[4]
        time_limit = sys.argv[5]
    else:
        HOST = ''
        PORT = 9999
        num_res = 10
        max_lock_per_resource = 3
        max_lock_resources = 5
        time_limit = 45
except:
    print ("UNKNOWN COMMAND")
    exit()

print('PORT: %i' % PORT)
print('Number of resources: %i' % num_res)
print('Max locks per resource: %i' % max_lock_per_resource)
print('Max resource locked: %i' % max_lock_resources)
print('Lock time limit: %i' % time_limit)

pool = lock_pool(num_res,max_lock_per_resource,max_lock_resources,time_limit)
sock = sock_utils.create_tcp_server_socket(HOST, PORT, 1)


while True:
    try:
        resp = ''
        (conn_sock, addr) = sock.accept()

        print ("\n----------------------------------")
        print('Connected to: ', addr)


        pool.clear_expired_locks()

        msg1 = conn_sock.recv(1024)
        msg = msg1.decode();

        #print('Mensagem: %s' % msg)

        client_cmd = msg.split()

        if client_cmd[0] == 'LOCK':
            client_id = client_cmd[1]
            res_id = int(client_cmd[2])
            resp = pool.lock(res_id, client_id, time_limit)

        elif client_cmd[0] == 'RELEASE':
            client_id = client_cmd[1]
            res_id = int(client_cmd[2])
            resp = pool.release(res_id, client_id)

        elif client_cmd[0] == 'TEST':
            res_id = int(client_cmd[1])
            resp = str(pool.test(res_id))

        elif client_cmd[0] == 'STATS':
            res_id = int(client_cmd[1])
            resp += str(pool.stat(res_id))

        elif client_cmd[0] == 'STATS-Y':
            resp += str(pool.stat_y())

        elif client_cmd[0] == 'STATS-N':
            resp += str(pool.stat_n())
        else:
            resp = 'UNKNOWN COMMAND'

        print(pool)
        conn_sock.sendall(resp.encode())
        conn_sock.close()
         
    except Exception as e:
        if type(e) == ValueError:
            resp = 'UNKNOWN COMMAND'
        resp = conn_sock.recv(1024)
    finally:
        conn_sock.close()

      
sock.close()


