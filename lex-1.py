import re

# Abrimos archivo de prueba
with open("analizar.txt", "r") as file:
    source = file.read()

# Expresiones regulares basadas en el documento
token_specification = [
    ('COMENTARIO_LINEA',   r'//[^\n]*'),
    ('COMENTARIO_MULTI',   r'/\*[\s\S]*?\*/'),
    ('FLOTANTE',           r'\d+\.\d+'),
    ('ENTERO',             r'\d+'),
    ('OPERADOR',           r'==|!=|<=|>=|[+\-*/%|&=!<>]'),
    ('SIMBOLO',            r'[{}();:]'),
    ('ID_INVALIDO',        r'\b_[A-Za-z0-9_]*\b'),
    ('ID',                 r'\b[A-Za-z][A-Za-z0-9_]*\b'),
    ('DELIMITADOR',        r'[ \t]+'),
    ('NUEVA_LINEA',        r'\n'),
    ('ERROR',              r'[^\w+\-*/%|&=!<>{}();\.\s/\n]')
]

# Compilamos en un solo regex
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex)

# Escaneamos el código y guardamos resultados
line_num = 1
resultados = []
solo_tokens = []

for mo in get_token.finditer(source):
    kind = mo.lastgroup
    value = mo.group()
    if kind == 'NUEVA_LINEA':
        line_num += 1
    elif kind == 'DELIMITADOR':
        continue
    elif kind in ('COMENTARIO_LINEA', 'COMENTARIO_MULTI'):
        resultados.append(f"Línea {line_num}: Comentario → {value}")
        solo_tokens.append(value)
    elif kind == 'ID':
        resultados.append(f"Línea {line_num}: Identificador → {value}")
        solo_tokens.append(value)
    elif kind == 'ENTERO':
        resultados.append(f"Línea {line_num}: Entero → {value}")
        solo_tokens.append(value)
    elif kind == 'FLOTANTE':
        resultados.append(f"Línea {line_num}: Flotante → {value}")
        solo_tokens.append(value)
    elif kind == 'OPERADOR':
        resultados.append(f"Línea {line_num}: Operador → {value}")
        solo_tokens.append(value)
    elif kind == 'SIMBOLO':
        resultados.append(f"Línea {line_num}: Símbolo → {value}")
        solo_tokens.append(value)
    elif kind == 'ERROR':
        resultados.append(f"❌ Línea {line_num}: Carácter inválido → {value}")
        solo_tokens.append(value)
    elif kind == 'ID_INVALIDO':
        resultados.append(f"❌ Línea {line_num}: Identificador inválido → {value}")
        solo_tokens.append(value)

# Guardamos en archivos
with open("resultado_tokens.txt", "w", encoding="utf-8") as out_file:
    for linea in resultados:
        out_file.write(linea + "\n")

with open("solo_tokens.txt", "w", encoding="utf-8") as token_file:
    for token in solo_tokens:
        token_file.write(token + "\n")

# Imprimimos en terminal
for linea in resultados:
    print(linea)
