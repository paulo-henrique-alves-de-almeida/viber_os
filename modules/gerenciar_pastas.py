from pathlib import Path
from console import console, erro, aviso

class GerenciadorPastas:
    def __init__(self):
        self.caminho_atual = Path(__file__).parent / 'home'
            
    def get_caminho_home(self, sumprimir_home: bool =True) -> str:
        caminho_home = f'/{str(self.caminho_atual.as_posix())[str(self.caminho_atual).find('home'):]}'

        if sumprimir_home and caminho_home.count('/') >= 2:
            pastas = caminho_home.split('/')
            pastas.pop(1)
            pastas.pop(1)
            pastas[0] = '[magenta]~[/magenta]'
            caminho_home = '/'.join(pastas)
        
        return caminho_home
    
    def criar_pasta(self, nome_pasta: str) -> None:
        try:
            Path(self.caminho_atual / nome_pasta).mkdir(parents=True)
            console.print(f'Diretório [bold]{nome_pasta}[/bold] criado com sucesso.\n')
        except FileExistsError:
            erro(f'O diretório [bold]{nome_pasta}[/bold] já existe.')
    
    def criar_arquivo(self, nome_arquivo: str) -> None:
        try:
            Path(self.caminho_atual / nome_arquivo).touch(exist_ok=False)
            console.print(f'Arquivo [bold]{nome_arquivo}[/bold] criado com sucesso.\n')
        except FileExistsError:
            erro(f'O arquivo [bold]{nome_arquivo}[/bold] já existe.')
        except FileNotFoundError:
            erro('Pasta não encontrada.')
    
    def listar_pasta(self, nome_pasta: str ='') -> None:
        quantidade_pastas = 0
        quantidade_arquivos = 0
        tamanho_arquivos = 0
        tipo = ''
        caminho = Path(self.caminho_atual / nome_pasta)

        if nome_pasta:
            if caminho.exists() and caminho.is_dir():
                console.print(f'\n[magenta][bold]Diretório:[/bold] {self.get_caminho_home(False)}/{nome_pasta}[/magenta]')
            else:
                erro('Caminho não encontrado.')
                return

        console.print()

        for item in caminho.iterdir():
            if item.is_dir():
                quantidade_pastas += 1
                tipo = 'DIR'
            else:
                quantidade_arquivos += 1
                tamanho_arquivos += item.stat().st_size
                tipo = 'ARQ'

            print(f'\033[32m<\033[35m{tipo}\033[32m>\033[m ', end='')
            console.print(f'[magenta]{item.name}[/magenta]')

        console.print(f'\n    {quantidade_arquivos} {'Arquivo' if quantidade_arquivos <= 1 else 'Arquivos'}    |   {tamanho_arquivos} bytes')
        console.print(f'    {quantidade_pastas} {'Diretório' if quantidade_pastas <= 1 else 'Diretórios'}\n')
    
    def trocar_pasta(self, nome_pasta: str) -> None:
        if nome_pasta == '..':
            if self.get_caminho_home() == '/home':
                return
            self.caminho_atual = self.caminho_atual.parent
            return

        novo_caminho = Path(self.caminho_atual / nome_pasta)
        
        if novo_caminho.exists() and novo_caminho.is_dir():
            self.caminho_atual = novo_caminho
            return
        
        erro('Caminho não encontrado.')
    
    def deletar_pasta(self, nome_pasta: str) -> None:
        caminho = Path(self.caminho_atual / nome_pasta)

        if caminho.exists() and caminho.is_dir():
            try:
                caminho.rmdir()
                console.print(f'Diretório [bold]{nome_pasta}[/bold] deletado com sucesso.\n')
            except OSError:
                erro('Só é possível deletar pastas vazias.')
            
            return
        
        erro(f'Pasta [bold]{nome_pasta}[/bold] não encontrada.')
    
    def deletar_arquivo(self, nome_arquivo: str) -> None:
        caminho = Path(self.caminho_atual / nome_arquivo)

        if caminho.exists() and caminho.is_file():
            while True:
                certeza = console.input(f'>>> Deseja mesmo excluir [bold]{nome_arquivo}[/bold]? Ele não poderá ser recuperado depois. (S/N) ').strip().lower()

                if certeza == 's' or certeza == 'n':
                    break
                else:
                    aviso('Resposta inválida. Digite apenas S ou N.\n')
            
            if certeza == 's':
                caminho.unlink()
                console.print(f'Arquivo [bold]{nome_arquivo}[/bold] deletado com sucesso.\n')
                return
        
        erro(f'Arquivo {nome_arquivo} não encontrado.')
    
    def ler_arquivo(self, nome_arquivo: str) -> None:
        arquivo = Path(self.caminho_atual / nome_arquivo)

        if arquivo.exists() and arquivo.is_file():
            with open(arquivo, 'r') as arq:
                texto = arq.read()

                console.print(f'{texto}\n')
        else:
            erro(f'Arquivo [bold]{nome_arquivo}[/bold] não encontrado.')

    
    def adicionar_arquivo(self, nome_arquivo: str, texto: str) -> None:
        arquivo = Path(self.caminho_atual / nome_arquivo)
        
        if not (arquivo.exists() and arquivo.is_file()):
            self.criar_arquivo(nome_arquivo)

        with open(arquivo, 'a') as arq:
            arq.write(texto)

gerenciador_pastas = GerenciadorPastas()
