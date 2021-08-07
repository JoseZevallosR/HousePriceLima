from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver
import time

#Download Data
col_names=['Costo S/.','Costo $/.','Mantenimiento','Direccion','Ubicacion','Area'
          ,'Dormitorios','Baños','Estacionamiento']

df=pd.DataFrame(columns=col_names)

def atributes(flat):
    priceS=flat.find('span',class_='firstPrice')
    priceD=flat.find('span',class_='secondPrice')
    expense=flat.find('span',class_='postingCardExpenses  ')
    location=flat.find('span',class_='postingCardLocationTitle')
    distric=flat.find('span',class_='postingCardLocation go-to-posting')
    att_list=[]
    for att in [priceS,priceD,expense,location,distric]:
        if att!=None:
            att_list.append(re.sub('\s+', '', att.text))
        else:
            att_list.append(att)
    return att_list

#Distric URLS
ML='https://urbania.pe/buscar/venta-de-departamentos-en-pueblo-libre--lima--lima?page='
PL='https://urbania.pe/buscar/venta-de-departamentos-en-pueblo-libre--lima--lima?page='
SM='https://urbania.pe/buscar/venta-de-departamentos-en-san-miguel--lima--lima?page='
SB='https://urbania.pe/buscar/venta-de-departamentos-en-san-borja--lima--lima?page='
LC='https://urbania.pe/buscar/venta-de-departamentos-en-lince--lima--lima?page='
def urlgenerator(i,url=SB):
    return url + str(i)

for i in range(1,10):
    browser=webdriver.Chrome('C:/Users/JOSE/Documents/Python Scripts/chromedriver.exe')
    url=urlgenerator(i)
    browser.get(url)
    time.sleep(2)
    html=browser.page_source
    soup=BeautifulSoup(html,'lxml')

    for departamento in soup.find_all('div',class_='postingCard'):

        cos=atributes(departamento)
        carac=[re.sub('\s+', '', att.text) for att in departamento.find_all('li')]
        if len(carac)<4:
            carac.insert(3,'')
        information=cos+carac
        if len(information)==9:
            df2=pd.DataFrame([information],columns=col_names)
            df=df.append(df2)
            
    
    
    browser.close()

df.to_excel('C:/Users/JOSE/Documents/House_Price/LC_Precio.xlsx',index=False)