import socket as sock
import select
import sys
import threading
from collections import Counter

HOST = '' # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORT = 5000 # porta onde chegarao as mensagens para essa aplicacao

NUMBER_OF_WORDS = 10 # numero de palavras mais encontradas desejado

FILES_ROOT_PATH = 'arquivos/'

inputs = [sys.stdin]
connections = {}

def initialize():

    # cria um socket para comunicacao
    socket = sock.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

    socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

    # vincula a interface e porta para comunicacao
    socket.bind((HOST,PORT))

    # define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
    socket.listen(5)

    socket.setblocking(False)

    inputs.append(socket)

    return socket

def acceptConnection(serverSocket):

    socket, address = serverSocket.accept()

    connections[socket] = address

    # imprime o par (IP,PORTA) da conexao 
    print('Conexao estabelecida com:', address)

    return socket, address

def MostCommonWordsFromFile(fileName, numberOfWords):

    try:
        # le o arquivo de nome igual a mensagem recebida
        with open(FILES_ROOT_PATH + fileName, 'rt') as txtFile:
            
            # instancia um dicionario do tipo Counter a partir da lista de palavras contidas no arquivo
            # onde cada par (chave, valor) representa uma palavra e o numero de vezes que ela aparece
            counter = Counter(txtFile.read().lower().split())

            # pega a lista das n palavras mais frequentes do dicionario, onde n é NUMBER_OF_WORDS
            mostCommonWords = counter.most_common(NUMBER_OF_WORDS)

            # transforma a lista de palavras mais frequentes em string
            result = str(mostCommonWords)

    # caso um arquivo com o nome requisitado nao seja encontrado, envia mensagem de erro para o cliente
    except FileNotFoundError:
        result = 'ERRO - Arquivo nao encontrado!'
    
    return result

def handleRequests(connectionSocket, address):

    while True:

        # depois de conectar-se, espera uma mensagem
        receivedMsg = connectionSocket.recv(2048) # argumento indica a qtde maxima de dados

        if not receivedMsg:

            # fecha o socket da conexao
            connectionSocket.close()

            # imprime mensagem de conexao encerrada
            print('Conexao encerrada com:', address)

            return
        
        # transforma a mensagem recebida em bytes para string
        receivedMsgString = str(receivedMsg,encoding='utf-8')

        # imprime a mensagem recebida
        print(str(address) + ':', receivedMsgString)

        # acrescenta o formato .txt no fim do nome do arquivo caso necessario
        if not receivedMsgString.endswith('.txt'):
            receivedMsgString += '.txt'

        msgToSend = MostCommonWordsFromFile(receivedMsgString, NUMBER_OF_WORDS)

        # envia a lista de palavras mais frequentes para o cliente
        connectionSocket.send(bytes(msgToSend, encoding='utf-8'))

        # imprime a mensagem enviada
        # print('Mensagem enviada para', str(address) + ':', msgToSend)

def main():

    threads = []
    serverSocket = initialize()

    print('O servidor esta pronto para receber conexoes...')

    while True:

        rList, wList, xList = select.select(inputs, [], [])

        for ready in rList:

            if ready == serverSocket:
                connectionSocket, address = acceptConnection(serverSocket)
                thread = threading.Thread(target=handleRequests, args=(connectionSocket,address))
                threads.append(thread)
                thread.start()

            elif ready == sys.stdin:
                command = input().lower()
                if command == 'exit':
                    print('Aguardando clientes para encerrar servidor...')
                    for t in threads:
                        t.join()
                    serverSocket.close()
                    print('Servidor encerrado')
                    sys.exit(0)
                elif command == 'hist':
                    print(str(connections.values()))

main()