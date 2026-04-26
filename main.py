# importação da pasta modules
from sys import path
from pathlib import Path
pasta_modules = Path(__file__).resolve().parent / 'modules'

if str(pasta_modules) not in path:
    path.append(str(pasta_modules))

from modules.iniciar import boot, boas_vindas, menor_idade, checar_sehha, desligamento, coletar_dados
from modules.menu import menu
from modules.gerenciar_pastas import gerenciador_pastas

# outras importações
from json import load


if __name__ == '__main__':
    boot()

    arquivo_dados = Path(__file__).parent / 'dados' / 'dados.json'

    if not arquivo_dados.exists():
        coletar_dados()
        primeira_vez = True
    else:
        primeira_vez = False

    with open(arquivo_dados, 'r') as arquivo:
        dados = load(arquivo)

    if dados['idade'] < 18:
        menor_idade()

    else:
        if checar_sehha(primeira_vez):
            boas_vindas()

            # cria o diretório home e user
            nome = dados['nome'].lower().replace(' ', '-').replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-')
            if not Path(gerenciador_pastas.caminho_atual / nome).exists():
                gerenciador_pastas.criar_pasta(nome)
            gerenciador_pastas.trocar_pasta(nome)

            menu(nome, dados['nome'])
    
    desligamento()
