import pygame
import os
import random

larguraTela = 500
alturaTela = 800
imgCano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imgChao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imgBg = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imgPassaro =[
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))
]

pygame.font.init()
fontePontos = pygame.font.SysFont('arial', 50)

class Passaro:
    imagens = imgPassaro
    maxRotacao = 25
    velRotacao = 20
    tempoAnimacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y

        self.tempo = 0
        self.contagemImg = 0
        self.img = self.imagens[0]

    def pular(self):
        self.velocidade = -7.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #colocar o deslocamento
        self.tempo += 1
        deslocamento = 1.5 + (self.tempo ** 2) + self.velocidade * self.tempo

        #restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.maxRotacao:
                self.angulo = self.maxRotacao
        else:
            if self.angulo > -90:
                self.angulo -= self.velRotacao

    def desenhar(self, tela):
        self.contagemImg += 1

        if self.contagemImg < self.tempoAnimacao:
            self.img = self.imagens[0]
        elif self.contagemImg < self.tempoAnimacao * 2:
            self.img = self.imagens[1]
        elif self.contagemImg < self.tempoAnimacao * 3:
            self.img = self.imagens[2]
        elif self.contagemImg < self.tempoAnimacao * 4:
            self.img = self.imagens[1]
        elif self.contagemImg >= self.tempoAnimacao * 4 + 1:
            self.img = self.imagens[0]
            self.contagemImg = 0

        if self.angulo <= -80:
            self.img = self.imagens[1]
            self.contagemImg = self.tempoAnimacao * 2

        imagemRota = pygame.transform.rotate(self.img, self.angulo)
        posiCentroImg = self.img.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagemRota.get_rect(center=posiCentroImg)
        tela.blit(imagemRota, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posTopo = 0
        self.posBase = 0
        self.canoTopo = pygame.transform.flip(imgCano, False, True)
        self.canoBase = imgCano
        self.passou = False
        self.definirAltura()

    def definirAltura(self):
        self.altura = random.randrange(50, 450)
        self.posTopo = self.altura - self.canoTopo.get_height()
        self.posBase = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.canoTopo, (self.x, self.posTopo))
        tela.blit(self.canoBase, (self.x, self.posBase))

    def colidir(self, passaro):
        passaroMask = passaro.get_mask()
        topoMask = pygame.mask.from_surface(self.canoTopo)
        baseMask = pygame.mask.from_surface(self.canoBase)

        distanciaTopo = (self.x - passaro.x, self.posTopo - round(passaro.y))
        distanciaBase = (self.x - passaro.x, self.posBase - round(passaro.y))

        pontoTopo = passaroMask.overlap(topoMask, distanciaTopo)
        basePonto = passaroMask.overlap(baseMask, distanciaBase)

        if basePonto or pontoTopo:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = imgChao.get_width()
    imagem = imgChao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura


    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

def desenharTela(tela, passaros, canos, chao, pontos):
    tela.blit(imgBg, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (larguraTela - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro( 230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((larguraTela, alturaTela))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        for passaro in passaros:
            passaro.mover()
        chao.mover()

        ad_cano = False
        remv_cano = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    ad_cano = True
            cano.mover()
            if cano.x + cano.canoTopo.get_width() < 0:
                remv_cano.append(cano)

        if ad_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remv_cano:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.img.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenharTela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()