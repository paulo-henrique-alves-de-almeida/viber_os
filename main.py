# importação da pasta modules
from sys import path
from pathlib import Path
pasta_modules = Path(__file__).resolve().parent / 'modules'

if str(pasta_modules) not in path:
    path.append(str(pasta_modules))

from modules.iniciar import boot, boas_vindas, menor_idade, checar_sehha, desligamento, coletar_dados
from modules.menu import cabecalho, mostrar_aplicativos
from modules.console import console, erro
from modules.gerenciar_pastas import GerenciadorPastas

# outras importações
from time import sleep
from json import load

def menu(nome: str):
    aplicativo = True

    while True:
        if aplicativo:
            cabecalho(nome)
            mostrar_aplicativos()
            print()

        comando = console.input(f'[light_green]{nome}@vibe-os:[/light_green]{gerenciador_pastas.get_caminho_home()} > ').strip()

        comando_separado = comando.split(' ')

        match comando:
            case '':
                aplicativo = False
                continue

            case 'clear':
                aplicativo = True
                continue

            case 'ls':
                gerenciador_pastas.listar_pasta()
                aplicativo = False
            
            case 'whoiam':
                with open(arquivo_dados, 'r') as arquivo:
                    dados = load(arquivo)
                console.print(dados['nome'])
                aplicativo = False
            
            case 'pwd':
                console.print(gerenciador_pastas.get_caminho_home(False))
                aplicativo = False
            
            case 'hostname':
                console.print('vibe-os')
                aplicativo = False
            
            case 'uname':
                console.print('Vibelinux')

            case '0' | 'calc':
                pass
                aplicativo = True
                
            case '1' | 'notepad':
                pass
                aplicativo = True
            
            case '2' | 'calendar':
                pass
                aplicativo = True
            
            case '3' | 'music':
                pass
                aplicativo = True
            
            case '4' | 'vibegochi':
                pass
                aplicativo = True
            
            case '5' | 'gpt':
                pass
                aplicativo = True
            
            case '6' | 'man':
                pass
                aplicativo = False
            
            case '7' | 'shutdown':
                sleep(1)
                break

            # segredos
            case 'shrek':
                pass
                aplicativo = False

            # "else"
            case _:
                aplicativo = False
                match comando_separado[0]:
                    case 'cd':
                        if len(comando_separado) != 2:
                            erro('Caminho não encontrado.')
                        else:
                            gerenciador_pastas.trocar_pasta(comando_separado[1])
                    
                    case 'mkdir':
                        for command in comando_separado:
                            if command != 'mkdir':
                                gerenciador_pastas.criar_pasta(command)
                    
                    case 'touch':
                        if len(comando_separado) != 2:
                            erro('Comando inválido.')
                        else:
                            gerenciador_pastas.criar_arquivo(comando_separado[1])

                    case 'rm':
                        if len(comando_separado) != 2:
                            erro('Arquivo não encontrado.')
                        else:
                            gerenciador_pastas.deletar_arquivo(comando_separado[1])
                    
                    case 'rmdir':
                        if len(comando_separado) < 2:
                            erro('Diretório não encontrado')
                        else:
                            for command in comando_separado:
                                if command != 'rmdir':
                                    gerenciador_pastas.deletar_pasta(command)
                    
                    case 'cat':
                        if len(comando_separado) != 2:
                            erro('Arquivo não encontrado.')
                        else:
                            gerenciador_pastas.ler_arquivo(comando_separado[1])

                    
                    case 'echo':
                        match len(comando_separado):
                            case 1:
                                console.print('>>> \n')
                            case 2:
                                console.print(f'>>> {comando_separado[1]}\n')
                            case 3:
                                if comando_separado[2] == '>':
                                    erro('Esperava o nome de um arquivo após >.')
                                else:
                                    erro('Comando inválido.')
                            case 4:
                                if comando_separado[2] == '>':
                                    gerenciador_pastas.adicionar_arquivo(comando_separado[3], comando_separado[1])
                                else:
                                    erro('Comando inválido')
                            case _:
                                erro('Comando inválido.')
                    
                    case _: 
                        erro(f'Comando [italic]{comando}[/italic] desconhecido.')
                        aplicativo = False

if __name__ == '__main__':
    boot()

    arquivo_dados = Path(__file__).parent / 'dados' / 'dados.json'

    if not arquivo_dados.exists() or arquivo_dados.stat().st_size == 0:
        coletar_dados()

    with open(arquivo_dados, 'r') as arquivo:
        dados = load(arquivo)
    
    if dados['idade'] < 18:
        menor_idade()

    else:
        if checar_sehha():
            boas_vindas()

            gerenciador_pastas = GerenciadorPastas()
            gerenciador_pastas.criar_pasta(dados['nome'])
            gerenciador_pastas.trocar_pasta(dados['nome'])
            menu(dados['nome'])
    
    desligamento()
