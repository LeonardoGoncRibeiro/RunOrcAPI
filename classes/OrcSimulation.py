import OrcFxAPI
import os

class OrcSimulation:
    def __init__(self, parameters):

        self.file_name = parameters['file_name'] 
        self.number_of_simulations = parameters['number_of_simulations']
        self.ind_run_simulation = parameters['ind_run_simulation']
        self.ind_obter_configuracao_solo = parameters['ind_obter_configuracao_solo']
        self.ind_obter_cmp_e_lrg_queda = parameters['ind_obter_cmp_e_lrg_queda']
        self.ind_obter_energia = parameters['ind_obter_energia']
        self.ind_obter_configuracao_def = parameters['ind_obter_configuracao_def']
        self.ind_obter_estat_gerais = parameters['ind_obter_estat_gerais']

        self.base_model = OrcFxAPI.Model()

    def run_simulation(self):
    
        if self.ind_run_simulation:
            for i in range(self.number_of_simulations):
                self.base_model.LoadData(f"{self.file_name}.dat")
    
                self.base_model.RunSimulation( )

                if i < 10:
                    num_file = f"00{i}"
                elif i < 100:
                    num_file = f"0{i}"
                else:
                    num_file = f"{i}"
    
                self.base_model.SaveSimulation(f"{self.file_name}_{num_file}.sim")

    #def save_results(self):
    #
    #    sim_files = [sim for sim in os.listdir("input_files") if (self.file_name in sim) and (".sim" in sim)]

    #    for sim_file in sim_files:

    #        if self.ind_obter_estat_gerais:

    #            self.save_estat_gerais( )

    #def save_estat_gerais(self):

