import pygame
import random
import requests
import numpy as np
from io import BytesIO

pygame.display.set_caption("Taquing")

# Cette partie crée une grille de taquin à partir de la grille résolue en effectuant 100 déplacements aléatoirement

DIRECTIONS = [(0,1),(0,-1),(1,0),(-1,0)]

def neighbors(node): #node=tuple avec case vide égale à 0
    index_case_vide = node.index(9)
    i_vide, j_vide = index_case_vide//3, index_case_vide%3
    l=[]
    for i in range(len(DIRECTIONS)):
        direction = DIRECTIONS[i]
        new_tuple_l = list(node)
        if direction[1] == 0: #mouvement horizontal
            if 0 <= j_vide + direction[0] <= 2:
                new_tuple_l[index_case_vide] = node[index_case_vide+direction[0]]
                new_tuple_l[index_case_vide+direction[0]] = 9
                l.append(tuple(new_tuple_l))
        
        elif direction[0] == 0: #mouvement vertical
            if 0 <= i_vide + direction[1] <= 2:
                new_tuple_l[index_case_vide] = node[index_case_vide+direction[1]*3]
                new_tuple_l[index_case_vide+direction[1]*3] = 9
                l.append(tuple(new_tuple_l))
    
    return l

def random_board(nine=False):
    pos=(1,2,3,4,5,6,7,8,9)
    for _ in range(100):
        voisins = neighbors(pos)
        i=random.randint(0, len(voisins)-1)
        pos=voisins[i]
    arr = np.array(pos).reshape((3,3))
    if not nine: 
        arr = np.where(arr == 9, 0, arr)
        return arr.tolist()
    else:
        return arr

# Cette partie prend en entrée une grille, effectue un déplacement dans le but de se rapprocher de la victoire et renvoie la grille

def cout_hamming(noeud):
    somme = 0
    for i in range(len(noeud)):
        if noeud[i] != i+1:
            somme += 1
    return somme

def hamming_pouxchiant(starting_node):
    queue = [starting_node]
    path = {starting_node : [starting_node]}
    compteur = 0
    while queue != [] and compteur <= 5000:
        compteur += 1
        sommet = queue[0]
        del queue[0]
        voisins = neighbors(sommet)
        chemin = path[sommet]
        for voisin in voisins:
            if voisin == (1,2,3,4,5,6,7,8,9):
                chemin += [voisin]
                hint = list(chemin[1])
                for i in range(len(hint)):
                    if hint[i] == 9:
                        hint[i] = 0
                        break
                return [[hint[0],hint[1],hint[2]],[hint[3],hint[4],hint[5]],[hint[6],hint[7],hint[8]]]
            elif voisin not in path:
                cout_voisin = cout_hamming(voisin)
                place = False
                for i in range(len(queue)):
                    if cout_voisin < cout_hamming(queue[i]):
                        queue = queue[:i]+[voisin]+queue[i:]
                        place = True
                        break
                if place == False:
                    queue.append(voisin)
                path[voisin] = chemin + [voisin]
    return "pas de solus"

# On télécharge des images à l'aide d'url

def charger_image(url):
    reponse = requests.get(url)
    image = pygame.image.load(BytesIO(reponse.content))
    return image

grille = charger_image('https://is5-ssl.mzstatic.com/image/thumb/Purple128/v4/57/81/f4/5781f434-90a8-29ac-8cb4-fdf90142b5ef/source/512x512bb.jpg')
grillevide= charger_image("https://i.ibb.co/7yMdhJx/512x512bbv3.jpg")
un = charger_image('https://i.ibb.co/JtswBxR/output-onlinepngtools-2.png')
deux= charger_image("https://i.ibb.co/NyYKKxf/output-onlinepngtools-3.png")
trois= charger_image("https://i.ibb.co/58mkFXs/3.png")
quatre= charger_image("https://i.ibb.co/cg7vCZf/4.png")
cinq = charger_image("https://i.ibb.co/hVBtPQP/output-onlinepngtools.png")
six=charger_image("https://i.ibb.co/0DbQKk6/6.png")
sept= charger_image("https://i.ibb.co/FgWhpKk/7.png")
huit= charger_image("https://i.ibb.co/0cpNnGB/8.png")
image_victoire = charger_image('https://i.ibb.co/Jnj3gsW/VICTOIRE.png')

# on associe à chaque chiffre une image
images={1: un, 2: deux, 3: trois, 4: quatre, 5: cinq, 6: six, 7: sept, 8: huit}

# on note dans un dictionnaire la position des cases dans la fenêtre
cases = {1: (50, 50), 2: (190, 50), 3: (330, 50), 4: (50,190), 5: (190, 190), 6: (330, 190), 7: (50, 330), 8: (190, 330), 9: (330, 330)}

# on crée une grille de départ et la grille résolue
matvic = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
matchif = random_board()

# on trouve la position du zéro dans la grille de départ
def zero(matchif):
    for i in range(3):
        for j in range(3):
            if matchif[i][j]==0:
                return j,i

x0,y0=zero(matchif)



# Initialisation
# on définit des paramètres et des booléens pour créer des boutons

pygame.init()
screen = pygame.display.set_mode((512, 512))
clock = pygame.time.Clock()
menu = True
jeu = False
pause = False
victoire = False
settings = True
credits = False
en_cours = True
blanc = (255, 255, 255)
noir = (0, 0, 0)
marron = (131, 75, 14)
couleur_bouton = marron

# Définir la police
police = pygame.font.Font(None, 36)
policecredit = pygame.font.Font(None, 50)
policetitre = pygame.font.Font(None, 80)

# Définir les propriétés des boutons

bouton_Start = pygame.Rect(154, 220, 200, 40)
contour_Start = pygame.Rect(150, 216, 208, 48)
texte_bouton_Start = police.render("Start", True, noir)
rect_texte_Start = texte_bouton_Start.get_rect(center=(254, 238))

boutoncredit = pygame.Rect(154, 360, 200, 40)
contour_credit = pygame.Rect(150, 356, 208, 48)
texte_bouton2 = police.render("Credits", True, noir)
rect_texte2 = texte_bouton2.get_rect(center=(250, 378))

bouton_settings = pygame.Rect(154, 290, 200, 40)
contour_settings = pygame.Rect(150, 286, 208, 48)
texte_bouton3 = police.render("Settings", True, noir)
rect_texte3 = texte_bouton3.get_rect(center=(256, 308))

bouton_non = pygame.Rect(154, 290, 200, 40)
contour_non = pygame.Rect(150, 286, 208, 48)
texte_boutonnon = police.render("Non", True, noir)
rect_textenon = texte_boutonnon.get_rect(center=(256, 308))

bouton_titre = pygame.Rect(106, 84, 300, 60)
contour_titre = pygame.Rect(100, 80, 312, 68)
texte_bouton4 = policetitre.render("Taquing", True, noir)
rect_texte4 = texte_bouton4.get_rect(center=(250, 114))

bouton_hint = pygame.Rect(364, 8, 100, 30)
contour_hint = pygame.Rect(360, 4, 108, 38)
texte_bouton_hint = police.render("Hint", True, noir)
rect_texte_hint = texte_bouton_hint.get_rect(center=bouton_hint.center)

bouton_pause = pygame.Rect(60, 8, 100, 30)
contour_pause = pygame.Rect(56, 4, 108, 38)
texte_bouton_pause = police.render("Pause", True, noir)
rect_texte_pause = texte_bouton_pause.get_rect(center=bouton_pause.center)

bouton_resume = pygame.Rect(154, 220, 200, 40)
contour_resume = pygame.Rect(150, 216, 208, 48)
texte_bouton_resume = police.render("Resume", True, noir)
rect_texte_resume = texte_bouton_resume.get_rect(center=bouton_resume.center)

bouton_menu=pygame.Rect(364, 464, 100, 40)
contour_menu = pygame.Rect(360, 460, 108, 48)
texte_menu = police.render("Menu", True, noir)
rect_txt_menu = texte_menu.get_rect(center=bouton_menu.center)
        
# la boucle du jeu

while en_cours:
    clock.tick(800)
    # On récupère les évènements, il y en a deux types.
    # Ce sont soit des boutons qui sont cliqués et dans ce cas la valeur de certains booléens changent
    # Soit on a appuyé sur une flèche directionnelle, par exemple la flèche du haut, dans ce cas on échange la case vide avec celle en-dessous

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        if jeu and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y0 < 2 :
                matchif[y0][x0], matchif[y0 + 1][x0] = matchif[y0 + 1][x0], matchif[y0][x0]
                y0 += 1
            if event.key == pygame.K_DOWN and y0 > 0:
                matchif[y0][x0], matchif[y0 - 1][x0] = matchif[y0 - 1][x0], matchif[y0][x0]
                y0 -=1
            if event.key == pygame.K_LEFT and x0 < 2:
                matchif[y0][x0], matchif[y0][x0 + 1] = matchif[y0][x0 + 1], matchif[y0][x0]
                x0 += 1
            if event.key == pygame.K_RIGHT and x0 > 0:
                matchif[y0][x0], matchif[y0][x0 - 1] = matchif[y0][x0 - 1], matchif[y0][x0]
                x0 -= 1          
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu:
                if bouton_Start.collidepoint(event.pos):
                    menu = False
                    temps_debut = pygame.time.get_ticks()
                    jeu = True
                if boutoncredit.collidepoint(event.pos): 
                    menu = False
                    credits = True
                if bouton_settings.collidepoint(event.pos):
                    settings = False
            if credits:
                if bouton_menu.collidepoint(event.pos):
                    menu = True
                    credits = False
                    settings = True
            if jeu:
                if bouton_pause.collidepoint(event.pos):
                    jeu = False
                    pause = True
                if bouton_hint.collidepoint(event.pos):
                    board=np.array(matchif)
                    matchif=np.where(board == 0, 9, board)
                    matchif = hamming_pouxchiant(tuple(matchif.reshape((1,9)).tolist()[0]))
                    x0,y0 = zero(matchif)
            if pause:
                if bouton_resume.collidepoint(event.pos):
                    jeu = True
                    pause = False
                    temps_pause = temps_actuel - temps_ecoule - temps_debut
                    temps_debut = temps_debut + temps_pause
            if victoire:
                if bouton_menu.collidepoint(event.pos):
                    menu = True
                    settings = True
                    victoire= False
                    matchif = random_board()
                    x0,y0=zero(matchif)
                    
    # Ce qu'on affiche dans la fenêtre dépend de la valeur des booléens
    if menu:
        screen.blit(grille, (0, 0))
        pygame.draw.rect(screen, noir, contour_credit)
        pygame.draw.rect(screen, noir, contour_Start)
        pygame.draw.rect(screen, noir, contour_settings)
        pygame.draw.rect(screen, noir, contour_titre)
        pygame.draw.rect(screen, couleur_bouton, bouton_settings)
        pygame.draw.rect(screen, couleur_bouton, boutoncredit)
        pygame.draw.rect(screen, couleur_bouton, bouton_titre)
        pygame.draw.rect(screen, couleur_bouton, bouton_Start)
        screen.blit(texte_bouton3, rect_texte3)
        screen.blit(texte_bouton_Start, rect_texte_Start)
        screen.blit(texte_bouton2, rect_texte2)
        screen.blit(texte_bouton4, rect_texte4)
        if not settings:
            pygame.draw.rect(screen, noir, contour_settings)
            pygame.draw.rect(screen, couleur_bouton, bouton_non)
            screen.blit(texte_boutonnon, rect_textenon)


    if jeu:
        screen.blit(grillevide, (0, 0))
        temps_actuel = pygame.time.get_ticks()
        temps_ecoule = temps_actuel - temps_debut
        temps_ecoule_secondes = temps_ecoule // 1000
        texte_temps = police.render(f"Temps écoulé : {temps_ecoule_secondes} s", True, (0, 0, 0))
        rect_texte = texte_temps.get_rect(center=(170, 485))
        screen.blit(texte_temps, rect_texte)
        pygame.draw.rect(screen, noir, contour_hint)
        pygame.draw.rect(screen, couleur_bouton, bouton_hint)
        screen.blit(texte_bouton_hint, rect_texte_hint)
        pygame.draw.rect(screen, noir, contour_pause)
        pygame.draw.rect(screen, couleur_bouton, bouton_pause)
        screen.blit(texte_bouton_pause, rect_texte_pause)
        
        for i in range(0,3):
            for j in range(0,3):
                if matchif[i][j] != 0:
                    screen.blit(images[matchif[i][j]], cases[j+1+i*3])
                    
    if pause:
        screen.blit(grille, (0, 0))
        temps_actuel = pygame.time.get_ticks()
        pygame.draw.rect(screen, noir, contour_resume)
        pygame.draw.rect(screen, couleur_bouton, bouton_resume)
        screen.blit(texte_bouton_resume, rect_texte_resume)
        texte_temps = police.render(f"Temps écoulé : {temps_ecoule_secondes} s", True, (0, 0, 0))
        rect_texte = texte_temps.get_rect(center=(170, 485))
        screen.blit(texte_temps, rect_texte)

    if matchif == matvic and jeu:
        victoire = True
        jeu = False
    
    if victoire:
        screen.blit(image_victoire, (0,0))
        pygame.draw.rect(screen, noir, contour_menu)
        pygame.draw.rect(screen, couleur_bouton, bouton_menu)
        screen.blit(texte_menu, rect_txt_menu)
        texte_temps = police.render(f"Temps écoulé : {temps_ecoule_secondes} s", True, blanc)
        rect_texte = texte_temps.get_rect(center=(170, 485))
        screen.blit(texte_temps, rect_texte)
        
    if credits:
        screen.blit(grillevide, (0,0))
        ligne1 = "Avec la participation de :"
        ligne1_surface = policecredit.render(ligne1, True, (0, 0, 0))
        ligne1_rect = ligne1_surface.get_rect(center=(244, 64))
        ligne2 = "Kylian Mbappé"
        ligne2_surface = policecredit.render(ligne2, True, (0, 0, 0))
        ligne2_rect = ligne2_surface.get_rect(center=(244, 104))
        ligne3 = "ChatGPT"
        ligne3_surface = policecredit.render(ligne3, True, (0, 0, 0))
        ligne3_rect = ligne3_surface.get_rect(center=(244, 144))
        ligne4 = "Les Sandwichs"
        ligne4_surface = policecredit.render(ligne4, True, (0, 0, 0))
        ligne4_rect = ligne4_surface.get_rect(center=(244, 184))
        ligne5 = "Raphaël Poux"
        ligne5_surface = policecredit.render(ligne5, True, (0, 0, 0))
        ligne5_rect = ligne5_surface.get_rect(center=(244, 224))
        ligne6 = "Titouan Lestanguet"
        ligne6_surface = policecredit.render(ligne6, True, (0, 0, 0))
        ligne6_rect = ligne6_surface.get_rect(center=(244, 264))
        ligne7 = "Antoine Fondeur"
        ligne7_surface = policecredit.render(ligne7, True, (0, 0, 0))
        ligne7_rect = ligne7_surface.get_rect(center=(244, 304))
        ligne8 = "Baptiste Piar"
        ligne8_surface = policecredit.render(ligne8, True, (0, 0, 0))
        ligne8_rect = ligne8_surface.get_rect(center=(244, 344))
        ligne9 = "Sponsor: Taha"
        ligne9_surface = policecredit.render(ligne9, True, (0, 0, 0))
        ligne9_rect = ligne9_surface.get_rect(center=(244, 384))
        ligne10 = "Valérie Roy"
        ligne10_surface = policecredit.render(ligne10, True, (0, 0, 0))
        ligne10_rect = ligne10_surface.get_rect(center=(244, 424))
        ligne11 = "Flash Mcqueen "
        ligne11_surface = policecredit.render(ligne11, True, (0, 0, 0))
        ligne11_rect = ligne11_surface.get_rect(center=(244, 464))
        screen.blit(ligne1_surface, ligne1_rect)
        screen.blit(ligne2_surface, ligne2_rect)
        screen.blit(ligne3_surface, ligne3_rect)
        screen.blit(ligne4_surface, ligne4_rect)
        screen.blit(ligne5_surface, ligne5_rect)
        screen.blit(ligne6_surface, ligne6_rect)
        screen.blit(ligne7_surface, ligne7_rect)
        screen.blit(ligne8_surface, ligne8_rect)
        screen.blit(ligne9_surface, ligne9_rect)
        screen.blit(ligne10_surface, ligne10_rect)
        screen.blit(ligne11_surface, ligne11_rect)
        pygame.draw.rect(screen, noir, contour_menu)
        pygame.draw.rect(screen, couleur_bouton, bouton_menu)
        screen.blit(texte_menu, rect_txt_menu)
        
    
    pygame.display.update()
        
pygame.quit()
