from console import console, limpar_tela, erro, aviso
from caixa_som import caixa_som
from pathlib import Path
from rich.panel import Panel
from rich.text import Text
from rich.console import Group

def mostrar_biblioteca():
    console.print(Panel(Text('BIBLIOTECA DE MÚSICAS', justify='center', style='bold green')))
    console.print()

    musicas = caixa_som.listar_musicas()
    lista_musicas = Text()

    for index, music in enumerate(musicas):
        lista_musicas.append(f'{f"[{index + 1:>2}]":<5} {Path(music).stem}\n')
    
    musica_atual = Text(f'Música Atual: {Path(caixa_som.get_musica_atual()).stem}\n', justify='center', style='bold green')
    
    sair = Text('Digite [0] para sair.', justify='center', style='green')

    conteudo = Group('', lista_musicas, musica_atual, sair)
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
                musica = int(console.input('>>> '))

                if musica == 0:
                    break
                    
                if musica < 0 or musica > quantidade_musicas:
                    aviso(f'Digite apenas números de 1 a {quantidade_musicas} ou 0 para sair.')
                    continue

            except:
                erro(f'Digite apenas números de 1 a {quantidade_musicas} ou 0 para sair.')
            
            else:
                caixa_som.tocar_musica(caixa_som.listar_musicas()[musica - 1])
                break

if __name__ == '__main__':
    biblioteca_musicas()
