import numpy as np
import matplotlib.pyplot as plt
"""import networkx as nx"""
#%%
def gezginSaticiMaliyet():
    boyut = np.random.randint(15,20)
    maliyetTablo = np.zeros((boyut,boyut))
    
    for i in range(0,boyut):
        for j in range(i,boyut):
            if i==j:
                continue
            else:
                maliyetTablo[i,j]=np.random.randint(10,100)
                maliyetTablo[j,i]=maliyetTablo[i,j]
    return maliyetTablo

#Tavlama Benzetimi
def tavlamaBenzetimi(maliyetTablo,Tbasla = 1000,sogutmakatsayisi = 0.995,Tson=1):
    boyut=len(maliyetTablo)
    rota = list(range(boyut))
    np.random.shuffle(rota)
    
        
    def rotaMaliyet(rota):
        maliyet = 0
        for i in range(boyut-1):
            maliyet +=maliyetTablo[rota[i],rota[i+1]]
        maliyet += maliyetTablo[rota[-1],rota[0]]
        return maliyet
    mevcutRota = rota
    
    mevcutMaliyet = rotaMaliyet(rota)
    eniyiRota = list(mevcutRota)
    eniyiMaliyet = mevcutMaliyet
    
    
    
    sicaklik = Tbasla
    maliyetler = []
    
    
    while sicaklik > Tson:
        yeniRota = list(mevcutRota)
        i,j = np.random.randint(0,boyut,size=2)
        
        yeniRota[i], yeniRota[j] = yeniRota[j],yeniRota[i]
        
        
        yeniMaliyet = rotaMaliyet(yeniRota)
        
        Delta =yeniMaliyet - mevcutMaliyet
        
        if Delta < 0 or np.random.rand() < np.exp(-Delta/sicaklik):
            mevcutRota = yeniRota
            mevcutMaliyet = yeniMaliyet
            
            if yeniMaliyet < eniyiMaliyet:
                eniyiRota = list(yeniRota)
                eniyiMaliyet = yeniMaliyet
        maliyetler.append(eniyiMaliyet)
        sicaklik = sicaklik * sogutmakatsayisi
    
    return eniyiRota,eniyiMaliyet,maliyetler    
#%% maliyetli yollara ait grafikler
"""
def grafikCiz(maliyetTablo):
    G = nx.Graph()
    boyut = len(maliyetTablo)
    for i in range(boyut):
        for j in range(i+1, boyut):
            if maliyetTablo[i, j] != 0:
                G.add_edge(i, j, weight=int(maliyetTablo[i, j]))
    
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=700, font_size=12, font_weight="bold", edge_color="gray")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.show()
"""    
#%%    
maliyetTablo = gezginSaticiMaliyet()
"""grafikCiz(maliyetTablo)"""
print(maliyetTablo)
eniyiRota,eniyiMaliyet,maliyetler = tavlamaBenzetimi(maliyetTablo)
tavlamaBenzetimi(maliyetTablo)
print(eniyiRota)
print(eniyiMaliyet)
plt.figure(figsize=(10,6))
plt.plot(maliyetler,color="b")
plt.xlabel("Iterasyon")
plt.ylabel("En iyi maliyet")
plt.show()