# importações internas
from modules.vibegotchi.ascii import pegar_vibe
from modules.vibegotchi.pet import Vibegotchi
from modules.console import console, limpar_tela, erro

# importação de rich
from rich import box
from rich.panel import Panel
from rich.align import Align

# outras importações
from art import text2art
from pathlib import Path
import time
import json

#=========================================================================================================================

SAVE = Path(__file__).parent / 'dados' / 'save.json'

def salvar_jogo(pet: Vibegotchi) -> None:
    SAVE.parent.mkdir(parents=True, exist_ok=True)
    with open(SAVE, "w+", encoding="utf-8") as arquivo:
        json.dump(pet.para_dict(), arquivo, indent=4)

def carregar_jogo() -> None:
    if SAVE.exists():
        with open(SAVE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        return Vibegotchi.de_dict(dados)
    
    return None

def checar_vida(pet: Vibegotchi) -> bool:
    condicoes = [
        (pet.aura <= 0,      f"{pet.nome} perdeu toda a sua aura e se foi..."),
        (pet.aura >= 1000,   f"{pet.nome} atingiu a aura máxima e se tornou um ser de pura energia!"),
        (pet.fome >= 100,    f"{pet.nome} morreu de fome..."),
        (pet.fome <= -1,     f"{pet.nome} morreu de tanto comer..."),
        (pet.energia <= 0,   f"{pet.nome} morreu de exaustão..."),
        (pet.humor <= 0,     f"{pet.nome} morreu de tristeza..."),
    ]

    for condicao, mensagem in condicoes:
        if condicao:
            console.print(mensagem)
            SAVE.unlink()
            return True

    return False

#=========================================================================================================================

def play() -> None:
    limpar_tela()
    console.print(Panel(Align.center(text2art('VIBEGOTCHI')), style='green', box=box.DOUBLE))
    console.print()

    pet = carregar_jogo()
    ultimo_tempo = time.time()

    if pet is None:
        nome = console.input("Escolha o nome do seu Vibesgochi: ")
        pet = Vibegotchi(nome)

    #======================================================================================================================

    while True:
        limpar_tela()
        salvar_jogo(pet)
        
        tempo_atual = time.time()
        delta = tempo_atual - ultimo_tempo
        if delta >= 2:
            pet.passar_tempo()
            ultimo_tempo = tempo_atual
        
        if pet.aura <= 20:
            cor = "red"
        elif pet.humor > 70:
            cor = "yellow"
        else:
            cor = "cyan"

        painel_pet = Panel(
            Align.center(pegar_vibe(pet)),
            title=f"🐾 {pet.nome}",
            border_style=cor
        )

        status = f"""
        [green]Fome:[/green] {pet.fome}
        [yellow]Energia:[/yellow] {pet.energia}
        [magenta]Humor:[/magenta] {pet.humor}
        [cyan]Aura:[/cyan] {pet.aura}
        """

        painel_status = Panel(status, title="Status", border_style="green")

        limpar_tela()
        console.print(painel_pet)
        console.print(painel_status)

        console.print("""
        [bold]Ações:[/bold]
        [0] → Sair
        [1] → Alimentar
        [2] → Brincar
        [3] → Dormir
        """)

        while True:
            escolha = console.input(">>> ")

            match escolha:
                case '0':
                    break

                case '1':
                    pet.alimentar()
                    break

                case '2':
                    pet.brincar()
                    break
                
                case '3':
                    pet.dormir()
                    break

                case _:
                    erro("Opção inválida!")
        
        if escolha == '0':
            break
        
        #------------------------------------------------------------------------------------------------------------------------

        if checar_vida(pet):
            console.print()
            console.input('>>> ')
            break
