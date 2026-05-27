from console import console, erro, aviso, limpar_tela

from rich.panel import Panel
from rich import box
from rich.align import Align
from rich.text import Text

from art import text2art
import calendar
from rich.table import Table
from datetime import datetime
import msvcrt

MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
    'jan', 'fev', 'mar', 'abril', 'maio' 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'
]


def obter_ano_valido() -> int:
    while True:
        try:
            ano = int(console.input("Digite um ano: "))
            if verificar_ano_valido(ano):
                return ano
            aviso('Digite um ano positivo.')
        except ValueError:
            erro('Digite um ano válido.')


def obter_mes_valido() -> int:
    while True:
        try:
            mes_input = console.input("Digite um mês (nome ou número): ").lower().strip()

            if mes_input.isdigit():
                mes = int(mes_input)
                if not verificar_mes_valido(mes):
                    erro('Digite um mês válido.')
                    continue
            elif mes_input in MESES:
                mes = MESES.index(mes_input) + 1
                if mes > 12:
                    mes -= 12
            else:
                erro('Digite um mês válido.')
                continue

            return mes
        except:
            erro('Digite um mês válido.')


def obter_dia_valido(ano: int, mes: int) -> int:
    _, ultimo_dia = calendar.monthrange(ano, mes)
    while True:
        try:
            dia = int(console.input(f"Digite o dia (1-{ultimo_dia}): "))
            if verificar_dia_valido(dia, ano, mes):
                return dia
            aviso('Digite um dia válido.')
        except ValueError:
            erro('Digite apenas números.')


def verificar_ano_valido(ano: int) -> bool:
    return ano >= 1

def verificar_mes_valido(mes: int) -> bool:
    return 1 <= mes <= 12

def verificar_dia_valido(dia: int, ano: int, mes: int) -> bool:
    _, ultimo_dia = calendar.monthrange(ano, mes)
    return 1 <= dia <= ultimo_dia


def exibir_calendario(ano: int, mes: int, dia_escolhido: int) -> None:
    cal = calendar.monthcalendar(ano, mes)
    titulo = f"\n[bold green3]{MESES[mes-1].upper()} / {ano}[/bold green3]"
    tabela = Table(title=titulo, show_lines=True, header_style="bold green3")

    for d in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]:
        tabela.add_column(d, justify="center")

    for semana in cal:
        linha = [
            f"[bold green1][{dia}][/bold green1]" if dia == dia_escolhido else (str(dia) if dia != 0 else "")
            for dia in semana
        ]
        tabela.add_row(*linha)

    limpar_tela()
    console.print(Panel(Align.center(text2art('CALENDARIO')), style='green', box=box.DOUBLE))
    console.print(tabela)
    console.print(Text("\n←→: Mês anterior/próximo  |  G: Ir para data  |  Q: Sair", style="dim green", justify="center"))
    console.print()


def calendario() -> None:
    from modules.achievements.main_achievements import desbloquear
    desbloquear("cal_primeira_vez")

    agora = datetime.now()
    ano_exibido, mes_exibido, dia_exibido = agora.year, agora.month, agora.day

    while True:
        exibir_calendario(ano_exibido, mes_exibido, dia_exibido)

        key = msvcrt.getch()

        if key == b'\xe0':  # seta especial
            key2 = msvcrt.getch()

            if key2 == b'K':  # seta esquerda — mês anterior
                mes_exibido -= 1
                if mes_exibido < 1:
                    mes_exibido = 12
                    ano_exibido -= 1

            elif key2 == b'M':  # seta direita — próximo mês
                mes_exibido += 1
                if mes_exibido > 12:
                    mes_exibido = 1
                    ano_exibido += 1

        elif key.lower() == b'g':  # G — ir para data específica
            console.print()
            novo_ano = obter_ano_valido()
            novo_mes = obter_mes_valido()
            novo_dia = obter_dia_valido(novo_ano, novo_mes)
            ano_exibido, mes_exibido, dia_exibido = novo_ano, novo_mes, novo_dia

        elif key.lower() == b'q':  # Q — sair
            break

        # compatibilidade com comandos antigos de texto
        elif key.lower() == b'a':  # A — mês anterior
            mes_exibido -= 1
            if mes_exibido < 1:
                mes_exibido = 12
                ano_exibido -= 1

        elif key.lower() == b'd':  # D — próximo mês
            mes_exibido += 1
            if mes_exibido > 12:
                mes_exibido = 1
                ano_exibido += 1


if __name__ == "__main__":
    calendario()
