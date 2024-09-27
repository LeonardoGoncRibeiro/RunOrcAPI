import OrcFxAPI
import os
import pandas as pd

class OrcSimulation:
    def __init__(self, parameters, debug):
        
        if debug:
            print("\tInstanciando parâmetros...")

        self.file_name                   = parameters['file_name'] 
        self.number_of_simulations       = parameters['number_of_simulations']
        self.ind_run_simulation          = parameters['ind_run_simulation']
        self.ind_obter_configuracao_solo = parameters['ind_obter_configuracao_solo']
        self.ind_obter_cmp_e_lrg_queda   = parameters['ind_obter_cmp_e_lrg_queda']
        self.ind_obter_energia           = parameters['ind_obter_energia']
        self.ind_obter_configuracao_def  = parameters['ind_obter_configuracao_def']
        self.ind_obter_tensao_efetiva    = parameters['ind_obter_tensao_efetiva']
        self.ind_obter_curvatura         = parameters['ind_obter_curvatura']
        self.ind_obter_envoltorias       = parameters['ind_obter_envoltorias']
        self.ind_obter_estat_gerais      = parameters['ind_obter_estat_gerais']
        self.ind_rupture_on_top          = parameters['ind_rupture_on_top']
        self.ind_cabo                    = parameters['ind_cabo']
        self.linebot_name                = parameters['linebot_name']
        self.linetop_name                = parameters['linetop_name']
        self.cable_name                  = parameters['cable_name']
        self.seabed_depth                = parameters['seabed_depth']
        self.def_config_timestamps       = parameters['def_config_timestamps']
        self.eff_tension_timestamps      = parameters['eff_tension_timestamps']
        self.curv_timestamps             = parameters['curv_timestamps']

        self.debug = debug

        self.base_model = OrcFxAPI.Model()

    def run_simulation(self):

        if self.ind_run_simulation:
            for i in range(self.number_of_simulations):
                if self.debug:
                    print(f"\tRodando simulação número {i + 1}...")
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
            if self.ind_obter_curvatura:
                print(f"\t\t - Curvatura (em certos instantes de tempo).")
            if self.ind_obter_envoltorias:
                print(f"\t\t - Envoltórias (Raio de Curvatura, Velocidade, Tração).")
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

            if self.ind_obter_curvatura:

                if self.debug:
                    print("\t\t\tColetando curvatura...")

                self.save_curvature(file_to_get_results)

            if self.ind_obter_envoltorias:

                if self.debug:
                    print("\t\t\tColetando envoltórias...")

                self.save_envoltorias(file_to_get_results)

    def save_estat_gerais(self, file):

        N_nodes_ignore = 10

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
        Tmin = 0
        Tmax = 0
        Cmax = 0
        Vmax = 0
        Bmin = 0
        NitTotl = 0
        NitMean = 0

        line_list = []
        WCT_list = []
        SimComp_list = []
        FallTime_list = []
        Vmax_list = []
        Tmin_list = []
        Tmax_list = []
        Cmax_list = []
        Bmin_list = []
        NitTotl_list = []
        NitMean_list = []

        if SimComp:

            TotalSimTime = sum(gen.StageDuration[1:])

            linebot = model[self.linebot_name]
            linebotrange = linebot.RangeGraphXaxis('X')

            if self.ind_rupture_on_top == 0:
                linetop = model[self.linetop_name]
                linetoprange = linetop.RangeGraphXaxis('X')

            if self.ind_cabo == 1:
                cabo = model[self.cable_name]
                caborange = cabo.RangeGraphXaxis('X')

            time = model.SampleTimes(period = None)

            # Obtendo tempo de queda

            Ztop = linebot.TimeHistory("Z", None, OrcFxAPI.oeEndA)

            for k in range(len(time)):
                if Ztop[k] < -(Depth - 1):
                    FallTime = time[k]
                    break

            # Obtendo tensão efetiva máxima
            # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Tmax = max(linebot.RangeGraph("Effective Tension", None).Max[N_nodes_ignore:])

            # Obtendo tensão efetiva mínima
            # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Tmin = min(linebot.RangeGraph("Effective Tension", None).Min[N_nodes_ignore:])

            # Obtendo velocidade máxima
            # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Vmax = max(linebot.RangeGraph("Velocity", None).Max[N_nodes_ignore:])

            # Obtendo a curvatura máxima
            # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Cmax = max(linebot.RangeGraph("Curvature", None).Max[N_nodes_ignore:])

            # Obtendo a curvatura máxima
            # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
            Bmin = min(linebot.RangeGraph("Bend radius", None).Min[N_nodes_ignore:])

            # Número de Iterações
            iter = gen.TimeHistory("Implicit solver iteration count", None)

            NitTotl = sum(iter)
            NitMean = NitTotl/len(iter)

            line_list.append(self.linebot_name)
            WCT_list.append(WCT)
            SimComp_list.append(SimComp)
            FallTime_list.append(FallTime)
            Vmax_list.append(Vmax)
            Tmin_list.append(Tmin)
            Tmax_list.append(Tmax)
            Cmax_list.append(Cmax)
            Bmin_list.append(Bmin)
            NitTotl_list.append(NitTotl)
            NitMean_list.append(NitMean)

            if self.ind_rupture_on_top == 0:
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Tmax = max(linetop.RangeGraph("Effective Tension", None).Max[N_nodes_ignore:])

                # Obtendo tensão efetiva mínima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Tmin = min(linetop.RangeGraph("Effective Tension", None).Min[N_nodes_ignore:])

                # Obtendo velocidade máxima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Vmax = max(linetop.RangeGraph("Velocity", None).Max[N_nodes_ignore:])

                # Obtendo a curvatura máxima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Cmax = max(linetop.RangeGraph("Curvature", None).Max[N_nodes_ignore:])

                # Obtendo a curvatura máxima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Bmin = min(linetop.RangeGraph("Bend radius", None).Min[N_nodes_ignore:])

                # Número de Iterações
                iter = gen.TimeHistory("Implicit solver iteration count", None)

                NitTotl = sum(iter)
                NitMean = NitTotl/len(iter)

                line_list.append(self.linetop_name)
                WCT_list.append(WCT)
                SimComp_list.append(SimComp)
                FallTime_list.append(FallTime)
                Vmax_list.append(Vmax)
                Tmin_list.append(Tmin)
                Tmax_list.append(Tmax)
                Cmax_list.append(Cmax)
                Bmin_list.append(Bmin)
                NitTotl_list.append(NitTotl)
                NitMean_list.append(NitMean)

            if self.ind_cabo == 1:
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Tmax = max(cabo.RangeGraph("Effective Tension", None).Max[N_nodes_ignore:])

                # Obtendo tensão efetiva mínima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Tmin = min(cabo.RangeGraph("Effective Tension", None).Min[N_nodes_ignore:])

                # Obtendo velocidade máxima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Vmax = max(cabo.RangeGraph("Velocity", None).Max[N_nodes_ignore:])

                # Obtendo a curvatura máxima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Cmax = max(cabo.RangeGraph("Curvature", None).Max[N_nodes_ignore:])

                # Obtendo a curvatura máxima
                # São ignorados os N primeiros nós, que podem ter algum valor muito "esdrúxulo" por conta da proximidade com a ruptura
                Bmin = min(cabo.RangeGraph("Bend radius", None).Min[N_nodes_ignore:])

                # Número de Iterações
                iter = gen.TimeHistory("Implicit solver iteration count", None)

                NitTotl = sum(iter)
                NitMean = NitTotl/len(iter)

                line_list.append(self.cable_name)
                WCT_list.append(WCT)
                SimComp_list.append(SimComp)
                FallTime_list.append(FallTime)
                Vmax_list.append(Vmax)
                Tmin_list.append(Tmin)
                Tmax_list.append(Tmax)
                Cmax_list.append(Cmax)
                Bmin_list.append(Bmin)
                NitTotl_list.append(NitTotl)
                NitMean_list.append(NitMean)

        dict_write = {"Linha" : line_list,
                      "WCT" : WCT_list,
                      "SimComp" : SimComp_list,
                      "FallTime" : FallTime_list,
                      "Vmax" : Vmax_list,
                      "Tmin" : Tmin_list,
                      "Tmax" : Tmax_list,
                      "Cmax" : Cmax_list,
                      "Bmin" : Bmin_list,
                      "NitTotl": NitTotl_list,
                      "NitMean" : NitMean_list
                     }
        
        self.write_results(pd.DataFrame(dict_write), file[:-4] + "_GeneralResults.csv")

    def save_def_config(self, file):

        model = OrcFxAPI.Model()

        model.LoadSimulation(file)

        linebot = model[self.linebot_name]
        linebotrange = linebot.RangeGraphXaxis('X')

        if self.ind_rupture_on_top == 0:
            linetop = model[self.linetop_name]
            linetoprange = linetop.RangeGraphXaxis('X')

        if self.ind_cabo == 1:
            cabo = model[self.cable_name]
            caborange = cabo.RangeGraphXaxis('X')

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        gen = model.general

        BuildupTime = gen.StageDuration[0]

        if not SimComp:
            print("Simulação não finalizou. Não serão obtidos resultados da configuração deformada.")
        else:
            if self.ind_rupture_on_top == 0:

                dict_write = {}
                dict_write['X'] = linetoprange

                for timestamp in self.def_config_timestamps:

                    Xtop = linetop.RangeGraph('X', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean
                    Ytop = linetop.RangeGraph('Y', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean
                    Ztop = linetop.RangeGraph('Z', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean   

                    dict_write[f'X_{timestamp}'] = Xtop
                    dict_write[f'Y_{timestamp}'] = Ytop
                    dict_write[f'Z_{timestamp}'] = Ztop

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linetop_DeformedConfig.csv")

            if self.ind_cabo == 1:

                dict_write = {}
                dict_write['X'] = caborange

                for timestamp in self.def_config_timestamps:

                    Xcabo = cabo.RangeGraph('X', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean
                    Ycabo = cabo.RangeGraph('Y', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean
                    Zcabo = cabo.RangeGraph('Z', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean   

                    dict_write[f'X_{timestamp}'] = Xcabo
                    dict_write[f'Y_{timestamp}'] = Ycabo
                    dict_write[f'Z_{timestamp}'] = Zcabo

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Cabo_DeformedConfig.csv")

            dict_write = {}
            dict_write['X'] = linebotrange

            for timestamp in self.def_config_timestamps:

                Xbot = linebot.RangeGraph('X', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean
                Ybot = linebot.RangeGraph('Y', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean
                Zbot = linebot.RangeGraph('Z', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                dict_write[f'X_{timestamp}'] = Xbot
                dict_write[f'Y_{timestamp}'] = Ybot
                dict_write[f'Z_{timestamp}'] = Zbot

            self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linebot_DeformedConfig.csv")

    def save_eff_tension(self, file):

        model = OrcFxAPI.Model()

        model.LoadSimulation(file)

        linebot = model[self.linebot_name]
        linebotrange = linebot.RangeGraphXaxis('X')

        if self.ind_rupture_on_top == 0:
            linetop = model[self.linetop_name]
            linetoprange = linetop.RangeGraphXaxis('X')

        if self.ind_cabo == 1:
            cabo = model[self.cable_name]
            caborange = cabo.RangeGraphXaxis('X')

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        gen = model.general

        BuildupTime = gen.StageDuration[0]

        if not SimComp:
            print("Simulação não finalizou. Não serão obtidos resultados da configuração deformada.")
        else:
            if self.ind_rupture_on_top == 0:

                dict_write = {}
                dict_write['X'] = linetoprange

                for timestamp in self.eff_tension_timestamps:

                    Ttop = linetop.RangeGraph('Effective Tension', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                    dict_write[f'EffTens_{timestamp}'] = Ttop[0:len(linetoprange)]

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linetop_EffectiveTension.csv")

            if self.ind_cabo == 1:

                dict_write = {}
                dict_write['X'] = caborange

                for timestamp in self.eff_tension_timestamps:

                    Ttop = cabo.RangeGraph('Effective Tension', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                    dict_write[f'EffTens_{timestamp}'] = Ttop[0:len(caborange)]

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Cabo_EffectiveTension.csv")

            dict_write = {}
            dict_write['X'] = linebotrange

            for timestamp in self.eff_tension_timestamps:

                Tbot = linebot.RangeGraph('Effective Tension', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                dict_write[f'EffTens_{timestamp}'] = Tbot[0:len(linebotrange)]

            self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linebot_EffectiveTension.csv")

    def save_curvature(self, file):

        model = OrcFxAPI.Model()

        model.LoadSimulation(file)

        linebot = model[self.linebot_name]
        linebotrange = linebot.RangeGraphXaxis('X')

        if self.ind_rupture_on_top == 0:
            linetop = model[self.linetop_name]
            linetoprange = linetop.RangeGraphXaxis('X')

        if self.ind_cabo == 1:
            cabo = model[self.cable_name]
            caborange = cabo.RangeGraphXaxis('X')

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        gen = model.general

        BuildupTime = gen.StageDuration[0]

        if not SimComp:
            print("Simulação não finalizou. Não serão obtidos resultados da configuração deformada.")
        else:
            if self.ind_rupture_on_top == 0:

                dict_write = {}
                dict_write['X'] = linetoprange

                for timestamp in self.curv_timestamps:

                    Ctop = linetop.RangeGraph('Curvature', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                    dict_write[f'Curv_{timestamp}'] = Ctop[0:len(linetoprange)]

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linetop_Curvature.csv")

            if self.ind_cabo == 1:

                dict_write = {}
                dict_write['X'] = caborange

                for timestamp in self.curv_timestamps:

                    Ctop = cabo.RangeGraph('Curvature', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                    dict_write[f'Curv_{timestamp}'] = Ctop[0:len(caborange)]

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Cabo_Curvature.csv")

            dict_write = {}
            dict_write['X'] = linebotrange

            for timestamp in self.curv_timestamps:

                Cbot = linebot.RangeGraph('Curvature', OrcFxAPI.SpecifiedPeriod(timestamp - 0.001, timestamp)).Mean

                dict_write[f'Curv_{timestamp}'] = Cbot[0:len(linebotrange)]

            self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linebot_Curvature.csv")

    def save_envoltorias(self, file):

        model = OrcFxAPI.Model()

        model.LoadSimulation(file)

        gen = model.general

        TotalSimTime = sum(gen.StageDuration[1:])

        linebot = model[self.linebot_name]
        linebotrange = linebot.RangeGraphXaxis('X')

        if self.ind_rupture_on_top == 0:
            linetop = model[self.linetop_name]
            linetoprange = linetop.RangeGraphXaxis('X')

        if self.ind_cabo == 1:
            cabo = model[self.cable_name]
            caborange = cabo.RangeGraphXaxis('X')

        # Obtendo indicador de simulação completa
        SimComp = model.simulationComplete

        gen = model.general

        BuildupTime = gen.StageDuration[0]

        if not SimComp:
            print("Simulação não finalizou. Não serão obtidos resultados da configuração deformada.")
        else:
            if self.ind_rupture_on_top == 0:

                dict_write = {}
                dict_write['X'] = linetoprange

                Bmax = linetop.RangeGraph('Bend radius', OrcFxAPI.pnWholeSimulation).Max
                Bmin = linetop.RangeGraph('Bend radius', OrcFxAPI.pnWholeSimulation).Min
                Tmax = linetop.RangeGraph('Effective tension', OrcFxAPI.pnWholeSimulation).Max
                Tmin = linetop.RangeGraph('Effective tension', OrcFxAPI.pnWholeSimulation).Min
                Vmax = linetop.RangeGraph('Velocity', OrcFxAPI.pnWholeSimulation).Max
                Vmin = linetop.RangeGraph('Velocity', OrcFxAPI.pnWholeSimulation).Min

                dict_write[f'Bmax'] = Bmax[0:len(linetoprange)]
                dict_write[f'Bmin'] = Bmin[0:len(linetoprange)]
                dict_write[f'Tmax'] = Tmax[0:len(linetoprange)]
                dict_write[f'Tmin'] = Tmin[0:len(linetoprange)]
                dict_write[f'Vmax'] = Vmax[0:len(linetoprange)]
                dict_write[f'Vmin'] = Vmin[0:len(linetoprange)]

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linetop_Envoltorias.csv")

            if self.ind_cabo == 1:

                dict_write = {}
                dict_write['X'] = caborange

                Bmax = cabo.RangeGraph('Bend radius', OrcFxAPI.pnWholeSimulation).Max
                Bmin = cabo.RangeGraph('Bend radius', OrcFxAPI.pnWholeSimulation).Min
                Tmax = cabo.RangeGraph('Effective tension', OrcFxAPI.pnWholeSimulation).Max
                Tmin = cabo.RangeGraph('Effective tension', OrcFxAPI.pnWholeSimulation).Min
                Vmax = cabo.RangeGraph('Velocity', OrcFxAPI.pnWholeSimulation).Max
                Vmin = cabo.RangeGraph('Velocity', OrcFxAPI.pnWholeSimulation).Min

                dict_write[f'Bmax'] = Bmax[0:len(caborange)]
                dict_write[f'Bmin'] = Bmin[0:len(caborange)]
                dict_write[f'Tmax'] = Tmax[0:len(caborange)]
                dict_write[f'Tmin'] = Tmin[0:len(caborange)]
                dict_write[f'Vmax'] = Vmax[0:len(caborange)]
                dict_write[f'Vmin'] = Vmin[0:len(caborange)]

                self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Cabo_Envoltorias.csv")

            dict_write = {}
            dict_write['X'] = linebotrange

            Bmax = linebot.RangeGraph('Bend radius', OrcFxAPI.pnWholeSimulation).Max
            Bmin = linebot.RangeGraph('Bend radius', OrcFxAPI.pnWholeSimulation).Min
            Tmax = linebot.RangeGraph('Effective tension', OrcFxAPI.pnWholeSimulation).Max
            Tmin = linebot.RangeGraph('Effective tension', OrcFxAPI.pnWholeSimulation).Min
            Vmax = linebot.RangeGraph('Velocity', OrcFxAPI.pnWholeSimulation).Max
            Vmin = linebot.RangeGraph('Velocity', OrcFxAPI.pnWholeSimulation).Min

            dict_write[f'Bmax'] = Bmax[0:len(linebotrange)]
            dict_write[f'Bmin'] = Bmin[0:len(linebotrange)]
            dict_write[f'Tmax'] = Tmax[0:len(linebotrange)]
            dict_write[f'Tmin'] = Tmin[0:len(linebotrange)]
            dict_write[f'Vmax'] = Vmax[0:len(linebotrange)]
            dict_write[f'Vmin'] = Vmin[0:len(linebotrange)]

            self.write_results(pd.DataFrame(dict_write), file[:-4] + "_Linebot_Envoltorias.csv")

    def write_results(self, df, name):

        df.to_csv(name, index = False)
