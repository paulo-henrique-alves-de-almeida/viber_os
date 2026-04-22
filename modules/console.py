from rich.console import Console

console = Console(style='green')

def limpar_tela() -> None:
    console.clear()

def erro(msg: str) -> None:
    console.print(f'[bold red]Erro:[/bold red] {msg}\n')

def aviso(msg: str) -> None:
    console.print(f'[bold yellow]Aviso:[/bold yellow] {msg}\n')
