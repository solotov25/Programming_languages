import sys

reserved_words = ["Put", "float", "integer", "while", "for", "array", "Function", "to", "output", "if", "Get", "or",
                     "and", "input", "next", "else", "returns", "Main", "SquareRoot", "RaiseToPower", "AbsoluteValue",
                     "RandomNumber", "size", "elseif", "SeedRandomNumbers", "evaluates", "not", "nothing", "decimal", "with", "places"]

reserved_words.sort()

operators = {'+':"tkn_plus", '-':"tkn_minus", '*':"tkn_times", '/':"tkn_div",
            '%':"tkn_mod", '<':"tkn_less", '>':"tkn_greater", '<=':"tkn_leq",
                '>=':"tkn_geq", '==':"tkn_equal", '!=':"tkn_neq", '?':"tkn_question_mark",
                '.':"tkn_period", ';':"tkn_semicolon", 
                '=':"tkn_assign", ',':"tkn_comma", ')':"tkn_closing_par", '(':"tkn_opening_par"
                , ']':"tkn_closing_bra",'[':"tkn_opening_bra"
                }

output = []


def look_up_end_quotes(data, index, row):
    end = index + 1
    char_to_search = '"' 
    
    if data.find(char_to_search, index + 1) != -1:
        tmp = data.index(char_to_search, index + 1)
        while (data[tmp-1] == "\\"):
            # print(data[-2:])
            if data[-2:] == '\\"':
                line = f'>>> Error lexico (linea: {row}, posicion: {index + 1})'
                print(line)
                return -1
                
            if data.find(char_to_search, tmp + 1) != -1:
                tmp = data.index(char_to_search, tmp + 1)
            else:
                line = f'>>> Error lexico (linea: {row}, posicion: {index + 1})'
                print(line)
                return -1
        line = f'<tkn_str,{data[index+1:tmp ]},{row},{index + 1}>'
        print(line)
    else:
        line = f'>>> Error lexico (linea: {row}, posicion: {index + 1})'
        print(line)

        return -1

    return tmp + 1

def look_up_end_words(data, index, row):
    end_num = index
    # print(data)

    if data[end_num].isnumeric():
        num_buffer = data[end_num]
        flag_point_on = False
        # First part of number
        while data[end_num] != " " and end_num < len(data)-1:
            end_num += 1
            if data[end_num].isnumeric():
                num_buffer += data[end_num]
                # 235.7

            elif end_num + 1 < len(data) and data[end_num] == "." and data[end_num + 1].isnumeric() == True :
                if flag_point_on == True:
                    line = f'<tkn_float,{data[index:end_num]},{row},{index + 1}>'
                    print(line)
                    return end_num
                num_buffer += "."
                flag_point_on = True
            else:
                line = f'<tkn_integer,{num_buffer},{row},{index + 1}>' if flag_point_on == False else f'<tkn_float,{num_buffer},{row},{index + 1}>'
                print(line)
                return end_num
        line = f'<tkn_integer,{num_buffer},{row},{index + 1}>' if flag_point_on == False else f'<tkn_float,{num_buffer},{row},{index + 1}>'
        print(line)
        if data[end_num] in operators and end_num == len(data)-1:
            line = f'<{operators[data[end_num]]},{row},{end_num + 1}>'
            print(line)
        return end_num + 1
    else:
        end = index
        buffer = ""
        while (data[end] not in operators and data[end] != "!" ) and data[end] != " ":
            buffer += data[end]
            end += 1
            if end == len(data):
                break
        if buffer.strip() in reserved_words:
            line = f'<{buffer},{row},{index + 1}>'
            print(line)
        else:
            if buffer.isalnum() is True or buffer.find("_") !=-1 and buffer[0] != "_":
                line = f'<id,{buffer},{row},{index + 1}>'
                print(line)
            else:
                line = f'>>> Error lexico (linea: {row}, posicion: {index + 1})'
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
        elif cont + 1 < len(line_array) and line_array[cont] == "!" and line_array[cont+1]== "=":
            op = line_array[cont] + line_array[cont+1]
            line = f'<{operators[op]},{row},{cont + 1}>'
            cont += 2
            print(line)
        elif line_array[cont] in operators:
            if cont + 1 < len(line_array) and line_array[cont +1] != " " and line_array[cont+1] == "=":
                if line_array[cont] == "<" and  line_array[cont+1] == "=":
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
        elif line_array[cont] == '"':
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
        if data[index].startswith("//") or data[index].strip().startswith("//"):
            index += 1
            continue
        else:
            # if "//" in data[index]:
            #     data[index] = data[index][:data[index].index("//")]
            val = look_up_reserved_word(data[index], index + 1, 0)
            if val == -1:
                break
            index += 1


lexical_analyzer()
