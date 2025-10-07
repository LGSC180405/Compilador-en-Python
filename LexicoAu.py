import ply.lex as lex

# Cargar palabras reservadas desde archivo
def cargar_palabras_reservadas():
    reservadas = {}
    with open("tokens.txt", "r") as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) == 2:
                id_token, palabra = partes
                reservadas[palabra] = f"RESERVADA_{id_token}"
    return reservadas

reserved = cargar_palabras_reservadas()

# Lista de tokens
tokens = [
    'ID', 'INT_CONST', 'FLOAT_CONST', 'STRING_CONST',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    'SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMENT'
] + list(set(reserved.values()))

# Reglas de expresiones regulares
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ      = r'=='
t_NEQ     = r'!='
t_LT      = r'<'
t_GT      = r'>'
t_LE      = r'<='
t_GE      = r'>='
t_SEMI    = r';'
t_COMMA   = r','
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'

# Comentarios
def t_COMMENT(t):
    r'\/\/.*|\/\*[\s\S]*?\*\/'
    pass

# Cadenas
def t_STRING_CONST(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Identificadores
def t_ID(t):
    r'[a-zA-Z_](?!.*__)[a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Números
def t_FLOAT_CONST(t):
    r'[+-]?((\d+\.\d*|\.\d+)([eE][+-]?\d+)?|\d+[eE][+-]?\d+)'
    return t

def t_INT_CONST(t):
    r'[+-]?\d+'
    return t

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Errores
errores_encontrados = []

def t_error(t):
    errores_encontrados.append(f"{t.lineno}: {t.value}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Leer el contenido del archivo fuente
with open("codigo_fuente.txt", "r") as archivo:
    codigo = archivo.read()

# Primera pasada: tokens con tipo y línea
lexer.input(codigo)
with open("tokens_generados.txt", "w") as salida:
    while True:
        tok = lexer.token()
        if not tok:
            break
        salida.write(f"{tok.type}: {tok.value} (línea {tok.lineno})\n")

# Segunda pasada: solo valores
lexer.input(codigo)
with open("tokens_numero.txt", "w") as salida:
    while True:
        tok = lexer.token()
        if not tok:
            break
        salida.write(f"{tok.value}\n")

# Guardar errores si existen
if errores_encontrados:
    with open("destacables.txt", "w") as f:
        for error in errores_encontrados:
            f.write(error + "\n")
        f.write(f"\nTotal de errores léxicos: {len(errores_encontrados)}\n")
