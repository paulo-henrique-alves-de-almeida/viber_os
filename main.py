# importação da pasta modules
from sys import path
from pathlib import Path
pasta_modules = Path(__file__).resolve().parent / 'modules'

if str(pasta_modules) not in path:
    path.append(str(pasta_modules))

from modules.iniciar import boot, boas_vindas, menor_idade, checar_sehha, desligamento, coletar_dados
from modules.menu import cabecalho, mostrar_aplicativos
from modules.console import console, erro, aviso
from modules.gerenciar_pastas import GerenciadorPastas

# outras importações
import os
from time import sleep
from json import load
from simpleeval import SimpleEval, OperatorNotDefined, NumberTooHigh

from rich.markdown import Markdown
from rich.panel import Panel

def menu(nome_dados: str) -> None:
    aplicativo = True

    while True:
        try:
            if aplicativo:
                cabecalho(nome_dados)
                mostrar_aplicativos()
                console.print()

            comando = console.input(f'[light_green]{nome}@vibe-os:[/light_green]{gerenciador_pastas.get_caminho_home()} > ').strip()

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
                
                case 'cd..':
                    gerenciador_pastas.trocar_pasta('..')
                    aplicativo = False
                
                case 'whoiam':
                    with open(arquivo_dados, 'r') as arquivo:
                        dados = load(arquivo)
                    console.print(f'[magenta]{dados['nome']}[/magenta]\n')
                    aplicativo = False
                
                case 'pwd':
                    console.print(f'{gerenciador_pastas.get_caminho_home(False)}\n')
                    aplicativo = False
                
                case 'hostname':
                    console.print('[light_green]vibe-os[/light_green]\n')
                    aplicativo = False
                
                case 'uname':
                    console.print('Vibelinux 1.0\n')
                    aplicativo = False

                case '1' | 'calendar':
                    pass
                    aplicativo = True
                
                case '2' | 'music':
                    pass
                    aplicativo = True
                
                case '3' | 'vibegochi':
                    pass
                    aplicativo = True
                
                case '4' | 'gpt':
                    pass
                    aplicativo = True
                
                case '5' | 'help':
                    with open(Path(__file__).parent / 'modules' / 'help.md', encoding='utf-8') as man:
                        markdown = Markdown(man.read())
                    console.print()
                    console.print(Panel(markdown))
                    console.print()
                    aplicativo = False
                
                case '6' | 'shutdown':
                    sleep(1)
                    break

                # segredos
                case 'shrek':
                    pass
                    aplicativo = False
                
                case 'rick':
                    aplicativo = True
                    print('\033[32m')
                    os.system('curl ascii.live/rick')
                    
                # "else"
                case _:
                    comando_separado = comando.split(' ')
                    aplicativo = False
                    match comando_separado[0]:
                        case 'man':
                            if len(comando_separado) != 2:
                                erro('Comando não reconhecido.')
                            else:
                                comandos = {'clear': [1, 2], 'whoiam': [3, 4], 'pwd': [5, 6], 'hostname': [7, 8], 'uname': [9, 10], 'ls': [11, 14], 'man': [15, 18], 'cd': [19, 21], 'mkdir': [22, 25], 'touch': [26, 28], 'rm': [29, 31], 'rmdir': [32, 35], 'cat': [36, 38], 'echo': [39, 43], 'calendar': [44, 45], 'music': [46, 47], 'vibegotchi': [48, 49], 'gpt': [50, 51], 'help': [52, 53], 'shutdown': [54, 55]}
                                
                                if comando_separado[1] in comandos:
                                    caminho = Path(__file__).parent / 'modules' / 'help.md'
                                    nome_comando = comando_separado[1]

                                    with open(caminho, 'r', encoding="utf-8") as helpmd:
                                        linhas = helpmd.readlines()
                                        linhas = linhas[comandos[nome_comando][0]:comandos[nome_comando][1]]
                                        texto_parcial = ''.join(linhas)

                                    markdown = Markdown(texto_parcial)
                                    console.print()
                                    console.print(Panel(markdown))
                                    console.print()
                                else:
                                    erro('Comando não reconhecido.')
                        
                        case 'ls':
                            if len(comando_separado) != 2:
                                erro('Caminho não encontrado.')
                            else:
                                gerenciador_pastas.listar_pasta(comando_separado[1])

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
                            calculadora = SimpleEval(functions={}, names={})
                            calculadora.disallow_attributes = True

                            try:
                                resultado = calculadora.eval(comando.replace(',', '.'))
                                # inteiro, _, decimal = str(resultado).partition('.')
                                # resultado = f"{int(inteiro):,}" + (f",{decimal}" if decimal else "")

                                console.print(f'>>> {resultado:g}\n')
                            except ZeroDivisionError:
                                console.print('>>> Indefinido ou indeterminado. \n')
                            except OperatorNotDefined:
                                erro('Operador desconhecido')
                            except NumberTooHigh:
                                aviso('A expressão é grande demais.')
                            except:
                                erro(f'Comando [italic]{comando}[/italic] desconhecido.')
        except:
        # except Exception as e:
        # print(e)
            console.print()

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

            gerenciador_pastas = GerenciadorPastas()

            # cria o diretório home e user
            nome = dados['nome'].lower().replace(' ', '-').replace('/', '-').replace('\\', '-').replace(':', '-').replace('*', '-').replace('?', '-').replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-')
            if not Path(gerenciador_pastas.caminho_atual / nome).exists():
                gerenciador_pastas.criar_pasta(nome)
            gerenciador_pastas.trocar_pasta(nome)

            menu(dados['nome'])
    
    desligamento()
