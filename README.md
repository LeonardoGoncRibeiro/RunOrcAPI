# RunOrcAPI

Programa em Python RunOrcAPI, para facilitar a simulação de múltiplos arquivos e a coleta de resultados.

O programa requer um arquivo input, com dados que serão considerados em uma rodada. O arquivo possui labels, que detém os parâmetros a serem lidos e considerados na rodada. As principais labels são:

%HEADER

Label que contém uma descrição do arquivo que será rodado. Serve como cabeçalho do arquivo. Não possui nenhuma importância prática.

%FILE.NAME

Nome do arquivo .dat que será rodado, ou parte do nome do arquivo .sim que será obtido o resultado. Deve ser colocado somento o nome do arquivo, e não a sua extensão. Se o arquivo estiver em alguma pasta, deve-se colocar todo o caminho do arquivo, por exemplo:

 - input_files/CatenariaPaperMarStrHBL_BaseCase

%IND.RUN.SIMULATION

Indicador de que a simulação será rodada. Se o interesse for somente extrair resultados de um arquivo .sim já rodado, marcar como 0. Se for necessário rodar a simulação e salvar o arquivo .sim, para posterior coleta de resultados, marcar como 1.

Domínio aceito: 0 ou 1.

%NUMBER.OF.SIMULATIONS

Número de simulações que serão rodadas (se for rodadas simulações). A simulação será rodada e salva com o nome do arquivo .dat, mas com o final referente ao número da simulação, no formato "nome_do_arquivo_dat_XXX.sim", em que XXX é o número da simulação (ex: nome_do_arquivo_dat_017.sim).

Domínio aceito: Entre 1 e 999.

%IND.RUPT.TOP

Indicador de que a ruptura foi no topo. Se 0, indica que a ruptura foi numa região intermediária do riser, e serão coletados resultados considerando um trecho superior (linetop) e um trecho inferior (linebot). Se 1, indica que a ruptura foi no topo do riser, na conexão com a plataforma, e só serão coletados resultados considerando o trecho inferior do riser (linebot).

Domínio aceito: 0 ou 1.

%LINE.BOT.NAME

Nome do elemento de linha que representa o trecho inferior do riser. Por exemplo:

 - Linebot

%LINE.TOP.NAME

Nome do elemento de linha que representa o trecho superior do riser. Se não houver, nome será ignorado. Por exemplo:

 - Linetop

%SEABED.DEPTH

Profundidade do leito marinho. Utilizado para auxiliar o cálculo do tempo de queda.

%IND.GENERAL.STATISTICS

Indicador de que vai gravar arquivo .csv com algumas estatísticas gerais. 

Domínio aceito: 0 ou 1.

%IND.DEFORMED.CONFIGURATION

Indicador de que vai gravar arquivo .csv com posição X, Y e Z do riser em alguns tempos específicos. 

Domínio aceito: 0 ou 1.

%IND.ENVOLTORIAS

Indicador de que vai gravar arquivo .csv com as envoltórias de Raio de Curvatura, Tensão efetiva (tração) e Velocidade.

Domínio aceito: 0 ou 1.

%DEFORMED.CONFIGURATION.TIMESTAMPS

Timestamps que serão gravados a posição X, Y e Z do riser, caso a label %IND.DEFORMED.CONFIGURATION seja marcada como 1. Os tempos devem ser separados por vírgula, com um espaço entre eles, por exemplo:

 - 10, 20, 30, 40

Domínio aceito: Entre 0 e o tempo total de simulação do arquivo.

%IND.EFFECTIVE.TENSION

Indicador de que vai gravar arquivo .csv com a tensão efetiva do riser em alguns tempos específicos. 

Domínio aceito: 0 ou 1.

%EFFECTIVE.TENSION.TIMESTAMPS

Timestamps que será gravada a tensão efetiva do riser, caso a label %IND.EFFECTIVE.TENSION seja marcada como 1. Os tempos devem ser separados por vírgula, com um espaço entre eles, por exemplo:

 - 10, 20, 30, 40

Domínio aceito: Entre 0 e o tempo total de simulação do arquivo.