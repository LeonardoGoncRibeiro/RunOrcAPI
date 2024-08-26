def read_input_parameters(input_file_name):

    # Setando parâmetros default
    parameters = {
                  "header" : "cabeçalho",
                  "sim_file_name" : "simulation.sim",
                  "number_of_simulations" : 1
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
        case "%SIM.FILE.NAME":
            return "sim_file_name"
        case "%NUMBER.OF.SIMULATIONS":
            return "number_of_simulations"
        case _:
            print(f"Não há parâmetro denominado {param_header} configurado.")
            return ''
        
def get_parameter_value(param_name, line):

    param_to_return = line[:-1] if line[-1] == "\n" else line 

    match param_name:
        case "header":
            return param_to_return
        case "sim_file_name":
            return param_to_return
        case "number_of_simulations":
            return int(param_to_return)


