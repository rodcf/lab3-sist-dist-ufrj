import socket as sock
import select
import sys
import threading
from collections import Counter

# localizacao do servidor
HOST = '' # '' possibilita acessar qualquer endereco alcancavel da maquina local
PORT = 5000 # porta onde chegarao as mensagens para essa aplicacao

NUMBER_OF_WORDS = 10 # numero de palavras mais encontradas desejado

# define o caminho para o diretorio onde se encontram os arquivos de texto
FILES_ROOT_PATH = 'arquivos/' 

# lista de entradas (I/O) a serem observados pela aplicacao
inputs = [sys.stdin]

# armazena todas as conexoes estabelecidas ao longo da execucao da aplicacao
connections = {}

def initialize():
    '''Cria um socket para o servidor e o coloca em modo de espera por conexoes
    Saida: o socket de servidor criado'''

    # cria um socket para comunicacao
    socket = sock.socket() # valores default: socket.AF_INET, socket.SOCK_STREAM  

    # permite o reuso da porta caso a aplicacao seja finalizada de forma abrupta
    socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

    # vincula a interface e porta para comunicacao
    socket.bind((HOST,PORT))

    # define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
    socket.listen(5)

    # define o socket do servidor como nao-bloqueante
    socket.setblocking(False)

    # adiciona o socket do servidor na lista de entradas da aplicacao
    inputs.append(socket)

    return socket

def acceptConnection(serverSocket):
    '''Estabelece conexao com um cliente
    Entrada: o socket do servidor
    Saida: o socket de conexao criado e o endereco (IP, PORTA) do cliente'''

    # Aceita o pedido de conexao do cliente
    socket, address = serverSocket.accept()

    # Armazena o endereco do cliente no historico de conexoes
    connections[socket] = address

    # imprime o par (IP,PORTA) da conexao estabelecida
    print('Conexao estabelecida com:', address)

    return socket, address

def mostCommonWordsFromFile(fileName, numberOfWords):
    '''Le um arquivo de texto e retorna as palavras mais encontradas nele,
    ordenadas da mais frequente para a menos frequente
    Entrada: o nome do arquivo de texto e o numero de palavras mais frequentes desejado
    Saida: lista das palavras mais frequentes ou mensagem de erro'''

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
    '''Recebe e processa mensagens do cliente, enviando para ele os retornos gerados pela aplicacao
    para o input recebido
    Entrada: o socket da conexao e o endereco do cliente'''

    while True:

        # recebe uma mensagem do cliente
        receivedMsg = connectionSocket.recv(2048) # argumento indica a qtde maxima de dados

        # caso receba dados vazios: cliente encerrou a conexao
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

        # gera a mensagem a ser enviada como resposta para o cliente
        msgToSend = mostCommonWordsFromFile(receivedMsgString, NUMBER_OF_WORDS)

        # envia o retorno da aplicacao para o cliente
        connectionSocket.send(bytes(msgToSend, encoding='utf-8'))

        # imprime a mensagem enviada
        # print('Mensagem enviada para', str(address) + ':', msgToSend)

def main():
    '''Loop principal do servidor'''

    # armazena as threads criadas para tratar requisicoes
    threads = []

    # inicializa o servidor
    serverSocket = initialize()

    print('O servidor esta pronto para receber conexoes...')

    while True:

        # espera ate que alguma entrada da lista de entradas de interesse esteja pronta
        rList, wList, xList = select.select(inputs, [], [])

        # trata as entradas prontas
        for ready in rList:

            # caso seja um novo pedido de conexao
            if ready == serverSocket:

                # estabelece conexao com o cliente
                connectionSocket, address = acceptConnection(serverSocket)

                # cria uma nova thread para tratar as requisicoes do cliente
                thread = threading.Thread(target=handleRequests, args=(connectionSocket,address))

                # adiciona a nova thread na lista de threads
                threads.append(thread)

                # inicia a thread
                thread.start()

            # caso seja uma entrada padrao
            elif ready == sys.stdin:

                # armazena a entrada padrao
                command = input().lower()

                # caso seja uma solicitacao de encerramento do servidor
                if command == 'exit':

                    print('Aguardando clientes para encerrar servidor...')

                    # aguarda todas as threads (clientes) finalizarem
                    for t in threads:
                        t.join()

                    # encerra o socket do servidor
                    serverSocket.close()

                    print('Servidor encerrado')

                    # encerra a aplicacao
                    sys.exit(0)

                # caso seja uma solicitacao de historico de conexoes
                elif command == 'hist':

                    # imprime todas as conexoes estabelecidas ao longo da execucao
                    print(str(connections.values()))

# inicia o loop principal da aplicacao
main()