from console import console, limpar_tela

from rich.align import Align
from rich.panel import Panel
from rich import box

from art import text2art
from datetime import date

def cabecalho(nome: str, titulo = 'Lista de Aplicativos'):
    limpar_tela()
    console.print(Panel(Align.center(f'User: {nome}  |  Date: {date.today()}'), border_style="green", box=box.SIMPLE_HEAD, expand=False), justify="center")
    console.print(Panel(Align.center(text2art('VibeOS')), border_style="green", box=box.DOUBLE))
    console.print(Panel(f"[bold green]{titulo}[/bold green]", border_style="green", box=box.SIMPLE_HEAD, expand=False), justify="center")

def mostrar_aplicativos():
    console.print(Panel('''[1] Calendário
                        
[2] Biblioteca de músicas
                        
[3] Vibegotchi
                        
[4] Vibe Box
                        
[5] Ajuda
                        
[6] Desligar sistema'''))

if __name__ == '__main__':
    cabecalho('Paulo')
    comandos_aceitos = mostrar_aplicativos()
