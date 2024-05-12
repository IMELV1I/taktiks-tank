import pygame
import math
import time
from pygame.locals import*
from random import*

#############################################################################
# variables
angle = 0
fond = True
état = 0
x = 1680
y = 1050
pygame.init()
flags = pygame.FULLSCREEN
screen = pygame.display.set_mode((x,y), flags)
#importation de toute les images néssecaire au jeu (+réglage de leurs tailles):
balle_joueur1 = pygame.transform.scale(pygame.image.load("balleJ1.png"),(25,25))
balle_joueur2 = pygame.transform.scale(pygame.image.load("balleJ2.png"),(25,25))
caisse = pygame.transform.scale(pygame.image.load("caisse.png"),(150,150))
background = pygame.transform.scale(pygame.image.load("fondmapV1.png"),(x,y))
Terrain = pygame.transform.scale(pygame.image.load("fondV6.png"),(x,y))
fond_victoire = pygame.transform.scale(pygame.image.load("fondV5.png"),(x,y))
fond_menu = pygame.transform.scale(pygame.image.load("fondV5.png"),(x,y))
win_J1 = pygame.image.load("win_J1.png")
win_J2 = pygame.image.load("win_J2.png")
J2= pygame.transform.scale(pygame.image.load("J2.png"),(256,100))
J1 = pygame.transform.scale(pygame.image.load("J1.png"),(256,100))
attention = pygame.transform.scale(pygame.image.load("attention.png"),(256,64))
logo = pygame.transform.scale(pygame.image.load("logo.png"),(1024,600))
jouer_foncé = pygame.transform.scale(pygame.image.load("jouer_foncé.png"),(512,128))
jouer_clair = pygame.transform.scale(pygame.image.load("jouer_clair.png"),(512,128))
rejouer_foncé = pygame.transform.scale(pygame.image.load("rejouer_foncé.png"),(512,128))
rejouer_clair = pygame.transform.scale(pygame.image.load("rejouer_clair.png"),(512,128))
menu_foncé = pygame.transform.scale(pygame.image.load("menu_foncé.png"),(256,64))
menu_clair = pygame.transform.scale(pygame.image.load("menu_clair.png"),(256,64))
recommencer = pygame.transform.scale(pygame.image.load("recommencer.png"),(50,50))
bouton_quitter = pygame.transform.scale(pygame.image.load("bouton_quitter.png"),(165,43))
info_foncé = pygame.transform.scale(pygame.image.load("info_foncé.png"),(165,64))
info_clair = pygame.transform.scale(pygame.image.load("info_clair.png"),(165,64))
full_vieJ1 = pygame.transform.scale(pygame.image.load("full_vie.png"),(280,90))
mi_vieJ1 = pygame.transform.scale(pygame.image.load("mi_vie.png"),(280,90))
pas_de_vieJ1 = pygame.transform.scale(pygame.image.load("pas_de_vie.png"),(280,90))
full_vieJ2 = pygame.transform.scale(pygame.image.load("full_vie.png"),(280,90))
mi_vieJ2 = pygame.transform.scale(pygame.image.load("mi_vie.png"),(280,90))
pas_de_vieJ2 = pygame.transform.scale(pygame.image.load("pas_de_vie.png"),(280,90))
fond_info = pygame.transform.scale(pygame.image.load("fond_infoV1.png"),(x,y))
fleche_retour = pygame.transform.scale(pygame.image.load("fleche_retour.png"),(90,90))
#coordonnées des tirs du joueur n°1 et du joueur n°2:
tir_player1 = pygame.Vector2(50 , screen.get_height() / 2)
tir_player2 = pygame.Vector2(1525 , screen.get_height() / 2)
#variables pour la rotation du joueur:
newrotationJ1 = 0
rotationJ1 = -90
touchepressJ1 = 2
newrotationJ2 = 0
rotationJ2 = 90
touchepressJ2 = 3
#variables pour les tirs et leur rotation :
angle_vitesse1 = 3
angle_vitesse2 = 2
tir1_1=0
tir1=0
tir2_1=0
tir2=0
#variables pour l'état du tank suivant le nombre de tirs reçu:
etat_f_J1 = 0
etat_f_J2 = 0
#variables pour le choix des tanks dans le menu:
choix_J1 = 0
choix_J2 = 0
xJ1 = 0
yJ1 = 0
xJ2 = 0
yJ2 = 0
#variable pour reinitialiser l'image des tanks ou encore le nombre de vie a atteindre pour perdre:
init_partie = 0
nb_vie_perdu=0
#variable pour créer la grille pour le terrain
a3= x//150 -2
b3= y//150 +1

grille2 = []
position2 =[]

dernier_tir1 = time.time()
dernier_tir2 = time.time()
touche_press = time.time()

##Parametre modifiable du jeu##
vitesse_joueur = 1
vitesse_balle = 2
nb_vie = 3


#########################################################################################
#fonction pour créer la grille de façon aléatoire
def creer_grille(a3, b3, grille2):
    grille1=[]
    grille2=[]
    for w in range(a3):
        for p in range(b3):
            grille1.append(randint(0,3))
        grille2.append(grille1)
        grille1 = []
    return grille2

#affichage des caisses sur le terrain
def creer_position_caisse(a3, b3, grille2, position2):
    position=[]
    position2=[]
    for e in range(a3):
        for j in range(b3):
            if grille2[e][j] == 1:
                screen.blit(caisse,(e*150+150,j*150))
                position.append(e*150+150)
                position.append(j*150)
                position2.append(position)
                position = []
    return position2

#définition d'une fonction pour éviter les colisions entre les joueurs et les boites
def colision_caisse(player_pos,vitesse,liste,état):
    for l in range(len(liste)):
        if player_pos.y + 100 > liste[l][1] and player_pos.y < liste[l][1]+150 and player_pos.x +100 > liste[l][0] and player_pos.x < liste[l][0]+150:
            if player_pos.x > liste[l][0]+140:
                player_pos.x += vitesse
            elif player_pos.y > liste[l][1]+140:
                player_pos.y += vitesse
            elif player_pos.x < liste[l][0]-90:
                player_pos.x -= vitesse
            elif player_pos.y < liste[l][1]-90:
                player_pos.y -= vitesse

#définition d'une fonction pour éviter les colisions entre les balles et les boites
def colision_caisse_balle(tir_player, liste,tir,tirbis):
    for l in range(len(liste)):
        if tir_player.y > liste[l][1] and tir_player.y < liste[l][1]+150 and tir_player.x > liste[l][0] and tir_player.x < liste[l][0]+150:
            if tir_player.x > liste[l][0]:
                tir = 0
                tirbis = 0
            elif tir_player.y > liste[l][1]:
                tir = 0
                tirbis = 0
            elif tir_player.x < liste[l][0]-90:
                tir = 0
                tirbis = 0
            elif tir_player.y < liste[l][1]-90:
               tir = 0
               tirbis = 0
    return tir, tirbis



#cette definition empeche les joueur de passer à travers les murs des bords:
def mur(player_pos,x,y,vitesse):
    if player_pos.y > y -100:
        player_pos.y -= vitesse
    if player_pos.x > x -100:
        player_pos.x -= vitesse
    if player_pos.y < 0:
        player_pos.y += vitesse
    if player_pos.x < 0:
        player_pos.x += vitesse

############################################################################################################
# boucle principale
while fond == True:

    for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type==pygame.KEYDOWN and event.key== K_ESCAPE):
                pygame.quit()
                exit(0)

    keys = pygame.key.get_pressed()# est-ce qu'une touche du clavier est cliquer
    position_souris = pygame.mouse.get_pos()# recuperation de la positon de la souris
    bouton_souris = pygame.mouse.get_pressed()#est-ce qu'un bouton de la souris est cliquer


#################### ## Etat 0 ## ########################

    if état == 0:
        screen.blit(fond_menu,(0,0))
        #initialisation des images des tanks dans le menu:
        if init_partie==0:
            tankvert_f0 = pygame.transform.scale(pygame.image.load("tankvert_f0.png"),(300,300))
            tankbleu_f0 = pygame.transform.scale(pygame.image.load("tankbleu_f0.png"),(300,300))
            tankrouge_f0 = pygame.transform.scale(pygame.image.load("tankrouge_f0.png"),(300,300))
            tankrose_f0 = pygame.transform.scale(pygame.image.load("tankrose_f0.png"),(300,300))
            init_partie=1

        #gestion du choix des tanks pour le joueur n°1 et n°2:
        #derriere le nom des fichier il y a soit "f0,f1,f2" cela correspond a l'état du tank(fissure0,fissure1,fissure2)
        screen.blit(tankvert_f0,(10,150))
        screen.blit(tankrouge_f0,(10,500))
        screen.blit(tankbleu_f0,(1375,150))
        screen.blit(tankrose_f0,(1375,500))
        if position_souris[0] > 10  and position_souris[0] < 260 and position_souris[1] > 150 and position_souris[1] < 400 : # prend la position des tanks en l'occurence "vert" dans ce cas:
            if bouton_souris[0] == 1: # clique gauche de la souris correspond au choix du joueur n°1
                    choix_J1 = 1
                    xJ1 = 160-128 # les coordonnées xJ1 et yJ1 servent a placé l'image "J1" pendant la selection des tanks
                    yJ1 = 250
                    joueur1_choix = pygame.transform.scale(pygame.image.load("tankvert_f0.png"),(100,100))#fait apparaitre lors de la partie le tank du joueur n°1 avec la couleur choisi et avec un etat parfait
                    couleurJ1 = ["tankvert_f0.png","tankvert_f1.png","tankvert_f2.png"]#la liste couleurJ1 sert pour l'etat du tank et sa couleur
            if bouton_souris[2] == 1: # clique droit de la souris correspond au choix du joueur n°2
                    choix_J2 = 1
                    xJ2 = 160-128 # les coordonnées xJ2 et yJ2 servent a placé l'image "J1" pendant la selection des tanks
                    yJ2 = 250
                    joueur2_choix = pygame.transform.scale(pygame.image.load("tankvert_f0.png"),(100,100))#fait apparaitre lors de la partie le tank du joueur n°2 avec la couleur choisi et avec un etat parfait
                    couleurJ2 = ["tankvert_f0.png","tankvert_f1.png","tankvert_f2.png"]#la liste couleurJ2 sert pour l'etat du tank et sa couleur
        if position_souris[0] > 10  and position_souris[0] < 260 and position_souris[1] > 500 and position_souris[1] < 750 :
            if bouton_souris[0] == 1:
                    choix_J1 = 1
                    xJ1 = 160-128
                    yJ1 = 600
                    joueur1_choix = pygame.transform.scale(pygame.image.load("tankrouge_f0.png"),(100,100))
                    couleurJ1 = ["tankrouge_f0.png","tankrouge_f1.png","tankrouge_f2.png"]
            if bouton_souris[2] == 1:
                    choix_J2 = 1
                    xJ2 = 160-128
                    yJ2 = 600
                    joueur2_choix = pygame.transform.scale(pygame.image.load("tankrouge_f0.png"),(100,100))
                    couleurJ2 = ["tankrouge_f0.png","tankrouge_f1.png","tankrouge_f2.png"]
        if position_souris[0] > 1375  and position_souris[0] < 1675 and position_souris[1] > 150 and position_souris[1] < 400 :
            if bouton_souris[0] == 1:
                    choix_J1 = 1
                    xJ1 = 1525-128
                    yJ1 = 250
                    joueur1_choix = pygame.transform.scale(pygame.image.load("tankbleu_f0.png"),(100,100))
                    couleurJ1 = ["tankbleu_f0.png","tankbleu_f1.png","tankbleu_f2.png"]
            if bouton_souris[2] == 1:
                    choix_J2 = 1
                    xJ2 = 1525-128
                    yJ2 = 250
                    joueur2_choix = pygame.transform.scale(pygame.image.load("tankbleu_f0.png"),(100,100))
                    couleurJ2 = ["tankbleu_f0.png","tankbleu_f1.png","tankbleu_f2.png"]
        if position_souris[0] > 1375  and position_souris[0] < 1675 and position_souris[1] > 500 and position_souris[1] < 750 :
            if bouton_souris[0] == 1:
                    choix_J1 = 1
                    xJ1 = 1525-128
                    yJ1 = 600
                    joueur1_choix = pygame.transform.scale(pygame.image.load("tankrose_f0.png"),(100,100))
                    couleurJ1 = ["tankrose_f0.png","tankrose_f1.png","tankrose_f2.png"]
            if bouton_souris[2] == 1:
                    choix_J2 = 1
                    xJ2 = 1525-128
                    yJ2 = 600
                    joueur2_choix = pygame.transform.scale(pygame.image.load("tankrose_f0.png"),(100,100))
                    couleurJ2 = ["tankrose_f0.png","tankrose_f1.png","tankrose_f2.png"]
        if choix_J1 == 1:
            screen.blit(J1,(xJ1,yJ1))
        if choix_J2 == 1:
            screen.blit(J2,(xJ2,yJ2))

        #logo
        screen.blit(logo,(x/2-512,y/2-425))
        #bouton "JOUER" pour lancer une partie
        co_rejouer_x = x/2-256
        co_rejouer_y = y/2+250
        screen.blit(jouer_foncé,(co_rejouer_x,co_rejouer_y))
        if position_souris[0] > co_rejouer_x and position_souris[0] < co_rejouer_x + 512 and position_souris[1] > co_rejouer_y and position_souris[1] < co_rejouer_y + 128 :
            screen.blit(jouer_clair,(co_rejouer_x,co_rejouer_y))
            if choix_J1 ==0 or choix_J2 ==0:#texte "attention" pendant la selection des tanks (ce texte apparait si le joueur n°1 ou le joueur°2 n'a pas selectionnait de tanks)
                screen.blit(attention,(co_rejouer_x + 128 , co_rejouer_y + 100 ))
            if bouton_souris[0] == 1 and choix_J1 == 1 and choix_J2 == 1:# on ne peut donc pas lancer une partie tant que le J1 et J2 n'ont pas choisi de tank:
                état = 1
                init_partie=0
        #bouton "Exit" pour quitter le jeu
        screen.blit(bouton_quitter,(x-(336/2),6))
        if position_souris[0] > x-(336/2) and position_souris[0] < x - 6 and position_souris[1] > 6 and position_souris[1] < 92/2 :
            if bouton_souris[0] == 1:
                pygame.quit()
                exit(0)
        #bouton "Info" pour avoir des informations essentielles au bon déroulement du jeu
        screen.blit(info_foncé,(10,6))
        temps_actuel = time.time()
        if temps_actuel - touche_press >= 1 :
            if position_souris[0] > 10 and position_souris[0] < 320 and position_souris[1] > 6 and position_souris[1] < 78 :
                screen.blit(info_clair,(10,6))
                if bouton_souris[0] == 1:
                    état = 2
                    init_partie=0
                    touche_press = time.time()
            pygame.display.flip()

#################### ## Etat 1 ## ########################

    if état == 1:
        screen.blit(background, (0, 0))
        #initialisation des images des tanks dans la partie ainsi que le nombre de vie des tanks:
        if init_partie==0:
            joueur1 = joueur1_choix
            joueur2 = joueur2_choix
            joueur1 = pygame.transform.rotate(joueur1, -90)
            joueur2 = pygame.transform.rotate(joueur2, 90)
            player_pos1 = pygame.Vector2( 50 ,randint(100,950))
            player_pos2 = pygame.Vector2( 1525,randint(100,950))
            nb_vieJ1 = 3
            nb_vieJ2 = 3
            vitesse_joueur = 3
            vitesse_balle = 5
            nb_vie = 3
            grille2=creer_grille(a3, b3, grille2)
            print(init_partie, grille2)
            init_partie=1
        screen.blit(joueur1,(player_pos1.x,player_pos1.y))
        screen.blit(joueur2,(player_pos2.x,player_pos2.y))

        position2=creer_position_caisse(a3, b3, grille2, position2)


        #bouton "Exit" pour quitter le jeu
        screen.blit(bouton_quitter,(x-(336/2),3))
        if position_souris[0] > x-(336/2) and position_souris[0] < x  and position_souris[1] > 0 and position_souris[1] < 92/2 :
            if bouton_souris[0] == 1:
                pygame.quit()
                exit(0)
        #bouton "Menu" pour quitter le jeu et revenir au menu:
        screen.blit(menu_foncé,(x/2-200,10))
        if position_souris[0] > x/2-200  and position_souris[0] < x/2-200+256 and position_souris[1] > 10 and position_souris[1] < 74 :
            screen.blit(menu_clair,(x/2-200,10))
            if bouton_souris[0] == 1:
                état = 0
                init_partie=0
                newrotationJ1 = 0
                rotationJ1 = -90
                touchepressJ1= 2
                newrotationJ2 = 0
                rotationJ2 = 90
                touchepressJ2 = 3
        #bouton "recommencer" pour arreter la partie en cours est replacer les tanks avec leurs nb de vie au maximum au départs aléatoirement:
        screen.blit(recommencer,(x/2 +50,15))
        if position_souris[0] > x/2 +50  and position_souris[0] < x/2 +100 and position_souris[1] > 15 and position_souris[1] < 65 :
            if bouton_souris[0] == 1:
                état = 1
                init_partie=0

        #partie du programme qui permet de changer l'image du tanks du joueurn °1 suivant son nombre de vie:
        if nb_vieJ2 == 3:
            screen.blit(full_vieJ1,(x/4-360,25))
            if etat_f_J1 == 0:
                joueur1 = pygame.transform.scale(pygame.image.load(couleurJ1[0]),(100,100))
                joueur1 = pygame.transform.rotate(joueur1, -90)
                etat_f_J1 = 1
        if nb_vieJ2 == 2:#nombre de vie restant au tank
            screen.blit(mi_vieJ1,(x/4-360,25))# image du nombre de vie du joueur n°1
            if etat_f_J1 == 1:# cet instruction "if" permet de realiser cet partie une seule fois
                joueur1 = pygame.transform.scale(pygame.image.load(couleurJ1[1]),(100,100))
                joueur1 = pygame.transform.rotate(joueur1, newrotationJ1)#replace l'image du tanks dans le bon sens
                etat_f_J1 = 2
        if nb_vieJ2 == 1:
            screen.blit(pas_de_vieJ1,(x/4-360,25))
            if etat_f_J1 == 2:
                joueur1 = pygame.transform.scale(pygame.image.load(couleurJ1[2]),(100,100))
                joueur1 = pygame.transform.rotate(joueur1, newrotationJ1)
                etat_f_J1 = 0
        #partie du programme qui permet de changer l'image du tanks du joueurn °2 suivant son nombre de vie:
        if nb_vieJ1 == 3:
            screen.blit(full_vieJ2,((x/4)*3,25))
            if etat_f_J2 == 0:
                joueur2 = pygame.transform.scale(pygame.image.load(couleurJ2[0]),(100,100))
                joueur2 = pygame.transform.rotate(joueur2, 90)
                etat_f_J2 =1
        if nb_vieJ1 == 2:
            screen.blit(mi_vieJ2,((x/4)*3,25))
            if etat_f_J2 == 1:
                joueur2 = pygame.transform.scale(pygame.image.load(couleurJ2[1]),(100,100))
                joueur2 = pygame.transform.rotate(joueur2, newrotationJ2)
                etat_f_J2 = 2
        if nb_vieJ1 == 1:
            screen.blit(pas_de_vieJ2,((x/4)*3,25))
            if etat_f_J2 == 2:
                joueur2 = pygame.transform.scale(pygame.image.load(couleurJ2[2]),(100,100))
                joueur2 = pygame.transform.rotate(joueur2, newrotationJ2)
                etat_f_J2 = 0

                 ### Deplacement du joueur n°1 + tir du joueur n°1 ###

        if keys[pygame.K_w]:#deplacement du joueur dans une direction suivant la touche
            player_pos1.y -= vitesse_joueur# vitesse du joueur
            if touchepressJ1 != 0:#permet la rotation du tank suivant sa direction
                touchepressJ1 = 0
                newrotationJ1 = 0
                joueur1 = pygame.transform.rotate(joueur1, newrotationJ1-rotationJ1)
                rotationJ1 = newrotationJ1

        if keys[pygame.K_s]:
            player_pos1.y += vitesse_joueur
            if touchepressJ1 != 1:
                touchepressJ1 = 1
                newrotationJ1 = 180
                joueur1 = pygame.transform.rotate(joueur1, newrotationJ1-rotationJ1)
                rotationJ1 = newrotationJ1

        if keys[pygame.K_a]:
            player_pos1.x -= vitesse_joueur
            if touchepressJ1 != 2:
                touchepressJ1 = 2
                newrotationJ1 = 90
                joueur1 = pygame.transform.rotate(joueur1, newrotationJ1-rotationJ1)
                rotationJ1 = newrotationJ1

        if keys[pygame.K_d]:
            player_pos1.x += vitesse_joueur
            if touchepressJ1 != 3:
                touchepressJ1 = 3
                newrotationJ1 = -90
                joueur1 = pygame.transform.rotate(joueur1, newrotationJ1-rotationJ1 )
                rotationJ1 = newrotationJ1
        # def qui permet au tank de ne pas sortir du cadre
        mur(player_pos1,x,y,vitesse_joueur)

        #def qui empeche le tank de traverser les caisses
        colision_caisse(player_pos1,vitesse_joueur,position2,touchepressJ1)

        #instruction pour les tir du tank
        if keys[pygame.K_q]:
            temps_actuel = time.time()
            if temps_actuel - dernier_tir1 >= 1:
                dernier_tir1 = time.time()
                tir1=1
                if tir1_1 == 0:# ici on recupere les coordonnées du tanks pour les donner a la balle + on place la balle au bout du canon du tank:
                    tir_player1.x = player_pos1.x
                    tir_player1.y = player_pos1.y
                    if touchepressJ1 == 0:
                        angle_vitesse1 = 0
                        tir_player1.x += 37
                        tir_player1.y -=10
                    if touchepressJ1 == 1:
                        angle_vitesse1 = 1
                        tir_player1.x +=37
                        tir_player1.y +=90
                    if touchepressJ1 == 2:
                        angle_vitesse1 = 2
                        tir_player1.x -=10
                        tir_player1.y +=37
                    if touchepressJ1 == 3:
                        angle_vitesse1 = 3
                        tir_player1.x +=90
                        tir_player1.y +=37
                tir1_1=1
        if tir1 == 1 : #je recupere les donnés recoltés au dessus et on les utilise:
            screen.blit(balle_joueur1,(tir_player1.x,tir_player1.y))#place la balle
            if angle_vitesse1 == 0:#direction de la balle
                tir_player1.y -= vitesse_balle#vitesse de la balle
            if angle_vitesse1 == 1:
                tir_player1.y += vitesse_balle
            if angle_vitesse1 == 2:
                tir_player1.x -= vitesse_balle
            if angle_vitesse1 == 3:
                tir_player1.x += vitesse_balle
            if tir_player1.y > y -15 or tir_player1.x > x -15 or tir_player1.y < 0 or tir_player1.x < 0:# est ce que la balle a touché un mur
                tir1=0
                tir1_1=0
            tir1, tir1_1=colision_caisse_balle(tir_player1, position2, tir1, tir1_1)

            #co_impact = tir_player1
            if tir_player1.x > player_pos2.x and tir_player1.x < player_pos2.x + 95 and tir_player1.y > player_pos2.y and tir_player1.y < player_pos2.y + 95: #est ce que la balle a touché le joueur n°2
                tir1 = 0
                tir1_1 = 0
                nb_vieJ1 -= 1
            # on regarde si le joueur n°1 a encore des vie
            if nb_vieJ1 == nb_vie_perdu:
                état = 3
                init_partie=0

            ### Deplacement du joueur n°2 + tir du joueur n°2 ### [ici tout est comme pour le joueur n°1 mais avec de nouvelle variables]

        if keys[pygame.K_UP]:
            player_pos2.y -= vitesse_joueur
            if touchepressJ2 != 0:
                touchepressJ2 = 0
                newrotationJ2 = 0
                joueur2 = pygame.transform.rotate(joueur2, newrotationJ2-rotationJ2)
                rotationJ2 = newrotationJ2

        if keys[pygame.K_DOWN]:
            player_pos2.y += vitesse_joueur
            if touchepressJ2 != 1:
                touchepressJ2 = 1
                newrotationJ2 = 180
                joueur2 = pygame.transform.rotate(joueur2, newrotationJ2-rotationJ2)
                rotationJ2 = newrotationJ2

        if keys[pygame.K_LEFT]:
            player_pos2.x -= vitesse_joueur
            if touchepressJ2 != 2:
                touchepressJ2 = 2
                newrotationJ2 = 90
                joueur2 = pygame.transform.rotate(joueur2, newrotationJ2-rotationJ2)
                rotationJ2 = newrotationJ2

        if keys[pygame.K_RIGHT]:
            player_pos2.x += vitesse_joueur
            if touchepressJ2 != 3:
                touchepressJ2 = 3
                newrotationJ2 = -90
                joueur2 = pygame.transform.rotate(joueur2, newrotationJ2-rotationJ2 )
                rotationJ2 = newrotationJ2


        mur(player_pos2,x,y,vitesse_joueur)
        colision_caisse(player_pos2,vitesse_joueur,position2,touchepressJ2)


        if keys[pygame.K_RCTRL]:
            temps_actuel = time.time()
            if temps_actuel - dernier_tir2 >= 1:
                dernier_tir2 = time.time()
            tir2=1
            if tir2_1 == 0:
                tir_player2.x = player_pos2.x
                tir_player2.y = player_pos2.y
                if touchepressJ2 == 0:
                    angle_vitesse2 = 0
                    tir_player2.x += 37
                    tir_player2.y -=10
                if touchepressJ2 == 1:
                    angle_vitesse2 = 1
                    tir_player2.x +=37
                    tir_player2.y +=90
                if touchepressJ2 == 2:
                    angle_vitesse2 = 2
                    tir_player2.x -=10
                    tir_player2.y +=37
                if touchepressJ2 == 3:
                    angle_vitesse2 = 3
                    tir_player2.x +=90
                    tir_player2.y +=37
                tir2_1=1
        if tir2 == 1 :
            screen.blit(balle_joueur2,(tir_player2.x,tir_player2.y))
            if angle_vitesse2 == 0:
                tir_player2.y -= vitesse_balle
            if angle_vitesse2 == 1:
                tir_player2.y += vitesse_balle
            if angle_vitesse2 == 2:
                tir_player2.x -= vitesse_balle
            if angle_vitesse2 == 3:
                tir_player2.x += vitesse_balle
            if tir_player2.y > y -15 or tir_player2.x > x -15 or tir_player2.y < 0 or tir_player2.x < 0:
                tir2=0
                tir2_1=0
            tir2, tir2_1=colision_caisse_balle(tir_player2, position2, tir2, tir2_1)
            if tir_player2.x > player_pos1.x and tir_player2.x < player_pos1.x + 95 and tir_player2.y > player_pos1.y and tir_player2.y < player_pos1.y + 95:
                tir2 = 0
                tir2_1 = 0
                nb_vieJ2 -= 1
            if nb_vieJ2 == nb_vie_perdu:
                état = 4
                init_partie=0

        pygame.display.flip()

#################### ## Etat 2 ## ########################
# affichage des infos
    if état == 2:
        screen.blit(fond_info,(0,0))
        #bouton "Exit" pour quitter le jeu
        screen.blit(bouton_quitter,(x-(336/2),6))
        if position_souris[0] > x-(336/2) and position_souris[0] < x - 6 and position_souris[1] > 6 and position_souris[1] < 92/2 :
            if bouton_souris[0] == 1:
                pygame.quit()
                exit(0)
        #bouton "retour" pour quitter le jeu
        temps_actuel = time.time()
        screen.blit(fleche_retour,(10,10))
        if temps_actuel - touche_press >=1 :
            if position_souris[0] > 10 and position_souris[0] < 100 and position_souris[1] > 10 and position_souris[1] < 100 :
                if bouton_souris[0] == 1:
                    état=0
                    init_partie=0
                    touche_press = time.time()

        pygame.display.flip()

#################### ## Etat 3 ## ########################
# victoire joueur 1
    if état == 3:
        co_rejouer_x = x/2-256
        co_rejouer_y = y/2+250
        screen.blit(fond_victoire,(0,0))#fond du menu de victoire
        if init_partie==0:
            joueur1 = pygame.transform.scale(pygame.image.load(couleurJ1[0]),(500,500))
            init_partie=1
        screen.blit(win_J1,(x/2-512,y/4-177))#titre si le gagnant est le joueur n°1 ou le joueur n°2
        screen.blit(joueur1,(x/2-250,y/2-260))#affichage du tank avec la bonne couleur
        #bouton "rejouer" pour relancer une partie
        screen.blit(rejouer_foncé,(co_rejouer_x,co_rejouer_y))
        if position_souris[0] > co_rejouer_x and position_souris[0] < co_rejouer_x + 512 and position_souris[1] > co_rejouer_y and position_souris[1] < co_rejouer_y + 128 :
            screen.blit(rejouer_clair,(co_rejouer_x,co_rejouer_y))
            if bouton_souris[0] == 1:
                état = 0
                init_partie=0
                newrotationJ1 = 0
                rotationJ1 = -90
                touchepressJ1= 2
                newrotationJ2 = 0
                rotationJ2 = 90
                touchepressJ2 = 3
        #bouton "menu" pour retourner au menu
        screen.blit(menu_foncé,(20,10))
        if position_souris[0] > 20  and position_souris[0] < 20+256 and position_souris[1] > 10 and position_souris[1] < 74 :
            screen.blit(menu_clair,(20,10))
            if bouton_souris[0] == 1:
                état = 0
                init_partie=0
                newrotationJ1 = 0
                rotationJ1 = -90
                touchepressJ1= 2
                newrotationJ2 = 0
                rotationJ2 = 90
                touchepressJ2 = 3
                touche_press = time.time()
        #bouton "quitter" pour quitter le jeu
        screen.blit(bouton_quitter,(x-(336/2),6))
        if position_souris[0] > x-(336/2) and position_souris[0] < x - 6 and position_souris[1] > 6 and position_souris[1] < 92/2 :
            if bouton_souris[0] == 1:
                pygame.quit()
                exit(0)

        pygame.display.flip()

#################### ## Etat 4 ## ######################## (exactement comme dans l'état 3 mais pour le joueur n°2 )
# victoire joueur 2
    if état == 4:
        co_rejouer_x = x/2-256
        co_rejouer_y = y/2+250
        screen.blit(fond_victoire,(0,0))
        if init_partie==0:
            joueur2 = pygame.transform.scale(pygame.image.load(couleurJ2[0]),(500,500))
            init_partie=1
        screen.blit(win_J2,(x/2-512,y/4-177))
        screen.blit(joueur2,(x/2-250,y/2-260))
        screen.blit(rejouer_foncé,(co_rejouer_x,co_rejouer_y))
        if position_souris[0] > co_rejouer_x and position_souris[0] < co_rejouer_x + 512 and position_souris[1] > co_rejouer_y and position_souris[1] < co_rejouer_y + 128 :
            screen.blit(rejouer_clair,(co_rejouer_x,co_rejouer_y))
            if bouton_souris[0] == 1:
                état = 0
                init_partie=0
                newrotationJ1 = 0
                rotationJ1 = -90
                touchepressJ1= 2
                newrotationJ2 = 0
                rotationJ2 = 90
                touchepressJ2 = 3

        screen.blit(menu_foncé,(20,10))
        if position_souris[0] > 20  and position_souris[0] < 20+256 and position_souris[1] > 10 and position_souris[1] < 74 :
            screen.blit(menu_clair,(20,10))
            if bouton_souris[0] == 1:
                état = 0
                init_partie=0
                newrotationJ1 = 0
                rotationJ1 = -90
                touchepressJ1= 2
                newrotationJ2 = 0
                rotationJ2 = 90
                touchepressJ2 = 3
                touche_press = time.time()

        screen.blit(bouton_quitter,(x-(336/2),6))
        if position_souris[0] > x-(336/2) and position_souris[0] < x - 6 and position_souris[1] > 6 and position_souris[1] < 92/2 :
            if bouton_souris[0] == 1:
                pygame.quit()
                exit(0)

        pygame.display.flip()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()


