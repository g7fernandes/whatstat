#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 14:51:57 2018


@author: gabriel fernandes


ESTE PROGRAMA LE ARQUIVO DE LOG DE GRUPO DE WHATSAPP E RETORNA O RANKING
DOS QUE MAIS ENVIARAM MENSAGENS

ENTRADA: arquivo em txt

Para obter o arquivo va no grupo de whatsapp, clique em configuraçoes (:), 
mais, exportar convesa. 
Ela sera exportada em .zip, extraia, renomeie o arquivo da conversa para um
nome mais facil e entao execute o whatstat_v2.py
> python whatstat_v2.py
O arquivo de conversa.txt e whatstat_v2.py devem estar na mesma pasta

São feitos gráficos de taxa de mensagens por mês de acordo com as instruções 
ditas no programa. O grárico de mensagens por mês é feito a partir de dados
semanais acomulativos. Ou seja, a taxa de mensagens em uma determinada semana
é definida pela quantidade de mensagens nas duas semanas anteriores e 
nas duas posteriores a ela. 

A correlação entre as conversas é feita a partir da taxa semanal se mensangens. 



SAIDA:
    O Ranking em .txt
    Taxa semanal acumulativa (fim da semana) em csv
    correlações em csv

    
"""

import csv

class grupozap:


    def __init__(self,nome_grupo):
        self.nome_grupo = nome_grupo
        self.lista_pessoas = [] #pessoas e numero de mensagens  
        self.acum_7 = [] #acumulativo semanal
        self.data = []
    
    def addmsg(self,nome,m,dia):
        def nextdata(da):
            da = round(da) 
            if str(da)[-1] == '4':
                if str(da)[4:6] == '12':
                    da = da + 1000 - 110 - 3
                else:
                    da = da + 10 - 3
            else:
                da = da + 1
            return da    
                        
        
        encontrada = 0
        
        for p in range(len(self.lista_pessoas)):
            if self.lista_pessoas[p][0] == nome:
                self.lista_pessoas[p][1] += m
                encontrada = 1
                break
                
        if not encontrada:
            nome = "".join(i for i in nome if 31 < ord(i) < 255)
            for p in range(len(self.lista_pessoas)):
                if self.lista_pessoas[p][0] == nome:
                    self.lista_pessoas[p][1] += m
                    encontrada = 1
                    break
          
        if not encontrada:            
            self.lista_pessoas.append([nome,m])  
            self.acum_7.append([0]*(len(self.data)+1))
            self.acum_7[-1][0] = nome

        data_now  = round(int(dia[0:6])*10 + 1 + (int(float(dia[6:8])>8) + \
                          int(int(dia[6:8])>15) +\
                          int(int(dia[6:8])>23)),1)
        
                       
                          
        if not len(self.data): # começa a lista de meses
            self.data = [data_now]
            data_next = data_now
        else:
            data_next = nextdata(self.data[-1])   

        if self.data[-1] != data_now:
            while data_next < data_now:
                for p in range(len(self.lista_pessoas)):
                    self.acum_7[p].append(self.lista_pessoas[p][1])
                self.data.append(data_next)    
                data_next = nextdata(data_next)      
            for p in range(len(self.lista_pessoas)):
                self.acum_7[p].append(self.lista_pessoas[p][1])
            self.data.append(data_now)

#        if not len(self.data): # começa a lista de meses
#            self.data = [data_now]
#        if self.data[-1] != data_now:
#            for p in range(len(self.lista_pessoas)):
#                self.acum_7[p].append(self.lista_pessoas[p][1])
#            self.data.append(data_now)
            
            
    def listar(self):
        resultado = open(''.join([self.nome_grupo,'_resultado.txt']),'w')
        resultado.write('Posiçao, No_de_mensagens, pessoa\n')
        p = 1
        for x in self.lista_pessoas:
            print('{}º {} {}'.format(p,x[1],x[0]))
            resultado.write('{}º, {}, {}\n'.format(p,x[1],x[0]))
            p += 1
        print('Resultado salvo em {}'.format(''.join([self.nome_grupo,'_resultado.txt'])))   
            
 
    def ordenar(self):
        def quicksort(L):
            if len(L) <= 1: 
                return L
            
            pivot = L[0][1]
            equal = [x for x in L if x[1] == pivot]
            lesser = [x for x in L if x[1] < pivot]
            greater = [x for x in L if x[1] > pivot]
            return quicksort(greater) + equal + quicksort(lesser)
        
        L = self.lista_pessoas
        self.lista_pessoas = quicksort(L)
        
    def semanal(self):
        file = ''.join([self.nome_grupo,'_semanal.csv'])
        datastr = []
        for d in self.data:
            datastr.append(str(d)[0:4] + '/' + str(d)[4:6]+'.'+str(d)[6])
        with open(file,'w') as new_file:
            fieldnames = ['nome'] + datastr
            csv_writer = csv.writer(new_file,delimiter=',')
            
            csv_writer.writerow(fieldnames)
#            
            for line in self.acum_7:
                if line[0] != '':
                    csv_writer.writerow(line)

        print('Resultado acumulativo salvo em {}'.format(''.join([self.nome_grupo,'_semanal.txt'])))                     
        return datastr

#%% Janelamento

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    np.hanning, np.hamming, np.bartlett, np.blackman, np.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError('smooth only accepts 1 dimension arrays.')

    if x.size < window_len:
        raise ValueError('Input vector needs to be bigger than window size')


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y


#%% Calcula a taxa mensal de conversa por pessoa
                    
def taxa(Lacum,data,grupo):          
    
    janelamento = 4
    
    acum = np.array([np.zeros(len(Lacum[2][:])-1)])
    Lacum.pop(0)
    for k in Lacum:
        acum = np.concatenate((acum,np.array([k[1:]])),axis=0)
    
    acum = np.delete(acum,0,0)
    # calcula taxa mensal
    rate = np.copy(acum)
    rate = rate*0
    rate7 = np.copy(rate)
    
    rate[:,0] = ((acum[:,0])*4+(acum[:,1])*2+(acum[:,3])*(4/3)+(acum[:,3]-acum[:,0])*4)/4
    rate[:,1] = ((acum[:,3]-acum[:,1])*2 + (acum[:,1])*2)/2 
    rate[:,2] = ((acum[:,3]-acum[:,2])*4 + (acum[:,2])*(4/3))/2   
    rate7[:,0] = acum[:,0];
    rate7[:,1] = acum[:,1]-acum[:,0]
    rate7[:,2] = acum[:,2]-acum[:,1]    
#    for k in range(3,len(data)-1):
#        rate7[:,k] = acum[:,k] - acum[:,k-1] 
#        rate[:,k] = acum[:,k+1]-acum[:,k-3]
#    k+=1
#    a1 = rate
    rate[:,3:] = acum[:,3:] - acum[:,0:-3]  

    rate7 = acum[:,1:] - acum[:,:-1]
#    rate[:,k] = ((acum[:,k]- acum[:,k-1])*4 + (acum[:,k]- acum[:,k-2])*2 + (acum[:,k]- acum[:,k-3])*(4/3) + (acum[:,k]- acum[:,k-4]) )/4

    a = input("Entre 1 para fazer gráfico da taxa Mensal dos que mais mandam mensagens em intervalos dum número de semanas.\nEntre 2 para fazer gráfico da taxa Mensal dos que mais mandam mensagens em um perídodo determinado.\nEntre 3 para fazer gráfico da taxa Mensal de pessoas específicas.\nEntre 4 para fazer gráfico da taxa Semanal dos que mais mandam mensagens em intervalos dum número de semanas.\nEntre 5 para fazer gráfico da taxa Semanal dos que mais mandam mensagens em um perídodo determinado.\nEntre 6 para fazer gráfico da taxa semanal de pessoas específicas.\nEntre N para não fazer gráfico.\n")
    while a.isdigit():       
        if a.isdigit() and int(a) == 1:
            tperiodo = int(input('Entre o comprimento dos intervalos em semanas. 1 ano = 50 semanas.\n'))# em semanas   
            top = int(input('Número de pessoas no gráfico. (mostra apenas as com mais mensagens)\n'))
            ninterv = round(len(data)/tperiodo)
            if ninterv < 1:
                ninterv = 1
            tops = np.zeros((top,ninterv),dtype='int8')
            k = 1
            while k < ninterv:
                aux1 = acum[:,k*tperiodo] - acum[:,(k-1)*tperiodo]
                dtype = [('id',int),('msg',int)]
                periodo = np.empty(len(Lacum),dtype=dtype)
                periodo['id'] = np.arange(len(Lacum))
                periodo['msg'] = aux1
                
                tops[:,k-1] =  np.sort(periodo, order='msg')['id'][-top:]
                k+=1
            
            aux1 = acum[:,-1] - acum[:,(k-1)*tperiodo]
            dtype = [('id',int),('msg',int)]
            periodo = np.empty(len(Lacum),dtype=dtype)
            periodo['id'] = np.arange(len(Lacum))
            periodo['msg'] = aux1
            
            tops[:,ninterv-1] =  np.sort(periodo, order='msg')['id'][-top:]
            
            
            k = 1   
    #        for w in range(len(data)):
    #            if data[w][-1] == '3':
    #                data[w] = ''.join((data[w][:-1],'2'))
    #            elif data[w][-1] != '1':
    #                data[w] = ' '
                          
            while k < ninterv:
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                x = data[(k-1)*tperiodo:k*tperiodo] #labx
    
    #            x = np.arange(len(labx))
    
                for p in range(top): 
                    l = ax1.plot(x,rate[tops[p,k-1],(k-1)*tperiodo:k*tperiodo],label=Lacum[tops[p,k-1]][0])  
                    if p == 0: lns = l 
                    else: lns += l 
            
                l = ax2.plot(x,np.sum(rate[:,(k-1)*tperiodo:k*tperiodo],axis=0),color='k',linestyle='--',label='Total') 
                lns += l
                labs = [l.get_label() for l in lns]
                leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                                 shadow=False, fancybox=True)
                    
                leg.get_frame().set_alpha(0.5)  
                ax1.set_xticklabels(x,rotation=70)
    #            xticks = ticker.MaxNLocator(len(x))
    #            ax1.xaxis.set_major_locator(xticks)
                fig.tight_layout() 
                ax1.grid(True,linestyle='--',linewidth=.25)
                ax1.set_ylabel('Mensagens/Mês de cada membro')
                ax1.set_xlabel('Mês (Mês.semana)')
                ax2.set_ylabel('Mensagens/Mês Total no grupo')
                plt.title(grupo)
                k +=1
                
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            
            x = data[(k-1)*tperiodo:]
          #  x = np.arange(len(labx))        
            for p in range(top): 
                l = ax1.plot(x,rate[tops[p,k-1],(k-1)*tperiodo:],label=Lacum[tops[p,k-1]][0])       
                if p == 0: lns = l 
                else: lns += l 
                
            l = ax2.plot(x,np.sum(rate[:,(k-1)*tperiodo:],axis=0),color='k',linestyle='--',label='Total') 
            lns += l
            labs = [l.get_label() for l in lns]
            leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                             shadow=False, fancybox=True)
            
            ax1.set_ylabel('Mensagens/Mês de cada membro')
            ax1.set_xlabel('Mês.semana')
            ax2.set_ylabel('Mensagens/Mês Total no grupo')
                
            leg.get_frame().set_alpha(0.5)  
            ax1.set_xticklabels(x,rotation=70)
            ax1.grid(True,linestyle='--',linewidth=.25)
    #        xticks = ticker.MaxNLocator(len(x))
    #        ax1.xaxis.set_major_locator(xticks)
            fig.tight_layout() 
            plt.title(grupo)
            print('Para continuar, feche o gráfico.\n')
            #plt.ioff()
            plt.show(block=True)
            
        if a.isdigit() and int(a) == 2:
            k = 0
            print('Índice | Semana\n')
            for s in datastr: 
                print('{}   {}'.format(k,s))
                k+=1
            print('Índice | Semana\n')
            inicial = int(input('Entre o índice da semana inicial (lista acima).\n'))
            final = int(input('Entre o índice da semana final.\n'))        
    
            top = int(input('Número de pessoas no gráfico. (mostra apenas as com mais mensagens)\n'))
            tops = np.zeros(top,dtype='int8')
            
            aux1 = acum[:,final] - acum[:,inicial]
            dtype = [('id',int),('msg',int)]
            periodo = np.empty(len(Lacum),dtype=dtype)
            periodo['id'] = np.arange(len(Lacum))
            periodo['msg'] = aux1
            tops[:] =  np.sort(periodo, order='msg')['id'][-top:]
    
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            
            labx = data[inicial:final]
            x = np.arange(len(labx))        
            for p in range(top): 
                l = ax1.plot(x,rate[tops[p],inicial:final],label=Lacum[tops[p]][0])       
                if p == 0: lns = l 
                else: lns += l 
                
            l = ax2.plot(x,np.sum(rate[:,inicial:final],axis=0),color='k',linestyle='--',label='Total') 
            lns += l
            labs = [l.get_label() for l in lns]
            leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                             shadow=False, fancybox=True)
            
            ax1.set_ylabel('Mensagens/Mês de cada membro')
            ax1.set_xlabel('Mês.semana')
            ax2.set_ylabel('Mensagens/Mês Total no grupo')
                
            aux = np.linspace(x[1],x[-1],num=10,dtype=int)
            ax1.set_xticks(aux)
            ax1.set_xticklabels([labx[i] for i in aux],rotation=70) 
            ax1.grid(True,linestyle='--',linewidth=.25)
    #        xticks = ticker.MaxNLocator(len(x))
    #        ax1.xaxis.set_major_locator(xticks)
            fig.tight_layout() 
            plt.title(grupo)
            print('Para continuar, feche o gráfico.\n') 
            #plt.ioff()
            plt.show(block=True)        
               
        if a.isdigit() and int(a) == 3:
            lista_pessoas = [(x,Lacum[x][0]) for x in range(len(Lacum))]
            lista_pessoas = sorted(lista_pessoas,key=lambda p: p[1])
            print('\nÍndice | Pessoa\n')
            
            for s in lista_pessoas: 
                print('  {}    {}'.format(s[0],s[1]))
            print('Índice | Pessoa\n')        
            ip = input('Entre o índice das pessoas que deseja fazer o gráfico separado por espaços.\n')
            tops = np.array(ip.split(),dtype=int)
    
    
            k = 0
            print('\nÍndice | Semana\n')
            for s in datastr: 
                print('{}   {}'.format(k,s))
                k+=1
            print('Índice | Semana\n')
            inicial = int(input('Entre o índice da semana inicial (lista acima).\n'))
            final = int(input('Entre o índice da semana final.\n'))        
    
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            
            labx = data[inicial:final]
            x = np.arange(len(labx))        
            for p in range(len(tops)): 
                l = ax1.plot(x,rate[tops[p],inicial:final],label=Lacum[tops[p]][0])       
                if p == 0: lns = l 
                else: lns += l 
                
            l = ax2.plot(x,np.sum(rate[:,inicial:final],axis=0),color='k',linestyle='--',label='Total') 
            lns += l
            labs = [l.get_label() for l in lns]
            leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                             shadow=False, fancybox=True)
            
            ax1.set_ylabel('Mensagens/Mês de cada membro')
            ax1.set_xlabel('Mês.semana')
            ax2.set_ylabel('Mensagens/Mês Total no grupo')
               

            leg.get_frame().set_alpha(0.5)  
            aux = np.linspace(x[1],x[-1],num=10,dtype=int)
            ax1.set_xticks(aux)
            ax1.set_xticklabels([labx[i] for i in aux],rotation=70)           
#            ax2.set_xticklabels(labx,rotation=70)
#            ax1.grid(True,linestyle='--',linewidth=.25)
            fig.tight_layout() 
            plt.title(grupo)
            plt.xticks()
#            ax1.locator_params(tight='True',axis='x',nbins=10)        
            print('Para continuar, feche o gráfico.\n')
            #plt.ioff()
            plt.show(block=True)        

        if a.isdigit() and int(a) == 4:
            tperiodo = int(input('Entre o comprimento dos intervalos em semanas. 1 ano = 50 semanas.\n'))# em semanas   
            top = int(input('Número de pessoas no gráfico. (mostra apenas as com mais mensagens)\n'))
            ninterv = round(len(data)/tperiodo)
            if ninterv < 1:
                ninterv = 1
            tops = np.zeros((top,ninterv),dtype='int8')
            k = 1
            while k < ninterv:
                aux1 = acum[:,k*tperiodo] - acum[:,(k-1)*tperiodo]
                dtype = [('id',int),('msg',int)]
                periodo = np.empty(len(Lacum),dtype=dtype)
                periodo['id'] = np.arange(len(Lacum))
                periodo['msg'] = aux1
                
                tops[:,k-1] =  np.sort(periodo, order='msg')['id'][-top:]
                k+=1
            
            aux1 = acum[:,-1] - acum[:,(k-1)*tperiodo]
            dtype = [('id',int),('msg',int)]
            periodo = np.empty(len(Lacum),dtype=dtype)
            periodo['id'] = np.arange(len(Lacum))
            periodo['msg'] = aux1
            
            tops[:,ninterv-1] =  np.sort(periodo, order='msg')['id'][-top:]
            
            
            k = 1   
    #        for w in range(len(data)):
    #            if data[w][-1] == '3':
    #                data[w] = ''.join((data[w][:-1],'2'))
    #            elif data[w][-1] != '1':
    #                data[w] = ' '
                          
            while k < ninterv:
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()
                x = data[(k-1)*tperiodo:k*tperiodo] #labx
    
    #            x = np.arange(len(labx))
    
                for p in range(top): 
                    A = smooth(rate7[tops[p,k-1],(k-1)*tperiodo:k*tperiodo],janelamento,'hanning')
                    l = ax1.plot(x,A[janelamento-1:],label=Lacum[tops[p,k-1]][0])  
                    if p == 0: lns = l 
                    else: lns += l 
                A = smooth(np.sum(rate7[:,(k-1)*tperiodo:k*tperiodo],axis=0),janelamento,'hanning')
                l = ax2.plot(x,A[janelamento-1:],color='k',linestyle='--',label='Total') 
                lns += l
                labs = [l.get_label() for l in lns]
                leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                                 shadow=False, fancybox=True)
                    
                leg.get_frame().set_alpha(0.5)  
                ax1.set_xticks(x)
                ax1.set_xticklabels(x,rotation=70)
                plt.locator_params(axis='x',nbins=10)
    #            ax2.locator_params(tight='True',nbins=10,axis='x')
    #            xticks = ticker.MaxNLocator(len(x))
    #            ax1.xaxis.set_major_locator(xticks)
                fig.tight_layout() 
                ax1.grid(True,linestyle='--',linewidth=.25)
                ax1.set_ylabel('Mensagens/Semana de cada membro')
                ax1.set_xlabel('Mês (Mês.semana)')
                ax2.set_ylabel('Mensagens/Semana Total no grupo')
                plt.title(grupo+'janelamento hanning = {}'.format(janelamento))
                k +=1
                
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            
            x = data[(k-1)*tperiodo:]

          #  x = np.arange(len(labx))        
            for p in range(top): 
                A = smooth(rate7[tops[p,k-1],(k-1)*tperiodo:],janelamento,'hanning')

                l = ax1.plot(x,A[janelamento-2:],label=Lacum[tops[p,k-1]][0])       
                if p == 0: lns = l 
                else: lns += l 
            A = smooth(np.sum(rate7[:,(k-1)*tperiodo:],axis=0),janelamento,'hanning')
            l = ax2.plot(x,A[janelamento-2:],color='k',linestyle='--',label='Total') 
            lns += l
            labs = [l.get_label() for l in lns]
            leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                             shadow=False, fancybox=True)
            
            ax1.set_ylabel('Mensagens/Semana de cada membro')
            ax1.set_xlabel('Mês.semana')
            ax2.set_ylabel('Mensagens/Semana Total no grupo')
                
            leg.get_frame().set_alpha(0.5)  
            ax1.set_xticklabels(x,rotation=70)
            ax1.grid(True,linestyle='--',linewidth=.25)
    #        xticks = ticker.MaxNLocator(len(x))
    #        ax1.xaxis.set_major_locator(xticks)
            fig.tight_layout() 
            plt.title(grupo+'janelamento hanning = {}'.format(janelamento))
            print('Para continuar, feche o gráfico.\n')
            #plt.ioff()
            plt.show(block=True)
            
        if a.isdigit() and int(a) == 5:
            k = 0
            print('Índice | Semana\n')
            for s in datastr: 
                print('{}   {}'.format(k,s))
                k+=1
            print('Índice | Semana\n')
            inicial = int(input('Entre o índice da semana inicial (lista acima).\n'))
            final = int(input('Entre o índice da semana final.\n'))        
    
            top = int(input('Número de pessoas no gráfico. (mostra apenas as com mais mensagens)\n'))
            tops = np.zeros(top,dtype='int8')
            
            aux1 = acum[:,final] - acum[:,inicial]
            dtype = [('id',int),('msg',int)]
            periodo = np.empty(len(Lacum),dtype=dtype)
            periodo['id'] = np.arange(len(Lacum))
            periodo['msg'] = aux1
            tops[:] =  np.sort(periodo, order='msg')['id'][-top:]
    
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            
            labx = data[inicial:final]
            x = np.arange(len(labx))        
            for p in range(top): 
                A = smooth(rate7[tops[p],inicial:final],janelamento,'hanning')
                l = ax1.plot(x,A[janelamento-1:],label=Lacum[tops[p]][0])       
                if p == 0: lns = l 
                else: lns += l 
            A = smooth(np.sum(rate7[:,inicial:final],axis=0),janelamento,'hanning')   
            l = ax2.plot(x,A[janelamento-1:],color='k',linestyle='--',label='Total') 
            lns += l
            labs = [l.get_label() for l in lns]
            leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                             shadow=False, fancybox=True)
            
            ax1.set_ylabel('Mensagens/Semana de cada membro')
            ax1.set_xlabel('Mês.semana')
            ax2.set_ylabel('Mensagens/Semana Total no grupo')
                
            leg.get_frame().set_alpha(0.5)  
            aux = np.linspace(x[1],x[-1],num=10,dtype=int)
            ax1.set_xticks(aux)
            ax1.set_xticklabels([labx[i] for i in aux],rotation=70)   
    #        xticks = ticker.MaxNLocator(len(x))
    #        ax1.xaxis.set_major_locator(xticks)
            fig.tight_layout() 
            plt.title(grupo+'janelamento hanning = {}'.format(janelamento))
            print('Para continuar, feche o gráfico.\n')
            #plt.ioff()
            plt.show(block=True)        
               
        if a.isdigit() and int(a) == 6:
            lista_pessoas = [(x,Lacum[x][0]) for x in range(len(Lacum))]
            lista_pessoas = sorted(lista_pessoas,key=lambda p: p[1])
            print('\nÍndice | Pessoa\n')
            
            for s in lista_pessoas: 
                print('  {}    {}'.format(s[0],s[1]))
            print('Índice | Pessoa\n')        
            ip = input('Entre o índice das pessoas que deseja fazer o gráfico separado por espaços.\n')
            tops = np.array(ip.split(),dtype=int)
    
    
            k = 0
            print('\nÍndice | Semana\n')
            for s in datastr: 
                print('{}   {}'.format(k,s))
                k+=1
            print('Índice | Semana\n')
            inicial = int(input('Entre o índice da semana inicial (lista acima).\n'))
            final = int(input('Entre o índice da semana final.\n'))        
    
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            
            labx = data[inicial:final]
            x = np.arange(len(labx))        
            for p in range(len(tops)): 
                A = smooth(rate7[tops[p],inicial:final],janelamento,'hanning')
                l = ax1.plot(x,A[janelamento-1:],label=Lacum[tops[p]][0])       
                if p == 0: lns = l 
                else: lns += l 
            A =  smooth(np.sum(rate7[:,inicial:final],axis=0),janelamento,'hanning')
            l = ax2.plot(x,A[janelamento-1:],color='k',linestyle='--',label='Total') 
            lns += l
            labs = [l.get_label() for l in lns]
            leg = ax1.legend(lns, labs, loc='best', ncol=2, mode="expand", \
                             shadow=False, fancybox=True)
            
            ax1.set_ylabel('Mensagens/Semana de cada membro')
            ax1.set_xlabel('Mês.semana')
            ax2.set_ylabel('Mensagens/Semana Total no grupo')
                
            aux = np.linspace(x[1],x[-1],num=10,dtype=int)
            ax1.set_xticks(aux)
            ax1.set_xticklabels([labx[i] for i in aux],rotation=70)   
            ax1.grid(True,linestyle='--',linewidth=.25)
    #        xticks = ticker.MaxNLocator(len(x))
    #        ax1.xaxis.set_major_locator(xticks)
            fig.tight_layout() 
            plt.title(grupo+'janelamento hanning = {}'.format(janelamento))
            print('Para continuar, feche o gráfico.\n')
            #plt.ioff()
            plt.show(block=True)        
        a = input("Entre 1 para fazer gráfico da taxa Mensal dos que mais mandam mensagens em intervalos dum número de semanas.\nEntre 2 para fazer gráfico da taxa Mensal dos que mais mandam mensagens em um perídodo determinado.\nEntre 3 para fazer gráfico da taxa Mensal de pessoas específicas.\nEntre 4 para fazer gráfico da taxa Semanal dos que mais mandam mensagens em intervalos dum número de semanas.\nEntre 5 para fazer gráfico da taxa Semanal dos que mais mandam mensagens em um perídodo determinado.\nEntre 6 para fazer gráfico da taxa semanal de pessoas específicas.\nEntre N para não fazer gráfico.\n")
            
    return rate7
    
        
#%%
def zapcorr(rate,datastr,Lacum):
    a = input('Entre 1 para calcular as maiores correlações de cada membro.\nEntre 2 para calcular as correlações de um membro específico num período espefícico.\n')
    if a.isdigit() and a == '1':
        a = input('Entre o tamanho dos periodos para amostragem em semanas. Menos de 50 é ruim. 1 ano ~ 50 semanas\n')
        if a.isdigit():
            tperiodo = int(a)
        else:    
            tperiodo = 75
        ninterv = round(len(datastr)/tperiodo)
        impr = [] # pra salvar em arquivo
    
        # periodo total
        C = np.tril(np.corrcoef(rate),-1)
        C = np.tril(np.corrcoef(rate),-1)        
        print('\nPeríodo Total {} à {}'.format(datastr[0],datastr[-1]))
        impr.append('Período Total {} a {},-,-'.format(datastr[0],datastr[1]))
        dtype = [('id1',int),('id2',int),('corr',float)]
        RankCorr = np.empty(len(Lacum),dtype=dtype)
        RankCorr['id1'] = np.arange(len(Lacum),dtype='int8')
        RankCorr['id2'] = np.argmax(C,axis=0)   
        RankCorr['corr'] =  np.nanmax(C,axis=0)*-1
        RankCorr = np.sort(RankCorr, order='corr')
        RankCorr['corr'] = RankCorr['corr']*-1
        
        duplas = []
        
        for i in RankCorr:
            if i[2] > .6:
                duplas.append([Lacum[i[0]][0],Lacum[i[1]][0],i[2]])
                print('{} & {} - {:.3}'.format(duplas[-1][0],duplas[-1][1],duplas[-1][2]))
                impr.append('{},{},{:.3}'.format(duplas[-1][0],duplas[-1][1],duplas[-1][2]))                
    
        
        
        # adiciona ruido aos zeros para permitir np.corrcoef funcionar
        # isso não é certo, mas não deve influenciar muito os resultados para
        # um tempo de amostra maior que 75
        for i in range(rate.shape[0]):
            for j in range(rate.shape[1]):    
                 if rate[i,j] == 0:
                     rate[i,j] = np.random.rand()/100  
                     
        for k in range(ninterv):
            if k < (ninterv-1):
                C = np.tril(np.corrcoef(rate[:,k*tperiodo:(k+1)*tperiodo]),-1)
                print('\nPeríodo {} à {}'.format(datastr[k*tperiodo],datastr[(k+1)*tperiodo]))
                impr.append('Período {} a {},-,-'.format(datastr[k*tperiodo],datastr[(k+1)*tperiodo]))
                if len(datastr[k*tperiodo:(k+1)*tperiodo]) < 50:
                    print('Pequena amostragem, evite conclusões!')
                    
            else:
                C = np.tril(np.corrcoef(rate[:,k*tperiodo:]),-1)    
                print('\nPeríodo {} à {}'.format(datastr[k*tperiodo],datastr[-1]))                 
                impr.append('Período {} a {},-,-'.format(datastr[k*tperiodo],datastr[-1]))
                if len(datastr[k*tperiodo:]) < 50:
                    print('Pequena amostragem, evite conclusões!')
                
            dtype = [('id1',int),('id2',int),('corr',float)]
            RankCorr = np.empty(len(Lacum),dtype=dtype)
            RankCorr['id1'] = np.arange(len(Lacum),dtype='int8')
            RankCorr['id2'] = np.argmax(C,axis=0)   
            RankCorr['corr'] =  np.nanmax(C,axis=0)*-1
            RankCorr = np.sort(RankCorr, order='corr')
            RankCorr['corr'] = RankCorr['corr']*-1
            
            duplas = []
            
           
            for i in RankCorr:
                if i[2] > .6:
                    duplas.append([Lacum[i[0]][0],Lacum[i[1]][0],i[2]])
                    print('{} & {} - {:.3}'.format(duplas[-1][0],duplas[-1][1],duplas[-1][2]))
                    impr.append('{},{},{:.3}'.format(duplas[-1][0],duplas[-1][1],duplas[-1][2]))                
    
        a = input('Salvar correlação? [S/n]\n')
        if a == 'S' or a == 's':
            resultado = open(''.join([grupo.nome_grupo,'_correlacao.csv']),'w')
            resultado.write('Membro1, Membro2, Correlação\n')
            p = 1
            for x in impr:
                resultado.write('{}\n'.format(x))
                p += 1
            print('Resultado salvo!\n')  
            resultado.close()

    if a.isdigit() and a == '2':
        lista_pessoas = [(x,Lacum[x][0]) for x in range(len(Lacum))]
        lista_pessoas = sorted(lista_pessoas,key=lambda p: p[1])
        print('\nÍndice | Pessoa\n')
        
        for s in lista_pessoas: 
            print('  {}    {}'.format(s[0],s[1]))
        print('Índice | Pessoa\n')        
        ip = int(input('Entre o índice das pessoa.\n'))
        k = 0
        print('\nÍndice | Semana\n')
        for s in datastr: 
            print('{}   {}'.format(k,s))
            k+=1
        print('Índice | Semana\n')
        inicial = int(input('Entre o índice da semana inicial (lista acima).\n'))
        final = int(input('Entre o índice da semana final.\n'))  
        if inicial < 0:
            inicial = 0
        if final >= len(datastr):
            final = len(datastr)-1
        
        if (final - inicial) < 51:
            print('Período de amostragem curto. Evite conclusões!\n')
        C = np.corrcoef(rate[:,inicial:final])
        
        dtype = [('id1',int),('corr',float)]
        RankCorr = np.empty(len(grupo.acum_7),dtype=dtype)
        RankCorr['id1'] = np.arange(len(grupo.acum_7),dtype='int8')
        RankCorr['corr'] =  C[:,ip]*-1
        RankCorr = np.sort(RankCorr, order='corr')
        RankCorr['corr'] = RankCorr['corr']*-1

        print('\nCorrelações de {} no período {} à {}'.format(Lacum[ip][0],datastr[inicial],datastr[final]))        
        for i in RankCorr:
            print('{:.3} {}'.format(i[1],Lacum[i[0]][0]))                  
    

                    
#%%        


print('Analizador de conversas em grupo de whatsapp \n')
print('gere um arquivo de backup entrando no grupo > configuraçoes (:) > mais > exportar conversa e salve na mesma pasta do arquivo whatstat.py\n')
file_name = input('Entre o arquivo .txt\n')
lenfn = len(file_name)

grupo = grupozap(file_name[0:lenfn-4])    

lista_pessoas = [] #pessoas e numero de mensagens

anterior = ''
anteriorN = 0;

ling = int(input('Em qual língua está o celular? Digite 1 para PT ou EN, digite 2 para DE, digite 3 para FR.\n'))

if ling == 1:
    with open(file_name,encoding='utf-8') as file:
        for line in file:
            palavras = line.split()
            try:
                if len(palavras) > 4 and palavras[3][0:1] != '\u200e':
                    if palavras[0][0:2].isdigit() and palavras[1][0:2].isdigit() and palavras[2] == '-':
                        #amarzena nome com ate 4 palavras
                        i = 3;
                        pessoa = palavras[3]
                        while i < 7:
                            len_nome = len(palavras[i])
                            if palavras[i][-1] != ':':
                                pessoa = ' '.join((pessoa,palavras[i+1]))
                                i+=1
                            else:                         
                                if pessoa == anterior:
                                    anteriorN +=1
                                else:
                                    data = palavras[0][6:10] + palavras[0][3:5] + palavras[0][0:2]
                                    grupo.addmsg(anterior[0:len(anterior)-1],anteriorN,data)
                                    anterior = pessoa
                                    anteriorN = 1                    
                                i = 7 
            except IndexError:
                pass                  
        try:                        
            grupo.addmsg(anterior[0:len(anterior)-1],anteriorN,data)
        except:
            pass        
elif ling == 2:
    with open(file_name,encoding='utf-8') as file:
        for line in file:
            palavras = line.split()
            try:
                if len(palavras) > 4 and palavras[3][0:1] != '\u200e':
                    if palavras[0][0:2].isdigit() and palavras[1][0:2].isdigit() and palavras[2] == '-':
                        #amarzena nome com ate 4 palavras
                        i = 3;
                        pessoa = palavras[3]
                        while i < 7:
                            len_nome = len(palavras[i])
                            if palavras[i][-1] != ':':
                                pessoa = ' '.join((pessoa,palavras[i+1]))
                                i+=1
                            else:                         
                                if pessoa == anterior:
                                    anteriorN +=1
                                else:
                                    data = '20' + palavras[0][6:8] + palavras[0][3:5] + palavras[0][0:2]
                                    grupo.addmsg(anterior[0:len(anterior)-1],anteriorN,data)
                                    anterior = pessoa
                                    anteriorN = 1                    
                                i = 7 
            except IndexError:
                pass                  
        try:                        
            grupo.addmsg(anterior[0:len(anterior)-1],anteriorN,data)
        except:
            pass

elif ling == 3:
    with open(file_name,encoding='utf-8') as file:
        for line in file:
            palavras = line.split()
            try:
                if len(palavras) > 4 and palavras[3][0:1] != '\u200e':
                    if palavras[0][0:2].isdigit() and palavras[1][0:2].isdigit() and palavras[3] == '-':
                        #amarzena nome com ate 4 palavras
                        i = 3;
                        pessoa = palavras[3]
                        while i < 7:
                            len_nome = len(palavras[i])
                            if palavras[i][-1] != ':':
                                pessoa = ' '.join((pessoa,palavras[i+1]))
                                i+=1
                            else:                         
                                if pessoa == anterior:
                                    anteriorN +=1
                                else:
                                    data = palavras[0][6:10] + palavras[0][3:5] + palavras[0][0:2]
                                    grupo.addmsg(anterior[0:len(anterior)-1],anteriorN,data)
                                    anterior = pessoa
                                    anteriorN = 1                    
                                i = 7 
            except IndexError:
                pass                  
        try:                        
            grupo.addmsg(anterior[0:len(anterior)-1],anteriorN,data)
        except:
            pass        
                
grupo.ordenar()                
grupo.listar()
datastr = grupo.semanal()   
             
           
print('Para calcular taxa temporal necessita-se do pacote NumPy e Matplotlib')
a = input('Calcular taxa temporal de mensangens? [S/n]\n') 


#%%

if a == 'S' or a == 's':
    try:
        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt
        rate = taxa(grupo.acum_7,datastr,grupo.nome_grupo)  
        
        a = input('Calcular correlação? [S/n]\n')
        while a != 'n': 
            if a == 'S' or a == 's':    
                zapcorr(rate,datastr,grupo.acum_7)
            a = input('\n Calcular outra correlação? [S/n]\n')
            
    except ImportError:
        print('NumPy e/ou Matplotlib não encontrados!')
        print('Estes módulos são necessários para programação vetor-orientada')
        print('e para fazer gráficos respectivamente.')
        print('Obtenha-os incluidos na distribuição anaconda:')
        print('https://www.anaconda.com/download/')
        
a = input('Clique qualquer coisa para sair.')   
     
