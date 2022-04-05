import csv
import os
import sys
import time
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.animation as manimation
import numpy as np



################################
#aide à la création de la video
###############################
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)
########################################################


##############################""
# ajout de lignes de commentaires pour vérifier si je comprends guthub
############################



###############################################################################
###############################################################################
# Cette classe a pour but de donner les fonctions permettant de récupérer
# tous les fichiers présent dans un répertoire et de les trier en fonction de
# leur extension (.csv, .txt, .dat etc....)
###############################################################################
###############################################################################

class Extension :

    def __init__(self,path):
        self._path = path               # chemin jusqu'au dossier contenant les fichiers
        self._liste_fichier=[]          # liste contenant tous les fichiers du dossier
        self._dict_extension_fichier={} # dictionnaire qui a chaque extension  donnera la liste de tous les fichiers de la même extension
        self._nbre_extension =0         # nombre de type d'extension

    def __repr__(self):
        print('{')
        for key in self._dict_extension_fichier :
            print(len(self._dict_extension_fichier[key]),"fichiers ", key, ": \n", self._dict_extension_fichier[key], "\n")
        print('}')
    ###########################################################################
    # Les fonctions ayant un @propertuy au dessus servent à accéder aux éléments
    # definis dans __init__
    ############################################################################
    @property
    def path(self):
        return self._path

    @property
    def nbre_extension(self):
        return self._nbre_extension


    @property
    def liste_fichier(self):
        return self._liste_fichier


    @property
    def extension(self):
        return self._dict_extension_fichier

    #recupère tous les noms des fichiers contenu dans le dossier
    def recupere(self):
        self._liste_fichier = os.listdir(self._path)
        self.trie_des_extension()

    # créé un dictionnaire qui a chaque extension associe une liste des noms des
    # fichier ayant cette extension
    # {'.txt' : [], '.csv': [], etc...}
    def trie_des_extension(self):
        for i in range(len(self._liste_fichier)):
            extension = os.path.splitext(self._liste_fichier[i])[1] #recupère l'extension du fichier traité
            if extension == '':
                extension = 'dossier'
            #la boucle ci-dessous indique que si l'extension existe deja dans le dictionnaire
            #nous ajoutons le fichier àa la liste existante
            #sinon, nus créons une nouvelle cles de dictionnaire ainsi que la liste associée
            if extension in self._dict_extension_fichier :
                self._dict_extension_fichier[extension]+=[self._liste_fichier[i]]
            else:
                self._dict_extension_fichier[extension] =[self._liste_fichier[i]]
                self._nbre_extension +=1

    def nbre_fichier_de_l_extension(self,key):
        return len(self._dict_extension_fichier[key])

    def affichage_nbre_extension(self):
        print('Il y a', self._nbre_extension,'types de fichier')
        for key in self._dict_extension_fichier :
             print(self.nbre_fichier_de_l_extension(key),'fichiers', key)



###############################################################################
###############################################################################
#Cette classe permet de trier les listes des fichiers résultats comme on le
#souhaite, ordre alapha, par nomre croissant en déut de nom ou fin de nom
###############################################################################
###############################################################################
class Trie(Extension):

    ###########################################################################
    #la particularité des fonctions ci-dessous est qu'elle prenen en entrée la
    # clef permettant de les répérer dans le dictionnaire
    ###########################################################################

    def trie_les_fichiers_par_ordre_alphabetique(self,key):
        #for key in self._dict_extension_fichier:
        self._dict_extension_fichier[key] = sorted(self._dict_extension_fichier[key])
        #liste =sorted(liste)


    def trie_les_fichiers_commencant_par_un_chiffre(self,key):
        #for key in self._dict_extension_fichier:
        liste_iteration=[] #sert a recupérer les nombres des noms des fichiers
        for i in range(len(self._dict_extension_fichier[key])):
            iter_string = re.findall('\d+',self._dict_extension_fichier[key][i])    #recupère l'integer du nom du fichier
            liste_iteration += iter_string               #ajoute l'integer (en chaine de caractère) à la liste
        fin_nom_fichier = "".join(re.findall('\D+',self._dict_extension_fichier[key][0])) # recupère la chaine de caractère du nom
        liste_iteration = list(map(str,sorted(list(map(int, liste_iteration)))))

        for i in range(0, len(liste_iteration)) :
            liste_iteration[i] = liste_iteration[i]+fin_nom_fichier
            #self._dict_extension_fichier[key] = liste_iteration
        self._dict_extension_fichier[key] =liste_iteration


    def trie_les_fichiers_finissant_par_un_chiffre(self,key):
        #for key in self._dict_extension_fichier:
        liste_iteration=[]
        for i in range(len(self._dict_extension_fichier[key])):
            iter_string = re.findall('\d+',self._dict_extension_fichier[key][i])    #recupère l'integer du nom du fichier
            liste_iteration += iter_string               #ajoute l'integer (en chaine de caractère) à la liste
        debut_nom_fichier = "".join(re.findall('\D+',os.path.splitext(self._dict_extension_fichier[key][0])[0])) # recupère la chaine de caractère du nom
        liste_iteration = list(map(str,sorted(list(map(int, liste_iteration)))))
        extension = os.path.splitext(self._liste_fichier[i])[1]
        for i in range(0, len(liste_iteration)) :
            liste_iteration[i] = debut_nom_fichier+liste_iteration[i]+os.path.splitext(self._dict_extension_fichier[key][0])[1]
            #self._dict_extension_fichier[key] = liste_iteration
        self._dict_extension_fichier[key] =liste_iteration


        # def trie_les_fichiers_par_date(self):
        #
        #     for keys in self._dict_extension_fichier:
        #         liste_iteration=[]
        #         #sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        #         #sorted(self._dict_extension_fichier[key].iterdir(), key=os.path.getmtime)
        #         self._dict_extension_fichier[keys].sort(key=os.path.getctime)
        #         #print(self._dict_extension_fichier[keys])


class GenericReaders:

    def __init__(self,path,namefile):
        self._content=[]
        self._path = path
        self.namefile = namefile
        self._up_to_date = False

    @property
    def content(self):
        return self._content

    #
    def line(self,indice):
        return self._content[indice].split(',')

    def  __repr__(self):
        return '<Str: namefile={}, open={}>'.format(self.namefile, self._open)


    @property
    def _is_up_to_date(self):
        if not self._up_to_date:
            raise AttributeError("File {} not up to date.".format(self.namefile))



class TxtReader(GenericReaders):

    ############################################################################
    # La fonction read, lis ligne par ligne le fichier texte et range dans une liste
    # chaque ligne sous forme d'un string
    ############################################################################
    def read(self):
        self.namefile = self._path +'/'+ self.namefile
        file=open(self.namefile,'r')
        self._content=[]
        for line in  file:
            self._content.append(line[:-1])
        file.close()
        self._open = True

    ############################################################################
    # cette fonction lit notre fichier ligne par ligne, mais chaque ligne est conservée
    # sous forme de liste, qui est ensuite rangé dans une grande liste, ce qui
    # revient a créer une grande matrice de la forme du fichier de résultat
    ############################################################################

    def info_list_parse(self):
        parseLine = lambda a : a.split()
        self.namefile = self._path +'/'+ self.namefile
        with open(self.namefile, "r") as file:
            self._content = []
            for line in file:
                if(len(parseLine(line))>1):
                    self._content.append(parseLine(line))
            #for x in matrice:
            #    print(*x, sep=" ")
            #return matrice

    def getLineFromcolumn(self):
        lineX  = []
        lineY  = []
        lineXC = []
        lineYC = []
        time   = self._content[0][3] #recupère le temps dans les fichiers de sorties
        for i in range(2,len(self._content)):
            #index,
            #l'indice des index commence à 0, et les virgules comptent comme une colonne
            #les données sont donc contenues que aux indices pairs ,0, 2, 4 et 6
            lineX.append(float(self._content[i][0]))
            lineY.append(float(self._content[i][2]))
            lineXC.append(float(self._content[i][4]))
            lineYC.append(float(self._content[i][6]))
        return(lineX, lineY, lineXC,lineYC,time)





class CsvReader(GenericReaders):



    def read(self):
        self.namefile = self._path +'/'+ self.namefile
        file = open(self.namefile, 'r')
        # Read csv format
        csvr = csv.reader(file)#,  delimiter=',')
        # Iterate over csv reader
        for line in csvr:
            str=' '.join(line)
            self._content.append(str)
            # format and append content
        self._open = True
            # Close file
        file.close()

    def info_list_parse(self):
        parseLine = lambda a : a.split()
        self.namefile = self._path +'/'+ self.namefile
        file = open(self.namefile, 'r')
        csvr = csv.reader(file)#,  delimiter=',')
        for line in csvr:
            self._content = []
            for line in file:
                if(len(parseLine(line))>1):
                    self._content.append(parseLine(line))
            #for x in matrice:
            #    print(*x, sep=" ")

    def getLineFromcolumn(self):
        lineX  = []
        lineY  = []
        lineXC = []
        lineYC = []
        time   = self._content[0][3] #recupère le temps dans les fichiers de sorties
        for i in range(2,len(self._content)):
            #index,
            #l'indice des index commence à 0, et les virgules comptent comme une colonne
            #les données sont donc contenues que aux indices pairs ,0, 2, 4 et 6
            lineX.append(float(self._content[i][0]))
            lineY.append(float(self._content[i][2]))
            lineXC.append(float(self._content[i][4]))
            lineYC.append(float(self._content[i][6]))
        return(lineX, lineY, lineXC,lineYC,time)


    def __getitem__(self,key):
        self._is_up_to_date
        for line in self.content:
            print(line[0])
            if line[0] == key:
                return list(float(el) for el in line[1:])
                print("key {} non trouvée dans le fichier {}".format(key, self.namefile))

class Trace:

    def __init__(self,path):
        self._path = path



    def chemin_existe(self):
        if os.path.exists(self._path+"/animation"):
            print("le dossier d'animation pour ces résultats existe déjà : ",self._path+"/animation")
        else:
            os.mkdir(self._path+"/animation")
            print( " le self._path d'accès aux animations est : ", self._path+"/animation")




    # def trace_courbe(self,titre_video):
    #
    #     fig = plt.figure(1)
    #     with writer.saving(fig, chemin+"/animation/"+titre_video+"".mp4",150):
    #         for i in range(0,len(matrice_plate)):
    #             #y = matrice_plate[i][:]
    #             plt.plot(X_substrat_plat,matrice_plate[0][:],color='g',label ='etat initial', animated = True)
    #             plt.plot(X_substrat_plat,matrice_plate[i][:],color='red',label= liste_temps[i]+ " secondes", animated = True)
    #             plt.grid()
    #             plt.xlabel("Abscisses (cm)", fontsize =10)
    #             plt.ylabel("Hauteur du fluide (µm)", fontsize = 10)
    #             plt.ylim(0,max(max(matrice_plate))+50)
    #             plt.legend(prop={'size':10})
    #             plt.xlim(X_substrat_plat[0],X_substrat_plat[len(X_substrat_plat)-1])
    #             plt.title('Simulation du mouvement du fluide sur un substrat plat')
    #             writer.grab_frame()
    #             plt.clf()
    #         print("animation plate prête")
