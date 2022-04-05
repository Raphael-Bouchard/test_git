#auteur : Raphaël BOUCHARD
#run it with python3.6

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.animation as manimation
import numpy as np
import os
import re


################################
#aide à la création de la video
###############################
FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)
########################################################


##################################
# definition des fonctions utiles#
###################################


parseLine = lambda a : a.split()


#transforme les tableaux de données en matrice géante
def info_list_parse(str_path_client_list):
    with open(str_path_client_list, "r") as file:
        matrice = []
        for line in file:
            if(len(parseLine(line))>1):
                matrice.append(parseLine(line))
        #for x in matrice:
        #    print(*x, sep=" ")
        return matrice

        #create vector with information selected
def getLineFromcolumn(matrice):
    lineX  = []
    lineY  = []
    lineXC = []
    lineYC = []
    time   = matrice[0][3] #recupère le temps dans les fichiers de sorties
    for i in range(2,len(matrice)):
        #index,
        #l'indice des index commence à 0, et les virgules comptent comme une colonne
        #les données sont donc contenues que aux indices pairs ,0, 2, 4 et 6
        lineX.append(float(matrice[i][0]))
        lineY.append(float(matrice[i][2]))
        lineXC.append(float(matrice[i][4]))
        lineYC.append(float(matrice[i][6]))
    return(lineX, lineY, lineXC,lineYC,time)

def lineToStr(line):
    lineStr = " "
    for x in line:
        lineStr += x + " "
    lineStr+="\n"
    return lineStr

# fonction permettant de trier une liste d'entier
def tri_insertion(L):
    N = len(L)
    for n in range(1,N):
        cle = L[n]
        j = n-1
        while j>=0 and L[j] > cle:
            L[j+1] = L[j] # decalage
            j = j-1
        L[j+1] = cle
    return L

# fonction permettant de trier les fichiers dans le bon ordre
#bon en fait elle trie rien du tout
def tri_fichiers_resultats(chemin):
    #permet de parcourir la liste de fichier contenu dans le dossier et de les conservers, c'est une liste.
    files = os.listdir(chemin)



    #vecteur contenant les itérations des fichiers de sorties
    liste_iteration =[]

    #parcours l'ensemble des fichiers dans le dossier
    for filename in files:
        iter_string = re.findall('\d+',filename) #recupère l'integer du nom du fichier
        liste_iteration += iter_string     #ajoute l'integer (en chaine de caractère) à la liste
    fin_nom_fichier = "".join(re.findall('\D+',files[0]))



    #transforme les chaines de charactères en entier
    liste_iteration = sorted(list(map(int, liste_iteration)))


    #trie les entiers
    #tri_insertion(liste_iteration)

    #transforme les entier en chaine de character
    liste_iteration = list(map(str, liste_iteration))
    #on a la liste des fichiers dans l'ordre des iterations après ça
    #permet de boucler sur les elements dans le bon ordre

    #ajoute la fin des noms des fichiers
    for i in range(0, len(liste_iteration)) :
        liste_iteration[i] = liste_iteration[i]+fin_nom_fichier
    return liste_iteration


#####################################
#Fin des fonctions
#####################################


#chemin d'accès aux fichiers résultats
chemin = "courbe"
#créé une liste avec le nom des fichiers résultats
#bien penser à trier le dossier avec les resultats part nom
liste_nom_fichiers = tri_fichiers_resultats(chemin)

#print (liste_nom_fichiers)

#initialise les matrices contenant les résultats selon la configuration et les pas de temps
matrice_Courbee = []
matrice_plate   = []
liste_temps     = []


#m#recupération des données du substrat
matrice1=info_list_parse(chemin+"/substrat.dat")
X_substrat_plat,  Y_substrat_plat ,X_substrat_Courbee ,Y_substrat_Courbee ,tampon =getLineFromcolumn(matrice1)
#ici tampon est un string, car le fichier substrat est pas formaté pareil que les autres fichiers reusltats
#mise en centimètre des abscisses et en micromètre des ordonnées
X_substrat_plat    = [i*100 for i in X_substrat_plat]
X_substrat_Courbee = [i*100 for i in X_substrat_Courbee]
Y_substrat_Courbee = [i*1000000 for i in Y_substrat_Courbee]


#print(Y_substrat_Courbee)

#remplissage des deux matrices geantes contenant les hauteurs à chaque pas de temps
for filename in liste_nom_fichiers :
    matrice = info_list_parse(chemin+"/"+filename)
    #print(filename)
    lineX,  lineY ,lineXC ,lineYC,time  =getLineFromcolumn(matrice)
    #mise en micromètre des ordonnées
    lineY  = [i*1000000 for i in lineY]
    lineYC = [i*1000000 for i in lineYC]
    #ajout de chaque liste dans leur liste respective
    matrice_Courbee.append(lineYC)
    matrice_plate.append(lineY)
    liste_temps.append(int(float(time)))
#transforme les integer en string pour s'en servir de label plus tard
liste_temps = list(map(str, liste_temps))
#print (liste_temps)


#creation du dossier contenant les animations
if os.path.exists(chemin+"/animation"):
    print("le dossier d'animation pour ces résultats existe déjà : ",chemin+"/animation")
else:
    os.mkdir(chemin+"/animation")
    print( " le chemin d'accès aux animations est : ", chemin+"/animation")


 # debut du tracé de l'animation

 #figure pour la courbe plate
fig = plt.figure(1)
with writer.saving(fig, chemin+"/animation/animation_plat.mp4",150):
    for i in range(0,len(matrice_plate)):
        #y = matrice_plate[i][:]
        plt.plot(X_substrat_plat,matrice_plate[0][:],color='g',label ='etat initial', animated = True)
        plt.plot(X_substrat_plat,matrice_plate[i][:],color='red',label= liste_temps[i]+ " secondes", animated = True)
        plt.grid()
        plt.xlabel("Abscisses (cm)", fontsize =10)
        plt.ylabel("Hauteur du fluide (µm)", fontsize = 10)
        plt.ylim(0,max(max(matrice_plate))+50)
        plt.legend(prop={'size':10})
        plt.xlim(X_substrat_plat[0],X_substrat_plat[len(X_substrat_plat)-1])
        plt.title('Simulation du mouvement du fluide sur un substrat plat')
        writer.grab_frame()
        plt.clf()

print("animation plate prête")

#figure pour la la représentation courbée
fig = plt.figure(2)
with writer.saving(fig, chemin+"/animation/animation_courbee.mp4",150):
    for i in range(0,len(matrice_Courbee)):
        #y = matrice_Courbee[i][:]
        plt.plot(X_substrat_Courbee , matrice_Courbee[0][:] ,color='g'  ,label ='état initial'              ,animated = True)
        plt.plot(X_substrat_Courbee , Y_substrat_Courbee    ,color='b'  , label ='substrat')
        plt.plot(X_substrat_Courbee , matrice_Courbee[i][:]                     ,color='red',label= liste_temps[i]+ " secondes" , animated = True)
        plt.grid()
        plt.xlabel("Abscisses (cm)", fontsize =10)
        plt.ylabel("Hauteur du fluide (µm)", fontsize = 10)
        plt.ylim(min(min(matrice_Courbee))-200,max(max(matrice_Courbee))+100)
        plt.legend(prop={'size':10})
        plt.xlim(X_substrat_plat[0],X_substrat_Courbee[len(X_substrat_plat)-1]+0.0005)
        plt.title('Simulation du mouvement du fluide sur un substrat courbé')
        writer.grab_frame()
        plt.clf()

print("animation courbée prête")
