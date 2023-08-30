import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import tabula
import PyPDF2
from PyPDF2 import PdfReader
import pandas as pd
import re
from manipulacao_csv import manipulacao
from tkinter import messagebox

def selecionar_arquivo_pdf():
    arquivo_pdf = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    tabela = tabula.read_pdf(arquivo_pdf)
    pdf = open(arquivo_pdf,"rb")
    conteudo_pdf = PyPDF2.PdfFileReader(pdf)
    pages = conteudo_pdf.numPages

    if tabela: #essa parte do programa ta ok, façta adicionar para a função ler como texto
        listas_tabela= tabula.read_pdf(arquivo_pdf,pages="all",multiple_tables=True)
        for tabela in listas_tabela:
            tabela=tabela.drop("Unnamed: 0",axis=1)
            tabela=tabela.drop("Unnamed: 1",axis=1)
            tabela=tabela.drop("Unnamed: 2",axis=1)
            tabela=tabela.drop("Unnamed: 3",axis=1)
        tabela.to_excel("extractionPDF.xlsx")


    elif pages == 1:
        pageObj = conteudo_pdf.getPage(0)
        pageObj.extractText()
        texto_pagina=pageObj.extractText() 
        lista_trans=texto_pagina.split("\n")
        df=pd.DataFrame(zip(lista_trans))
        df.to_csv("extractionPDF.csv")
        manipulacao()
    elif pages > 1:
        texto_pagina = []
        for i in range(pages):
            pageObj = conteudo_pdf.getPage(i)
            pageObj.extractText()
            texto_pagina.append(pageObj.extract_text())
        result_3=[item.split("\n") for item in texto_pagina]
        result_3_flat=[item for l in result_3 for item in l] 
        df=pd.DataFrame(zip(result_3_flat))
        df.to_csv("extractionPDF.csv")
        manipulacao()


vermelho_flamengo = "#bf2512" 
janela_1 = tk.Tk()
janela_1.geometry("700x500")
janela_1.config(bg="black")
janela_1.iconphoto(False, PhotoImage(file="crf-flamengo-3-1.png"))
janela_1.title("Extrator de pdf")
h1 = tk.Label (width=50,height=2,text="Olá Daniel Araya, selecione o pdf que deseja extrair os dados",font="arial 15 bold",fg=vermelho_flamengo, bg="black")
h1.grid(row=1,column=0)
h1.pack()
btn_selecionar_arquivo = tk.Button (text="Selecionar Arquivo pdf", bg=vermelho_flamengo, fg="black",font="arial",command=selecionar_arquivo_pdf)
btn_selecionar_arquivo.pack()
imagem_escudo = "escudo_flamengo.jpg" 
image = Image.open(imagem_escudo) #abrindo a imagem
photo = ImageTk.PhotoImage(image)
escudo = tk.Label (janela_1,image=photo)
escudo.pack()
janela_1.resizable(width=False, height=False)
janela_1.mainloop()