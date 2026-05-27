import json
import shutil
import msvcrt
from pathlib import Path
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.console import Group
from art import text2art

from console import console

# ─────────────────────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────────────────────
_MUSICAS_DIR    = Path(__file__).parents[2] / "medias" / "sons" / "musicas"
_CONQUISTAS_DIR = _MUSICAS_DIR / "conquistas"  # músicas bloqueadas ficam aqui

# ─────────────────────────────────────────────────────────────────────────────
# CONQUISTAS (ACHIEVEMENTS)
# Formato: ("id_unico", "Título", "Descrição", "arquivo.mp3 ou None")
# - id_unico: nunca mude depois de criado, é usado no save
# - arquivo.mp3: nome do arquivo dentro de medias/sons/musicas/conquistas/
#                coloque None se a conquista não tiver recompensa de música
# ─────────────────────────────────────────────────────────────────────────────
#   exemplo de uso dentro de qualquer arquivo do sistema:
# from modules.achievements.main_achievements import desbloquear
#
#       desbloquear("id_da_conquista")
#─────────────────────────────────────────────────────────────────────────────
# Exemplos de como implementar o gatilho para desbloquear uma conquista:
#
# # game.py — wave completada
# if self.wave == 5:
#  desbloquear("vi_wave_5")
#
# boss.py — boss derrotado
# if self.hp <= 0:
#   desbloquear("vi_boss_derrotado")
#
# score
# if self.score >= 500:
#  desbloquear("vi_score_500")
#─────────────────────────────────────────────────────────────────────────────

CONQUISTAS = [

    # ── Sistema ──────────────────────────────────────────────────────────────
    ("sys_primeiro_login","Bem-vindo ao VibeOS", "Faça login pela primeira vez",             None),
    ("sys_musica",        "Bom Gosto",           "Toque uma música na biblioteca",           None),
    ("sys_segredo",       " Curioso feito um gato", "descubra um comando secreto",           "memory_drift.mp3"),

    # ── Vibe Invaders ────────────────────────────────────────────────────────
    ("vi_primeira_onda",  "Primeira Onda",      "Complete a wave 1 no Vibe Invaders",        None),
    ("vi_wave_5",         "Resistência",         "Chegue até a wave 5 no Vibe Invaders",     None),
    ("vi_boss_derrotado", "Vibe Hero",   "Derrote o Vibe Destroyer na dificuldade Vibe (Dificil)",  "happy_vibe.mp3"),

    #── Vibegotchi ────────────────────────────────────────────────────────────
    ("vg_nomeado",        ":O", "Dê um nome pro seu Vibegotchi",                             None),
    ("vg_cuidado",        "Amigo do Gochinho", "Alimente o seu Vibegotchi 3 vezes",          None),
    ("vg_aura",           "Transcendência", "Faça seu Vibegotchi atingir a aura máxima",     None),

    #── Calendario ────────────────────────────────────────────────────────────
    ("cal_primeira_vez",  "Que dia é hoje?", "Acesse o calendário pela primeira vez",        None),
    
    # ── Adicione mais conquistas abaixo ──────────────────────────────────────
    # ("id_unico", "Título", "Descrição", "arquivo.mp3"),  ← com música
    # ("id_unico", "Título", "Descrição", None),           ← sem música
]

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
_SAVE = Path(__file__).parent / "conquistas.json"


def _load() -> set:
    if not _SAVE.exists():
        return set()
    with open(_SAVE, "r") as f:
        return set(json.load(f))


def _save(desbloqueadas: set) -> None:
    _SAVE.parent.mkdir(parents=True, exist_ok=True)
    with open(_SAVE, "w") as f:
        json.dump(list(desbloqueadas), f)


def _desbloquear_musica(arquivo: str) -> None:
    """Copia a música de conquistas/ pra biblioteca principal."""
    origem  = _CONQUISTAS_DIR / arquivo
    destino = _MUSICAS_DIR / arquivo

    if not origem.exists():
        return  # arquivo não encontrado, ignora silenciosamente

    if destino.exists():
        return  # já foi copiada antes

    shutil.copy2(origem, destino)
    console.print(f"\n[bold yellow]  🎵 Música desbloqueada: {Path(arquivo).stem}![/bold yellow]\n")


# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES PRINCIPAIS
# ─────────────────────────────────────────────────────────────────────────────
def desbloquear(achievement_id: str) -> bool:
    """
    Desbloqueia uma conquista pelo id.
    Retorna True se foi desbloqueada agora, False se já estava.

    Uso em qualquer arquivo:
        from modules.achievements.main_achievements import desbloquear
        desbloquear("vi_boss_derrotado")
    """
    desbloqueadas = _load()
    if achievement_id in desbloqueadas:
        return False

    desbloqueadas.add(achievement_id)
    _save(desbloqueadas)

    # checa se tem música de recompensa
    for aid, _, _, musica in CONQUISTAS:
        if aid == achievement_id and musica:
            _desbloquear_musica(musica)
            break

    return True


def esta_desbloqueada(achievement_id: str) -> bool:
    """Checa se uma conquista já foi desbloqueada."""
    return achievement_id in _load()


# ─────────────────────────────────────────────────────────────────────────────
# DRAW
# ─────────────────────────────────────────────────────────────────────────────
def _draw(desbloqueadas: set) -> None:
    titulo = Text(text2art("    Conquistas"), style="green")

    table = Table(
        box=box.SIMPLE_HEAD,
        border_style="green",
        expand=True,
        show_header=False,
        padding=(0, 2),
    )

    table.add_column("check", width=3, no_wrap=True)
    table.add_column("info",  ratio=1)

    for aid, titulo_ach, descricao, musica in CONQUISTAS:
        if aid in desbloqueadas:
            check = Text("☑", style="bold green")
            nome  = Text(titulo_ach, style="bold green")
            desc  = Text(descricao,  style="bold green")
        else:
            check = Text("☐", style="dim white")
            nome  = Text(titulo_ach, style="bold white")
            desc  = Text(descricao,  style="dim white")

        # indicador de recompensa de música
        if musica:
            sufixo = " 🎵" if aid in desbloqueadas else " 🔒"
            nome.append(sufixo, style="bold green" if aid in desbloqueadas else "dim white")

        info = Group(nome, desc)
        table.add_row(check, info)
        table.add_section()

    total  = len(CONQUISTAS)
    feitas = len(desbloqueadas & {a[0] for a in CONQUISTAS})
    rodape = Text(f"\n  {feitas}/{total} conquistas desbloqueadas", style="dim green")

    conteudo = Group(titulo, table, rodape)

    panel = Panel(
        conteudo,
        border_style="green",
        expand=True,
        title="[bold green]Conquistas[/bold green]",
    )

    console.print(Align.center(panel))


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main() -> None:
    desbloqueadas = _load()
    _draw(desbloqueadas)
    console.print("\n[dim green]  Pressione Q para voltar...[/dim green]")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            if key == b'q':
                break
