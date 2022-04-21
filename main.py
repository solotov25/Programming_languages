import sys

reserved_words = ["and", "archivo", "caso", "const", "cadena",
                    "constantes","desde","eval","fin",
                    "hasta","inicio","lib","libext", "numerico",
                    "matriz","mientras","not","or", "logico",
                    "paso","subrutina","programa","ref",
                    "registro","repetir","retorna","si",
                    "sino","tipos","var","variables", "vector",
                    "leer","imprimir", "TRUE", "FALSE", "SI", "NO",
                    "dim", "cls", "set_ifs", "abs", "arctan", "ascii",
                    "cos", "dec", "eof", "exp", "get_ifs", "inc", "int",
                    "log","lower", "mem", "ord", "paramval", "pcount",
                    "pos", "random", "sec", "set_stdin", "set_stdout",
                    "sin", "sqrt", "str", "strdup", "strlen", "substr",
                    "tan", "upper", "val", "alen","numerico"]

reserved_words.sort()

operators = {'+':"tk_suma", '-':"tk_resta", '*':"tk_multiplicacion", '/':"tk_division",
            '%':"tk_modulo", '^':"tk_potenciacion", '<':"tk_menor", '>':"tk_mayor", '<=':"tk_menor_igual",
                '>=':"tk_mayor_igual", '==':"tk_igual_que", '<>':"tk_distinto_de",
                '.':"tk_punto", ';':"tk_punto_y_coma", ':':"tk_dos_puntos", 
                '=':"tk_asignacion", ',':"tk_coma", ']':"tk_corchete_derecho",
                '[':"tk_corchete_izquierdo", '}':"tk_llave_derecha", '{':"tk_llave_izquierda",
                ')':"tk_parentesis_derecho", '(':"tk_parentesis_izquierdo"
                }

output = []


def look_up_end_comment(data, index, row):
    end_com = index
    cont_new_word = 0
    flag_on = False if data[end_com].find("*/") == -1 else True
    if flag_on == True:
        if data[end_com].index("*/") + 2 == len(data[end_com]):
            return end_com + 1 
        else:
            cont = data[end_com].index("*/") + 2
            line_array = data[index]
            
            while cont < len(line_array):
                # print(cont)
                if line_array[cont] == " ":
                    cont += 1
                    continue
                elif line_array[cont] in operators:
                    line = f'<{operators[line_array[cont]]},{index + 1 },{cont + 1}>'
                    cont += 1
                    print(line)
                elif line_array[cont] == '"' or line_array[cont] == "'":
                    cont = look_up_end_quotes(line_array, cont, row + 1)
                else:
                    # print(line_array[cont])
                    cont = look_up_end_words(line_array, cont, row + 1)
    
    while flag_on is False and end_com < len(data)-1:
        end_com += 1
        
        if data[end_com].find("*/") != -1:
            flag_on = True
            if data[end_com].index("*/") + 2 == len(data[end_com]):
                return end_com + 1  
            else:
                cont = data[end_com].index("*/") + 2
                line_array = data[end_com]
                while cont < len(line_array):
                    if line_array[cont] == " ":
                        cont += 1
                        continue
                    elif line_array[cont] in operators:
                        line = f'<{operators[line_array[cont]]},{index + 1 },{cont + 1}>'
                        cont += 1
                        print(line)
                    elif line_array[cont] == '"' or line_array[cont] == "'":
                        cont = look_up_end_quotes(line_array, cont, row)
                    else:
                        cont = look_up_end_words(line_array, cont, end_com + 1)
    
    if flag_on == False: 
        cont = index
        line_array = data[cont]
        while cont < len(line_array):
            if line_array[cont] == " ":
                cont += 1
                continue
            elif line_array[cont] in operators:
                line = f'<{operators[line_array[cont]]},{index + 1 },{cont + 1}>'
                cont += 1
                print(line)
            elif line_array[cont] == '"' or line_array[cont] == "'":
                cont = look_up_end_quotes(line_array, cont, row)
            else:
                cont = look_up_end_words(line_array, cont, end_com + 1)

    return end_com + 1 if flag_on == True else index +1

def look_up_end_quotes(data, index, row):
    end = index + 1
    char_to_search = '"' if data[index] == '"' else "'"
    if data.find(char_to_search, index + 1) != -1:
        end = data.index(char_to_search, index + 1)
        line = f'<tk_cadena,{data[index:end + 1]},{row},{index + 1}>'
        print(line)
    else:
        line = f'>>> Error lexico(linea:{row},posicion:{index + 1})'
        print(line)

        return -1

    return end + 1

def look_up_end_words(data, index, row):
    end_num = index
    # print(data)

    if data[end_num].isnumeric():
        num_buffer = data[end_num]
        flag_point_on = False
        flag_exp_on = False
        # First part of number
        while data[end_num] != " " and end_num < len(data)-1:
            end_num += 1
            if data[end_num].isnumeric():
                num_buffer += data[end_num]
                # 235.7

            elif data[end_num] == ".":
                if flag_point_on == True:
                    line = f'<tk_numero,{data[index:end_num]},{row},{index + 1}>'
                    print(line)
                    return end_num
                num_buffer += "."
                flag_point_on = True

            elif data[end_num] == "E" or data[end_num] == "e":
                if flag_exp_on == True:
                    line = f'<tk_numero,{data[index:end_num]},{row},{index + 1}>'
                    print(line)
                    return end_num
                num_buffer += data[end_num]
                flag_exp_on = True

                if data[end_num + 1] == "+" or data[end_num + 1] == "-":
                    num_buffer += data[end_num+1]
                    end_num += 1
            else:
                line = f'<tk_numero,{data[index:end_num]},{row},{index + 1}>'
                print(line)
                return end_num
        line = f'<tk_numero,{num_buffer},{row},{index + 1}>'
        print(line)
        if data[end_num] in operators and end_num == len(data)-1:
            line = f'<{operators[data[end_num]]},{row},{end_num + 1}>'
            print(line)
        return end_num + 1
    else:
        end = index
        buffer = ""
        while data[end] not in operators and data[end] != " ":
            buffer += data[end]
            end += 1
            if end == len(data):
                break
        if buffer.strip() in reserved_words:
            line = f'<{buffer},{row},{index + 1}>'
            print(line)
        else:
            if buffer.isalnum() is True or buffer.find("_") !=-1:
                line = f'<id,{buffer},{row},{index + 1}>'
                print(line)
            else:
                line = f'>>> Error lexico(linea:{row},posicion:{index + 1})'
                print(line)
                return -1
        return end 


def look_up_reserved_word(line_array, row, col ):
    cont = 0
    while cont < len(line_array):
        # print(cont)
        if line_array[cont] == " ":
            cont += 1
            continue
        elif line_array[cont] in operators:
            if cont + 1 < len(line_array) and line_array[cont +1] != " " and (line_array[cont+1] == ">" or line_array[cont+1] == "="):
                if line_array[cont] == "<" and (line_array[cont+1] == ">" or line_array[cont+1] == "="):
                    op = line_array[cont] + line_array[cont+1]
                    line = f'<{operators[op]},{row},{cont + 1}>'
                    cont += 2
                    print(line)
                elif line_array[cont] == ">" and  line_array[cont+1] == "=":
                    op = line_array[cont] + line_array[cont+1]
                    line = f'<{operators[op]},{row},{cont + 1}>'
                    print(line)
                    cont += 2
                elif line_array[cont] == "=" and  line_array[cont+1] == "=":
                    op = line_array[cont] + line_array[cont+1]
                    line = f'<{operators[op]},{row},{cont + 1}>'
                    print(line)
                    cont += 2
                
            else:
                line = f'<{operators[line_array[cont]]},{row},{cont + 1}>'
                cont += 1
                print(line)
        elif line_array[cont] == '"' or line_array[cont] == "'":
            cont = look_up_end_quotes(line_array, cont, row) 
            if cont == -1:
                return -1
        else:
            # print(line_array[cont])
            cont = look_up_end_words(line_array, cont, row)
            if cont == -1:
                return -1
    return 0


def lexical_analyzer(): 
    data = sys.stdin.readlines()
    data = [line.rstrip() for line in data]

    index = 0

    while index < len(data):
        if data[index].startswith("//"):
            index += 1
            continue
        elif data[index].strip().startswith("/*"):
            index = look_up_end_comment(data, index, 0)
        else:
            if "//" in data[index]:
                data[index] = data[index][:data[index].index("//")]
            val = look_up_reserved_word(data[index], index + 1, 0)
            if val == -1:
                break
            index += 1


lexical_analyzer()
