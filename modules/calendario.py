import calendar
import os
from rich.console import Console
from rich.table import Table

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_data_valida():
    while True:
        try:
            ano = int(input("Ano: "))
            if ano > 0: break
        except ValueError:
            continue

    while True:
        mes_input = input("Mês (nome ou número): ").lower()
        if mes_input.isdigit():
            mes = int(mes_input)
        elif mes_input in MESES:
            mes = MESES.index(mes_input) + 1
        else:
            continue
        if 1 <= mes <= 12: break

    _, ultimo_dia = calendar.monthrange(ano, mes)
    while True:
        try:
            dia = int(input(f"Dia (1-{ultimo_dia}): "))
            if 1 <= dia <= ultimo_dia: return ano, mes, dia
        except ValueError:
            continue

def exibir_calendario(ano, mes, dia_escolhido):
    console = Console()
    cal = calendar.monthcalendar(ano, mes)
    titulo = f"\n[bold green3]{MESES[mes-1].upper()} {ano}[/bold green3]"
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

def ir_para_data_especifica():
    try:
        ano = int(input("Digite o ano: "))
        mes_input = input("Digite o mês (Nome ou número): ").lower()
        if mes_input.isdigit():
            mes = int(mes_input)
        elif mes_input in MESES:
            mes = MESES.index(mes_input) + 1
        else:
            return None, None, None
        if not (1 <= mes <= 12):
            return None, None, None
        _, ultimo_dia = calendar.monthrange(ano, mes)
        try:
            dia = int(input(f"Digite o dia (1-{ultimo_dia}): "))
        except ValueError:
            return None, None, None
        if not (1 <= dia <= ultimo_dia):
            return None, None, None
        return ano, mes, dia
    except ValueError:
        return None, None, None

def principal():
    agora = datetime.now()
    ano_exibido, mes_exibido, dia_exibido = agora.year, agora.month, agora.day
    while True:
        exibir_calendario(ano_exibido, mes_exibido, dia_exibido)
        print("\n[A] Anterior | [D] Próximo | [G] Ir para... | [Q] Sair")
        comando = input("Escolha: ").lower()
        if comando == 'd':
            mes_exibido += 1
            if mes_exibido > 12:
                mes_exibido = 1
                ano_exibido += 1
        elif comando == 'a':
            mes_exibido -= 1
            if mes_exibido < 1:
                mes_exibido = 12
                ano_exibido -= 1
        elif comando == 'g':
            novo_ano, novo_mes, novo_dia = ir_para_data_especifica()
            if novo_ano:
                ano_exibido, mes_exibido, dia_exibido = novo_ano, novo_mes, novo_dia
        elif comando == 'q':
            break

if __name__ == "__main__":
    principal()