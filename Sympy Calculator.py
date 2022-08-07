# IMPORTANDO AS BIBLIOTECAS
from tkinter import *
import pyperclip, sys, os
import sympy as sp                           # pip install sympy
from sympy.parsing.latex import parse_latex  # pip install antlr4-python3-runtime
import numpy as np

lista1 = np.array([
    ' ', '$', '\int', 'int', '\cos', 'cos', '\sin', 'sen', 'sin', r'\tan', 'tan',
    'r)', 'ang(', 'rad(', '**', 'd/dx',
    '\pi', '\e', 'pi', 'e', '\ln', 'ln'
])

lista2 = np.array([
    '', '', 'int', '\int', 'cos', '\cos', 'sin', 'sin', '\sin', 'tan', r'\tan',
    ' * (3.14159 / 180))', '(180 / 3.14159) * (', '(3.14159/180) * (',
    '^', r'\frac{d}{dx}',
    'pi', 'e', '3.14159', '2.71828', 'ln', '\ln'
])


# SUBSTITUI TODAS AS STRINGS DA LISTA 1 PELAS STRING CORRESPONDENTES NA LISTA 2
def replaceList(string, listaPalavras, listaReplace):
    for c in range(len(listaPalavras)):
        string = string.replace(listaPalavras[c], listaReplace[c])

    return string

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def strFloat(valor, casasDecimais):
    try:
        valor = float(valor)
        valor = round(valor, casasDecimais)
    except:
        valor = sp.sympify(valor)
    return str(valor).replace('**', '^').replace('*', '').replace('I', '*I')

# RECEBE UMA STRING COM UMA EXPRESSÃO MATEMÁTICA EM CÓDIGO LATEX E A RESOLVE
def solveExpression(expressaoLatex):
    expressaoLatex = replaceList(expressaoLatex, lista1, lista2)

    blockPrint()
    equacao = parse_latex(expressaoLatex)
    enablePrint()

    if type(equacao) != sp.core.relational.Equality:
        solucoes = equacao.doit()
        return strFloat(solucoes, 3)

    solucoes = sp.solve(equacao)
    for c, sol in enumerate(solucoes):
        sol = sp.N(sol)
        solucoes[c] = strFloat(sol, 3)

    return ', '.join(solucoes)

# CONFIGURANDO AS PROPRIEDADES DE UMA JANELA TKINTER
def ConfigurarJanela(titulo, nLinhas, nColunas, width, height):
    root = Tk()
    root.title(titulo)

    # CENTRALIZANDO A JANELA NO MEIO DA TELA DO PC
    screenWidth = root.winfo_screenwidth()
    screenHeignt = root.winfo_screenheight()

    x = (screenWidth/2) - (width/2)
    y = (screenHeignt/2) - (height/2)

    root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # PERMITIR QUE O USUÁRIO COLOQUE EM TELA CHEIA E AJUSTE
    root.resizable(True, True)

    # CONFIGURANDO AS LINHAS E COLUNAS PARA ESTICAR JUNTO COM A JANELA (USAR STICKY)
    for c in range(0, nLinhas):
        root.rowconfigure(c, weight=1)
    for c in range(0, nColunas):
        root.columnconfigure(c, weight=1)
    return root


def Calculadora():
    root = ConfigurarJanela('Calculadora Avançada', 3, 3, width=600, height=250)
    solveExpression('2+2')

    lblEquacao = Label(root, text='Digite Sua Equação', font=('Arial', 16))
    lblEquacao.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    lblAux = Label(root, text='')
    lblAux.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

    caixaTexto = Entry(root, width=10, borderwidth=3, font=('Arial', 16), justify=CENTER)
    caixaTexto.grid(row=1, column=0, columnspan=3, padx=10, pady=10, ipady=20, sticky='nsew')

    quadro = LabelFrame(root, text='Resultado', padx=20, pady=10)
    quadro.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

    lblResultado = Label(quadro, text='', font=('Arial', 14))
    lblResultado.pack(padx=10, pady=10, anchor=CENTER)

    def action(event):
        texto = solveExpression(caixaTexto.get())

        pyperclip.copy(texto)
        caixaTexto.delete(0, END)

        lblResultado['text'] = texto

    root.bind("<Return>", action)
    root.mainloop()

Calculadora()

