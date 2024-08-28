from helpers.functions import *
from classes.OrcSimulation import OrcSimulation

def main():

    input_file_name = "input_file.txt"

    parameters = read_input_parameters(input_file_name)

    simulacao = OrcSimulation(parameters)

    # TO DO: Fazer método da classe OrcSimulation, que vai rodar um número N de simulações
    #        especificado na entrada. O arquivo dat utilizado será utilizado como base, e, a 
    #        cada arquivo de simulação rodado, será alterada a seed de simulação. A seed aumentará
    #        de 1 até N, e a seed será colocada no nome do arquivo no formato:
    #          - nome_do_arquivo_XXX.dat
    #        em que os três algarismos finais representarão a seed (por exemplo, 043).
    #
    # if parameters['ind_run_simulation'] == 1:
    #   simulacao.run_simulation()

    # TO DO: Fazer método da classe OrcSimulation, que vai salvar os resultados da simulação.
    #        Múltiplos resultados podem ser salvos para uma mesma simulação, e existirá uma função
    #        específica para cada tipo de resultado. A escolha de quais resultados devem ser salvos 
    #        será feita a partir de labels do arquivo de entrada.
    #        O método vai chamar várias funções que criam cada uma um resultado específico.
    #        Devem ser criadas funções para salvar os seguintes resultados:
    #         - Configuração no solo (coordenadas X e Y ao final da simulação)
    #         - Comprimento e largura de queda, assim como posição do TDP (X e Y)
    #         - Energia cinética e gravitacional total ao longo do tempo (Para cada instante de tempo, obter somatório de m*v^2/2 e de m*g*h ao longo do riser)
    #         - Configuração deformada (Em instantes específicos de tempo, obter as coordenadas X, Y, Z do riser)
    #         - Estatísticas gerais (Planilha geral contendo as seguintes estatísticas gerais: Wall-Clock Time, Velocidade máxima, Tempo de queda)
    #
    # simulacao.save_results(parameters)

if __name__ == "__main__":
    main()

