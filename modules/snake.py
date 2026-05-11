import pygame
import random

pygame.init()
pygame.display.set_caption("Snake Eater")

largura, altura = 600, 500
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

preta = (0, 0, 0)
branca = (255, 255, 255)
verde = (0, 255, 0)
verde_claro = (144, 238, 144)
verde_escuro = (34, 139, 34)
azul_escuro = (0, 0, 139)
vermelho = (255, 0, 0)
laranja = (255, 165, 0)
ovo = (230, 220, 140)

tamanho_quadrado = 10
velocidade_jogo = 13

def gerar_comida(pixels):
    while True:
        comida_x = random.randrange(0, largura - tamanho_quadrado + 1, tamanho_quadrado)
        comida_y = random.randrange(0, altura - tamanho_quadrado + 1, tamanho_quadrado)
        if [comida_x, comida_y] not in pixels:
            return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, ovo, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, azul_escuro, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontos):
    fonte = pygame.font.SysFont("Helvetica", 25)
    texto = fonte.render(f"pontos: {pontos}", True, vermelho)
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla, velocidade_x, velocidade_y):
    proxima_velocidade_x, proxima_velocidade_y = velocidade_x, velocidade_y

    if tecla == pygame.K_s:
        proxima_velocidade_x = 0
        proxima_velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_w:
        proxima_velocidade_x = 0
        proxima_velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_d:
        proxima_velocidade_x = tamanho_quadrado
        proxima_velocidade_y = 0
    elif tecla == pygame.K_a:
        proxima_velocidade_x = -tamanho_quadrado
        proxima_velocidade_y = 0

    if (proxima_velocidade_x == -velocidade_x and proxima_velocidade_y == -velocidade_y) and (velocidade_x != 0 or velocidade_y != 0):
        return velocidade_x, velocidade_y

    return proxima_velocidade_x, proxima_velocidade_y

def mostrar_menu():
    fonte_titulo = pygame.font.SysFont("Helvetica", 48)
    fonte_instr = pygame.font.SysFont("Helvetica", 24)

    while True:
        tela.fill(verde_escuro)
        titulo = fonte_titulo.render("Snake Eater", True, branca)
        instr1 = fonte_instr.render("Pressione Q para jogar", True, branca)
        instr2 = fonte_instr.render("Pressione ESC para sair", True, branca)

        rect_titulo = titulo.get_rect(center=(largura // 2, altura // 3))
        rect_instr1 = instr1.get_rect(center=(largura // 2, altura // 2))
        rect_instr2 = instr2.get_rect(center=(largura // 2, altura // 2 + 40))

        tela.blit(titulo, rect_titulo)
        tela.blit(instr1, rect_instr1)
        tela.blit(instr2, rect_instr2)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False

        relogio.tick(15)

def rodar_jogo():
    fim_jogo = False

    x = largura // 2 // tamanho_quadrado * tamanho_quadrado
    y = altura // 2 // tamanho_quadrado * tamanho_quadrado

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []


    comida_x, comida_y = gerar_comida(pixels)

    while not fim_jogo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

        x += velocidade_x
        y += velocidade_y

        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True

        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                fim_jogo = True
                break

        tela.fill(verde_escuro)
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        desenhar_cobra(tamanho_quadrado, pixels)
        desenhar_pontuacao(tamanho_cobra - 1)

        pygame.display.update()

        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida(pixels)

        relogio.tick(velocidade_jogo)

    mostrar_game_over()
    return True 

def mostrar_game_over():
    fonte_titulo = pygame.font.SysFont("Helvetica", 48)
    fonte_instr = pygame.font.SysFont("Helvetica", 24)

    espera_ticks = 0
    while True:
        tela.fill(verde_escuro)
        titulo = fonte_titulo.render("Game Over", True, branca)
        instr1 = fonte_instr.render("Pressione Q para jogar novamente", True, branca)
        instr2 = fonte_instr.render("Pressione ESC para sair", True, branca)

        rect_titulo = titulo.get_rect(center=(largura // 2, altura // 3))
        rect_instr1 = instr1.get_rect(center=(largura // 2, altura // 2))
        rect_instr2 = instr2.get_rect(center=(largura // 2, altura // 2 + 40))

        tela.blit(titulo, rect_titulo)
        tela.blit(instr1, rect_instr1)
        tela.blit(instr2, rect_instr2)

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    return
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        relogio.tick(10)
        espera_ticks += 1
        if espera_ticks > 30:
            pass

def main():
    rodando = True
    while rodando:
        iniciar = mostrar_menu()
        if not iniciar:
            rodando = False
            break
        resultado = rodar_jogo()
        if resultado is False:
            rodando = False
            break

    pygame.quit()

if __name__ == "__main__":
    main()