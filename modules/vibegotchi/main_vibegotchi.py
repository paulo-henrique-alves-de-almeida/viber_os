# importações internas
from modules.vibegotchi.ascii import pegar_vibe
from modules.vibegotchi.pet import Vibegotchi
from modules.console import console, limpar_tela, erro
from modules.achievements.main_achievements import desbloquear

# importação de rich
from rich import box
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# outras importações
from art import text2art
from pathlib import Path
import time
import json
import msvcrt

#=========================================================================================================================

SAVE = Path(__file__).parent / 'dados' / 'save.json'

# ── ações navegáveis ──────────────────────────────────────────────────────────
ACOES = ["Sair", "Alimentar", "Brincar", "Dormir"]


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
            if pet.aura >= 1000:
                desbloquear("vg_aura")
            console.print(mensagem)
            SAVE.unlink()
            return True

    return False

def _draw_acoes(selected: int) -> None:
    """Renderiza o menu de ações com o cursor na opção selecionada."""
    acoes_text = Text(justify="center")
    acoes_text.append("\n Ações:\n\n", style="bold green")
    for i, acao in enumerate(ACOES):
        if i == selected:
            acoes_text.append(f"▶  {acao}\n\n", style="bold green")
        else:
            acoes_text.append(f"   {acao}\n\n", style="dim green")
    acoes_text.append("↑ ↓: Navegar  |  Enter: Confirmar", style="dim green")
    console.print(Panel(acoes_text, border_style="green"))

#=========================================================================================================================

def play() -> None:
    limpar_tela()
    console.print(Panel(Align.center(text2art('VIBEGOTCHI')), style='green', box=box.DOUBLE))
    console.print()

    pet = carregar_jogo()
    ultimo_tempo = time.time()
    selected = 0  # índice da ação selecionada

    if pet is None:
        nome = console.input("Escolha o nome do seu Vibesgochi: ")
        pet = Vibegotchi(nome)
        desbloquear("vg_nomeado")

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
        _draw_acoes(selected)

        # ── leitura de input por setas ────────────────────────────────────────
        escolha = None
        while escolha is None:
            key = msvcrt.getch()

            if key == b'\xe0':  # seta especial
                key2 = msvcrt.getch()
                if key2 == b'H':  # seta cima
                    selected = (selected - 1) % len(ACOES)
                elif key2 == b'P':  # seta baixo
                    selected = (selected + 1) % len(ACOES)

                # re-desenha só o painel de ações
                limpar_tela()
                console.print(painel_pet)
                console.print(painel_status)
                _draw_acoes(selected)

            elif key in (b'\r', b'\n'):  # Enter confirma
                escolha = selected

        # ── executa a ação ────────────────────────────────────────────────────
        match escolha:
            case 0:  # Sair
                break
            case 1:  # Alimentar
                pet.alimentar()
                if pet.vezes_alimentado >= 3:
                    desbloquear("vg_cuidado")
            case 2:  # Brincar
                pet.brincar()
            case 3:  # Dormir
                pet.dormir()

        #------------------------------------------------------------------------------------------------------------------------

        if checar_vida(pet):
            console.print()
            console.input('>>> ')
            break
