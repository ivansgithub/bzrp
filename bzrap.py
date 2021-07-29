import requests
import csv
from bs4 import BeautifulSoup as BS
import re
import pandas as pd


url='https://www.letras.com/bizarrap/'
rec=requests.get(url)

soup = BS(rec.text, 'html.parser')

nombres=soup.find_all('a',{'class':'song-name'})


nombres_filtrados=[n for n in nombres if "Music Sessions" in n.text ]
nombres_filtrados2=[n for n in nombres_filtrados if not "BZRP Freestyle &" in n.text]

names=[]
for n in nombres_filtrados2:

    names.append(n.text)
    
links=[]
for i in nombres_filtrados2:
    
    
    links.append('https://www.letras.com'+i.get('href'))
    

letra_completa=[]
for link in links:
    entrando=requests.get(link)
    soup2=BS(entrando.text,'html.parser')
    letras=soup2.find('div',{'class':'cnt-letra p402_premium'})
    letras_limpias=letras.find_all('p')
    letras_limpias2=letras.find_all('br')
    
    letra_complete=[]
    for le in letras_limpias2:
        letra_complete.append(le.nextSibling)
        
    
    for l in letras_limpias:
        letra_complete.append(l.next_element)
        
    letra_completa.append(letra_complete)
        
lista_numero_palabras=[]  
for e in range(len(letra_completa)):
    
    aaa=letra_completa[e]        
    listToStr = ' '.join([str(elem) for elem in aaa])
    a=listToStr.split()
    lista_numero_palabras.append(len(a))


combi=[]
for pair in zip(names, lista_numero_palabras):
    combi.append(pair)


nombres_letras=[]
for nn in combi:
    y=nn[0].lower().split('(')    
    y2=y[1].replace('session ', 'sessions').replace('#','| vol.').replace(')','').split('|')
    y21=" ".join(y2[0].split())
    y22=" ".join(y2[1].split())
    y3=(y[0],y21 +', '+ y22,nn[1])

    nombres_letras.append(y3)



urls='https://genius.com/albums/Bizarrap-and-ecko/Ecko-bzrp-freestyle-music-sessions'
res=requests.get(urls)


soups = BS(res.content, 'html.parser')


nombres_faltantes=soups.find_all('a',class_='u-display_block')


namesa=[]
for n in nombres_faltantes:
    

    n1=' '.join(n.text.split())
    n2=n1.replace(' Lyrics','').split(':')
    n3=' '.join(n2[1].split())
    
    n4=n2[0]+'|'+n3.replace('Vol. ','Vol.')
    n5=n4.lower().split('|')
    namesa.append(tuple(n5))
    

    
linksa=[]
for ia in nombres_faltantes:
    
    linksa.append(ia.get('href'))


letra_completaa=[]
for linka in linksa:
    entrandoa=requests.get(linka)
    soup2a=BS(entrandoa.text,'html.parser')
    letrasad=soup2a.find('div',{'class':'lyrics'})
    le2=letrasad.find('p').text
    letrasasv = re.sub(r'\[.*?\]', '', le2)
    le1=letrasasv.split()
    ar=len(le1)
    letra_completaa.append(ar)

ae=namesa[1]
be=letra_completaa[1]
ce=ae+(be,)

nombres_letras.append(ce)




todo=[]
with open('bza.csv',encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    
    for iu in csv_reader:
        todo.append(iu)

algo3=[un for un in todo if 'Music Session' in un[0]]


spoti=[]
for hj in algo3:
    spoti.append(hj[0].replace(' #',', Vol. ')+'|'+hj[1])



   
spoti2=[]

for io in spoti:
    
    aja=io.lower().replace('bzrp','|')
    ib=(aja.replace(':','').replace('- ','').split('|'))
    h1=ib[1].replace('session,','sessions,').split(',') 
    h2=''.join(h1[1].split(' '))
    h3=h2.replace('(feat.pacoamoroso)','')
    ib2=(ib[0]+';'+'bzrp'+h1[0]+', '+h3+';'+ib[2]).split(';')
    print(ib2)
    spoti2.append(ib2)
    
    
   
lista_compara_spo=[]
for u in spoti2:
    
    
    lista_compara_spo.append(u[1])
    
lista_compara_le=[]
for m in nombres_letras:
    lista_compara_le.append(m[1])




print(set(lista_compara_spo)- set(lista_compara_le))

    
spoti2.sort(key=lambda x:x[1])

nombres_letras.sort(key=lambda x:x[1])


pra=[]
for numo, lra in zip(nombres_letras,spoti2):
    ao=numo
    bo=lra[2]
    co=ao+(bo,)
    pra.append(co)
    

    
df = pd.DataFrame(pra,columns =['nombre', 'session#','palabras','tiempo'])
    




df['tiempo']=df['tiempo'].astype(float)



df['palabras por minuto']=df['palabras']/df['tiempo']


df.to_csv ('musicsession.csv', index = False, header=True)


