import OrcFxAPI
import os
import pandas as pd

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
        self.ind_rupture_on_top = parameters['ind_rupture_on_top']
        self.linebot_name = parameters['linebot_name']
        self.linetop_name = parameters['linetop_name']
        self.seabed_depth = parameters['seabed_depth']

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

    def save_results(self):
        
        try:
            path_sim  = "/".join(self.file_name.split('/')[0:-1])
            name_file = self.file_name.split('/')[-1]
        except IndexError:
            path_sim  = ""
            name_file = self.file_name

        sim_files = [file for file in os.listdir(path_sim) if (name_file in file) and (".sim" in file)]

        for sim_file in sim_files:

            if self.ind_obter_estat_gerais:

                self.save_estat_gerais(path_sim + "/" + sim_file)

    def save_estat_gerais(self, file):

        model = OrcFxAPI.Model()

        gen = model.general

        env = model.environment

        Depth = self.seabed_depth

        model.LoadSimulation(file)

        # Obtendo tempo gasto na simulação
        WCT = gen.WallClockTime

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        FallTime = 9999
        Vmax = 0
        NitTotl = 0
        NitMean = 0
        if SimComp:

            TotalSimTime = sum(gen.StageDuration[1:])

            linebot = model[self.linebot_name]
            linebotrange = linebot.RangeGraphXaxis('X')

            if self.ind_rupture_on_top == 0:
                linetop = model[self.linetop_name]
                linetoprange = linetop.RangeGraphXaxis('X')

            time = model.SampleTimes(period = None)

            # Obtendo tempo de queda

            Ztop = linebot.TimeHistory("Z", None, OrcFxAPI.oeEndA)

            
            for k in range(len(time)):
                if Ztop[k] < -(Depth - 1):
                    FallTime = time[k]
                    break

            # Obtendo velocidade máxima
            # São ignorados os 10 primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Vmax = max(linebot.RangeGraph("Velocity", None).Max[10:])

            # Número de Iterações
            iter = gen.TimeHistory("Implicit solver iteration count", None)

            NitTotl = sum(iter)
            NitMean = NitTotl/len(iter)

        dict_write = {"WCT" : [WCT],
                      "SimComp" : [SimComp],
                      "FallTime" : [FallTime],
                      "Vmax" : [Vmax],
                      "NitTotl" : [NitTotl],
                      "NitMean" : [NitMean]
                     }
        
        self.write_results(pd.DataFrame(dict_write), file[:-3] + "_GeneralResults.csv")

    def write_results(self, df, name):

        df.to_csv(name, index = False)
