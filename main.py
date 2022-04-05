from readers import *

#chemin jusqu'au fichiers : peut être modifier
chemin ='calcul_8'

################################################################################
# Certe partie du fichier sert à récuérer les fichiers de données et les triers
################################################################################
#créé l'objet trie  qui est un objet descendant de l'objet extension
liste_fichier = Trie(chemin)

#recupère tous les fichiers compris dans le dossier : Ne pas modifier
# recupere est une fonction de la classe extension permettant de crer ue liste
# de l'ensemble des fichiers / dossiers présent dans le répertoire donné par 'chemin'
# puis appelle automatiquement la fonction trie_des_extension, permettant la
#creation d'un dictionnaire des extensions.
liste_fichier.recupere() # ne pas modifier


#remplis un dictionnaire qui a chaque extension associe la liste des fichiers de cette extension
#liste_fichier.trie_des_extension() # ne pas modifier

#fonction permettant d'afficher le dictionnaire
#si on l'utilise avant la création du dico ça ne sert à rien
#liste_fichier.__repr__()



#ici nous avons décider de récupérer les fichiers txt : A modifier si l'on veutn
liste_fichier.trie_les_fichiers_commencant_par_un_chiffre('.txt')



#Recupère les listes du dictionnaire
liste_des_fichiers_txt = liste_fichier.extension['.txt']
liste_des_fichiers_dat = liste_fichier.extension['.dat']
#liste_des_fichiers_csv = liste_fichier.extension['.csv']


# file = CsvReader(chemin,liste_des_fichiers_csv[0])
# file.info_list_parse()



##############################################################################"
# TOUT SE QUI SERT AU TRACE "
#creation des matrices qui nous servirons pour le tracé
matrice_Courbee = []
matrice_plate   = []
liste_temps     = []


#recupération des données du substrat
file = TxtReader(chemin,liste_des_fichiers_dat[2]) # créér un objet pour lire les ficheirs
file.info_list_parse()
# X_substrat_plat,  Y_substrat_plat ,X_substrat_Courbee ,Y_substrat_Courbee ,tampon =file.getLineFromcolumn()
# #ici tampon est un string, car le fichier substrat est pas formaté pareil que les autres fichiers reusltats
#
#
# #mise en centimètre des abscisses et en micromètre des ordonnées
# #purement relatif à notre cas traité
# X_substrat_plat    = [i*100 for i in X_substrat_plat]
# X_substrat_Courbee = [i*100 for i in X_substrat_Courbee]
# Y_substrat_Courbee = [i*1000000 for i in Y_substrat_Courbee]
#
#
# #boucle itérative de lecture de l'ensemble des fichiers txt
# # avoir sur quel type de fichier on veut le faire
# for i in range(len(liste_des_fichiers_txt)):
#     file = TxtReader(chemin,liste_des_fichiers_txt[i]) # créér un objet pour lire les ficheirs
#     file.info_list_parse()                    # recupere les données et le smets sous une forme de matrice
#     #la fonction getLineFromColumn peut nécessiter des modifications
#     lineX,  lineY ,lineXC ,lineYC,time  =file.getLineFromcolumn() # créé des listes de chacunes des colonnes
#
#
#     #mise en micromètre des ordonnées # mise ne forme des données
#     lineY  = [i*1000000 for i in lineY]
#     lineYC = [i*1000000 for i in lineYC]
#     #ajout de chaque liste dans leur liste respective
#     matrice_Courbee.append(lineYC)
#     matrice_plate.append(lineY)
#     liste_temps.append(int(float(time)))
# #transforme les integer en string pour s'en servir de label plus tard
#
# liste_temps = list(map(str, liste_temps))
#
#
# trace=Trace(chemin)
# trace.chemin_existe()
#
#
#
# fig = plt.figure(1)
# with writer.saving(fig, chemin+"/animation/animation_plat.mp4",15):
#     for i in range(0,len(matrice_plate)):
#         #y = matrice_plate[i][:]
#         plt.plot(X_substrat_plat,matrice_plate[0][:],color='g',label ='etat initial', animated = True)
#         plt.plot(X_substrat_plat,matrice_plate[i][:],color='red',label= liste_temps[i]+ " secondes", animated = True)
#         plt.grid()
#         plt.xlabel("Abscisses (cm)", fontsize =10)
#         plt.ylabel("Hauteur du fluide (µm)", fontsize = 10)
#         plt.ylim(0,max(max(matrice_plate))+50)
#         plt.legend(prop={'size':10})
#         plt.xlim(X_substrat_plat[0],X_substrat_plat[len(X_substrat_plat)-1])
#         plt.title('Simulation du mouvement du fluide sur un substrat plat')
#         writer.grab_frame()
#         plt.clf()
#
# print("animation plate prête")
#
# #figure pour la la représentation courbée
# fig = plt.figure(2)
# with writer.saving(fig, chemin+"/animation/animation_courbee.mp4",15):
#     for i in range(0,len(matrice_Courbee)):
#         #y = matrice_Courbee[i][:]
#         plt.plot(X_substrat_Courbee , matrice_Courbee[0][:] ,color='g'  ,label ='état initial'              ,animated = True)
#         plt.plot(X_substrat_Courbee , Y_substrat_Courbee    ,color='b'  , label ='substrat')
#         plt.plot(X_substrat_Courbee , matrice_Courbee[i][:]                     ,color='red',label= liste_temps[i]+ " secondes" , animated = True)
#         plt.grid()
#         plt.xlabel("Abscisses (cm)", fontsize =10)
#         plt.ylabel("Hauteur du fluide (µm)", fontsize = 10)
#         plt.ylim(min(min(matrice_Courbee))-200,max(max(matrice_Courbee))+100)
#         plt.legend(prop={'size':10})
#         plt.xlim(X_substrat_plat[0],X_substrat_Courbee[len(X_substrat_plat)-1]+0.0005)
#         plt.title('Simulation du mouvement du fluide sur un substrat courbé')
#         writer.grab_frame()
#         plt.clf()
#
# print("animation courbée prête")
#
#
#
# # ##instanciation
# # txtreader = TxtReader('0iterations.txt')
# # # lecture du fichier
# # txtreader.read()
# # # Affichage de la représentation
# # print(repr(txtreader))
# # # affichage de la 3ème ligne
# # print(txtreader.line(1))
# # #
# # #
# # #
# #
# #
# # # instanciation
# # csvreader = CsvReader('huricane.csv')
# # # ouverture du fichier
# # csvreader.read()
# # # affichage de la 3ème ligne
# # csvreader.line(2)
