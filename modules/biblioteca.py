# importações internas
from console import console, limpar_tela, erro, aviso
from caixa_som import caixa_som


# importação de Rich
from rich.panel import Panel
from rich import box
from rich.align import Align
from rich.text import Text
from rich.console import Group

# outras importações
from pathlib import Path
from art import text2art

def mostrar_biblioteca():
    console.print(Panel(Align.center(text2art('BIBLIOTECA DE MUSICAS')), style='bold green', box=box.DOUBLE))
    console.print()

    musicas = caixa_som.listar_musicas()
    musicas.sort()
    lista_musicas = Text()

    for index, music in enumerate(musicas):
        lista_musicas.append(f'\n{f"[{f'0{index + 1}' if index < 9 else index + 1}]":<5} {Path(music).stem}\n')
    
    musica_atual = Text(f'Música Atual: {str(Path(caixa_som.get_musica_atual()).stem).title()}\n', justify='center', style='bold green')
    
    mute = Text('Digite [-1] para deixar a música muda.\n', justify='center', style='green')
    sair = Text('Digite [0] para sair.', justify='center', style='green')

    conteudo = Group(lista_musicas, musica_atual, mute, sair)
    console.print(Panel(conteudo))
    console.print()

def biblioteca_musicas():
    caixa_som.init()
    quantidade_musicas = len(caixa_som.listar_musicas())

    while True:
        limpar_tela()
        mostrar_biblioteca()

        while True:
            try:
                musica = console.input('>>> ').strip()

                if musica == '':
                    continue
                    
                musica = int(musica)

                if musica == -1:
                    caixa_som.tocar_musica('mute')
                    break

                if musica == 0:
                    break
                    
                if musica < -1 or musica > quantidade_musicas:
                    aviso(f'Digite apenas números de 1 a {quantidade_musicas}, -1 para deixar a música muda ou 0 para sair.')
                    continue

            except ValueError:
                erro(f'Digite apenas números de 1 a {quantidade_musicas}, -1 para deixar a música muda ou 0 para sair.')
            
            else:
                caixa_som.tocar_musica(caixa_som.listar_musicas()[musica - 1], 0.5)
                break
        
        if musica == 0:
            break

if __name__ == '__main__':
    biblioteca_musicas()
