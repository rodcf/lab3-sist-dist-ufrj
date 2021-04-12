import socket as sock

HOST = 'localhost' # maquina onde esta o servidor
PORT = 5000        # porta que o servidor esta escutando

# cria socket
clientSocket = sock.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o servidor
clientSocket.connect((HOST, PORT))

while True:

    # obtem a mensagem a ser enviada por meio do input do usuario (nome do arquivo)
    msgToSend = input('Digite o nome do arquivo ou \'exit\' para encerrar: ')

    # caso a mensagem inserida seja a palavra-chave 'exit', encerra o loop
    if msgToSend == 'exit':
        break

    # envia a mensagem para o servidor
    clientSocket.send(bytes(msgToSend, encoding='utf-8'))

    # imprime a mensagem enviada
    print('Mensagem enviada: ', msgToSend)

    #espera a resposta do servidor (chamada pode ser BLOQUEANTE)
    receivedMsg = clientSocket.recv(2048) # argumento indica a qtde maxima de bytes da mensagem

    # imprime a mensagem recebida
    print('Mensagem recebida: ', str(receivedMsg, encoding='utf-8'))

# encerra a conexao
clientSocket.close()