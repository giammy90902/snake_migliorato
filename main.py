import pygame
import random
import sys

# Inizializzazione Pygame
pygame.init()

# Impostazioni dello schermo
larghezza_schermo = 600
altezza_schermo = 600
schermo = pygame.display.set_mode((larghezza_schermo, altezza_schermo))
pygame.display.set_caption("Snake modificato by giammy")

# Colori
nero = (0, 0, 0)
verde_scuro = (0, 100, 0)
rosso_scuro = (0, 0, 0)
bianco = (255, 255, 255)

# Font
font = pygame.font.SysFont(None, 30)

# Variabili di gioco
direzione = None
cambio_direzione = None
mele_mangiate = 0
lunghezza_blocco = 1
blocchi = []
testa_blocco = [0, 0]
dimensione_blocco = 1
posizione_mela = [0, 0]
posizione_mela_precedente = [0, 0]

# Variabile di fine partita
fine_partita = False

# Variabile di difficoltà
difficolta = 'normale'

# Velocità iniziale del blocco
velocita_blocco = 1
velocita_normale = 1  # Velocità normale

# Dizionari delle immagini
mela_imgs = {}
testa_img = None
corpo_img = None

# Variabile per l'username
username = ""

def disegna_griglia():
    for x in range(0, larghezza_schermo, dimensione_blocco):
        for y in range(0, altezza_schermo, dimensione_blocco):
            rect = pygame.Rect(x, y, dimensione_blocco, dimensione_blocco)
            pygame.draw.rect(schermo, verde_scuro, rect, 1)

def mostra_menu_dimensione_blocco():
    global dimensione_blocco
    menu = True

    while menu:
        schermo.fill(nero)
        mostra_testo("Scegli la dimensione della griglia di gioco:", bianco, -50)
        mostra_testo("1. Piccolo (150)", bianco, -10)
        mostra_testo("2. Medio (100)", bianco, 20)
        mostra_testo("3. Grande (60)", bianco, 50)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    dimensione_blocco = 150
                    menu = False
                if evento.key == pygame.K_2:
                    dimensione_blocco = 100
                    menu = False
                if evento.key == pygame.K_3:
                    dimensione_blocco = 60
                    menu = False

def mostra_menu_difficolta():
    global difficolta
    menu = True

    while menu:
        schermo.fill(nero)
        mostra_testo("Scegli la difficoltà:", bianco, -50)
        mostra_testo("1. Normale", bianco, -10)
        mostra_testo("2. Difficile", bianco, 20)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    difficolta = 'normale'
                    menu = False
                if evento.key == pygame.K_2:
                    difficolta = 'difficile'
                    menu = False

def fine_gioco():
    global fine_partita
    fine_partita = True

    while True:
        schermo.fill(nero)
        mostra_testo(f"HAI PERSO {username}!".upper(), bianco, 0)
        mostra_testo(f"Mele Mangiate: {mele_mangiate}", bianco, -(altezza_schermo // 2 - 30))
        mostra_testo("Premi 'R' per riprovare o 'ESC' per uscire.", bianco, 30)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    fine_partita = False
                    main()
                    return
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def schermata_vittoria():
    global fine_partita
    fine_partita = True

    while True:
        schermo.fill(nero)
        mostra_testo(f"HAI VINTO {username}!".upper(), bianco, 0)
        mostra_testo(f"Mele Mangiate: {mele_mangiate}", bianco, -(altezza_schermo // 2 - 30))
        mostra_testo("Premi 'R' per riprovare o 'ESC' per uscire.", bianco, 30)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    fine_partita = False
                    main()
                    return
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def reset_game():
    global direzione, cambio_direzione, mele_mangiate, lunghezza_blocco, blocchi, testa_blocco, posizione_mela, velocita_blocco, difficolta, testa_img, corpo_img, dimensione_mela, posizione_mela_precedente, velocita_normale
    direzione = None
    cambio_direzione = None
    mele_mangiate = 0
    lunghezza_blocco = 1
    blocchi = []
    testa_blocco = [larghezza_schermo // 2 // dimensione_blocco * dimensione_blocco, altezza_schermo // 2 // dimensione_blocco * dimensione_blocco]
    blocchi.append(list(testa_blocco))
    posizione_mela_precedente = [0, 0]
    posizione_mela = genera_posizione_mela()
    dimensione_mela = dimensione_blocco
    if difficolta == 'normale':
        velocita_blocco = 1
        velocita_normale = 1  # Impostiamo la velocità normale
    elif difficolta == 'difficile':
        velocita_blocco = 5
        velocita_normale = 5  # Impostiamo la velocità normale

def carica_immagini():
    global mela_imgs, testa_img, corpo_img
    try:
        testa_img = pygame.image.load('testa.png')
        corpo_img = pygame.image.load('corpo.png')
        mela_imgs[60] = pygame.image.load('mela.png')
        mela_imgs[100] = pygame.image.load('mela.png')
        mela_imgs[150] = pygame.image.load('mela.png')
    except pygame.error as e:
        print(f"Errore nel caricamento delle immagini: {e}")
        pygame.quit()
        sys.exit()

def mostra_testo(testo, colore, y_offset=0):
    testo_renderizzato = font.render(testo, True, colore)
    testo_rett = testo_renderizzato.get_rect(center=(larghezza_schermo // 2, altezza_schermo // 2 + y_offset))
    schermo.blit(testo_renderizzato, testo_rett)

def mostra_punteggio():
    punteggio = font.render(f"Mele Mangiate: {mele_mangiate}", True, bianco)
    schermo.blit(punteggio, [0, 0])

def genera_posizione_mela():
    global posizione_mela_precedente
    liberi = [
        [x * dimensione_blocco, y * dimensione_blocco]
        for x in range(larghezza_schermo // dimensione_blocco)
        for y in range(altezza_schermo // dimensione_blocco)
        if [x * dimensione_blocco, y * dimensione_blocco] not in blocchi and [x * dimensione_blocco, y * dimensione_blocco] != posizione_mela_precedente
    ]

    if not liberi:
        schermata_vittoria()

    posizione = random.choice(liberi)
    posizione_mela_precedente = posizione
    return posizione

def ottieni_username():
    global username
    input_attivo = True
    username = ""
    clock = pygame.time.Clock()

    while input_attivo:
        schermo.fill(nero)
        mostra_testo("Inserisci il tuo username:", bianco, -30)
        mostra_testo(username, bianco, 10)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    input_attivo = False
                elif evento.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += evento.unicode

def main():
    global direzione, cambio_direzione, mele_mangiate, lunghezza_blocco, blocchi, testa_blocco, posizione_mela, velocita_blocco, dimensione_mela, fine_partita, velocita_normale

    try:
        carica_immagini()
        ottieni_username()
        mostra_menu_dimensione_blocco()
        mostra_menu_difficolta()
        reset_game()

        clock = pygame.time.Clock()

        while not fine_partita:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP and direzione != 'GIU':
                        cambio_direzione = 'SU'
                    if evento.key == pygame.K_DOWN and direzione != 'SU':
                        cambio_direzione = 'GIU'
                    if evento.key == pygame.K_LEFT and direzione != 'DESTRA':
                        cambio_direzione = 'SINISTRA'
                    if evento.key == pygame.K_RIGHT and direzione != 'SINISTRA':
                        cambio_direzione = 'DESTRA'
                    if evento.key == pygame.K_SPACE:
                        if difficolta == 'normale':
                            velocita_blocco = 2
                        elif difficolta == 'difficile':
                            velocita_blocco = 15
                    if direzione is None:
                        direzione = cambio_direzione
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_SPACE:
                        velocita_blocco = velocita_normale

            if direzione is not None:
                if cambio_direzione == 'SU':
                    nuova_testa = [testa_blocco[0], testa_blocco[1] - dimensione_blocco]
                if cambio_direzione == 'GIU':
                    nuova_testa = [testa_blocco[0], testa_blocco[1] + dimensione_blocco]
                if cambio_direzione == 'SINISTRA':
                    nuova_testa = [testa_blocco[0] - dimensione_blocco, testa_blocco[1]]
                if cambio_direzione == 'DESTRA':
                    nuova_testa = [testa_blocco[0] + dimensione_blocco, testa_blocco[1]]
                direzione = cambio_direzione

                if nuova_testa[0] < 0 or nuova_testa[0] >= larghezza_schermo or nuova_testa[1] < 0 or nuova_testa[1] >= altezza_schermo:
                    fine_gioco()

                if nuova_testa == posizione_mela:
                    mele_mangiate += 1
                    lunghezza_blocco += 1
                    posizione_mela = genera_posizione_mela()
                else:
                    blocchi.pop(0)

                blocchi.append(nuova_testa)
                testa_blocco = nuova_testa

                if difficolta == 'difficile':
                    for blocco in blocchi[:-1]:
                        if blocco == testa_blocco:
                            fine_gioco()

            schermo.fill(nero)
            disegna_griglia()
            mostra_punteggio()

            for i, segmento in enumerate(blocchi):
                if i == len(blocchi) - 1:
                    schermo.blit(pygame.transform.scale(testa_img, (dimensione_blocco, dimensione_blocco)), segmento)
                else:
                    schermo.blit(pygame.transform.scale(corpo_img, (dimensione_blocco, dimensione_blocco)), segmento)

            schermo.blit(pygame.transform.scale(mela_imgs[dimensione_mela], (dimensione_blocco, dimensione_blocco)), posizione_mela)
            pygame.display.update()

            if direzione is not None:
                clock.tick(velocita_blocco)
    except Exception as e:
        print(f"Errore: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()