import OrcFxAPI
import os
import pandas as pd

class OrcSimulation:
    def __init__(self, parameters, debug):
        
        if debug:
            print("\tInstanciando parâmetros...")

        self.file_name = parameters['file_name'] 
        self.number_of_simulations = parameters['number_of_simulations']
        self.ind_run_simulation = parameters['ind_run_simulation']
        self.ind_obter_configuracao_solo = parameters['ind_obter_configuracao_solo']
        self.ind_obter_cmp_e_lrg_queda = parameters['ind_obter_cmp_e_lrg_queda']
        self.ind_obter_energia = parameters['ind_obter_energia']
        self.ind_obter_configuracao_def = parameters['ind_obter_configuracao_def']
        self.ind_obter_tensao_efetiva = parameters['ind_obter_tensao_efetiva']
        self.ind_obter_estat_gerais = parameters['ind_obter_estat_gerais']
        self.ind_rupture_on_top = parameters['ind_rupture_on_top']
        self.linebot_name = parameters['linebot_name']
        self.linetop_name = parameters['linetop_name']
        self.seabed_depth = parameters['seabed_depth']
        self.def_config_timestamps = parameters['def_config_timestamps']
        self.eff_tension_timestamps = parameters['eff_tension_timestamps']

        self.debug = debug

        self.base_model = OrcFxAPI.Model()

    def run_simulation(self):

        if self.ind_run_simulation:
            for i in range(self.number_of_simulations):
                if self.debug:
                    print(f"\tRodando simulação número {i + 1}...)")
                self.base_model.LoadData(f"{self.file_name}.dat")
    
                self.base_model.RunSimulation( )

                if i + 1 < 10:
                    num_file = f"00{i + 1}"
                elif i + 1 < 100:
                    num_file = f"0{i + 1}"
                else:
                    num_file = f"{i + 1}"
    
                self.base_model.SaveSimulation(f"{self.file_name}_{num_file}.sim")
        else:
            if self.debug:
                print("\tConforme arquivo de entrada, não será rodada simulação do arquivo (provavelmente a simulação já foi rodada.)")

    def save_results(self):

        if self.debug:
            print("\tIniciando coleta de resultados...")
        
        try:
            path_sim  = "/".join(self.file_name.split('/')[0:-1])
            name_file = self.file_name.split('/')[-1]
        except IndexError:
            path_sim  = ""
            name_file = self.file_name

        sim_files = [file for file in os.listdir(path_sim) if (name_file in file) and (".sim" in file)]

        if self.debug:
            print("\tSerão coletados resultados para os seguintes arquivos de simulação:")
            for sim_file in sim_files:
                print(f"\t\t - {sim_file}")
            print("\tSerão coletados resultados de:")
            if self.ind_obter_estat_gerais:
                print(f"\t\t - Estatísticas gerais sobre o processo.")
            if self.ind_obter_configuracao_def:
                print(f"\t\t - Configuração deformada (em certos instantes de tempo).")
            if self.ind_obter_tensao_efetiva:
                print(f"\t\t - Tensão efetiva (em certos instantes de tempo).")
            print("\n")
            print("\tIniciando coleta de resultados...")

        for sim_file in sim_files:

            file_to_get_results = path_sim + "/" + sim_file
            if self.debug:
                print(f"\t\tColeta de resultados do arquivo {file_to_get_results}.")

            if self.ind_obter_estat_gerais:

                if self.debug:
                    print("\t\t\tColetando estatísticas gerais...")

                self.save_estat_gerais(file_to_get_results)

            if self.ind_obter_configuracao_def:

                if self.debug:
                    print("\t\t\tColetando configuração deformada...")

                self.save_def_config(file_to_get_results)

            if self.ind_obter_tensao_efetiva:

                if self.debug:
                    print("\t\t\tColetando tensão efetiva...")

                self.save_eff_tension(file_to_get_results)

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

            # Obtendo tensão efetiva máxima
            # São ignorados os 10 primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Tmax = max(linebot.RangeGraph("Effective Tension", None).Max[10:])

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
                      "Tmax" : [Tmax],
                      "NitTotl" : [NitTotl],
                      "NitMean" : [NitMean]
                     }
        
        self.write_results(pd.DataFrame(dict_write), file[:-3] + "_GeneralResults.csv")

    def save_def_config(self, file):

        model = OrcFxAPI.Model()

        model.LoadSimulation(file)

        linebot = model[self.linebot_name]
        linebotrange = linebot.RangeGraphXaxis('X')

        if self.ind_rupture_on_top == 0:
            linetop = model[self.linetop_name]
            linetoprange = linetop.RangeGraphXaxis('X')

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        gen = model.general

        BuildupTime = gen.StageDuration[0]

        if not SimComp:
            print("Simulação não finalizou. Não serão obtidos resultados da configuração deformada.")
        else:
            if self.ind_rupture_on_top == 0:

                dict_write = {}

                for timestamp in self.def_config_timestamps:

                    Xtop = linetop.RangeGraph('X', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean
                    Ytop = linetop.RangeGraph('Y', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean
                    Ztop = linetop.RangeGraph('Z', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean   

                    dict_write[f'X_{timestamp}'] = Xtop
                    dict_write[f'Y_{timestamp}'] = Ytop
                    dict_write[f'Z_{timestamp}'] = Ztop

                self.write_results(pd.DataFrame(dict_write), file[:-3] + "_Linetop_DeformedConfig.csv")

            dict_write = {}

            for timestamp in self.def_config_timestamps:

                Xbot = linebot.RangeGraph('X', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean
                Ybot = linebot.RangeGraph('Y', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean
                Zbot = linebot.RangeGraph('Z', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean

                dict_write[f'X_{timestamp}'] = Xbot
                dict_write[f'Y_{timestamp}'] = Ybot
                dict_write[f'Z_{timestamp}'] = Zbot

            self.write_results(pd.DataFrame(dict_write), file[:-3] + "_Linebop_DeformedConfig.csv")

    def save_eff_tension(self, file):

        model = OrcFxAPI.Model()

        model.LoadSimulation(file)

        linebot = model[self.linebot_name]
        linebotrange = linebot.RangeGraphXaxis('X')

        if self.ind_rupture_on_top == 0:
            linetop = model[self.linetop_name]
            linetoprange = linetop.RangeGraphXaxis('X')

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        gen = model.general

        BuildupTime = gen.StageDuration[0]

        if not SimComp:
            print("Simulação não finalizou. Não serão obtidos resultados da configuração deformada.")
        else:
            if self.ind_rupture_on_top == 0:

                dict_write = {}

                for timestamp in self.eff_tension_timestamps:

                    Ttop = linetop.RangeGraph('Effective Tension', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean

                    dict_write[f'EffTens_{timestamp}'] = Ttop

                self.write_results(pd.DataFrame(dict_write), file[:-3] + "_Linetop_EffectiveTension.csv")

            dict_write = {}

            for timestamp in self.def_config_timestamps:

                Tbot = linebot.RangeGraph('Effective Tension', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001 + BuildupTime, timestamp + BuildupTime)).Mean

                dict_write[f'EffTens_{timestamp}'] = Tbot

            self.write_results(pd.DataFrame(dict_write), file[:-3] + "_Linebop_EffectiveTension.csv")

    def write_results(self, df, name):

        df.to_csv(name, index = False)
