def read_input_parameters(input_file_name):

    # Setando parâmetros default
    parameters = {
                  "header"                      : "cabeçalho",
                  "file_name"                   : "simulation",
                  "number_of_simulations"       : 1,
                  "ind_run_simulation"          : 1,
                  "ind_obter_configuracao_solo" : 1,
                  "ind_obter_cmp_e_lrg_queda"   : 1,
                  "ind_obter_energia"           : 1,
                  "ind_obter_configuracao_def"  : 1,
                  "ind_obter_estat_gerais"      : 1,
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
        case _:
            print(f"Não há parâmetro denominado {param_header} configurado.")
            return ''
        
def get_parameter_value(param_name, line):

    param_to_return = line[:-1] if line[-1] == "\n" else line 

    match param_name:
        case "header":
            return param_to_return
        case "file_name":
            return param_to_return
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


