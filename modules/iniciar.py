# importação de modules
from console import console, limpar_tela, erro, aviso
from caixa_som import caixa_som

# importação de Rich
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.align import Align

# outras importações
from time import sleep
from winsound import Beep
from pathlib import Path
from json import dump, load
from art import text2art
from pwinput import pwinput

def boot() -> None:
    limpar_tela()
    console.print("\n")

    caixa_som.init()
    caixa_som.tocar_musica('playstation-2-startup-intro-ps2.mp3', loop=0, fadeout=5000)
    
    etapas = ['Iniciando aplicativos...', 'Entrando na vibe...', 'Codando...', 'Organizando pastas...', 'Deixando tudo pronto...']
    with Progress(SpinnerColumn('bouncingBar', style="green"), TextColumn("[green]{task.description}"), BarColumn(bar_width=40, style="green", complete_style="bright_green"), console=console, transient=True) as progress:
        tarefa = progress.add_task("Inicializando...", total=len(etapas))
        for etapa in etapas:
            progress.update(tarefa, description=etapa, advance=1)
            sleep(1)

    console.print(Panel("[bold bright_green]  VibeOS INICIALIZADO COM SUCESSO!  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")
    sleep(1)

def boas_vindas() -> None:
    limpar_tela()

    caixa_som.init()
    caixa_som.tocar_musica('VibeOS.mp3', volume=0.5)

    console.print(Panel(Align.center(text2art('Bem vindo ao VibeOS!')), border_style="green", box=box.DOUBLE))
    sleep(1)

def coletar_dados() -> None:
    # coleta idade
    limpar_tela()
    console.print(Panel("[bold bright_green]  DIGITE SUA IDADE:  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")
    while True:
        try:
            idade = int(console.input('>>> '))

            if idade < 0 or idade > 125:
                aviso('Idade inválida.')
            else:
                break
        except:
            erro('Digite apenas números.')

    sleep(0.5)

    dados = {"idade": idade}
    caminho = Path(__file__).parent.parent / 'dados' / 'dados_usuario.json'
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    with open(caminho, "w+") as arquivo:
        dump(dados, arquivo, indent=4, ensure_ascii=False)
    
    if idade < 18:
        return
    
    # coleta o nome de usuário
    limpar_tela()
    console.print(Panel("[bold bright_green]  DIGITE SEU NOME DE USUÁRIO:  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")
    while True:
        nome = console.input('>>> ').strip()

        if len(nome) < 3:
            aviso('O nome deve possui, pelo menos, 3 caracteres.')
        else:
            break
    
    sleep(0.5)

    # define a senha do usuário
    limpar_tela()
    console.print(Panel("[bold bright_green]  DEFINA SUA SENHA:  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")
    console.print('>>> ', end='')
    senha = pwinput('').strip()

    dados = {"idade": idade, "nome": nome, "senha": senha}
    with open(caminho, "w", encoding="utf-8") as arquivo:
        dump(dados, arquivo, indent=4, ensure_ascii=False)
    
    sleep(0.5)

def menor_idade() -> None:
    limpar_tela()
    console.print("\n")
    console.print(Panel("[bold bright_green]  Acesso bloqueado no Brasil devido à sua idade.  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")
    console.input('>>> ')

def checar_sehha(primeira_vez: bool =False) -> bool:
    if not primeira_vez:
        caminho = Path(__file__).parent.parent / 'dados' / 'dados_usuario.json'
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = load(arquivo)
        
        for i in range(0, 3):
            limpar_tela()
            console.print(Panel("[bold bright_green]  DIGITE SUA SENHA:  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")
            
            if i > 0:
                console.print(Panel(Align.center(f'[red]Senha incorreta. {3 - i} tentaivas antes do desligamento forçado.[/red]'), border_style="red", box=box.DOUBLE))
            
            console.print('>>> ', end='')
            senha = pwinput('')
            
            if senha == dados['senha']:
                return True
    
        return False
    
    return True

def desligamento() -> None:
    limpar_tela()
    console.print("\n")
    etapas = ['Desligando aplicativos...', 'Saindo da vibe...', 'Salvando pastas...', 'Deixando tudo pronto para desligar...']
    with Progress(SpinnerColumn('bouncingBar', style="green"), TextColumn("[green]{task.description}"), BarColumn(bar_width=40, style="green", complete_style="bright_green"), console=console, transient=True) as progress:
        tarefa = progress.add_task("Inicializando...", total=len(etapas))
        for etapa in etapas:
            progress.update(tarefa, description=etapa, advance=1)
            Beep(900, 300)
            sleep(0.3)

    console.print(Panel("[bold bright_green]  OBRIGADO POR USAR VibeOS! :)  [/bold bright_green]", border_style="bright_green", box=box.DOUBLE), justify="center")


if __name__ == '__main__':
    boot()
    sleep(1)
    coletar_dados()
    sleep(1)
    checar_sehha()
    sleep(1)
    desligamento()
