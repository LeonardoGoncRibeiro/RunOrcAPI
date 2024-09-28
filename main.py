from helpers.functions import *
from classes.OrcSimulation import OrcSimulation
import os

def main():

    # Entrada:
    # input_file_name - Colocar nome do arquivo input.txt, com os parâmetros para rodada do programa.
    # debug - Coloque True para a versão debug, que possui alguns impressões ao longo do código para auxílio em possíveis debugs.

    input_file_name = "InputSPA1_A2M5_Correntes.txt"
    debug = True

    # --------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------

    if debug:
        print("Lendo arquivo de entrada...")

    # TO DO: Ajustar leitura dos parâmetros, para verificar se o valor definido de um parâmetro está dentro do domínio aceito.

    parameters = read_input_parameters(f"input_files/{input_file_name}") 

    if debug:
        print("Arquivo de entrada lido.\n")

    if debug:
        print("Instanciando objeto para auxiliar a simulação e coleta de resultados, considerando os parâmetros de entrada...")

    simulacao = OrcSimulation(parameters, debug)

    if debug:
        print("Objeto instanciado.\n")

    if debug:
        print("Rodando simulação...")

    simulacao.run_simulation( )

    if debug:
        print("Simulação(ões) rodada(s).\n")

    # TO DO: Fazer método da classe OrcSimulation, que vai salvar os resultados da simulação.
    #        Múltiplos resultados podem ser salvos para uma mesma simulação, e existirá uma função
    #        específica para cada tipo de resultado. A escolha de quais resultados devem ser salvos 
    #        será feita a partir de labels do arquivo de entrada.
    #        O método vai chamar várias funções que criam cada uma um resultado específico.
    #        Devem ser criadas funções para salvar os seguintes resultados:
    #         - Comprimento e largura de queda, assim como posição do TDP (X e Y) - Incluir dentro da obtenção dos resultados gerais
    #         - Energia cinética e gravitacional total ao longo do tempo (Para cada instante de tempo, obter somatório de m*v^2/2 e de m*g*h ao longo do riser)
    #         - Envoltórias (Obter envoltórias com tensão máxima e mínima, velocidade máxima e mínima, aceleração máxima e mínima e curvatura máxima e mínima)

    if debug:
        print("Salvando resultados...")

    simulacao.save_results( )

    if debug:
        print("Resultados salvos.\n")
        print("Fim do programa.")

if __name__ == "__main__":
    main()

