from helpers.functions import *
from classes.OrcSimulation import OrcSimulation
import os

def main():

    input_file_name = "input_catenaria_paper.txt"

    parameters = read_input_parameters(f"input_files/{input_file_name}")

    simulacao = OrcSimulation(parameters)

    simulacao.run_simulation( )

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
    #         - Tensão efetiva do riser em certos instantes de tempo
    #         - Envoltórias (Obter envoltórias com tensão máxima e mínima, velocidade máxima e mínima, aceleração máxima e mínima e curvatura máxima e mínima)
    #         - Estatísticas gerais (Planilha geral contendo as seguintes estatísticas gerais: Wall-Clock Time, Velocidade máxima, Tempo de queda)
    #
    simulacao.save_results( )

if __name__ == "__main__":
    main()

