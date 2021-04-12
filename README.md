# lab3-sist-dist-ufrj
Laboratório 3 da disciplina de Sistemas Distribuídos da UFRJ

O objetivo deste Laboratório é estender a aplicação distribuída desenvolvida no Laboratório 2 para aplicar os conceitos estudados sobre servidores concorrentes (ou multitarefa) e seguir praticando com a programação usando sockets.

A aplicação é a mesma do Laboratório 2: consiste em contar as ocorrências das palavras em um arquivo texto.

• Entrada: usuário informa o nome do arquivo texto.

• Saída (com sucesso): a aplicação exibe a lista das 10 palavras mais encontradas no arquivo, ordenadas da mais frequente para a menos frequente, e o número de
ocorrências de cada palavra.

• Saída (com erro): informa que o arquivo solicitado não foi encontrado.

As arquiteturas de software e de sistema também permanecem as mesmas do Laboratório 2, assim como a implementação do processo cliente. Apenas a implementação
do processo servidor deverá ser modificada para transformá-lo em um servidor concorrente.

Roteiro:

1. Altere o projeto de implementação do servidor para que ele seja capaz de receber comandos básicos da entrada padrão (inclua no mínimo um comando para permitir finalizar o servidor quando não houver clientes ativos). Use a função select.

2. Altere o projeto de implementação do servidor para que ele se torne um servidor concorrente, isto é, trate cada nova conexão de cliente como um novo fluxo de
execução e atenda as requisições desse cliente dentro do novo fluxo de execução. Crie threads ou processos filhos.

A interação com os clientes (incluindo o formato das mensagens trocadas) não deve ser alterada.