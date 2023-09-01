import pandas as pd
import re
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog 
from tkinter import messagebox
import openpyxl

def manipulacao():
    tabela = pd.read_csv("extractionPDF.csv")
    tabela = pd.read_csv("extractionPDF.csv").set_index("Unnamed: 0")
    tabela=tabela.rename(columns={"0":"Description"})
    tabela['Total']= None
    index_description=tabela.columns.get_loc("Description")
    index_total=tabela.columns.get_loc("Total")
    separacao_dados=r"[$]?\d[0-9]*[,]?\d[0-9]*[.]\d[0-9{2}]"
    for row in range (0,len(tabela)):
        total=re.search(separacao_dados, tabela.iat[row, index_description])
        if total is not None:
            total = total.group()
        tabela.iat[row, index_total]= total
        tabela.iat[row, index_description] = re.sub(separacao_dados, "", tabela.iat[row, index_description])
    tabela.to_excel("extractionPDF2.xlsx")
    os.remove("extractionPDF.csv")
    messagebox.showinfo('[AVISO]','Já terminei de extrair os dados e salvei o arquivo extractionPDF na pasta do programa.')
