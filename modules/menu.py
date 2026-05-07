# importação de modules internos
from console import console, erro, aviso, limpar_tela
from modules.gerenciar_pastas import gerenciador_pastas
from caixa_som import caixa_som
from calendario import calendario
from biblioteca import biblioteca_musicas
from video2ascii import VideoAscii
from space_invader import main_vibe_invader as vibe_invaders
from modules.vibegotchi import main_vibegotchi as vibegotchi

#importação da biblioteca rich
from rich.align import Align
from rich.panel import Panel
from rich import box
from rich.markdown import Markdown
from rich.panel import Panel

# outras importações
from pathlib import Path
from art import text2art
from datetime import date
from time import sleep
from simpleeval import SimpleEval, OperatorNotDefined, NumberTooHigh
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

def cabecalho(nome: str):
    limpar_tela()

    console.print(Panel(Align.center(f'User: {nome}  |  Music: {Path(caixa_som.get_musica_atual()).stem}  |  Date: {date.today()}'), border_style="green", box=box.SIMPLE_HEAD, expand=False), justify="center")
    
    console.print(Panel(Align.center(text2art('VibeOS')), border_style="green", box=box.DOUBLE))
    console.print(Panel("[bold green]Lista de Aplicativos[/bold green]", border_style="green", box=box.SIMPLE_HEAD, expand=False), justify="center")

def mostrar_aplicativos():
    console.print(Panel('''[1] Calendário
                        
[2] Biblioteca de músicas
                        
[3] Vibegotchi
                        
[4] Vibe Invaders
                        
[5] Ajuda
                        
[6] Desligar sistema'''))
    
def menu(nome: str, nome_dados: str) -> None:
    aplicativo = True

    while True:
        try:
            if not caixa_som.get_busy_music():
                caixa_som.tocar_musica(caixa_som.get_musica_atual(), 0.5)
            
            if aplicativo:
                cabecalho(nome_dados)
                mostrar_aplicativos()
                console.print()
            
            aplicativo = False
                
            comando = console.input(f'[light_green]{nome}@vibe-os:[/light_green]{gerenciador_pastas.get_caminho_home()} > ').strip()

            match comando:
                case '' | 'clear':
                    aplicativo = True if comando else False
                    continue

                case 'ls':
                    gerenciador_pastas.listar_pasta()
                
                case 'cd..':
                    gerenciador_pastas.trocar_pasta('..')
                
                case 'whoiam':
                    console.print(f'[magenta]{nome_dados}[/magenta]\n')
                
                case 'pwd':
                    console.print(f'{gerenciador_pastas.get_caminho_home(False)}\n')
                
                case 'hostname':
                    console.print('[light_green]vibe-os[/light_green]\n')
                
                case 'uname':
                    console.print('Vibelinux 1.0\n')

                case '1' | 'calendar':
                    aplicativo = True
                    calendario()
                
                case '2' | 'music':
                    aplicativo = True
                    biblioteca_musicas()
                
                case '3' | 'vibegochi':
                    aplicativo = True
                    pass
                
                case '4' | 'vibe_invaders':
                    aplicativo = True
                    limpar_tela()
                    vibe_invaders.main()
                
                case '5' | 'help':
                    with open(Path(__file__).parent / 'help.md', encoding='utf-8') as man:
                        markdown = Markdown(man.read())
                    console.print()
                    console.print(Panel(markdown))
                    console.print()
                
                case '6' | 'shutdown':
                    sleep(1)
                    break

                # segredos
                case 'shrek':
                    pass
                
                case 'rick':
                    aplicativo = True
                    
                    try:
                        video = VideoAscii('rickroll.mp4')
                        caixa_som.tocar_musica('Rickroll.mp3', 0.8, False, 0)
                        video.play()
                    except (KeyboardInterrupt, EOFError):
                        caixa_som.pausar_musica()
                        continue
                    
                # "else"
                case _:
                    comando_separado = comando.split(' ')
                    match comando_separado[0]:
                        case 'man':
                            if len(comando_separado) != 2:
                                erro('Comando não reconhecido.')
                            else:
                                comandos = {'clear': [1, 2], 'whoiam': [3, 4], 'pwd': [5, 6], 'hostname': [7, 8], 'uname': [9, 10], 'ls': [11, 14], 'man': [15, 18], 'cd': [19, 21], 'mkdir': [22, 25], 'touch': [26, 28], 'rm': [29, 31], 'rmdir': [32, 35], 'cat': [36, 38], 'echo': [39, 43], 'viber': [44, 46], 'calendar': [55, 56], 'music': [57, 58], 'vibegotchi': [59, 60], 'vibe_invaders': [61, 62], 'help': [47, 48], 'shutdown': [49, 50]}
                                
                                if comando_separado[1] in comandos:
                                    caminho = Path(__file__).parent / 'help.md'
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
                            if len(comando_separado) < 2:
                                aviso('Esperava o nome do diretório para ser criado.')
                            else:
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
                        
                        case 'viber':
                            if len(comando_separado) < 2:
                                aviso('Prompt esperado.')
                            else:
                                console.print('>>> Pensando[green]...[/green]\n')

                                genai.configure(api_key="AIzaSyBAg_yUG5d1-y4-fBsTLIi29CfwJI9w28o")

                                caminho = Path(__file__).parent / 'help.md'
                                with open(caminho, "r", encoding="utf-8") as arquivo_instrucoes:
                                    instrucoes = arquivo_instrucoes.read()
                                    
                                instrucoes_ia = '\n\n---\n\n# Instruções de IA\n\n- Você é um assistente de Sistema Operacional VibeOS em terminal, chamado Viber.\n- Responda sempre em português.\n-Se não souber a resposta, diga claramente. Nunca invente informações.\n- Seja profissional, mas amigável.\n- Não use comandos markdown em sua resposta.\n- Não utilize emojis.\n- Você ama tudo relacionado ao VibeOS, melhor sistema operacional que existe. Incluindo Vibe Invaders, Vibegotchi, músicas, segredos etc.\n- Você foi treinado por Paulo Henrique.\n- Luiza Silva Leite é a princesa do reino do qual o VibeOS faz parte.'
                                instrucoes += instrucoes_ia
                                    
                                model = genai.GenerativeModel(
                                    model_name='gemini-flash-latest',
                                    system_instruction=instrucoes
                                )

                                prompt = ''
                                for command in comando_separado:
                                    prompt += command

                                try:
                                    response = model.generate_content(prompt)

                                    console.print(f'[bold blue]Viber[/bold blue]: {response.text}\n')
                                except ResourceExhausted:
                                    aviso('Limite de requisições atingido. Espere um minuto e tente novamente.')
                                except:
                                    erro(f'Viber não está disponível no momento.')
                        
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
        # except:
        except (KeyboardInterrupt, EOFError):
            if aplicativo:
                continue
            else:
                console.print()

if __name__ == '__main__':
    cabecalho('Paulo')
    comandos_aceitos = mostrar_aplicativos()
