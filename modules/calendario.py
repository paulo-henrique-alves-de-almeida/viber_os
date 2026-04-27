import calendar
import os
from rich.console import Console
from rich.table import Table

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_entrada_valida():
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    
    while True:
        try:
            ano = int(input("Ano: "))
            if ano > 0: break
            print("Digite um ano positivo.")
        except ValueError:
            print("Digite um número válido para o ano.")

    while True:
        mes_input = input("Mês (nome ou número): ").lower()
        if mes_input.isdigit():
            mes = int(mes_input)
        elif mes_input in meses:
            mes = meses.index(mes_input) + 1
        else:
            print("Mês inválido.")
            continue
        if 1 <= mes <= 12: break

    _, ultimo_dia = calendar.monthrange(ano, mes)
    while True:
        try:
            dia = int(input(f"Dia (1-{ultimo_dia}): "))
            if 1 <= dia <= ultimo_dia: return ano, mes, dia, meses
            print(f"Erro: O mês selecionado só tem {ultimo_dia} dias.")
        except ValueError:
            print("Digite um número válido.")

def exibir_calendario(ano, mes, dia_escolhido, lista_meses):
    console = Console()
    cal = calendar.monthcalendar(ano, mes)
    
    titulo = f"\n[bold green3]{lista_meses[mes-1].upper()} {ano}[/bold green3]"
    tabela = Table(title=titulo, show_lines=True, header_style="bold green3")
    
    for d in ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]:
        tabela.add_column(d, justify="center")

    for semana in cal:
        linha = [
            f"[bold green1][{dia}][/]" if dia == dia_escolhido else (str(dia) if dia != 0 else "")
            for dia in semana
        ]
        tabela.add_row(*linha)
    
    limpar_tela()
    console.print(tabela)

if __name__ == "__main__":
    ano, mes, dia, lista_meses = obter_entrada_valida()
    exibir_calendario(ano, mes, dia, lista_meses)