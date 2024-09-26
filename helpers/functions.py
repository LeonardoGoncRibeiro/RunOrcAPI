def read_input_parameters(input_file_name):

    # Setando parâmetros default
    parameters = {
                  "header"                      : "cabeçalho",
                  "file_name"                   : "simulation",
                  "number_of_simulations"       : 1,
                  "ind_run_simulation"          : 0,
                  "ind_obter_configuracao_solo" : 0,
                  "ind_obter_cmp_e_lrg_queda"   : 0,
                  "ind_obter_energia"           : 0,
                  "ind_obter_configuracao_def"  : 0,
                  "ind_obter_estat_gerais"      : 0,
                  "ind_obter_tensao_efetiva"    : 0,
                  "ind_obter_curvatura"         : 0,
                  "ind_obter_envoltorias"       : 0,
                  "ind_rupture_on_top"          : 1,
                  "ind_cabo"                    : 1,
                  "linebot_name"                : "LineBot",
                  "linetop_name"                : "LineTop",
                  "cable_name"                  : "Cabo",
                  "seabed_depth"                : 100,
                  "def_config_timestamps"       : [],
                  "eff_tension_timestamps"      : [],
                  "curv_timestamps"             : []
                 }

    # Leitura do arquivo de entrada
    try:
        with open(input_file_name) as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise NameError(f"Arquivo input {input_file_name} não encontrado.")

    in_read_param = False
    param_name = ''

    for line in lines:
        if line[0] == '%':
            param_header = line[:-1] if line[-1] == "\n" else line 
            param_name = get_parameter_name(param_header)
            in_read_param = True
            continue

        if in_read_param:
            param_value = get_parameter_value(param_name, line)
            parameters[param_name] = param_value
            param_name = ''
            in_read_param = False

    return parameters

def get_parameter_name(param_header):
    match param_header:
        case "%HEADER":
            return "header"
        case "%FILE.NAME":
            return "file_name"
        case "%NUMBER.OF.SIMULATIONS":
            return "number_of_simulations"
        case "%IND.RUN.SIMULATION":
            return "ind_run_simulation"
        case "%IND.SOIL.CONFIG":
            return "ind_obter_configuracao_solo"
        case "%IND.FALL.LENGTH.AND.WIDTH":
            return "ind_obter_cmp_e_lrg_queda"
        case "%IND.ENERGY":
            return "ind_obter_energia"
        case "%IND.DEFORMED.CONFIGURATION":
            return "ind_obter_configuracao_def"
        case "%IND.GENERAL.STATISTICS":
            return "ind_obter_estat_gerais"
        case "%IND.EFFECTIVE.TENSION":
            return "ind_obter_tensao_efetiva"
        case "%IND.CURVATURE":
            return "ind_obter_curvatura"
        case "%IND.ENVOLTORIAS":
            return "ind_obter_envoltorias"
        case "%IND.RUPT.TOP":
            return "ind_rupture_on_top"
        case "%IND.CABO":
            return "ind_cabo"
        case "%LINE.BOT.NAME":
            return "linebot_name"
        case "%LINE.TOP.NAME":
            return "linetop_name"
        case "%CABLE.NAME":
            return "cable_name"
        case "%SEABED.DEPTH":
            return "seabed_depth"
        case "%DEFORMED.CONFIGURATION.TIMESTAMPS":
            return "def_config_timestamps"
        case "%EFFECTIVE.TENSION.TIMESTAMPS":
            return "eff_tension_timestamps"
        case "%CURVATURE.TIMESTAMPS":
            return "curv_timestamps"
        case _:
            print(f"Não há parâmetro denominado {param_header} configurado.")
            return ''
        
def get_parameter_value(param_name, line):

    param_to_return = line[:-1] if line[-1] == "\n" else line 

    match param_name:
        case "header":
            return str(param_to_return)
        case "file_name":
            return str(param_to_return)
        case "number_of_simulations":
            return int(param_to_return)
        case "ind_run_simulation":
            return int(param_to_return)
        case "ind_obter_configuracao_solo":
            return int(param_to_return)
        case "ind_obter_cmp_e_lrg_queda":
            return int(param_to_return)
        case "ind_obter_energia":
            return int(param_to_return)
        case "ind_obter_configuracao_def":
            return int(param_to_return)
        case "ind_obter_estat_gerais":
            return int(param_to_return)
        case "ind_obter_tensao_efetiva":
            return int(param_to_return)
        case "ind_obter_curvatura":
            return int(param_to_return)
        case "ind_obter_envoltorias":
            return int(param_to_return)
        case "ind_rupture_on_top":
            return int(param_to_return)
        case "ind_cabo":
            return int(param_to_return)
        case "linebot_name":
            return str(param_to_return)
        case "linetop_name":
            return str(param_to_return)
        case "cable_name":
            return str(param_to_return)
        case "seabed_depth":
            return float(param_to_return)
        case "def_config_timestamps":
            return [float(i) for i in param_to_return.split(", ")]
        case "eff_tension_timestamps":
            return [float(i) for i in param_to_return.split(", ")]
        case "curv_timestamps":
            return [float(i) for i in param_to_return.split(", ")]
        case _:
            print(f"Não há forma de leitura/tipo definido para o parâmetro {param_name}. Favor definir na função get_parameter_value().")


