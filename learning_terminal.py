#!/usr/bin/env python3
"""터미널 학습 도우미 | Python 3 only — stdlib only"""

import os, sys, json, re, time
from datetime import date, timedelta
import getpass

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    import msvcrt
    import ctypes
    # Windows Terminal / ConHost 에서 ANSI 색상 활성화
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass
else:
    import tty, termios

def getch():
    """엔터 없이 키 하나를 읽는다."""
    if IS_WINDOWS:
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):   # 특수키(화살표 등) — 두 번째 코드 버림
            msvcrt.getwch()
            return ''
        return ch
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# ── ANSI colours ──────────────────────────────────────────────────────────────
R  = "\033[0m"
B  = "\033[1m"
DM = "\033[2m"
CY = "\033[1;36m"
GR = "\033[1;32m"
YL = "\033[1;33m"
RD = "\033[1;31m"
MG = "\033[1;35m"
cy = "\033[36m"
gr = "\033[32m"
yl = "\033[33m"
rd = "\033[31m"

# ── Helpers ───────────────────────────────────────────────────────────────────
def clr():
    os.system("cls" if IS_WINDOWS else "clear")

def hr():
    print(f"{DM}{'─'*60}{R}")

def pause():
    input(f"\n{DM}  Enter를 눌러 계속...{R}")

_ANSI_RE = re.compile(r'\033\[[0-9;]*[mABCDEFGHJKSTfn]')

def typewrite(text, duration=2.0):
    """ANSI 코드를 보존하면서 전체 텍스트를 duration초 안에 타이핑 효과로 출력."""
    visible_len = max(len(_ANSI_RE.sub('', text).replace('\n', '')), 1)
    delay = duration / visible_len
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '\033' and i + 1 < len(text) and text[i + 1] == '[':
            j = i + 2
            while j < len(text) and text[j] not in 'mABCDEFGHJKSTfn':
                j += 1
            sys.stdout.write(text[i:j + 1])
            sys.stdout.flush()
            i = j + 1
        elif ch == '\n':
            sys.stdout.write(ch)
            sys.stdout.flush()
            i += 1
        else:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
            i += 1

# ── TUI Animations ────────────────────────────────────────────────────────────
def animate_progress_bar(current: int, total: int, label: str = "", width: int = 38):
    """현재/전체 비율로 진행률 바를 애니메이션으로 채운다."""
    if total == 0:
        return
    steps = 25
    for i in range(steps + 1):
        pct = (current * i / steps) / total
        filled = int(width * pct)
        bar = f"{GR}{'█' * filled}{DM}{'░' * (width - filled)}{R}"
        pct_int = int(pct * 100)
        sys.stdout.write(f"\r  [{bar}] {GR}{pct_int:3d}%{R}  {label}")
        sys.stdout.flush()
        time.sleep(0.025)
    print()

def spinner(msg: str, duration: float = 1.0):
    """로딩 스피너 애니메이션."""
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_t = time.time() + duration
    i = 0
    while time.time() < end_t:
        sys.stdout.write(f"\r  {CY}{frames[i % len(frames)]}{R}  {msg}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  {GR}✓{R}  {msg}                \n")
    sys.stdout.flush()

def celebrate():
    """레슨 완료 시 간단한 축하 애니메이션."""
    lines = [
        f"  {GR}★{R} {YL}★{R} {CY}★{R} {MG}★{R} {GR}★{R} {YL}★{R} {CY}★{R}",
        f"  {YL}✦{R} {CY}✦{R} {MG}✦{R} {GR}✦{R} {YL}✦{R} {CY}✦{R} {MG}✦{R}",
        f"  {CY}★{R} {MG}★{R} {GR}★{R} {YL}★{R} {CY}★{R} {MG}★{R} {GR}★{R}",
    ]
    for _ in range(4):
        for line in lines:
            sys.stdout.write(f"\r{line}")
            sys.stdout.flush()
            time.sleep(0.12)
    print(f"\r  {GR}{B}🎉 완료! 모든 레슨을 마쳤습니다!{R}          ")

def fireworks():
    """카테고리 전체 완료 시 폭죽 애니메이션."""
    clr()
    stages = [
        [
            f"                    {YL}*{R}",
            f"                   {YL}*{R} {YL}*{R}",
            f"                  {YL}*{R} {YL}O{R} {YL}*{R}",
            f"                   {YL}*{R} {YL}*{R}",
        ],
        [
            f"    {CY}*{R}               {YL}*{R} {YL}*{R} {YL}*{R}",
            f"   {CY}*{R}{CY}*{R}             {YL}*{R} {YL}O{R} {YL}*{R}    {MG}*{R}",
            f"  {CY}*{R}{CY}O{R}{CY}*{R}            {YL}*{R} {YL}*{R} {YL}*{R}   {MG}*{R}{MG}*{R}",
            f"   {CY}*{R}{CY}*{R}                        {MG}O{R}",
        ],
        [
            f"  {GR}* * *{R}          {YL}* * *{R}       {MG}* *{R}",
            f"  {GR}* O *{R}          {YL}* O *{R}       {MG}* O{R}",
            f"  {GR}* * *{R}          {YL}* * *{R}       {MG}* *{R}",
        ],
    ]
    for stage in stages:
        clr()
        print()
        for line in stage:
            print(line)
        time.sleep(0.25)
    clr()
    print()
    print(f"  {CY}{B}╔══════════════════════════════════════════╗{R}")
    print(f"  {CY}{B}║{R}   {GR}{B}🎊  모든 레슨 완료!  축하합니다!  🎊{R}   {CY}{B}║{R}")
    print(f"  {CY}{B}╚══════════════════════════════════════════╝{R}")
    print()

def splash_screen():
    """시작 시 애니메이션 스플래시 화면."""
    clr()
    lines = [
        f"  {CY}{B}╔═════════════════════════════════════════════╗{R}",
        f"  {CY}{B}║                                             ║{R}",
        f"  {CY}{B}║   {GR}터미널 학습 도우미{CY}  ·  {YL}v2.0{CY}             ║{R}",
        f"  {CY}{B}║   {DM}Terminal Learning Assistant{CY}              ║{R}",
        f"  {CY}{B}║                                             ║{R}",
        f"  {CY}{B}╚═════════════════════════════════════════════╝{R}",
    ]
    for line in lines:
        print(line)
        time.sleep(0.08)
    print()
    items = [
        ("터미널 기초 레슨", 0.35),
        ("Vim 에디터 레슨", 0.30),
        ("tmux 레슨", 0.25),
        ("학습 데이터", 0.20),
    ]
    for label, dur in items:
        spinner(label + " 로드 중...", dur)
    time.sleep(0.2)
    clr()

# ── Storage paths ─────────────────────────────────────────────────────────────
if IS_WINDOWS:
    CFG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "learning-terminal")
else:
    CFG_DIR = os.path.expanduser("~/.config/learning-terminal")
CONFIG_FILE  = os.path.join(CFG_DIR, "config.json")
PROGRESS_FILE= os.path.join(CFG_DIR, "progress.json")

def ensure_dirs():
    os.makedirs(CFG_DIR, exist_ok=True)

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_config():
    return load_json(CONFIG_FILE, {"claude_key": "", "openai_key": "", "active_ai": "claude"})

def save_config(cfg):
    save_json(CONFIG_FILE, cfg)

def load_progress():
    default = {"terminal": {}, "vim": {}, "powershell": {}, "tmux": {}}
    p = load_json(PROGRESS_FILE, default)
    if "terminal" not in p: p["terminal"] = {}
    if "vim" not in p: p["vim"] = {}
    if "powershell" not in p: p["powershell"] = {}
    if "tmux" not in p: p["tmux"] = {}
    return p

def save_progress(p):
    save_json(PROGRESS_FILE, p)

# ── Spaced repetition ─────────────────────────────────────────────────────────
INTERVALS = [1, 3, 7, 30, 90]  # days

def mark_learned(ltype: str, lid: str):
    p = load_progress()
    today = date.today().isoformat()
    cnt = 0
    entry = p[ltype].get(lid, {})
    if entry:
        cnt = entry.get("review_count", 0)
    days = INTERVALS[min(cnt, len(INTERVALS)-1)]
    p[ltype][lid] = {
        "learned": True,
        "learned_date": today,
        "review_count": cnt,
        "next_review": (date.today() + timedelta(days=days)).isoformat(),
    }
    save_progress(p)

def update_review(ltype: str, lid: str, correct: bool):
    p = load_progress()
    entry = p[ltype].get(lid, {})
    if not entry:
        return
    if correct:
        cnt = entry.get("review_count", 0) + 1
        days = INTERVALS[min(cnt, len(INTERVALS)-1)]
    else:
        cnt = 0
        days = INTERVALS[0]
    entry["review_count"] = cnt
    entry["next_review"] = (date.today() + timedelta(days=days)).isoformat()
    p[ltype][lid] = entry
    save_progress(p)

def get_due():
    p = load_progress()
    today = date.today().isoformat()
    due = []
    for ltype in ("terminal", "vim", "tmux"):
        for lid, info in p[ltype].items():
            if info.get("learned") and info.get("next_review", "9999") <= today:
                due.append((ltype, lid))
    return due

def is_learned(ltype: str, lid: str) -> bool:
    p = load_progress()
    return p[ltype].get(lid, {}).get("learned", False)

def learned_count(ltype: str) -> int:
    p = load_progress()
    return sum(1 for v in p[ltype].values() if v.get("learned"))

# ── Terminal lessons ───────────────────────────────────────────────────────────
TERMINAL_LESSONS = [
    {
        "id": "pwd",
        "name": "pwd: 현재 위치 확인",
        "summary": "pwd(Print Working Directory) 명령어로 현재 디렉터리 경로를 출력합니다.",
        "content": f"""{CY}{B}  pwd — 현재 위치 확인{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}pwd{R}는 {CY}Print Working Directory{R}의 약자입니다.
  지금 내가 파일시스템의 어디에 있는지 절대경로로 알려줍니다.

  {B}📌 문법{R}
{yl}  $ pwd{R}

  {B}📌 출력 예시{R}
{gr}  /Users/name/Documents{R}

  {B}📌 경로 구조{R}
  {DM}/ (루트){R}
   └─ {DM}Users/{R}
       └─ {DM}name/{R}
           └─ {cy}Documents/{R}  ← 지금 여기

  {B}📌 언제 쓰나요?{R}
  • 현재 위치가 헷갈릴 때 제일 먼저 쓰는 명령어
  • 스크립트 작성 시 절대경로가 필요할 때
  • 다른 명령어 실행 전 위치 확인

  {B}💡 팁{R}
  {DM}  macOS/Linux 어디서나 동일하게 동작합니다.{R}
  {DM}  터미널에서 길을 잃었다면 — pwd 먼저!{R}
""",
        "quizzes": [
            {
                "q": "pwd는 무엇의 약자인가요?",
                "type": "choice",
                "choices": [
                    "Print Working Directory",
                    "Path Write Directory",
                    "Process Work Data",
                    "Present Working Document",
                ],
                "answer": 0,
            },
            {
                "q": "현재 디렉터리 경로를 출력하는 명령어를 입력하세요.",
                "type": "input",
                "answer": "pwd",
                "validate": lambda s: s.strip() == "pwd",
            },
        ],
    },
    {
        "id": "ls",
        "name": "ls: 파일 목록 보기",
        "summary": "ls 명령어로 디렉터리 안의 파일과 폴더 목록을 확인합니다.",
        "content": f"""{CY}{B}  ls — 파일 목록 보기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}ls{R}는 {CY}list{R}의 약자로, 디렉터리 내용을 보여줍니다.

  {B}📌 기본 사용법{R}
{yl}  $ ls{R}          {DM}# 현재 디렉터리{R}
{yl}  $ ls /etc{R}     {DM}# 특정 디렉터리{R}

  {B}📌 주요 옵션{R}
  {gr}ls -l{R}    긴 형식(권한, 크기, 날짜 포함)
  {gr}ls -a{R}    숨김파일 포함 (.으로 시작하는 파일)
  {gr}ls -la{R}   숨김파일 포함 + 긴 형식
  {gr}ls -lh{R}   긴 형식 + 파일크기를 K/M/G 단위로

  {B}📌 ls -la 출력 예시{R}
{DM}  drwxr-xr-x  5 name  staff   160 Mar 20 10:00 .{R}
{DM}  -rw-r--r--  1 name  staff  4096 Mar 19 09:30 notes.txt{R}
{DM}  -rwxr-xr-x  1 name  staff   512 Mar 18 14:00 run.sh{R}

  {B}📌 권한 읽는 법{R}
  {cy}d{R}{gr}rwx{R}{yl}r-x{R}{rd}r-x{R}  →  {cy}d{R}=디렉터리  {gr}rwx{R}=소유자  {yl}r-x{R}=그룹  {rd}r-x{R}=기타

  {B}💡 팁{R}
  {DM}  ls -lh 는 가장 많이 쓰는 조합입니다.{R}
  {DM}  숨김파일(.bashrc, .zshrc 등)을 보려면 -a 옵션 필수!{R}
""",
        "quizzes": [
            {
                "q": "숨김파일 포함 상세 목록을 보는 옵션은?",
                "type": "choice",
                "choices": ["ls -l", "ls -a", "ls -la", "ls -s"],
                "answer": 2,
            },
            {
                "q": "ls의 -h 옵션이 하는 역할은?",
                "type": "choice",
                "choices": [
                    "숨김파일을 표시한다",
                    "파일크기를 K/M/G 단위로 표시한다",
                    "하위 디렉터리도 함께 표시한다",
                    "파일 해시값을 표시한다",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "cd",
        "name": "cd: 디렉터리 이동",
        "summary": "cd 명령어로 원하는 디렉터리로 이동합니다.",
        "content": f"""{CY}{B}  cd — 디렉터리 이동{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}cd{R}는 {CY}Change Directory{R}의 약자입니다.
  터미널에서 폴더를 이동할 때 사용합니다.

  {B}📌 주요 사용법{R}
{yl}  $ cd Documents{R}    {DM}# 하위 폴더로 이동{R}
{yl}  $ cd /etc{R}         {DM}# 절대경로로 이동{R}
{yl}  $ cd ~{R}            {DM}# 홈 디렉터리로 이동 (cd 만 입력해도 됨){R}
{yl}  $ cd ..{R}           {DM}# 한 단계 상위 폴더로 이동{R}
{yl}  $ cd ../..{R}        {DM}# 두 단계 상위 폴더로 이동{R}
{yl}  $ cd -{R}            {DM}# 바로 이전 위치로 돌아가기{R}

  {B}📌 경로 표기{R}
  {gr}절대경로{R}  /Users/name/Documents    (루트 / 부터 시작)
  {gr}상대경로{R}  Documents/projects       (현재 위치 기준)

  {B}📌 실용 예시{R}
{yl}  $ pwd{R}
{gr}  /Users/name{R}
{yl}  $ cd Documents/projects{R}
{yl}  $ pwd{R}
{gr}  /Users/name/Documents/projects{R}
{yl}  $ cd -{R}
{gr}  /Users/name{R}                   {DM}# 이전 위치로 복귀{R}

  {B}💡 팁{R}
  {DM}  Tab 키를 누르면 폴더/파일 이름이 자동완성 됩니다!{R}
""",
        "quizzes": [
            {
                "q": "한 단계 상위 폴더로 이동하는 명령어를 입력하세요.",
                "type": "input",
                "answer": "cd ..",
                "validate": lambda s: s.strip() == "cd ..",
            },
            {
                "q": "cd - 명령어의 역할은?",
                "type": "choice",
                "choices": [
                    "홈 디렉터리로 이동",
                    "루트 디렉터리로 이동",
                    "이전 위치로 돌아가기",
                    "한 단계 위로 이동",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "mkdir_touch",
        "name": "mkdir & touch: 파일/폴더 생성",
        "summary": "mkdir으로 디렉터리를, touch로 빈 파일을 생성합니다.",
        "content": f"""{CY}{B}  mkdir & touch — 파일/폴더 생성{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}mkdir{R} = {CY}Make Directory{R}  |  {B}touch{R} = 파일 생성/타임스탬프 갱신

  {B}📌 mkdir 사용법{R}
{yl}  $ mkdir projects{R}               {DM}# 폴더 생성{R}
{yl}  $ mkdir -p a/b/c{R}              {DM}# 중간 경로 포함 한번에 생성{R}
{yl}  $ mkdir folder1 folder2{R}       {DM}# 여러 폴더 동시 생성{R}

  {B}📌 touch 사용법{R}
{yl}  $ touch hello.txt{R}             {DM}# 빈 파일 생성{R}
{yl}  $ touch a.txt b.txt c.txt{R}     {DM}# 여러 파일 동시 생성{R}
{yl}  $ touch existing.txt{R}          {DM}# 기존 파일은 타임스탬프만 갱신{R}

  {B}📌 mkdir -p 예시{R}
{yl}  $ mkdir -p ~/projects/python/hello{R}
  {DM}  → projects, python, hello 폴더를 한번에 모두 생성{R}
  {DM}  → -p 없이 하면 중간 폴더가 없으면 오류 발생{R}

  {B}📌 실전 조합{R}
{yl}  $ mkdir -p myapp/src myapp/tests{R}
{yl}  $ touch myapp/src/main.py myapp/README.md{R}

  {B}💡 팁{R}
  {DM}  -p 옵션은 "parents"의 뜻으로 부모 디렉터리를 자동 생성합니다.{R}
  {DM}  이미 폴더가 존재해도 오류 없이 넘어갑니다.{R}
""",
        "quizzes": [
            {
                "q": "중간 경로를 포함해 폴더를 한 번에 생성하려면?",
                "type": "choice",
                "choices": ["mkdir -r a/b/c", "mkdir -p a/b/c", "mkdir -m a/b/c", "mkdir -f a/b/c"],
                "answer": 1,
            },
            {
                "q": "hello.txt 파일을 생성하는 명령어를 입력하세요.",
                "type": "input",
                "answer": "touch hello.txt",
                "validate": lambda s: bool(re.match(r"^touch\s+hello\.txt$", s.strip())),
            },
        ],
    },
    {
        "id": "cp",
        "name": "cp: 파일 복사",
        "summary": "cp 명령어로 파일이나 디렉터리를 복사합니다.",
        "content": f"""{CY}{B}  cp — 파일 복사{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}cp{R}는 {CY}copy{R}의 약자입니다. 원본은 그대로 남깁니다.

  {B}📌 기본 문법{R}
{yl}  $ cp 원본 대상{R}

  {B}📌 사용 예시{R}
{yl}  $ cp file.txt backup.txt{R}         {DM}# 파일 복사{R}
{yl}  $ cp file.txt ~/Documents/{R}       {DM}# 다른 디렉터리로 복사{R}
{yl}  $ cp -r myfolder/ backup/{R}        {DM}# 폴더 전체 복사 (-r 필수){R}
{yl}  $ cp -rp myfolder/ backup/{R}       {DM}# 권한/날짜 포함 복사{R}

  {B}📌 주요 옵션{R}
  {gr}cp -r{R}   디렉터리(폴더) 복사 시 필수 (recursive)
  {gr}cp -i{R}   덮어쓰기 전 확인 메시지 표시
  {gr}cp -v{R}   복사 과정을 출력 (verbose)
  {gr}cp -p{R}   타임스탬프, 권한 등 속성 보존

  {B}📌 cp vs mv{R}
  {cy}cp{R}   원본이 {GR}남습니다{R} (복사)
  {cy}mv{R}   원본이 {RD}없어집니다{R} (이동/이름변경)

  {B}💡 팁{R}
  {DM}  폴더를 복사할 때 -r 옵션을 빠뜨리면 오류가 납니다.{R}
  {DM}  중요한 파일 복사 전에는 -i 옵션을 쓰는 것이 안전합니다.{R}
""",
        "quizzes": [
            {
                "q": "폴더를 복사할 때 반드시 필요한 옵션은?",
                "type": "choice",
                "choices": ["-f", "-p", "-r", "-v"],
                "answer": 2,
            },
            {
                "q": "cp와 mv의 차이는?",
                "type": "choice",
                "choices": [
                    "cp는 압축 복사, mv는 일반 복사",
                    "cp는 원본이 남고, mv는 원본이 없어진다",
                    "cp는 폴더만, mv는 파일만 처리",
                    "cp는 느리고, mv는 빠르다",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "mv",
        "name": "mv: 이동/이름 변경",
        "summary": "mv 명령어로 파일을 이동하거나 이름을 변경합니다.",
        "content": f"""{CY}{B}  mv — 이동 / 이름 변경{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}mv{R}는 {CY}move{R}의 약자입니다.
  이동과 이름 변경 모두 mv 하나로 처리합니다.

  {B}📌 기본 문법{R}
{yl}  $ mv 원본 대상{R}

  {B}📌 이름 변경{R}
{yl}  $ mv old.txt new.txt{R}           {DM}# 파일 이름 변경{R}
{yl}  $ mv oldfolder/ newfolder/{R}     {DM}# 폴더 이름 변경{R}

  {B}📌 파일 이동{R}
{yl}  $ mv file.txt ~/Documents/{R}     {DM}# Documents 폴더로 이동{R}
{yl}  $ mv *.log /tmp/{R}              {DM}# 모든 .log 파일 이동{R}

  {B}📌 주요 옵션{R}
  {gr}mv -i{R}   덮어쓰기 전 확인 메시지 표시
  {gr}mv -v{R}   이동 과정을 출력 (verbose)
  {gr}mv -n{R}   같은 이름 파일이 있으면 덮어쓰지 않음

  {B}📌 주의사항{R}
  {rd}  원본 파일은 사라집니다!{R}
  {DM}  mv는 같은 파일시스템 내에서는 즉각 완료됩니다.{R}

  {B}💡 팁{R}
  {DM}  mv -i 옵션으로 덮어쓰기 실수를 방지할 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "old.txt를 new.txt로 이름 변경하는 명령어를 입력하세요.",
                "type": "input",
                "answer": "mv old.txt new.txt",
                "validate": lambda s: bool(re.match(r"^mv\s+old\.txt\s+new\.txt$", s.strip())),
            },
            {
                "q": "mv 명령어 실행 후 원본 파일은?",
                "type": "choice",
                "choices": [
                    "원본이 그대로 남는다",
                    "원본이 없어진다 (이동됨)",
                    "원본이 백업된다",
                    "원본이 압축된다",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "rm",
        "name": "rm: 파일 삭제",
        "summary": "rm 명령어로 파일이나 디렉터리를 삭제합니다. 영구 삭제이므로 주의 필요!",
        "content": f"""{CY}{B}  rm — 파일 삭제{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}rm{R}은 {CY}remove{R}의 약자입니다.
  {RD}{B}  ⚠️  삭제한 파일은 휴지통 없이 영구 삭제됩니다!{R}

  {B}📌 기본 사용법{R}
{yl}  $ rm file.txt{R}             {DM}# 파일 삭제{R}
{yl}  $ rm -i file.txt{R}          {DM}# 삭제 전 확인 (안전!){R}
{yl}  $ rm -r myfolder/{R}         {DM}# 폴더와 내용 전체 삭제{R}

  {B}📌 주요 옵션{R}
  {GR}rm -i{R}   삭제 전 확인 메시지 표시 {gr}← 안전한 선택{R}
  {gr}rm -r{R}   디렉터리 재귀 삭제
  {gr}rm -v{R}   삭제 과정 출력
  {RD}rm -rf{R}  {rd}강제로 모두 삭제 (확인 없음!) ← 매우 위험{R}

  {B}📌 위험 예시{R}
{rd}  $ rm -rf /{R}   {RD}← 절대 실행 금지! 시스템 전체 삭제!{R}
{rd}  $ rm -rf ~/{R}  {RD}← 홈 디렉터리 전체 삭제!{R}

  {B}📌 와일드카드 사용{R}
{yl}  $ rm *.log{R}              {DM}# 모든 .log 파일 삭제{R}
{yl}  $ rm -i *.txt{R}           {DM}# 모든 .txt 파일 하나씩 확인 후 삭제{R}

  {B}💡 팁 — 안전하게 삭제하기{R}
  {DM}  1. rm 전에 ls 로 대상 파일을 먼저 확인하세요.{R}
  {DM}  2. -rf 는 꼭 필요한 경우만 사용하세요.{R}
  {DM}  3. 중요 파일은 삭제 전 백업을 권장합니다.{R}
""",
        "quizzes": [
            {
                "q": "삭제 전 확인 메시지를 표시하는 옵션은?",
                "type": "choice",
                "choices": ["-r", "-f", "-i", "-v"],
                "answer": 2,
            },
            {
                "q": "rm으로 삭제한 파일은?",
                "type": "choice",
                "choices": [
                    "휴지통으로 이동한다",
                    "/tmp 에 임시 보관된다",
                    "영구 삭제된다 (휴지통 없음)",
                    "숨김 파일로 변환된다",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "cat",
        "name": "cat: 파일 내용 보기",
        "summary": "cat 명령어로 파일 내용을 터미널에 출력합니다.",
        "content": f"""{CY}{B}  cat — 파일 내용 보기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}cat{R}은 {CY}concatenate{R}의 약자입니다.
  파일 내용을 출력하거나 여러 파일을 합칠 때 씁니다.

  {B}📌 기본 사용법{R}
{yl}  $ cat file.txt{R}               {DM}# 파일 내용 출력{R}
{yl}  $ cat -n file.txt{R}            {DM}# 줄 번호와 함께 출력{R}
{yl}  $ cat file1.txt file2.txt{R}    {DM}# 두 파일 연속 출력{R}

  {B}📌 파일 합치기 (리다이렉션과 함께){R}
{yl}  $ cat a.txt b.txt > out.txt{R}  {DM}# 두 파일 합쳐서 새 파일 생성{R}
{yl}  $ cat a.txt >> out.txt{R}       {DM}# 파일에 내용 추가(append){R}

  {B}📌 주요 옵션{R}
  {gr}cat -n{R}   모든 줄에 번호 표시
  {gr}cat -b{R}   빈 줄 제외하고 줄 번호 표시
  {gr}cat -A{R}   제어문자를 시각화 (탭=^I, 줄끝=$)

  {B}📌 출력 예시 (cat -n notes.txt){R}
{DM}       1  안녕하세요{R}
{DM}       2  {R}
{DM}       3  오늘 배운 것들{R}
{DM}       4  - pwd, ls, cd{R}

  {B}💡 팁{R}
  {DM}  긴 파일은 cat 대신 less 를 사용하면 스크롤 가능합니다.{R}
  {DM}  less file.txt → 스페이스바로 이동, q로 종료{R}
""",
        "quizzes": [
            {
                "q": "줄 번호와 함께 파일 내용을 보는 명령어는?",
                "type": "choice",
                "choices": ["cat -v file.txt", "cat -n file.txt", "cat -l file.txt", "cat -b file.txt"],
                "answer": 1,
            },
            {
                "q": "cat a.txt b.txt > out.txt 의 결과는?",
                "type": "choice",
                "choices": [
                    "a.txt 내용만 out.txt에 저장",
                    "b.txt 내용만 out.txt에 저장",
                    "두 파일을 합쳐 out.txt에 저장",
                    "out.txt의 내용을 a.txt, b.txt로 분리",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "head_tail",
        "name": "head/tail: 파일 일부 보기",
        "summary": "head로 파일 앞부분, tail로 뒷부분을 봅니다. tail -f로 실시간 모니터링도 가능합니다.",
        "content": f"""{CY}{B}  head / tail — 파일 일부 보기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}head{R}  = 파일의 앞부분 출력
  {B}tail{R}  = 파일의 뒷부분 출력

  {B}📌 head 사용법{R}
{yl}  $ head file.txt{R}             {DM}# 기본: 앞 10줄{R}
{yl}  $ head -n 5 file.txt{R}        {DM}# 앞 5줄{R}
{yl}  $ head -n 20 /etc/hosts{R}     {DM}# /etc/hosts 앞 20줄{R}

  {B}📌 tail 사용법{R}
{yl}  $ tail file.txt{R}             {DM}# 기본: 마지막 10줄{R}
{yl}  $ tail -n 5 file.txt{R}        {DM}# 마지막 5줄{R}
{yl}  $ tail -f /var/log/system.log{R} {DM}# 실시간 모니터링!{R}

  {B}📌 tail -f (follow) — 로그 모니터링{R}
  {cy}  파일에 새 내용이 추가될 때마다 자동으로 출력됩니다.{R}
  {DM}  서버 로그, 애플리케이션 로그 디버깅 시 필수!{R}
{yl}  $ tail -f app.log{R}
{gr}  [2026-03-20 10:00:01] Server started{R}
{gr}  [2026-03-20 10:00:05] Request: GET /api/users{R}
  {DM}  ... (실시간으로 새 줄이 추가됨){R}
  {DM}  Ctrl+C 로 종료{R}

  {B}💡 팁{R}
  {DM}  head -n 1 file.txt → 첫 번째 줄만 빠르게 확인{R}
  {DM}  tail -n 50 -f app.log → 최근 50줄부터 실시간 모니터링{R}
""",
        "quizzes": [
            {
                "q": "로그 파일을 실시간으로 모니터링하는 명령어는?",
                "type": "choice",
                "choices": ["head -r log.txt", "cat -f log.txt", "tail -f log.txt", "tail -r log.txt"],
                "answer": 2,
            },
            {
                "q": "/etc/hosts 파일의 처음 5줄을 보는 명령어를 입력하세요.",
                "type": "input",
                "answer": "head -n 5 /etc/hosts",
                "validate": lambda s: bool(re.match(r"^head\s+-n\s+5\s+/etc/hosts$", s.strip())),
            },
        ],
    },
    {
        "id": "echo",
        "name": "echo: 텍스트 출력",
        "summary": "echo로 텍스트를 출력하고 환경변수 값을 확인하거나 파일에 저장합니다.",
        "content": f"""{CY}{B}  echo — 텍스트 출력{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}echo{R}는 텍스트를 터미널에 출력하는 명령어입니다.
  환경변수 확인, 파일 작성 등 매우 다양하게 활용됩니다.

  {B}📌 기본 사용법{R}
{yl}  $ echo "Hello, World!"{R}
{gr}  Hello, World!{R}

  {B}📌 환경변수 출력{R}
{yl}  $ echo $HOME{R}
{gr}  /Users/name{R}
{yl}  $ echo $USER{R}
{gr}  name{R}
{yl}  $ echo $PATH{R}
{gr}  /usr/local/bin:/usr/bin:/bin{R}

  {B}📌 파일에 저장 (리다이렉션){R}
{yl}  $ echo "안녕" > hello.txt{R}     {DM}# 새 파일 생성 (기존 내용 덮어씀){R}
{yl}  $ echo "세계" >> hello.txt{R}    {DM}# 기존 파일에 내용 추가{R}

  {B}📌 > 와 >> 의 차이{R}
  {RD}>{R}    파일을 {rd}덮어씁니다{R} (기존 내용 삭제!)
  {GR}>>{R}   파일 끝에 {gr}추가합니다{R} (기존 내용 보존)

  {B}📌 -e 옵션으로 이스케이프 처리{R}
{yl}  $ echo -e "줄1\\n줄2\\n줄3"{R}
{gr}  줄1{R}
{gr}  줄2{R}
{gr}  줄3{R}

  {B}💡 팁{R}
  {DM}  환경변수 이름 앞에 $ 를 붙여 값을 확인합니다.{R}
  {DM}  스크립트에서 출력 메시지를 표시할 때 자주 씁니다.{R}
""",
        "quizzes": [
            {
                "q": ">> 와 > 의 차이는?",
                "type": "choice",
                "choices": [
                    ">>는 덮어쓰기, >는 추가",
                    ">>는 추가(append), >는 덮어쓰기(overwrite)",
                    ">>는 파일 생성, >는 파일 삭제",
                    "둘 다 같은 동작을 한다",
                ],
                "answer": 1,
            },
            {
                "q": "현재 로그인된 사용자 이름을 출력하는 명령어는?",
                "type": "choice",
                "choices": ["echo $HOME", "echo $USER", "echo $PATH", "echo $NAME"],
                "answer": 1,
            },
        ],
    },
    {
        "id": "grep",
        "name": "grep: 텍스트 검색",
        "summary": "grep으로 파일이나 출력에서 특정 패턴의 텍스트를 검색합니다.",
        "content": f"""{CY}{B}  grep — 텍스트 검색{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}grep{R}은 {CY}Global Regular Expression Print{R}의 약자입니다.
  파일이나 출력 스트림에서 패턴과 일치하는 줄을 찾습니다.

  {B}📌 기본 사용법{R}
{yl}  $ grep "error" app.log{R}          {DM}# 파일에서 "error" 검색{R}
{yl}  $ grep "hello" *.txt{R}            {DM}# 여러 파일에서 검색{R}

  {B}📌 주요 옵션{R}
  {gr}grep -i{R}   대소문자 무시 (ignore case)
  {gr}grep -n{R}   줄 번호 표시
  {gr}grep -r{R}   하위 디렉터리 포함 재귀 검색
  {gr}grep -v{R}   패턴이 없는 줄만 출력 (invert match)
  {gr}grep -c{R}   매칭된 줄 개수만 출력
  {gr}grep -l{R}   패턴이 있는 파일 이름만 출력

  {B}📌 사용 예시{R}
{yl}  $ grep -i "Error" app.log{R}       {DM}# Error/error/ERROR 모두 검색{R}
{yl}  $ grep -n "TODO" main.py{R}        {DM}# TODO 있는 줄과 번호 표시{R}
{yl}  $ grep -r "password" ~/projects{R} {DM}# 디렉터리 전체 검색{R}
{yl}  $ grep -v "debug" app.log{R}       {DM}# debug 없는 줄만 출력{R}

  {B}📌 파이프와 함께 (자주 씁니다){R}
{yl}  $ ps aux | grep python{R}          {DM}# 실행 중인 python 프로세스 찾기{R}
{yl}  $ history | grep git{R}            {DM}# git 관련 명령어 히스토리{R}

  {B}💡 팁{R}
  {DM}  grep은 정규식(regex)을 지원합니다.{R}
  {DM}  grep -E "^[0-9]" file.txt  → 숫자로 시작하는 줄 찾기{R}
""",
        "quizzes": [
            {
                "q": "대소문자를 무시하고 검색하는 옵션은?",
                "type": "choice",
                "choices": ["-n", "-v", "-i", "-r"],
                "answer": 2,
            },
            {
                "q": "grep -v \"error\" app.log 의 의미는?",
                "type": "choice",
                "choices": [
                    "error 를 포함한 줄만 출력",
                    "error 단어를 삭제",
                    "error 없는 줄만 출력",
                    "error 개수를 세어 출력",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "pipe",
        "name": "파이프(|): 명령어 연결",
        "summary": "파이프(|)로 명령어의 출력을 다른 명령어의 입력으로 연결합니다.",
        "content": f"""{CY}{B}  파이프(|) — 명령어 연결{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}파이프 |{R}는 앞 명령어의 {cy}출력{R}을 뒤 명령어의 {cy}입력{R}으로 전달합니다.
  여러 명령어를 조합해 강력한 데이터 처리를 할 수 있습니다.

  {B}📌 기본 개념{R}
{yl}  $ 명령어1 | 명령어2 | 명령어3{R}

  {B}📌 자주 쓰는 조합{R}
{yl}  $ ls -l | grep ".txt"{R}           {DM}# txt 파일만 목록에서 필터{R}
{yl}  $ ls | wc -l{R}                   {DM}# 현재 디렉터리 파일 개수{R}
{yl}  $ cat log.txt | sort{R}            {DM}# 파일 내용 정렬{R}
{yl}  $ history | grep "git"{R}          {DM}# git 명령어 히스토리 검색{R}
{yl}  $ ps aux | grep python | head -5{R} {DM}# python 프로세스 앞 5개{R}

  {B}📌 파이프 활용 예시 (실무){R}
{yl}  $ cat /etc/passwd | cut -d: -f1 | sort{R}
  {DM}  → 시스템 사용자 목록 정렬{R}

{yl}  $ ls -lh | sort -k5 -rh | head -10{R}
  {DM}  → 용량 큰 파일 상위 10개{R}

  {B}📌 파이프 vs 리다이렉션{R}
  {cy}파이프 |{R}     명령어 → 명령어 (프로세스 연결)
  {cy}리다이렉션 >{R}  명령어 → 파일

  {B}💡 팁{R}
  {DM}  파이프는 개수 제한 없이 연결할 수 있습니다.{R}
  {DM}  각 명령어는 독립적으로 실행되어 병렬 처리됩니다.{R}
""",
        "quizzes": [
            {
                "q": "현재 디렉터리의 파일 개수를 세는 명령어는?",
                "type": "choice",
                "choices": ["ls -c", "ls | count", "ls | wc -l", "ls -n"],
                "answer": 2,
            },
            {
                "q": "파이프(|)의 역할은?",
                "type": "choice",
                "choices": [
                    "파일 내용을 다른 파일로 복사",
                    "앞 명령어의 출력을 뒷 명령어의 입력으로 전달",
                    "두 파일을 하나로 합치기",
                    "명령어를 병렬로 실행",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "wc",
        "name": "wc: 줄/단어/글자 수 세기",
        "summary": "wc 명령어로 파일의 줄 수, 단어 수, 문자 수를 셉니다.",
        "content": f"""{CY}{B}  wc — 줄/단어/글자 수 세기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}wc{R}는 {CY}Word Count{R}의 약자입니다.

  {B}📌 기본 사용법{R}
{yl}  $ wc file.txt{R}
{gr}       5      23     148 file.txt{R}
  {DM}       ↑줄수   ↑단어수  ↑바이트수{R}

  {B}📌 주요 옵션{R}
  {gr}wc -l{R}   줄 수(lines)만 출력
  {gr}wc -w{R}   단어 수(words)만 출력
  {gr}wc -c{R}   바이트 수(bytes)만 출력
  {gr}wc -m{R}   문자 수(characters)만 출력

  {B}📌 사용 예시{R}
{yl}  $ wc -l /etc/hosts{R}
{gr}       35 /etc/hosts{R}            {DM}# 35줄{R}
{yl}  $ cat app.log | wc -l{R}
{gr}       1482{R}                     {DM}# 로그 파일 1482줄{R}

  {B}📌 파이프와 활용{R}
{yl}  $ ls | wc -l{R}                  {DM}# 디렉터리 파일 개수{R}
{yl}  $ grep "error" app.log | wc -l{R} {DM}# 에러 로그 줄 수{R}
{yl}  $ cat *.py | wc -l{R}            {DM}# 전체 Python 코드 줄 수{R}

  {B}💡 팁{R}
  {DM}  wc -l 은 파이프와 함께 개수 세기에 가장 많이 씁니다.{R}
""",
        "quizzes": [
            {
                "q": "줄 수만 출력하는 옵션은?",
                "type": "choice",
                "choices": ["wc -w", "wc -l", "wc -c", "wc -m"],
                "answer": 1,
            },
            {
                "q": "ls | wc -l 의 의미는?",
                "type": "choice",
                "choices": [
                    "ls 명령어의 글자 수 세기",
                    "현재 디렉터리의 파일 개수 세기",
                    "파일 내 줄 수 세기",
                    "ls 명령어 단어 수 세기",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "date_cal",
        "name": "date/cal: 날짜와 달력",
        "summary": "date로 현재 날짜/시간을 확인하고, cal로 달력을 봅니다.",
        "content": f"""{CY}{B}  date / cal — 날짜와 달력{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 date 기본 사용법{R}
{yl}  $ date{R}
{gr}  Fri Mar 20 10:30:00 KST 2026{R}

  {B}📌 date 포맷 지정{R}
{yl}  $ date "+%Y-%m-%d"{R}
{gr}  2026-03-20{R}
{yl}  $ date "+%H:%M:%S"{R}
{gr}  10:30:00{R}
{yl}  $ date "+%Y/%m/%d %H:%M"{R}
{gr}  2026/03/20 10:30{R}

  {B}📌 포맷 코드{R}
  {cy}%Y{R}  4자리 연도   {cy}%m{R}  2자리 월   {cy}%d{R}  2자리 일
  {cy}%H{R}  시(24h)     {cy}%M{R}  분         {cy}%S{R}  초

  {B}📌 cal — 달력 보기{R}
{yl}  $ cal{R}                         {DM}# 이번 달 달력{R}
{yl}  $ cal 3 2026{R}                  {DM}# 2026년 3월 달력{R}
{yl}  $ cal 2026{R}                    {DM}# 2026년 전체 달력{R}

  {B}📌 실용 예시{R}
{yl}  $ echo "백업시각: $(date "+%Y%m%d_%H%M%S")"{R}
{gr}  백업시각: 20260320_103000{R}

{yl}  $ mkdir "backup_$(date +%Y%m%d)"{R}
  {DM}  → 오늘 날짜 폴더 자동 생성{R}

  {B}💡 팁{R}
  {DM}  date 포맷은 스크립트에서 타임스탬프 파일명에 매우 유용합니다.{R}
""",
        "quizzes": [
            {
                "q": "날짜를 2026-03-20 형식으로 출력하는 명령어는?",
                "type": "choice",
                "choices": [
                    'date "+%d-%m-%Y"',
                    'date "+%Y-%m-%d"',
                    'date "+%Y/%m/%d"',
                    'date "+%m-%d-%Y"',
                ],
                "answer": 1,
            },
            {
                "q": "2026년 3월 달력을 보는 명령어를 입력하세요.",
                "type": "input",
                "answer": "cal 3 2026",
                "validate": lambda s: bool(re.match(r"^cal\s+3\s+2026$", s.strip())),
            },
        ],
    },
    {
        "id": "man_history",
        "name": "man/which/history: 도움말과 히스토리",
        "summary": "man으로 명령어 매뉴얼을, which로 명령어 위치를, history로 이전 명령어를 확인합니다.",
        "content": f"""{CY}{B}  man / which / history — 도움말과 히스토리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 man — 매뉴얼 페이지{R}
{yl}  $ man ls{R}                {DM}# ls 명령어 상세 설명{R}
{yl}  $ man grep{R}              {DM}# grep 매뉴얼{R}
  {DM}  스페이스바: 다음 페이지 | b: 이전 | q: 종료{R}
  {DM}  /검색어: 내용 검색 | n: 다음 결과{R}

  {B}📌 which — 명령어 실제 위치 찾기{R}
{yl}  $ which python3{R}
{gr}  /usr/bin/python3{R}
{yl}  $ which git{R}
{gr}  /usr/local/bin/git{R}
  {DM}  PATH에 없는 명령어는 아무것도 출력하지 않습니다.{R}

  {B}📌 history — 명령어 히스토리{R}
{yl}  $ history{R}               {DM}# 전체 히스토리 출력{R}
{yl}  $ history 20{R}            {DM}# 최근 20개만 출력{R}
{yl}  $ history | grep git{R}    {DM}# git 관련 명령어만 검색{R}
{yl}  $ !42{R}                   {DM}# 42번 명령어 재실행{R}
{yl}  $ !!{R}                    {DM}# 바로 이전 명령어 재실행{R}

  {B}📌 Ctrl+R — 히스토리 실시간 검색{R}
  {cy}  터미널에서 Ctrl+R 을 누르면:{R}
{yl}  (reverse-i-search)`': {R}
  {DM}  타이핑하면 일치하는 이전 명령어가 실시간 표시{R}
  {DM}  Enter: 실행 | Ctrl+R: 다음 결과 | Ctrl+C: 취소{R}

  {B}💡 팁{R}
  {DM}  man 을 모를 때 tldr 도구도 유용합니다 (간단한 예시 제공).{R}
  {DM}  history | tail -20 으로 최근 명령어를 빠르게 확인하세요.{R}
""",
        "quizzes": [
            {
                "q": "명령어의 실제 설치 위치를 찾는 명령어는?",
                "type": "choice",
                "choices": ["man", "which", "history", "locate"],
                "answer": 1,
            },
            {
                "q": "히스토리를 실시간으로 검색하는 단축키는?",
                "type": "choice",
                "choices": ["Ctrl+H", "Ctrl+F", "Ctrl+R", "Ctrl+S"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "find",
        "name": "find: 파일/디렉터리 검색",
        "summary": "find 명령어로 파일시스템에서 조건에 맞는 파일을 강력하게 검색합니다.",
        "content": f"""{CY}{B}  find — 파일/디렉터리 검색{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}find{R}는 파일시스템을 탐색하며 조건에 맞는 파일을 찾습니다.
  grep이 파일 내용을 검색한다면, find는 파일 자체를 검색합니다.

  {B}📌 기본 문법{R}
{yl}  $ find [경로] [조건] [동작]{R}

  {B}📌 이름으로 검색{R}
{yl}  $ find . -name "*.py"{R}           {DM}# 현재 폴더에서 .py 파일{R}
{yl}  $ find ~ -name "notes.txt"{R}      {DM}# 홈 디렉터리에서 파일 찾기{R}
{yl}  $ find . -iname "*.TXT"{R}         {DM}# 대소문자 무시 검색{R}

  {B}📌 종류로 검색{R}
{yl}  $ find . -type f{R}               {DM}# 파일만 검색{R}
{yl}  $ find . -type d{R}               {DM}# 디렉터리만 검색{R}

  {B}📌 크기/날짜로 검색{R}
{yl}  $ find . -size +1M{R}             {DM}# 1MB 초과 파일{R}
{yl}  $ find . -mtime -7{R}             {DM}# 7일 이내 수정된 파일{R}
{yl}  $ find . -newer reference.txt{R}  {DM}# reference.txt 보다 최신 파일{R}

  {B}📌 검색 + 동작{R}
{yl}  $ find . -name "*.log" -delete{R}  {DM}# 찾아서 삭제{R}
{yl}  $ find . -name "*.py" -exec wc -l {{}} \\;{R}
  {DM}  → 각 .py 파일의 줄 수 출력{R}

  {B}📌 유용한 조합{R}
{yl}  $ find . -name "*.py" | xargs grep "TODO"{R}
  {DM}  → 모든 .py 파일에서 TODO 검색{R}

  {B}💡 팁{R}
  {DM}  find / -name 처럼 루트부터 찾으면 느립니다. 범위를 좁히세요.{R}
  {DM}  2>/dev/null 을 붙이면 권한 오류 메시지를 숨길 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "현재 디렉터리에서 .py 파일만 찾는 명령어는?",
                "type": "choice",
                "choices": [
                    'grep -r ".py" .',
                    'find . -name "*.py"',
                    'ls -r "*.py"',
                    'locate "*.py"',
                ],
                "answer": 1,
            },
            {
                "q": "find에서 디렉터리만 검색하는 옵션은?",
                "type": "choice",
                "choices": ["-type d", "-type f", "-kind dir", "-d only"],
                "answer": 0,
            },
        ],
    },
    {
        "id": "chmod_chown",
        "name": "chmod/chown: 권한 변경",
        "summary": "chmod로 파일 권한을, chown으로 파일 소유자를 변경합니다.",
        "content": f"""{CY}{B}  chmod / chown — 파일 권한 변경{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}chmod{R} = {CY}change mode{R}  |  {B}chown{R} = {CY}change owner{R}

  {B}📌 권한 구조 복습{R}
{DM}  -rwxr-xr--{R}
   {cy}d{R}{gr}rwx{R}{yl}r-x{R}{rd}r--{R}
   {cy}↑유형{R} {gr}↑소유자{R} {yl}↑그룹{R} {rd}↑기타{R}

  {B}📌 권한 숫자 표기{R}
  {gr}r{R}=4  {gr}w{R}=2  {gr}x{R}=1
  {cy}7{R} = rwx(4+2+1)  {cy}6{R} = rw-(4+2)  {cy}5{R} = r-x(4+1)  {cy}4{R} = r--(4)

  {B}📌 chmod 사용법{R}
{yl}  $ chmod 755 script.sh{R}     {DM}# 소유자 rwx, 그룹/기타 r-x{R}
{yl}  $ chmod 644 data.txt{R}      {DM}# 소유자 rw-, 그룹/기타 r--{R}
{yl}  $ chmod +x run.sh{R}         {DM}# 실행 권한 추가{R}
{yl}  $ chmod -w file.txt{R}       {DM}# 쓰기 권한 제거{R}
{yl}  $ chmod -R 755 myfolder/{R}  {DM}# 폴더 전체 재귀 적용{R}

  {B}📌 chown 사용법{R}
{yl}  $ chown alice file.txt{R}           {DM}# 소유자를 alice로{R}
{yl}  $ chown alice:staff file.txt{R}     {DM}# 소유자:그룹 함께 변경{R}
{yl}  $ sudo chown -R www-data /var/www{R} {DM}# 재귀 소유자 변경{R}

  {B}📌 자주 쓰는 권한 조합{R}
  {cy}755{R}  실행 스크립트, 디렉터리 표준
  {cy}644{R}  일반 파일 표준 (소유자만 쓰기)
  {cy}600{R}  개인 파일 (SSH 키 등)
  {cy}777{R}  {RD}모두에게 모든 권한 — 보안상 위험!{R}

  {B}💡 팁{R}
  {DM}  chmod +x script.sh 후 ./script.sh 로 직접 실행합니다.{R}
  {DM}  SSH 키 파일(.pem)은 chmod 400 이어야 접속 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "chmod 755 에서 소유자의 권한은?",
                "type": "choice",
                "choices": ["r--", "rw-", "r-x", "rwx"],
                "answer": 3,
            },
            {
                "q": "스크립트에 실행 권한을 추가하는 명령어는?",
                "type": "choice",
                "choices": ["chmod +r script.sh", "chmod +w script.sh", "chmod +x script.sh", "chmod +a script.sh"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "ps_kill",
        "name": "ps/kill: 프로세스 관리",
        "summary": "ps로 실행 중인 프로세스를 확인하고, kill로 프로세스를 종료합니다.",
        "content": f"""{CY}{B}  ps / kill — 프로세스 관리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}ps{R}  = {CY}process status{R}  — 실행 중인 프로세스 목록
  {B}kill{R} = 프로세스에 신호 전송 (주로 종료)

  {B}📌 ps 사용법{R}
{yl}  $ ps{R}                    {DM}# 현재 터미널의 프로세스{R}
{yl}  $ ps aux{R}                {DM}# 시스템 전체 프로세스 (상세){R}
{yl}  $ ps aux | grep python{R}  {DM}# python 프로세스만 필터{R}

  {B}📌 ps aux 출력 형식{R}
{DM}  USER  PID  %CPU %MEM  ...  COMMAND{R}
{DM}  name  1234  0.0  0.1  ...  python3 server.py{R}
  {cy}PID{R} = 프로세스 ID (각 프로세스의 고유 번호)

  {B}📌 kill 사용법{R}
{yl}  $ kill 1234{R}             {DM}# PID 1234 프로세스 종료 요청{R}
{yl}  $ kill -9 1234{R}          {DM}# PID 1234 강제 종료{R}
{yl}  $ kill -l{R}               {DM}# 사용 가능한 신호 목록{R}

  {B}📌 주요 신호{R}
  {gr}SIGTERM (15){R}  정상 종료 요청 — 기본값
  {RD}SIGKILL  (9){R}  즉시 강제 종료 — 무시 불가

  {B}📌 killall / pkill{R}
{yl}  $ killall python3{R}       {DM}# 이름으로 모든 프로세스 종료{R}
{yl}  $ pkill -f "server.py"{R}  {DM}# 명령어 패턴으로 종료{R}

  {B}📌 실전 흐름{R}
{yl}  $ ps aux | grep server.py{R}
{gr}  name  5678  2.1  0.5  ... python3 server.py{R}
{yl}  $ kill -9 5678{R}          {DM}# 강제 종료{R}

  {B}💡 팁{R}
  {DM}  kill -9 보다 kill 을 먼저 시도하세요 (clean 종료).{R}
  {DM}  top 또는 htop 명령어로 실시간 프로세스 모니터링도 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "시스템 전체 프로세스를 상세히 보는 명령어는?",
                "type": "choice",
                "choices": ["ps -e", "ps aux", "ps -l", "ps all"],
                "answer": 1,
            },
            {
                "q": "kill -9 와 kill 의 차이는?",
                "type": "choice",
                "choices": [
                    "kill -9 는 9번 반복 종료, kill 은 1번",
                    "kill -9 는 강제 즉시 종료, kill 은 정상 종료 요청",
                    "kill -9 는 그룹 종료, kill 은 단일 종료",
                    "kill -9 는 파일 삭제, kill 은 프로세스 정지",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "tar",
        "name": "tar: 압축과 해제",
        "summary": "tar 명령어로 파일을 묶고 압축하거나, 압축된 아카이브를 해제합니다.",
        "content": f"""{CY}{B}  tar — 압축과 해제{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}tar{R}는 {CY}Tape ARchive{R}의 약자입니다.
  여러 파일을 하나로 묶고, gzip/bzip2로 압축할 수 있습니다.

  {B}📌 압축하기{R}
{yl}  $ tar -czf archive.tar.gz myfolder/{R}   {DM}# gzip 압축{R}
{yl}  $ tar -cjf archive.tar.bz2 myfolder/{R}  {DM}# bzip2 압축 (더 작음){R}
{yl}  $ tar -cf archive.tar myfolder/{R}        {DM}# 압축 없이 묶기만{R}

  {B}📌 해제하기{R}
{yl}  $ tar -xzf archive.tar.gz{R}             {DM}# 현재 위치에 해제{R}
{yl}  $ tar -xzf archive.tar.gz -C /tmp/{R}    {DM}# /tmp 에 해제{R}
{yl}  $ tar -xjf archive.tar.bz2{R}            {DM}# bzip2 해제{R}

  {B}📌 내용 확인 (해제 없이){R}
{yl}  $ tar -tzf archive.tar.gz{R}             {DM}# 목록 보기{R}

  {B}📌 옵션 의미{R}
  {cy}c{R}  create (생성)     {cy}x{R}  extract (해제)
  {cy}z{R}  gzip              {cy}j{R}  bzip2
  {cy}f{R}  파일 지정 (필수)  {cy}v{R}  verbose (진행 출력)
  {cy}t{R}  list (목록)       {cy}C{R}  해제 경로 지정

  {B}📌 기억법 (암기 팁){R}
  {MG}  압축: c z f  →  "czf로 Create!"{R}
  {MG}  해제: x z f  →  "xzf로 eXtract!"{R}

  {B}📌 zip/unzip{R}
{yl}  $ zip -r archive.zip myfolder/{R}
{yl}  $ unzip archive.zip{R}

  {B}💡 팁{R}
  {DM}  -v 옵션을 추가하면 압축/해제 진행 파일 목록이 출력됩니다.{R}
  {DM}  tar.gz 는 리눅스/macOS 표준, .zip 은 Windows 호환에 유리합니다.{R}
""",
        "quizzes": [
            {
                "q": "myfolder를 gzip으로 압축해 archive.tar.gz로 만드는 명령어는?",
                "type": "choice",
                "choices": [
                    "tar -xzf archive.tar.gz myfolder/",
                    "tar -czf archive.tar.gz myfolder/",
                    "tar -tzf archive.tar.gz myfolder/",
                    "tar -czv archive.tar.gz myfolder/",
                ],
                "answer": 1,
            },
            {
                "q": "tar에서 -x 옵션의 의미는?",
                "type": "choice",
                "choices": ["압축 생성 (create)", "파일 지정", "압축 해제 (extract)", "목록 보기 (list)"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "env_export",
        "name": "env/export: 환경변수 관리",
        "summary": "환경변수를 조회하고, export로 변수를 설정하며, .zshrc/.bashrc에 영구 저장합니다.",
        "content": f"""{CY}{B}  env / export — 환경변수 관리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}환경변수{R}란 셸 전체에서 공유되는 이름=값 형태의 변수입니다.
  PATH, HOME, USER 등이 대표적입니다.

  {B}📌 환경변수 조회{R}
{yl}  $ env{R}                   {DM}# 전체 환경변수 목록{R}
{yl}  $ echo $PATH{R}            {DM}# PATH 값 확인{R}
{yl}  $ echo $HOME{R}            {DM}# 홈 디렉터리 경로{R}
{yl}  $ printenv PATH{R}         {DM}# printenv로도 확인 가능{R}

  {B}📌 export — 변수 설정 및 내보내기{R}
{yl}  $ export MY_NAME="Alice"{R}         {DM}# 변수 설정{R}
{yl}  $ echo $MY_NAME{R}
{gr}  Alice{R}
{yl}  $ export PATH="$PATH:/usr/local/bin"{R}  {DM}# PATH에 경로 추가{R}

  {B}📌 export vs 일반 변수{R}
{yl}  $ name="Bob"{R}            {DM}# 현재 셸에서만 유효{R}
{yl}  $ export name="Bob"{R}     {DM}# 자식 프로세스에도 전달됨{R}

  {B}📌 영구 저장 (~/.zshrc 또는 ~/.bashrc){R}
{yl}  $ echo 'export MY_API_KEY="abc123"' >> ~/.zshrc{R}
{yl}  $ source ~/.zshrc{R}       {DM}# 변경사항 즉시 적용{R}

  {B}📌 자주 쓰는 환경변수{R}
  {cy}$PATH{R}    명령어 검색 경로 (: 로 구분)
  {cy}$HOME{R}    홈 디렉터리 (/Users/이름)
  {cy}$USER{R}    현재 사용자 이름
  {cy}$SHELL{R}   사용 중인 셸 경로
  {cy}$EDITOR{R}  기본 편집기

  {B}💡 팁{R}
  {DM}  API 키 같은 민감한 값은 .zshrc에 직접 저장하지 마세요.{R}
  {DM}  source ~/.zshrc 없이 새 터미널 열면 자동 적용됩니다.{R}
""",
        "quizzes": [
            {
                "q": "export 와 일반 변수 할당의 차이는?",
                "type": "choice",
                "choices": [
                    "차이 없음, 같은 동작",
                    "export는 자식 프로세스에도 전달됨",
                    "export는 파일에 저장됨",
                    "export는 읽기 전용 변수를 만듦",
                ],
                "answer": 1,
            },
            {
                "q": ".zshrc에 추가한 export 설정을 현재 터미널에 즉시 반영하려면?",
                "type": "choice",
                "choices": [
                    "restart zsh",
                    "reload ~/.zshrc",
                    "source ~/.zshrc",
                    "exec ~/.zshrc",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "ssh",
        "name": "ssh: 원격 서버 접속",
        "summary": "SSH로 원격 서버에 접속하고, 키 기반 인증을 설정하는 법을 배웁니다.",
        "content": f"""{CY}{B}  ssh — 원격 서버 접속{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}SSH{R}(Secure Shell)는 네트워크를 통해 원격 서버에 안전하게 접속하는 프로토콜입니다.

  {B}📌 기본 접속{R}
{yl}  $ ssh user@host{R}             {DM}# 사용자명@서버주소{R}
{yl}  $ ssh user@192.168.1.10{R}     {DM}# IP 주소로 접속{R}
{yl}  $ ssh -p 2222 user@host{R}     {DM}# 포트 지정 (기본: 22){R}

  {B}📌 SSH 키 생성 & 등록{R}
{yl}  $ ssh-keygen -t ed25519{R}      {DM}# 키 쌍 생성 (권장 알고리즘){R}
{yl}  $ ssh-copy-id user@host{R}      {DM}# 공개키를 서버에 등록{R}
  {DM}  이후 비밀번호 없이 접속 가능!{R}

  {B}📌 파일 전송{R}
{yl}  $ scp file.txt user@host:~/  {R}  {DM}# 로컬→원격 복사{R}
{yl}  $ scp user@host:~/file.txt . {R}  {DM}# 원격→로컬 복사{R}
{yl}  $ scp -r dir/ user@host:~/   {R}  {DM}# 디렉터리 복사{R}

  {B}📌 SSH 설정 파일 (~/.ssh/config){R}
{gr}  Host myserver{R}
{gr}    HostName 192.168.1.10{R}
{gr}    User ubuntu{R}
{gr}    Port 2222{R}
{gr}    IdentityFile ~/.ssh/id_ed25519{R}
{yl}  $ ssh myserver{R}               {DM}# 별칭으로 간단히 접속{R}

  {B}💡 팁{R}
  {DM}  ~/.ssh/config 에 서버 정보를 저장하면 긴 명령어를 반복 입력하지 않아도 됩니다.{R}
""",
        "quizzes": [
            {
                "q": "SSH 키 쌍을 생성하는 명령어는?",
                "type": "choice",
                "choices": [
                    "ssh-create -t ed25519",
                    "ssh-keygen -t ed25519",
                    "ssh-init ed25519",
                    "keygen --type ed25519",
                ],
                "answer": 1,
            },
            {
                "q": "로컬 파일을 원격 서버로 복사하는 명령어 형태는?",
                "type": "choice",
                "choices": [
                    "ssh-copy file.txt user@host:~/",
                    "rsync file.txt user@host:~/",
                    "scp file.txt user@host:~/",
                    "cp file.txt user@host:~/",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "curl",
        "name": "curl: HTTP 요청 보내기",
        "summary": "curl로 API를 호출하고, 파일을 다운로드하고, 헤더/데이터를 전송합니다.",
        "content": f"""{CY}{B}  curl — HTTP 요청 보내기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}curl{R}은 URL로 데이터를 주고받는 범용 명령어입니다.
  API 테스트, 파일 다운로드, 웹 요청 등에 광범위하게 사용됩니다.

  {B}📌 기본 GET 요청{R}
{yl}  $ curl https://example.com{R}           {DM}# 기본 GET{R}
{yl}  $ curl -s https://example.com{R}        {DM}# -s: 진행 표시 숨김 (silent){R}
{yl}  $ curl -o file.html https://example.com{R} {DM}# 파일로 저장{R}
{yl}  $ curl -O https://example.com/file.zip{R}  {DM}# 원래 파일명으로 저장{R}

  {B}📌 자주 쓰는 옵션{R}
{yl}  $ curl -L URL{R}         {DM}# 리다이렉트 따라가기{R}
{yl}  $ curl -I URL{R}         {DM}# 헤더만 보기 (HEAD 요청){R}
{yl}  $ curl -v URL{R}         {DM}# 자세한 요청/응답 내용{R}

  {B}📌 POST 요청 (API 테스트){R}
{yl}  $ curl -X POST URL \\{R}
{yl}       -H "Content-Type: application/json" \\{R}
{yl}       -d '{{"key": "value"}}'{R}

  {B}📌 인증 헤더{R}
{yl}  $ curl -H "Authorization: Bearer TOKEN" URL{R}

  {B}📌 JSON 응답 예쁘게 보기{R}
{yl}  $ curl -s URL | python3 -m json.tool{R}
{yl}  $ curl -s URL | jq .{R}              {DM}# jq 설치 시{R}

  {B}💡 팁{R}
  {DM}  -s (silent) + -o /dev/null + -w "%{{http_code}}" 조합으로 상태코드만 확인 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "curl로 파일을 원래 파일명 그대로 저장하는 옵션은?",
                "type": "choice",
                "choices": ["-o", "-O (대문자)", "-s", "-f"],
                "answer": 1,
            },
            {
                "q": "curl로 JSON 데이터를 POST 전송할 때 필요한 헤더를 지정하는 옵션은?",
                "type": "choice",
                "choices": ["-d", "-X", "-H", "-j"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "sed_awk",
        "name": "sed/awk: 텍스트 처리",
        "summary": "sed로 텍스트를 치환하고, awk로 필드를 추출하는 강력한 텍스트 처리 도구입니다.",
        "content": f"""{CY}{B}  sed / awk — 텍스트 처리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 sed — 스트림 편집기{R}
  파이프나 파일에서 텍스트를 {cy}치환/삭제/삽입{R}합니다.

{yl}  $ sed 's/old/new/' file.txt{R}      {DM}# 각 줄 첫 번째 치환{R}
{yl}  $ sed 's/old/new/g' file.txt{R}     {DM}# g: 모든 일치 치환{R}
{yl}  $ sed -i 's/old/new/g' file.txt{R}  {DM}# -i: 파일 직접 수정{R}
{yl}  $ sed '/pattern/d' file.txt{R}      {DM}# 패턴 있는 줄 삭제{R}
{yl}  $ sed -n '3,7p' file.txt{R}         {DM}# 3~7번째 줄만 출력{R}

  {B}📌 awk — 필드 처리 도구{R}
  공백/탭으로 나뉜 {cy}컬럼(필드)을 추출{R}하거나 가공합니다.
  {cy}$1, $2, ...{R} = 각 필드,  {cy}$NF{R} = 마지막 필드

{yl}  $ awk '{{print $1}}' file.txt{R}      {DM}# 첫 번째 컬럼 출력{R}
{yl}  $ awk '{{print $1, $3}}' file.txt{R}  {DM}# 1, 3번째 컬럼{R}
{yl}  $ awk -F: '{{print $1}}' /etc/passwd{R} {DM}# -F: 구분자를 : 으로{R}
{yl}  $ awk 'NR>1 {{print $2}}' file.txt{R} {DM}# 2번째 줄부터 2번째 컬럼{R}

  {B}📌 실전 조합 예시{R}
{yl}  $ ps aux | awk '{{print $1, $11}}'{R}  {DM}# 프로세스 소유자+이름{R}
{yl}  $ cat log.txt | sed 's/ERROR/[ERROR]/g'{R}

  {B}💡 팁{R}
  {DM}  sed는 줄 단위 치환, awk는 컬럼 추출이 주 용도라고 기억하세요.{R}
""",
        "quizzes": [
            {
                "q": "sed로 파일 안의 모든 'foo'를 'bar'로 파일 직접 수정하는 명령어는?",
                "type": "choice",
                "choices": [
                    "sed 's/foo/bar/' file.txt",
                    "sed -i 's/foo/bar/g' file.txt",
                    "sed --replace foo bar file.txt",
                    "sed 's/foo/bar/1' file.txt",
                ],
                "answer": 1,
            },
            {
                "q": "awk에서 구분자를 콜론(:)으로 지정하는 옵션은?",
                "type": "choice",
                "choices": ["-d :", "-s :", "-F :", "-t :"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "redirect",
        "name": "리디렉션: 입출력 방향 바꾸기",
        "summary": "> >> < 2>&1 /dev/null 등으로 명령어의 입출력 방향을 바꿉니다.",
        "content": f"""{CY}{B}  리디렉션 — 입출력 방향 바꾸기{R}
{DM}  ─────────────────────────────────────────────{R}

  터미널 명령어의 {cy}입력(stdin){R}, {cy}출력(stdout){R}, {cy}오류(stderr){R}를
  파일이나 다른 명령어로 연결할 수 있습니다.

  {B}📌 출력 리디렉션{R}
{yl}  $ echo "hello" > file.txt{R}    {DM}# 파일에 쓰기 (덮어씀){R}
{yl}  $ echo "world" >> file.txt{R}   {DM}# 파일에 추가 (append){R}
{yl}  $ ls /etc > list.txt{R}         {DM}# ls 결과를 파일로{R}

  {B}📌 오류(stderr) 리디렉션{R}
{yl}  $ ls /없는폴더 2> err.txt{R}    {DM}# 오류 메시지만 파일로{R}
{yl}  $ ls /없는폴더 2>&1{R}          {DM}# 오류를 stdout으로 합침{R}
{yl}  $ cmd > out.txt 2>&1{R}         {DM}# stdout + stderr 모두 파일로{R}

  {B}📌 /dev/null — 쓰레기통{R}
{yl}  $ cmd > /dev/null{R}            {DM}# 출력 버리기{R}
{yl}  $ cmd 2> /dev/null{R}           {DM}# 오류 버리기{R}
{yl}  $ cmd > /dev/null 2>&1{R}       {DM}# 모든 출력 버리기{R}

  {B}📌 입력 리디렉션{R}
{yl}  $ sort < names.txt{R}           {DM}# 파일을 입력으로 사용{R}
{yl}  $ wc -l < file.txt{R}           {DM}# 파일 줄 수 세기{R}

  {B}📌 Here-document{R}
{yl}  $ cat << EOF{R}
{yl}  > 여러 줄{R}
{yl}  > 입력{R}
{yl}  > EOF{R}

  {B}💡 팁{R}
  {DM}  > 는 덮어쓰기, >> 는 추가. 중요한 파일에 실수로 > 쓰지 않도록!{R}
  {DM}  2>&1 은 "stderr(2)를 stdout(1)으로 합쳐라" 는 뜻입니다.{R}
""",
        "quizzes": [
            {
                "q": "기존 파일에 내용을 추가(append)하는 리디렉션 기호는?",
                "type": "choice",
                "choices": [">", ">>", "<", "2>&1"],
                "answer": 1,
            },
            {
                "q": "모든 출력(stdout + stderr)을 버리는 명령어 형태는?",
                "type": "choice",
                "choices": [
                    "cmd > /dev/null",
                    "cmd 2> /dev/null",
                    "cmd > /dev/null 2>&1",
                    "cmd < /dev/null",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "alias_func",
        "name": "alias: 나만의 단축 명령어",
        "summary": "alias로 긴 명령어를 짧게 줄이고, ~/.bashrc 또는 ~/.zshrc에 저장해 영구 적용합니다.",
        "content": f"""{CY}{B}  alias — 나만의 단축 명령어{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}alias{R}는 긴 명령어를 짧은 이름으로 등록합니다.
  자주 쓰는 명령어를 단 두 글자로 줄일 수 있어요!

  {B}📌 기본 사용법{R}
{yl}  $ alias ll='ls -lah'{R}          {DM}# ll → ls -lah{R}
{yl}  $ alias gs='git status'{R}       {DM}# gs → git status{R}
{yl}  $ alias ..='cd ..'{R}            {DM}# .. → cd ..{R}
{yl}  $ alias cls='clear'{R}           {DM}# cls → clear{R}

  {B}📌 alias 목록 확인{R}
{yl}  $ alias{R}                       {DM}# 등록된 alias 전체 목록{R}
{yl}  $ alias ll{R}                    {DM}# 특정 alias 확인{R}

  {B}📌 alias 삭제{R}
{yl}  $ unalias ll{R}                  {DM}# 특정 alias 삭제{R}
{yl}  $ unalias -a{R}                  {DM}# 모든 alias 삭제{R}

  {B}📌 영구 저장 (쉘 설정 파일){R}
{yl}  # ~/.zshrc 또는 ~/.bashrc 에 추가{R}
{gr}  alias ll='ls -lah'{R}
{gr}  alias gs='git status'{R}
{gr}  alias gp='git push'{R}
{yl}  $ source ~/.zshrc{R}             {DM}# 즉시 적용{R}

  {B}📌 실용 alias 모음{R}
{gr}  alias grep='grep --color=auto'{R}
{gr}  alias mkdir='mkdir -pv'{R}
{gr}  alias df='df -h'{R}
{gr}  alias free='free -h'{R}

  {B}💡 팁{R}
  {DM}  alias에 공백이 있으면 작은따옴표로 묶으세요.{R}
  {DM}  = 양쪽에 공백이 없어야 합니다: alias ll='ls -la' ✓{R}
""",
        "quizzes": [
            {
                "q": "alias 등록 시 = 양쪽에 공백이 있으면 어떻게 되나요?",
                "type": "choice",
                "choices": [
                    "정상 동작한다",
                    "오류가 발생한다",
                    "공백이 자동으로 제거된다",
                    "alias 이름에 포함된다",
                ],
                "answer": 1,
            },
            {
                "q": "설정한 alias를 영구 적용하려면 어느 파일에 저장해야 하나요?",
                "type": "choice",
                "choices": [
                    "/etc/hosts",
                    "~/.profile만 가능",
                    "~/.bashrc 또는 ~/.zshrc",
                    "/usr/local/bin/alias",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "git_basics",
        "name": "Git 기초: init · add · commit · log",
        "summary": "Git으로 파일 변경을 추적하는 핵심 4단계 — init, add, commit, log를 익힙니다.",
        "content": f"""{CY}{B}  Git 기초 — init · add · commit · log{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Git{R}은 코드 변경 이력을 추적하는 {cy}버전 관리 시스템{R}입니다.
  파일의 "스냅샷"을 찍어 언제든 과거로 되돌아갈 수 있습니다.

  {B}📌 저장소 초기화{R}
{yl}  $ git init{R}                    {DM}# 현재 폴더를 Git 저장소로{R}
{yl}  $ git clone URL{R}               {DM}# 원격 저장소 복사{R}

  {B}📌 변경 확인{R}
{yl}  $ git status{R}                  {DM}# 변경된 파일 목록{R}
{yl}  $ git diff{R}                    {DM}# 변경 내용 상세 비교{R}

  {B}📌 스테이징 (add){R}
{yl}  $ git add file.txt{R}            {DM}# 특정 파일 스테이징{R}
{yl}  $ git add .{R}                   {DM}# 모든 변경 파일 스테이징{R}
{yl}  $ git add -p{R}                  {DM}# 변경 부분별로 선택{R}

  {B}📌 커밋 (commit){R}
{yl}  $ git commit -m "메시지"{R}      {DM}# 스냅샷 저장{R}
{yl}  $ git commit -am "메시지"{R}     {DM}# add + commit 한 번에{R}

  {B}📌 이력 확인 (log){R}
{yl}  $ git log{R}                     {DM}# 전체 커밋 이력{R}
{yl}  $ git log --oneline{R}           {DM}# 한 줄씩 간략히{R}
{yl}  $ git log --oneline --graph{R}   {DM}# 브랜치 그래프 포함{R}

  {B}📌 Git 3단계 흐름{R}
  {DM}  작업 디렉터리{R} → {cy}git add{R} → {DM}스테이지{R} → {cy}git commit{R} → {DM}저장소{R}

  {B}💡 팁{R}
  {DM}  커밋 메시지는 "무엇을 왜 했는지" 명확하게 쓰세요.{R}
  {DM}  git status 를 습관적으로 확인하면 실수를 줄일 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "스테이지에 올린 파일을 저장소에 기록하는 명령어는?",
                "type": "choice",
                "choices": ["git add", "git push", "git commit", "git save"],
                "answer": 2,
            },
            {
                "q": "커밋 이력을 한 줄씩 간략히 보는 명령어를 입력하세요.",
                "type": "input",
                "answer": "git log --oneline",
                "validate": lambda s: s.strip() == "git log --oneline",
            },
        ],
    },
    {
        "id": "git_branch",
        "name": "Git 브랜치: branch · checkout · merge",
        "summary": "Git 브랜치로 독립적인 작업 공간을 만들고, 완료 후 main에 병합합니다.",
        "content": f"""{CY}{B}  Git 브랜치 — branch · checkout · merge{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}브랜치{R}는 main 코드를 건드리지 않고 새 기능을 개발하는 {cy}독립 작업 공간{R}입니다.

  {B}📌 브랜치 생성 & 이동{R}
{yl}  $ git branch feature{R}          {DM}# 브랜치 생성{R}
{yl}  $ git checkout feature{R}        {DM}# 브랜치로 이동{R}
{yl}  $ git checkout -b feature{R}     {DM}# 생성 + 이동 한 번에{R}
{yl}  $ git switch -c feature{R}       {DM}# 최신 방식 (git 2.23+){R}

  {B}📌 브랜치 목록 확인{R}
{yl}  $ git branch{R}                  {DM}# 로컬 브랜치 목록{R}
{yl}  $ git branch -a{R}               {DM}# 원격 포함 전체 목록{R}

  {B}📌 병합 (merge){R}
{yl}  $ git checkout main{R}           {DM}# main으로 돌아오기{R}
{yl}  $ git merge feature{R}           {DM}# feature를 main에 합치기{R}

  {B}📌 브랜치 삭제{R}
{yl}  $ git branch -d feature{R}       {DM}# 병합된 브랜치 삭제{R}
{yl}  $ git branch -D feature{R}       {DM}# 강제 삭제{R}

  {B}📌 일반적인 브랜치 워크플로{R}
  {gr}① main{R} 브랜치에서 {cy}git checkout -b feature/로그인{R}
  {gr}② 기능 개발 후 {cy}git add . && git commit -m "..."{R}
  {gr}③ {cy}git checkout main && git merge feature/로그인{R}
  {gr}④ {cy}git branch -d feature/로그인{R}

  {B}💡 팁{R}
  {DM}  브랜치 이름은 feature/기능명, fix/버그명 형식이 관례입니다.{R}
  {DM}  merge 전 반드시 git status 로 변경사항이 없는지 확인하세요.{R}
""",
        "quizzes": [
            {
                "q": "브랜치를 생성하면서 동시에 그 브랜치로 이동하는 명령어는?",
                "type": "choice",
                "choices": [
                    "git branch -m feature",
                    "git checkout feature",
                    "git checkout -b feature",
                    "git branch --move feature",
                ],
                "answer": 2,
            },
            {
                "q": "feature 브랜치를 main에 병합할 때 main에서 실행하는 명령어는?",
                "type": "choice",
                "choices": [
                    "git pull feature",
                    "git merge feature",
                    "git join feature",
                    "git rebase main",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "df_du",
        "name": "df & du: 디스크 사용량 확인",
        "summary": "df로 전체 디스크 용량을, du로 특정 폴더/파일 크기를 확인합니다.",
        "content": f"""{CY}{B}  df & du — 디스크 사용량 확인{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}df{R} = {CY}Disk Free{R} (전체 디스크 현황)
  {B}du{R} = {CY}Disk Usage{R} (특정 경로 사용량)

  {B}📌 df — 전체 디스크 현황{R}
{yl}  $ df -h{R}                       {DM}# 사람이 읽기 쉬운 단위(G/M/K){R}
{yl}  $ df -h /{R}                     {DM}# 루트 파티션만{R}

  {B}📌 df 출력 예시{R}
{DM}  Filesystem   Size  Used  Avail  Use%  Mounted on{R}
{gr}  /dev/disk1  500G  120G   380G   24%  /{R}

  {B}📌 du — 폴더/파일 크기{R}
{yl}  $ du -sh ~/Documents{R}          {DM}# 폴더 전체 크기 요약{R}
{yl}  $ du -sh *{R}                    {DM}# 현재 폴더 항목별 크기{R}
{yl}  $ du -sh * | sort -h{R}          {DM}# 크기 순 정렬{R}
{yl}  $ du -h --max-depth=1{R}         {DM}# 1단계 깊이만 (Linux){R}
{yl}  $ du -hd 1{R}                    {DM}# 1단계 깊이만 (macOS){R}

  {B}📌 가장 큰 폴더 찾기{R}
{yl}  $ du -sh * | sort -rh | head -10{R}  {DM}# 상위 10개{R}

  {B}📌 df vs du{R}
  {cy}df{R}  파티션 전체 남은 공간 → "전체 디스크가 얼마나 찼나?"
  {cy}du{R}  특정 경로 실제 사용 → "이 폴더가 얼마나 차지하나?"

  {B}💡 팁{R}
  {DM}  -h 옵션은 human-readable. 숫자가 K/M/G로 보기 좋게 나옵니다.{R}
  {DM}  du -sh * | sort -rh 조합으로 용량 잡아먹는 폴더를 빠르게 찾을 수 있어요.{R}
""",
        "quizzes": [
            {
                "q": "현재 폴더의 항목별 크기를 사람이 읽기 쉬운 단위로 보고, 크기순으로 정렬하는 명령어는?",
                "type": "choice",
                "choices": [
                    "df -h | sort",
                    "du -sh * | sort -rh",
                    "ls -lh | sort",
                    "du -a | sort -n",
                ],
                "answer": 1,
            },
            {
                "q": "df와 du의 차이로 올바른 것은?",
                "type": "choice",
                "choices": [
                    "df는 파일 크기, du는 디렉터리 크기만 본다",
                    "df는 파티션 전체 현황, du는 특정 경로 사용량을 본다",
                    "df는 macOS 전용, du는 Linux 전용이다",
                    "차이 없이 동일한 명령어이다",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "sort_uniq",
        "name": "sort & uniq: 정렬과 중복 제거",
        "summary": "sort로 줄을 정렬하고, uniq로 중복 줄을 제거합니다. 조합하면 강력한 텍스트 분석 도구가 됩니다.",
        "content": f"""{CY}{B}  sort & uniq — 정렬과 중복 제거{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}sort{R} — 줄을 정렬  |  {B}uniq{R} — 연속된 중복 줄 처리

  {B}📌 sort 기본 사용법{R}
{yl}  $ sort file.txt{R}            {DM}# 알파벳 오름차순{R}
{yl}  $ sort -r file.txt{R}         {DM}# 내림차순{R}
{yl}  $ sort -n file.txt{R}         {DM}# 숫자 정렬 (10이 9 뒤로){R}
{yl}  $ sort -k2 file.txt{R}        {DM}# 2번째 필드 기준 정렬{R}
{yl}  $ sort -u file.txt{R}         {DM}# 정렬 + 중복 제거 (-u = unique){R}

  {B}📌 uniq 기본 사용법{R}
{yl}  $ sort file.txt | uniq{R}     {DM}# 중복 줄 제거 (sort 먼저 필요){R}
{yl}  $ sort file.txt | uniq -c{R}  {DM}# 각 줄 등장 횟수 출력{R}
{yl}  $ sort file.txt | uniq -d{R}  {DM}# 중복된 줄만 출력{R}
{yl}  $ sort file.txt | uniq -u{R}  {DM}# 유일한 줄만 출력{R}

  {B}📌 실전 조합{R}
{yl}  # 가장 많이 등장하는 단어 TOP 5{R}
{yl}  $ cat log.txt | sort | uniq -c | sort -rn | head -5{R}

{yl}  # 접속한 IP 중 중복 제거 후 몇 개인지{R}
{yl}  $ awk '{{print $1}}' access.log | sort -u | wc -l{R}

  {B}💡 팁{R}
  {DM}  uniq는 인접한 줄만 비교합니다. 반드시 sort 먼저!{R}
  {DM}  sort -u 는 sort | uniq 와 동일하지만 한 명령어로 처리됩니다.{R}
""",
        "quizzes": [
            {
                "q": "uniq -c 옵션이 하는 역할은?",
                "type": "choice",
                "choices": [
                    "중복 줄을 제거한다",
                    "각 줄의 등장 횟수를 앞에 출력한다",
                    "대소문자 구분 없이 중복을 처리한다",
                    "빈 줄을 제거한다",
                ],
                "answer": 1,
            },
            {
                "q": "숫자가 담긴 파일을 내림차순으로 정렬하는 명령어는?",
                "type": "choice",
                "choices": [
                    "sort -d file.txt",
                    "sort -rn file.txt",
                    "sort -z file.txt",
                    "sort --desc file.txt",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "xargs",
        "name": "xargs: 파이프 인수 전달",
        "summary": "xargs는 stdin 입력을 다른 명령어의 인수로 변환합니다. 파이프와 함께 쓰면 강력합니다.",
        "content": f"""{CY}{B}  xargs — 파이프 인수 전달{R}
{DM}  ─────────────────────────────────────────────{R}

  일부 명령어는 파이프로 stdin을 받지 못합니다.
  {B}xargs{R}는 stdin을 {cy}명령어의 인수(argument){R}로 변환해줍니다.

  {B}📌 기본 원리{R}
{yl}  $ echo "file1 file2 file3" | xargs rm{R}
  {DM}  → rm file1 file2 file3 실행{R}

  {B}📌 실전 예시{R}
{yl}  $ find . -name "*.log" | xargs rm{R}        {DM}# 모든 .log 삭제{R}
{yl}  $ find . -name "*.py" | xargs wc -l{R}      {DM}# py 파일 줄 수 합산{R}
{yl}  $ cat urls.txt | xargs curl -O{R}           {DM}# URL 목록 일괄 다운로드{R}
{yl}  $ ls *.txt | xargs grep "error"{R}          {DM}# 여러 파일에서 검색{R}

  {B}📌 주요 옵션{R}
  {gr}xargs -n 1{R}    한 번에 인수 1개씩 전달
  {gr}xargs -P 4{R}    4개 프로세스로 병렬 실행
  {gr}xargs -I{R} {{}}  인수 위치를 직접 지정
  {gr}xargs -p{R}      실행 전 확인 프롬프트

  {B}📌 -I {{}} 위치 지정 예시{R}
{yl}  $ ls *.txt | xargs -I {{}} cp {{}} backup/{R}
  {DM}  → 각 .txt 파일을 backup/ 폴더로 복사{R}

{yl}  $ cat ids.txt | xargs -I {{}} -n1 curl "api.com/user/{{}}" {R}

  {B}💡 팁{R}
  {DM}  파일명에 공백이 있으면 find -print0 | xargs -0 조합을 쓰세요.{R}
  {DM}  -P 옵션으로 병렬 처리하면 대량 작업이 훨씬 빨라집니다.{R}
""",
        "quizzes": [
            {
                "q": "xargs가 하는 역할로 가장 정확한 것은?",
                "type": "choice",
                "choices": [
                    "파이프라인을 병렬로 실행한다",
                    "stdin 입력을 명령어의 인수(argument)로 변환한다",
                    "여러 명령어를 순차 실행한다",
                    "명령어 실행 결과를 파일로 저장한다",
                ],
                "answer": 1,
            },
            {
                "q": "find . -name '*.log' 결과를 rm 명령어에 넘겨 삭제하는 파이프 명령어는?",
                "type": "input",
                "answer": "find . -name '*.log' | xargs rm",
                "validate": lambda s: "xargs" in s and "rm" in s and "find" in s,
            },
        ],
    },
    {
        "id": "rsync",
        "name": "rsync: 효율적인 파일 동기화",
        "summary": "rsync는 변경된 부분만 전송하는 고효율 파일 동기화·백업 도구입니다. 로컬·원격 모두 지원합니다.",
        "content": f"""{CY}{B}  rsync — 효율적인 파일 동기화{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}rsync{R}는 {cy}변경된 파일만{R} 전송하는 스마트 복사 도구입니다.
  cp보다 빠르고, SSH를 통한 원격 동기화도 지원합니다.

  {B}📌 기본 문법{R}
{yl}  $ rsync [옵션] 출발지 목적지{R}

  {B}📌 로컬 동기화{R}
{yl}  $ rsync -av src/ dst/{R}         {DM}# src 내용을 dst에 동기화{R}
{yl}  $ rsync -av --delete src/ dst/{R} {DM}# dst에서 src에 없는 파일 삭제{R}
{yl}  $ rsync -av --dry-run src/ dst/{R} {DM}# 실제 실행 없이 미리보기{R}

  {B}📌 원격 동기화 (SSH){R}
{yl}  $ rsync -avz src/ user@host:~/dst/{R}   {DM}# 로컬 → 원격{R}
{yl}  $ rsync -avz user@host:~/src/ dst/{R}   {DM}# 원격 → 로컬{R}

  {B}📌 주요 옵션{R}
  {gr}rsync -a{R}   archive 모드 (권한·날짜·심볼릭링크 보존)
  {gr}rsync -v{R}   verbose (진행 상황 출력)
  {gr}rsync -z{R}   전송 시 압축 (원격에 유리)
  {gr}rsync -P{R}   진행률 표시 + 중단된 전송 재개
  {gr}rsync -n{R}   dry-run (실제 파일 변경 없음)

  {B}📌 백업 스크립트 예시{R}
{yl}  $ rsync -avz --delete ~/Documents/ user@nas:~/backup/docs/{R}

  {B}📌 rsync vs cp{R}
  {cy}cp{R}   항상 전체 복사, 원격 불가
  {cy}rsync{R} 변경분만 전송, 원격 지원, 중단 재개 가능

  {B}💡 팁{R}
  {DM}  출발지 끝에 / 유무가 중요합니다:{R}
  {DM}  src/  → src 안의 내용을 복사{R}
  {DM}  src   → src 폴더 자체를 복사 (dst/src/ 가 됨){R}
""",
        "quizzes": [
            {
                "q": "rsync에서 전송 전 변경 내용을 미리 확인(실제 실행 없음)하는 옵션은?",
                "type": "choice",
                "choices": ["--preview", "--dry-run", "--check", "--simulate"],
                "answer": 1,
            },
            {
                "q": "rsync -a 옵션(archive 모드)이 보존하는 것은?",
                "type": "choice",
                "choices": [
                    "파일 이름만",
                    "파일 크기만",
                    "권한·날짜·심볼릭링크 등 메타데이터",
                    "파일 내용의 체크섬",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "jq",
        "name": "jq: JSON 처리",
        "summary": "jq는 커맨드라인에서 JSON을 파싱·필터링·변환하는 도구입니다. API 응답 처리에 필수입니다.",
        "content": f"""{CY}{B}  jq — JSON 처리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}jq{R}는 JSON을 커맨드라인에서 다루는 도구입니다.
  {cy}curl API 응답{R}을 보기 좋게 출력하거나 원하는 필드만 추출합니다.

  {B}📌 설치{R}
{yl}  $ brew install jq{R}          {DM}# macOS{R}
{yl}  $ sudo apt install jq{R}      {DM}# Ubuntu/Debian{R}

  {B}📌 기본 사용법{R}
{yl}  $ echo '{{"name":"Alice","age":30}}' | jq '.'{R}  {DM}# 예쁘게 출력{R}
{yl}  $ echo '{{"name":"Alice","age":30}}' | jq '.name'{R}  {DM}# name 필드{R}
{yl}  $ cat data.json | jq '.users[0]'{R}   {DM}# 배열 첫 번째 요소{R}

  {B}📌 자주 쓰는 필터{R}
{yl}  $ jq '.[]'{R}                  {DM}# 배열 전체 순회{R}
{yl}  $ jq '.[].name'{R}             {DM}# 배열 각 요소의 name 필드{R}
{yl}  $ jq 'length'{R}               {DM}# 배열 길이{R}
{yl}  $ jq 'keys'{R}                 {DM}# 객체의 키 목록{R}
{yl}  $ jq 'select(.age > 20)'{R}    {DM}# 조건 필터링{R}

  {B}📌 curl + jq 실전 조합{R}
{yl}  $ curl -s https://api.github.com/users/octocat | jq '.name'{R}
{yl}  $ curl -s URL | jq '.items[] | .title'{R}  {DM}# 배열 내 title만 추출{R}

  {B}📌 유용한 옵션{R}
  {gr}jq -r{R}   raw output (따옴표 없이 출력)
  {gr}jq -c{R}   compact output (한 줄로)
  {gr}jq -e{R}   필터 실패 시 종료코드 1

  {B}💡 팁{R}
  {DM}  jq '.' 만으로도 JSON 예쁘게 출력(pretty-print)이 됩니다.{R}
  {DM}  -r 옵션으로 스크립트에서 값을 변수로 받을 수 있습니다:{R}
  {DM}  name=$(curl -s URL | jq -r '.name'){R}
""",
        "quizzes": [
            {
                "q": "curl API 응답에서 .items 배열의 각 .title만 추출하는 jq 명령어는?",
                "type": "choice",
                "choices": [
                    "jq '.items.title'",
                    "jq '.items[] | .title'",
                    "jq '.items[title]'",
                    "jq 'select(.items.title)'",
                ],
                "answer": 1,
            },
            {
                "q": "jq -r 옵션의 역할은?",
                "type": "choice",
                "choices": [
                    "재귀적으로 모든 키를 출력한다",
                    "원격 URL에서 JSON을 가져온다",
                    "결과를 따옴표 없이 raw 텍스트로 출력한다",
                    "읽기 전용으로 파일을 연다",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "crontab",
        "name": "crontab: 작업 스케줄링",
        "summary": "cron은 특정 시각/주기에 명령어를 자동 실행하는 스케줄러입니다. crontab으로 등록·관리합니다.",
        "content": f"""{CY}{B}  crontab — 작업 스케줄링{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}cron{R}은 지정한 시간에 명령어를 자동으로 실행하는 데몬입니다.
  {B}crontab{R}으로 스케줄을 등록·수정·삭제합니다.

  {B}📌 crontab 관리 명령어{R}
{yl}  $ crontab -e{R}               {DM}# 스케줄 편집 (vim 열림){R}
{yl}  $ crontab -l{R}               {DM}# 현재 스케줄 목록 확인{R}
{yl}  $ crontab -r{R}               {DM}# 모든 스케줄 삭제 (주의!){R}

  {B}📌 cron 표현식 형식{R}
{gr}  분  시  일  월  요일  명령어{R}
{gr}  *   *   *   *   *     command{R}

  {B}📌 각 필드 범위{R}
  {cy}분{R}     0-59
  {cy}시{R}     0-23
  {cy}일{R}     1-31
  {cy}월{R}     1-12
  {cy}요일{R}   0-7  (0,7=일요일, 1=월요일)

  {B}📌 자주 쓰는 패턴{R}
{yl}  0 9 * * *{R}         {DM}# 매일 오전 9시{R}
{yl}  */10 * * * *{R}      {DM}# 10분마다{R}
{yl}  0 0 * * 0{R}         {DM}# 매주 일요일 자정{R}
{yl}  0 9 1 * *{R}         {DM}# 매월 1일 오전 9시{R}
{yl}  30 18 * * 1-5{R}     {DM}# 평일(월~금) 오후 6시 30분{R}

  {B}📌 실전 예시 (crontab -e 에 입력){R}
{gr}  # 매일 자정 백업 스크립트 실행{R}
{gr}  0 0 * * * /home/user/backup.sh >> /var/log/backup.log 2>&1{R}
{gr}  # 5분마다 서버 상태 체크{R}
{gr}  */5 * * * * curl -s http://localhost/health > /dev/null{R}

  {B}💡 팁{R}
  {DM}  crontab -r 은 되돌릴 수 없습니다. 삭제 전 -l 로 백업하세요.{R}
  {DM}  cron 작업의 출력은 기본적으로 이메일로 전송됩니다. 로그 파일로{R}
  {DM}  리디렉션(>> log 2>&1)하는 것이 일반적입니다.{R}
""",
        "quizzes": [
            {
                "q": "매일 오전 9시에 실행되는 cron 표현식은?",
                "type": "choice",
                "choices": [
                    "9 0 * * *",
                    "0 9 * * *",
                    "* 9 * * *",
                    "0 0 9 * *",
                ],
                "answer": 1,
            },
            {
                "q": "crontab -r 명령어가 하는 일은?",
                "type": "choice",
                "choices": [
                    "마지막 cron 작업을 재실행한다",
                    "cron 데몬을 재시작한다",
                    "현재 사용자의 모든 cron 스케줄을 삭제한다",
                    "cron 로그를 출력한다",
                ],
                "answer": 2,
            },
        ],
    },
]

# ── Tmux lessons ───────────────────────────────────────────────────────────────
TMUX_LESSONS = [
    {
        "id": "tmux_intro",
        "name": "tmux 소개 & 기본 개념",
        "summary": "tmux는 터미널 멀티플렉서입니다. 세션, 윈도우, 패인의 3단계 구조를 이해합니다.",
        "content": f"""{CY}{B}  tmux — 소개 & 기본 개념{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}tmux{R}는 {CY}Terminal Multiplexer{R}의 약자입니다.
  하나의 터미널에서 여러 세션/윈도우/패인을 동시에 관리할 수 있습니다.

  {B}📌 3단계 구조{R}
  {cy}Session{R}  최상위 단위. SSH 접속이 끊겨도 유지됨
  {cy}Window{R}   세션 안의 탭. 각각 독립적인 터미널
  {cy}Pane{R}     윈도우 안의 분할 영역. 화면 분할

  {B}📌 tmux 설치 확인{R}
{yl}  $ tmux -V{R}             {DM}# 버전 확인{R}

  {B}📌 tmux 시작/종료{R}
{yl}  $ tmux{R}                {DM}# 새 세션으로 시작{R}
{yl}  $ tmux new -s 이름{R}    {DM}# 이름 있는 세션 시작{R}
{yl}  $ exit{R}                {DM}# 현재 패인/윈도우 종료{R}

  {B}📌 Prefix 키{R}
  tmux의 모든 단축키는 {GR}Ctrl+b{R} (prefix) 를 먼저 누른 뒤 입력합니다.
  {DM}  예: Ctrl+b, 그 다음 d → 세션에서 detach{R}

  {B}💡 핵심 개념{R}
  {DM}  tmux를 쓰면 SSH가 끊겨도 세션이 살아있어 작업을 이어갈 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "tmux에서 모든 단축키 입력 전에 먼저 눌러야 하는 키는?",
                "type": "choice",
                "choices": ["Ctrl+a", "Ctrl+b", "Ctrl+t", "Ctrl+x"],
                "answer": 1,
            },
            {
                "q": "tmux의 3단계 구조를 상위에서 하위 순서로 나열하면?",
                "type": "choice",
                "choices": [
                    "Pane → Window → Session",
                    "Window → Session → Pane",
                    "Session → Window → Pane",
                    "Session → Pane → Window",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "tmux_session",
        "name": "tmux 세션 관리",
        "summary": "세션 생성, 목록 보기, attach/detach, 이름 변경, 종료를 배웁니다.",
        "content": f"""{CY}{B}  tmux — 세션 관리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 세션 생성{R}
{yl}  $ tmux{R}                    {DM}# 이름 없는 세션 시작{R}
{yl}  $ tmux new -s work{R}        {DM}# 'work'라는 세션 시작{R}
{yl}  $ tmux new-session -s dev{R} {DM}# 풀 명령어 형태{R}

  {B}📌 세션 목록 보기{R}
{yl}  $ tmux ls{R}                 {DM}# 실행 중인 세션 목록{R}
{yl}  $ tmux list-sessions{R}      {DM}# 풀 명령어 형태{R}

  {B}📌 세션 들어가기 / 나오기{R}
{yl}  $ tmux attach -t work{R}     {DM}# 'work' 세션에 연결{R}
{yl}  $ tmux a{R}                  {DM}# 마지막 세션에 연결 (단축){R}
  {GR}Ctrl+b, d{R}                 {DM}# 세션에서 detach (세션은 유지){R}

  {B}📌 세션 이름 변경{R}
  {GR}Ctrl+b, ${R}                 {DM}# 현재 세션 이름 변경{R}

  {B}📌 세션 종료{R}
{yl}  $ tmux kill-session -t work{R}  {DM}# 특정 세션 종료{R}
{yl}  $ tmux kill-server{R}           {DM}# 모든 세션 종료{R}
  {GR}Ctrl+b, :{R} kill-session      {DM}# 명령줄로 종료{R}

  {B}💡 팁{R}
  {DM}  detach는 세션을 백그라운드로 보내는 것. 작업이 계속 실행됩니다.{R}
""",
        "quizzes": [
            {
                "q": "'myproject' 라는 이름으로 tmux 세션을 시작하는 명령어는?",
                "type": "choice",
                "choices": [
                    "tmux start myproject",
                    "tmux new -s myproject",
                    "tmux open -n myproject",
                    "tmux session myproject",
                ],
                "answer": 1,
            },
            {
                "q": "tmux 세션에서 나오되 세션을 종료하지 않고 백그라운드로 보내는 단축키는?",
                "type": "choice",
                "choices": ["Ctrl+b, q", "Ctrl+b, x", "Ctrl+b, d", "Ctrl+b, z"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "tmux_window",
        "name": "tmux 윈도우 관리",
        "summary": "윈도우(탭) 생성, 전환, 이름 변경, 닫기를 배웁니다.",
        "content": f"""{CY}{B}  tmux — 윈도우 관리{R}
{DM}  ─────────────────────────────────────────────{R}

  윈도우는 세션 안의 {cy}탭{R}입니다. 브라우저 탭처럼 여러 작업을 전환합니다.

  {B}📌 윈도우 생성 / 닫기{R}
  {GR}Ctrl+b, c{R}   {DM}# 새 윈도우 생성 (create){R}
  {GR}Ctrl+b, &{R}   {DM}# 현재 윈도우 닫기 (확인 필요){R}

  {B}📌 윈도우 전환{R}
  {GR}Ctrl+b, n{R}   {DM}# 다음 윈도우 (next){R}
  {GR}Ctrl+b, p{R}   {DM}# 이전 윈도우 (previous){R}
  {GR}Ctrl+b, 0~9{R} {DM}# 번호로 이동 (0번, 1번...){R}
  {GR}Ctrl+b, w{R}   {DM}# 윈도우 목록에서 선택{R}
  {GR}Ctrl+b, l{R}   {DM}# 마지막으로 사용한 윈도우{R}

  {B}📌 윈도우 이름 변경{R}
  {GR}Ctrl+b, ,{R}   {DM}# 현재 윈도우 이름 변경{R}

  {B}📌 상태바 읽기{R}
  화면 하단 상태바 예시:
  {gr}  [main] 0:bash  1:vim* 2:server-{R}
  {DM}  * = 현재 윈도우,  - = 마지막 사용 윈도우{R}

  {B}💡 팁{R}
  {DM}  윈도우에 의미있는 이름을 붙이면 많은 창 사이에서 길을 잃지 않습니다.{R}
""",
        "quizzes": [
            {
                "q": "tmux에서 새 윈도우를 생성하는 단축키는?",
                "type": "choice",
                "choices": ["Ctrl+b, n", "Ctrl+b, w", "Ctrl+b, c", "Ctrl+b, t"],
                "answer": 2,
            },
            {
                "q": "tmux 상태바에서 * 표시의 의미는?",
                "type": "choice",
                "choices": [
                    "윈도우가 닫힘",
                    "현재 활성 윈도우",
                    "마지막으로 사용한 윈도우",
                    "새로 생성된 윈도우",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "tmux_pane",
        "name": "tmux 패인(Pane) 분할",
        "summary": "화면을 수직/수평으로 분할하고, 패인 사이를 이동하고, 크기를 조절합니다.",
        "content": f"""{CY}{B}  tmux — 패인(Pane) 분할{R}
{DM}  ─────────────────────────────────────────────{R}

  패인은 하나의 윈도우를 {cy}여러 영역으로 분할{R}한 것입니다.

  {B}📌 화면 분할{R}
  {GR}Ctrl+b, %{R}   {DM}# 수직 분할 (좌/우){R}
  {GR}Ctrl+b, "{R}   {DM}# 수평 분할 (위/아래){R}

  {B}📌 패인 이동{R}
  {GR}Ctrl+b, 방향키{R}          {DM}# 방향키로 이동{R}
  {GR}Ctrl+b, o{R}               {DM}# 다음 패인으로 순환{R}
  {GR}Ctrl+b, q, 번호{R}         {DM}# 번호로 이동{R}

  {B}📌 패인 크기 조절{R}
  {GR}Ctrl+b, Alt+방향키{R}      {DM}# 크기 조절{R}
  {GR}Ctrl+b, z{R}               {DM}# 현재 패인 전체화면 토글{R}

  {B}📌 패인 닫기 / 기타{R}
  {GR}Ctrl+b, x{R}               {DM}# 현재 패인 닫기{R}
  {GR}Ctrl+b, !{R}               {DM}# 패인을 새 윈도우로 분리{R}
  {GR}Ctrl+b, Space{R}           {DM}# 레이아웃 자동 변경{R}

  {B}💡 팁{R}
  {DM}  % 는 세로선(수직 분할), " 는 가로선(수평 분할)로 기억하세요.{R}
""",
        "quizzes": [
            {
                "q": "tmux에서 화면을 좌/우(수직)로 분할하는 단축키는?",
                "type": "choice",
                "choices": ['Ctrl+b, "', "Ctrl+b, %", "Ctrl+b, v", "Ctrl+b, h"],
                "answer": 1,
            },
            {
                "q": "현재 패인을 전체화면으로 확대/축소하는 단축키는?",
                "type": "choice",
                "choices": ["Ctrl+b, f", "Ctrl+b, m", "Ctrl+b, z", "Ctrl+b, x"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "tmux_copy",
        "name": "tmux 복사 모드 & 스크롤",
        "summary": "복사 모드(copy mode)로 스크롤하고 텍스트를 선택·복사하는 법을 배웁니다.",
        "content": f"""{CY}{B}  tmux — 복사 모드 & 스크롤{R}
{DM}  ─────────────────────────────────────────────{R}

  tmux 안에서는 마우스 스크롤이 기본 비활성화입니다.
  {cy}복사 모드{R}를 이용해 스크롤하고 텍스트를 복사합니다.

  {B}📌 복사 모드 진입 / 탈출{R}
  {GR}Ctrl+b, [{R}   {DM}# 복사 모드 진입{R}
  {gr}q{R}           {DM}# 복사 모드 탈출{R}
  {gr}Esc{R}         {DM}# 복사 모드 탈출{R}

  {B}📌 복사 모드 내 이동{R}
  {gr}방향키{R}      {DM}# 한 줄씩 이동{R}
  {gr}Page Up/Down{R} {DM}# 페이지 이동{R}
  {gr}Ctrl+u / Ctrl+d{R} {DM}# 반 페이지 이동{R}
  {gr}g / G{R}       {DM}# 맨 위 / 맨 아래로{R}

  {B}📌 텍스트 선택 & 복사 (기본 키바인딩){R}
  {gr}Space{R}       {DM}# 선택 시작{R}
  {gr}Enter{R}       {DM}# 선택 복사 후 복사 모드 종료{R}
  {GR}Ctrl+b, ]{R}   {DM}# 복사한 내용 붙여넣기{R}

  {B}📌 마우스 모드 활성화 (옵션){R}
{yl}  $ tmux set -g mouse on{R}  {DM}# 마우스 스크롤 활성화{R}
  {DM}  또는 ~/.tmux.conf 에 set -g mouse on 추가{R}

  {B}💡 팁{R}
  {DM}  vi 키바인딩 사용자는 .tmux.conf에 setw -g mode-keys vi 를 추가하면{R}
  {DM}  복사 모드에서 v로 선택, y로 복사가 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "tmux에서 복사 모드(스크롤 모드)에 진입하는 단축키는?",
                "type": "choice",
                "choices": ["Ctrl+b, c", "Ctrl+b, s", "Ctrl+b, [", "Ctrl+b, v"],
                "answer": 2,
            },
            {
                "q": "복사 모드에서 복사한 내용을 붙여넣는 단축키는?",
                "type": "choice",
                "choices": ["Ctrl+b, p", "Ctrl+b, ]", "Ctrl+b, v", "Ctrl+b, y"],
                "answer": 1,
            },
        ],
    },
    {
        "id": "tmux_config",
        "name": "tmux 설정 (.tmux.conf)",
        "summary": "~/.tmux.conf 파일로 prefix 키 변경, 마우스, 상태바 등을 커스터마이즈합니다.",
        "content": f"""{CY}{B}  tmux — 설정 (.tmux.conf){R}
{DM}  ─────────────────────────────────────────────{R}

  tmux 설정 파일: {cy}~/.tmux.conf{R}

  {B}📌 설정 파일 적용{R}
{yl}  $ tmux source-file ~/.tmux.conf{R}   {DM}# 재시작 없이 적용{R}
  {GR}Ctrl+b, :{R} source-file ~/.tmux.conf  {DM}# tmux 안에서 적용{R}

  {B}📌 자주 쓰는 설정 예시{R}
{gr}  # Prefix를 Ctrl+a로 변경 (screen 스타일){R}
{yl}  unbind C-b{R}
{yl}  set -g prefix C-a{R}
{yl}  bind C-a send-prefix{R}

{gr}  # 마우스 지원 활성화{R}
{yl}  set -g mouse on{R}

{gr}  # 인덱스를 1부터 시작{R}
{yl}  set -g base-index 1{R}

{gr}  # 256색 지원{R}
{yl}  set -g default-terminal "screen-256color"{R}

{gr}  # 상태바 색상{R}
{yl}  set -g status-bg black{R}
{yl}  set -g status-fg white{R}

  {B}📌 설정 직접 적용 (임시){R}
{yl}  $ tmux set -g mouse on{R}            {DM}# 현재 세션에만 적용{R}

  {B}💡 팁{R}
  {DM}  tmux Plugin Manager(tpm)를 이용하면 플러그인으로 쉽게 확장 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "~/.tmux.conf 변경사항을 tmux 재시작 없이 적용하는 명령어는?",
                "type": "choice",
                "choices": [
                    "tmux reload",
                    "tmux restart",
                    "tmux source-file ~/.tmux.conf",
                    "tmux apply ~/.tmux.conf",
                ],
                "answer": 2,
            },
            {
                "q": ".tmux.conf에서 마우스 지원을 활성화하는 설정은?",
                "type": "choice",
                "choices": [
                    "enable mouse",
                    "set mouse true",
                    "set -g mouse on",
                    "mouse-support on",
                ],
                "answer": 2,
            },
        ],
    },
]

# ── Vim lessons ────────────────────────────────────────────────────────────────
VIM_LESSONS = [
    {
        "id": "vim_intro",
        "name": "Vim 소개 & 나가는 법",
        "summary": "Vim은 터미널 기반 텍스트 에디터입니다. 가장 먼저 배울 것: 어떻게 나가는가!",
        "content": f"""{MG}{B}  Vim — 소개 & 나가는 법{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Vim{R}은 터미널에서 동작하는 강력한 텍스트 에디터입니다.
  처음엔 낯설지만, 익히면 마우스 없이도 빠른 편집이 가능합니다.

  {B}📌 Vim 열기{R}
{yl}  $ vim filename.txt{R}       {DM}# 파일 열기 (없으면 새로 생성){R}
{yl}  $ vim{R}                   {DM}# 빈 파일로 시작{R}

  {B}📌 가장 중요한 것 — 나가는 법{R}
  {RD}  vim을 열었다가 못 나오는 일이 매우 흔합니다!{R}

  먼저 {cy}Esc{R} 키를 누른 뒤:
  {GR}  :q!{R}   {gr}저장 없이 강제 종료{R}  ← 가장 확실한 탈출
  {GR}  :wq{R}   {gr}저장하고 종료{R}
  {GR}  :q{R}    {gr}변경사항 없을 때 종료{R}

  {B}📌 세 가지 주요 모드{R}
  {cy}Normal mode{R}   시작 모드. 커서 이동, 명령 입력
  {cy}Insert mode{R}   텍스트 입력 (-- INSERT -- 표시됨)
  {cy}Command mode{R}  : 를 입력하면 진입 (저장, 종료 등)

  {B}📌 모드 전환 핵심{R}
  일반 → 입력:  {gr}i{R} 누르기
  어디서든 일반:  {gr}Esc{R} 누르기

  {B}💡 팁{R}
  {DM}  헷갈리면 Esc를 여러 번 눌러 Normal mode로 돌아오세요.{R}
  {DM}  모든 명령은 Normal mode에서 시작합니다.{R}
""",
        "quizzes": [
            {
                "q": "Vim에서 저장 없이 강제 종료하는 명령어를 입력하세요.",
                "type": "input",
                "answer": ":q!",
                "validate": lambda s: s.strip() == ":q!",
            },
            {
                "q": "vim 파일을 열었을 때 처음 시작하는 모드는?",
                "type": "choice",
                "choices": ["Insert mode", "Normal mode", "Command mode", "Visual mode"],
                "answer": 1,
            },
        ],
    },
    {
        "id": "vim_modes",
        "name": "Vim 모드 시스템",
        "summary": "Vim의 핵심: Normal, Insert, Command, Visual 모드를 이해합니다.",
        "content": f"""{MG}{B}  Vim — 모드 시스템{R}
{DM}  ─────────────────────────────────────────────{R}

  Vim의 가장 큰 특징은 {cy}모드{R} 기반 편집입니다.
  각 모드마다 키의 의미가 달라집니다.

  {B}📌 Normal Mode (일반 모드){R}
  {cy}  기본 상태. 커서 이동, 삭제, 복사, 붙여넣기.{R}
  진입: {gr}Esc{R} (어느 모드에서도 Normal로 돌아옴)

  {B}📌 Insert Mode (입력 모드){R}
  {cy}  실제 텍스트를 입력하는 모드.{R}
  {DM}  화면 하단에 -- INSERT -- 표시됨{R}
  진입 방법:
  {gr}  i{R}  커서 앞에서 입력 시작
  {gr}  a{R}  커서 뒤에서 입력 시작
  {gr}  o{R}  현재 줄 아래에 새 줄 추가하고 입력
  {gr}  O{R}  현재 줄 위에 새 줄 추가하고 입력
  {gr}  A{R}  현재 줄 맨 끝에서 입력 시작

  {B}📌 Command Mode (명령 모드){R}
  {cy}  :를 입력해서 진입. 저장, 종료, 설정 등.{R}
  진입: {gr}:{R} (Normal mode에서)
  예시: {gr}:w{R} (저장)  {gr}:q{R} (종료)  {gr}:set number{R} (줄번호)

  {B}📌 Visual Mode (시각적 모드){R}
  {cy}  텍스트 범위를 선택하는 모드.{R}
  진입: {gr}v{R} (문자 단위)  {gr}V{R} (줄 단위)  {gr}Ctrl+v{R} (블록)

  {B}📌 모드 전환 흐름{R}
  {DM}  Normal ──i/a/o──→ Insert ──Esc──→ Normal{R}
  {DM}  Normal ────:──→ Command ──Enter──→ Normal{R}
  {DM}  Normal ────v──→ Visual ──Esc──→ Normal{R}
""",
        "quizzes": [
            {
                "q": "아랫줄을 추가하며 입력 모드로 진입하는 키는?",
                "type": "choice",
                "choices": ["i", "a", "o", "A"],
                "answer": 2,
            },
            {
                "q": "Insert 모드에서 Normal 모드로 돌아가는 키를 입력하세요.",
                "type": "input",
                "answer": "Esc",
                "validate": lambda s: s.strip().lower() in ("esc", "escape"),
            },
        ],
    },
    {
        "id": "vim_nav_basic",
        "name": "기본 이동 hjkl",
        "summary": "Vim의 기본 이동키 h j k l 과 숫자 접두사를 배웁니다.",
        "content": f"""{MG}{B}  Vim — 기본 이동: hjkl{R}
{DM}  ─────────────────────────────────────────────{R}

  Vim에서는 방향키 대신 {cy}hjkl{R}을 사용합니다.
  손이 홈 포지션에서 떠나지 않아 훨씬 빠릅니다.

  {B}📌 기본 이동키{R}
  {GR}  h{R}  ←  왼쪽
  {GR}  j{R}  ↓  아래
  {GR}  k{R}  ↑  위
  {GR}  l{R}  →  오른쪽

  {B}📌 기억법{R}
  {DM}  h  j  k  l{R}
  {DM}  ←  ↓  ↑  →{R}
  {DM}  j 는 아래로 내려가는 화살표 모양을 떠올리세요.{R}

  {B}📌 숫자 접두사 (매우 유용!){R}
  {cy}숫자 + 방향키{R}로 여러 줄을 한 번에 이동합니다.
{yl}  5j{R}   5줄 아래로 이동
{yl}  3k{R}   3줄 위로 이동
{yl}  10l{R}  오른쪽으로 10칸 이동
{yl}  7h{R}   왼쪽으로 7칸 이동

  {B}📌 왜 hjkl을 써야 할까?{R}
  {DM}  1. 방향키는 홈 포지션에서 손을 떼야 합니다.{R}
  {DM}  2. hjkl은 손가락이 이미 위에 있습니다.{R}
  {DM}  3. 숫자 접두사와 조합이 자연스럽습니다.{R}
  {DM}  4. 원격 서버에서 방향키가 안 되는 경우도 있습니다.{R}

  {B}💡 팁{R}
  {DM}  처음엔 방향키를 써도 되지만, hjkl 연습을 권장합니다.{R}
  {DM}  5j, 5k 등 숫자 이동을 습관화하면 편집이 빨라집니다.{R}
""",
        "quizzes": [
            {
                "q": "Vim에서 아래로 이동하는 키는?",
                "type": "choice",
                "choices": ["h", "j", "k", "l"],
                "answer": 1,
            },
            {
                "q": "5k 의 의미는?",
                "type": "choice",
                "choices": ["5칸 오른쪽", "5줄 아래로", "5줄 위로", "5번 삭제"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "vim_nav_advanced",
        "name": "단어/줄/파일 이동",
        "summary": "w, b, 0, $, gg, G 등으로 더 빠르게 이동합니다.",
        "content": f"""{MG}{B}  Vim — 단어/줄/파일 이동{R}
{DM}  ─────────────────────────────────────────────{R}

  hjkl 외에 더 빠른 이동 방법들입니다.

  {B}📌 단어 이동{R}
  {GR}  w{R}  다음 단어의 첫 글자로 이동
  {GR}  b{R}  이전 단어의 첫 글자로 이동
  {GR}  e{R}  현재/다음 단어의 끝 글자로 이동
  {cy}  3w{R}  3단어 앞으로 이동 (숫자 조합 가능)

  {B}📌 줄 이동{R}
  {GR}  0{R}  줄의 맨 처음으로 (첫 번째 컬럼)
  {GR}  ^{R}  줄의 첫 번째 비공백 문자로
  {GR}  ${R}  줄의 맨 끝으로
  {GR}  gg{R} 파일의 맨 처음(1번 줄)으로
  {GR}  G{R}  파일의 맨 끝으로
  {GR}  50G{R} 50번 줄로 이동 (숫자G)

  {B}📌 화면 이동{R}
  {gr}  Ctrl+f{R}  한 화면 아래 (forward)
  {gr}  Ctrl+b{R}  한 화면 위 (backward)
  {gr}  Ctrl+d{R}  반 화면 아래
  {gr}  Ctrl+u{R}  반 화면 위

  {B}📌 실전 조합 예시{R}
{yl}  gg{R}   파일 처음으로 이동 후 작업 시작
{yl}  G{R}    파일 끝으로 이동 (새 내용 추가 시)
{yl}  100G{R} 100번 줄로 바로 이동 (오류 위치 찾기)
{yl}  $a{R}   줄 맨끝으로 이동 후 입력 시작

  {B}💡 팁{R}
  {DM}  :set number 로 줄 번호를 켜면 숫자G 이동이 편합니다.{R}
""",
        "quizzes": [
            {
                "q": "파일의 맨 끝으로 이동하는 키는?",
                "type": "choice",
                "choices": ["gg", "G", "$", "0"],
                "answer": 1,
            },
            {
                "q": "줄의 맨 끝으로 이동하는 키는?",
                "type": "choice",
                "choices": ["0", "^", "$", "G"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "vim_insert",
        "name": "Insert 모드 진입 방법",
        "summary": "i, a, o, O, A 등 다양한 Insert 모드 진입 방법을 배웁니다.",
        "content": f"""{MG}{B}  Vim — Insert 모드 진입 방법{R}
{DM}  ─────────────────────────────────────────────{R}

  Insert 모드로 진입하는 방법이 여러 개 있습니다.
  상황에 맞는 키를 사용하면 편집이 훨씬 빨라집니다.

  {B}📌 Insert 모드 진입 키{R}
  {GR}  i{R}  커서 앞(왼쪽)에서 입력 시작         ← 가장 기본
  {GR}  a{R}  커서 뒤(오른쪽)에서 입력 시작
  {GR}  o{R}  현재 줄 아래에 새 줄 만들고 입력    ← 줄 추가
  {GR}  O{R}  현재 줄 위에 새 줄 만들고 입력
  {GR}  A{R}  현재 줄의 맨 끝에서 입력 시작       ← 줄 끝에 추가
  {GR}  I{R}  현재 줄의 맨 앞에서 입력 시작
  {GR}  s{R}  현재 문자 삭제 후 입력 시작
  {GR}  S{R}  현재 줄 전체 삭제 후 입력 시작

  {B}📌 각 키의 차이 — 예시{R}
  {DM}  커서 위치: hel|lo (| = 커서){R}

  {cy}i{R} 입력: {DM}hel(입력)|lo{R}   커서 앞에 삽입
  {cy}a{R} 입력: {DM}hel|(입력)lo{R}   커서 뒤에 삽입
  {cy}A{R} 입력: {DM}hello(입력)|{R}   줄 끝에 삽입

  {B}📌 실전 활용{R}
  {DM}  줄 끝에 ; 추가하기:{R}  {gr}A{R} → {gr};{R} → {gr}Esc{R}
  {DM}  새 줄 추가하기:{R}      {gr}o{R} → 내용 입력 → {gr}Esc{R}
  {DM}  줄 맨 앞에 추가:{R}     {gr}I{R} → 내용 입력 → {gr}Esc{R}

  {B}💡 팁{R}
  {DM}  i와 a는 한 글자 차이이지만, 자주 쓰는 상황이 다릅니다.{R}
  {DM}  o는 새 줄 추가에 매우 유용합니다.{R}
""",
        "quizzes": [
            {
                "q": "현재 줄의 맨 끝에서 입력을 시작하는 키는?",
                "type": "choice",
                "choices": ["a", "i", "A", "O"],
                "answer": 2,
            },
            {
                "q": "아래에 새 줄을 추가하고 입력 모드로 진입하는 키는?",
                "type": "choice",
                "choices": ["i", "a", "O", "o"],
                "answer": 3,
            },
        ],
    },
    {
        "id": "vim_save_quit",
        "name": "저장과 종료",
        "summary": ":w, :q, :wq, ZZ 등 저장과 종료 방법 모두 배우기.",
        "content": f"""{MG}{B}  Vim — 저장과 종료{R}
{DM}  ─────────────────────────────────────────────{R}

  Vim 에서 저장과 종료는 {cy}Command mode{R}에서 합니다.
  {DM}  먼저 Esc 를 눌러 Normal mode로 이동하세요.{R}

  {B}📌 저장 명령어{R}
  {GR}  :w{R}            현재 파일 저장 (write)
  {GR}  :w filename{R}   다른 이름으로 저장
  {GR}  :w!{R}           강제 저장 (읽기전용 파일에)

  {B}📌 종료 명령어{R}
  {GR}  :q{R}    변경 사항 없을 때 종료
  {GR}  :q!{R}   변경 사항 무시하고 강제 종료
  {GR}  :wq{R}   저장하고 종료              ← 가장 많이 씀
  {GR}  :x{R}    변경 있을 때만 저장 후 종료 (:wq 와 유사)

  {B}📌 단축키 (Normal mode에서){R}
  {GR}  ZZ{R}   저장하고 종료 (:wq 와 동일)
  {GR}  ZQ{R}   저장 없이 종료 (:q! 와 동일)

  {B}📌 여러 파일 종료{R}
  {gr}  :qa{R}   열린 모든 파일 종료
  {gr}  :wqa{R}  열린 모든 파일 저장 후 종료
  {gr}  :qa!{R}  모든 파일 강제 종료

  {B}📌 긴급 탈출 요약{R}
  {RD}  갇혔다 싶으면:{R}
  {GR}  Esc → :q! → Enter{R}

  {B}💡 팁{R}
  {DM}  :wq 와 ZZ 는 동일하지만 :wq 가 더 명시적입니다.{R}
  {DM}  :x 는 파일이 변경되지 않았으면 타임스탬프를 바꾸지 않습니다.{R}
""",
        "quizzes": [
            {
                "q": "저장하고 종료하는 명령어는?",
                "type": "choice",
                "choices": [":q!", ":w", ":wq", ":x!"],
                "answer": 2,
            },
            {
                "q": "ZZ와 같은 역할을 하는 명령어는?",
                "type": "choice",
                "choices": [":q!", ":w", ":x", ":wq"],
                "answer": 3,
            },
        ],
    },
    {
        "id": "vim_delete",
        "name": "삭제 명령어",
        "summary": "x, dd, dw, d$ 등 Vim의 다양한 삭제 명령어를 배웁니다.",
        "content": f"""{MG}{B}  Vim — 삭제 명령어{R}
{DM}  ─────────────────────────────────────────────{R}

  Vim의 삭제 명령어는 Normal mode에서 사용합니다.
  삭제된 내용은 {cy}레지스터{R}에 저장되어 붙여넣기 가능합니다.

  {B}📌 기본 삭제{R}
  {GR}  x{R}   커서 위치의 글자 하나 삭제
  {GR}  X{R}   커서 앞(왼쪽) 글자 하나 삭제 (Backspace)

  {B}📌 줄 삭제{R}
  {GR}  dd{R}  현재 줄 전체 삭제            ← 가장 많이 씀
  {GR}  3dd{R} 현재 줄부터 3줄 삭제
  {GR}  D{R}   커서부터 줄 끝까지 삭제 (= d$)

  {B}📌 단어/범위 삭제{R}
  {GR}  dw{R}  커서부터 다음 단어 앞까지 삭제
  {GR}  db{R}  커서부터 이전 단어 앞까지 삭제
  {GR}  d${R}  커서부터 줄 끝까지 삭제
  {GR}  d0{R}  커서부터 줄 처음까지 삭제
  {GR}  dgg{R} 커서부터 파일 처음까지 삭제
  {GR}  dG{R}  커서부터 파일 끝까지 삭제

  {B}📌 숫자 조합{R}
{yl}  3dd{R}  → 현재 줄 포함 3줄 삭제
{yl}  5x{R}   → 5글자 삭제
{yl}  2dw{R}  → 2단어 삭제

  {B}💡 팁{R}
  {DM}  dd로 삭제한 줄은 p(붙여넣기)로 되살릴 수 있습니다.{R}
  {DM}  u(undo)로 삭제를 취소할 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "현재 줄을 삭제하는 명령어는?",
                "type": "choice",
                "choices": ["d", "x", "dd", "dl"],
                "answer": 2,
            },
            {
                "q": "3dd 의 의미는?",
                "type": "choice",
                "choices": ["d를 3번 누름", "3번째 줄로 이동", "3줄 삭제", "3글자 삭제"],
                "answer": 2,
            },
        ],
    },
    {
        "id": "vim_yank",
        "name": "복사와 붙여넣기",
        "summary": "yy, yw, p, P로 Vim에서 텍스트를 복사하고 붙여넣습니다.",
        "content": f"""{MG}{B}  Vim — 복사와 붙여넣기{R}
{DM}  ─────────────────────────────────────────────{R}

  Vim에서 복사를 {cy}yank{R}라고 부릅니다. (y 키 사용)
  dd/dw 등 삭제 명령도 레지스터에 저장되어 붙여넣기 가능합니다!

  {B}📌 복사 (yank){R}
  {GR}  yy{R}  현재 줄 복사             ← 가장 많이 씀
  {GR}  3yy{R} 현재 줄부터 3줄 복사
  {GR}  yw{R}  커서부터 단어 복사
  {GR}  y${R}  커서부터 줄 끝까지 복사
  {GR}  yG{R}  커서부터 파일 끝까지 복사

  {B}📌 붙여넣기 (paste){R}
  {GR}  p{R}   커서 뒤(아래)에 붙여넣기   ← 줄 복사시: 아래줄에 붙여넣기
  {GR}  P{R}   커서 앞(위)에 붙여넣기    ← 줄 복사시: 위줄에 붙여넣기

  {B}📌 p와 P의 차이{R}
  {DM}  줄(yy/dd) 붙여넣기:{R}
  {cy}  p{R}  커서 줄 아래에 붙여넣기
  {cy}  P{R}  커서 줄 위에 붙여넣기
  {DM}  글자/단어 붙여넣기:{R}
  {cy}  p{R}  커서 오른쪽에 붙여넣기
  {cy}  P{R}  커서 왼쪽에 붙여넣기

  {B}📌 실전 — 줄 이동 방법{R}
{yl}  dd{R}  → 줄 삭제(레지스터 저장)
{yl}  이동{R} → 원하는 위치로 이동
{yl}  p{R}   → 아래에 붙여넣기

  {B}💡 팁{R}
  {DM}  5yy 로 5줄 복사 후 p로 붙여넣기 = 5줄 복제{R}
  {DM}  Visual 모드(v)로 선택 후 y로 복사하면 정확한 범위 복사!{R}
""",
        "quizzes": [
            {
                "q": "현재 줄을 복사하는 명령어는?",
                "type": "choice",
                "choices": ["y", "yy", "yw", "cy"],
                "answer": 1,
            },
            {
                "q": "p와 P의 차이는?",
                "type": "choice",
                "choices": [
                    "p는 전체 복사, P는 부분 복사",
                    "p는 커서 뒤/아래에, P는 커서 앞/위에 붙여넣기",
                    "p는 줄 복사, P는 단어 복사",
                    "p는 원본 유지, P는 원본 삭제",
                ],
                "answer": 1,
            },
        ],
    },
    {
        "id": "vim_undo",
        "name": "실행취소 / 재실행",
        "summary": "u로 실행취소, Ctrl+r로 재실행, .으로 마지막 명령 반복합니다.",
        "content": f"""{MG}{B}  Vim — 실행취소 / 재실행{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 실행취소 / 재실행{R}
  {GR}  u{R}        실행취소 (undo)          ← Normal mode에서
  {GR}  Ctrl+r{R}   재실행 (redo)
  {GR}  U{R}        현재 줄의 모든 변경 취소

  {B}📌 반복 실행 (매우 유용!){R}
  {GR}  .{R}  (점) 마지막 편집 명령 반복

  {B}📌 . (점) 명령어 — 실전 예시{R}
  {cy}  상황: 여러 줄에 같은 작업을 반복해야 할 때{R}

{yl}  dd{R}   {DM}# 한 줄 삭제{R}
{yl}  j.{R}   {DM}# 다음 줄로 이동 후 같은 삭제 반복{R}
{yl}  j.{R}   {DM}# 또 반복{R}

{yl}  A;Esc{R}  {DM}# 줄 끝에 ; 추가{R}
{yl}  j.{R}    {DM}# 다음 줄도 ; 추가{R}

  {B}📌 undo 횟수{R}
  {DM}  Vim은 기본적으로 무제한 undo를 지원합니다.{R}
  {DM}  .vimrc에 set undofile 로 파일 종료 후에도 undo 가능!{R}

  {B}📌 실수 복구 예시{R}
{yl}  dd{R}    {DM}# 실수로 줄 삭제{R}
{yl}  u{R}     {DM}# 즉시 취소 → 줄 복원{R}
{yl}  Ctrl+r{R} {DM}# 다시 삭제로{R}

  {B}💡 팁{R}
  {DM}  . 명령어는 Vim 숙련자가 가장 애용하는 기능 중 하나입니다.{R}
  {DM}  반복 작업이 있다면 항상 . 을 활용할 수 있는지 생각해보세요.{R}
""",
        "quizzes": [
            {
                "q": "실행취소 키를 입력하세요.",
                "type": "input",
                "answer": "u",
                "validate": lambda s: s.strip() == "u",
            },
            {
                "q": "마지막 명령을 반복하는 키는?",
                "type": "choice",
                "choices": ["r", "R", ".", ","],
                "answer": 2,
            },
        ],
    },
    {
        "id": "vim_search",
        "name": "검색",
        "summary": "/로 앞으로, ?로 뒤로 검색. n/N으로 다음/이전 결과로 이동합니다.",
        "content": f"""{MG}{B}  Vim — 검색{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 검색 명령어{R}
  {GR}  /pattern{R}   앞 방향으로 검색 (위에서 아래)
  {GR}  ?pattern{R}   뒤 방향으로 검색 (아래에서 위)
  {GR}  n{R}          같은 방향으로 다음 결과
  {GR}  N{R}          반대 방향으로 다음 결과
  {GR}  *{R}          커서 아래 단어를 앞 방향으로 검색
  {GR}  #{R}          커서 아래 단어를 뒤 방향으로 검색

  {B}📌 기본 검색 사용법{R}
{yl}  /error{R}    {DM}# "error"를 앞으로 검색{R}
  {DM}  → 첫 번째 결과로 커서 이동{R}
{yl}  n{R}        {DM}# 다음 "error"로 이동{R}
{yl}  N{R}        {DM}# 이전 "error"로 이동{R}
{yl}  /Error\\c{R} {DM}# 대소문자 무시 검색{R}

  {B}📌 하이라이트 제거{R}
  {GR}  :noh{R}   검색 하이라이트 제거 (no highlight)
  {DM}  검색 결과 형광펜 표시를 없앨 때{R}

  {B}📌 검색 + 이동 조합{R}
{yl}  /function{R}  {DM}# function 검색{R}
{yl}  n{R}          {DM}# 다음 function으로 이동{R}
{yl}  .{R}          {DM}# 그 자리에서 마지막 편집 반복{R}

  {B}📌 설정 (편리하게){R}
{yl}  :set hlsearch{R}   {DM}# 검색 결과 하이라이트 켜기{R}
{yl}  :set incsearch{R}  {DM}# 타이핑 중 실시간 검색{R}

  {B}💡 팁{R}
  {DM}  * 는 커서 단어를 바로 검색해 매우 편합니다.{R}
  {DM}  :set ignorecase 로 기본 대소문자 무시 검색 설정 가능.{R}
""",
        "quizzes": [
            {
                "q": '"error"를 검색하는 명령어를 입력하세요.',
                "type": "input",
                "answer": "/error",
                "validate": lambda s: s.strip() == "/error",
            },
            {
                "q": "검색 후 다음 결과로 이동하는 키는?",
                "type": "choice",
                "choices": ["m", "n", "N", "/"],
                "answer": 1,
            },
        ],
    },
    {
        "id": "vim_replace",
        "name": "치환 (찾기/바꾸기)",
        "summary": ":s/a/b/g 로 현재 줄, :%s/a/b/g 로 파일 전체를 치환합니다.",
        "content": f"""{MG}{B}  Vim — 치환 (찾기/바꾸기){R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 기본 치환 문법{R}
  {cy}  :[범위]s/찾을것/바꿀것/[플래그]{R}

  {B}📌 범위별 치환{R}
  {GR}  :s/a/b/{R}      현재 줄의 첫 번째 a → b
  {GR}  :s/a/b/g{R}     현재 줄의 모든 a → b
  {GR}  :%s/a/b/g{R}    파일 전체의 모든 a → b      ← 가장 많이 씀
  {GR}  :%s/a/b/gc{R}   파일 전체, 하나씩 확인하며 치환
  {GR}  :5,10s/a/b/g{R} 5~10번 줄에서 치환

  {B}📌 플래그(Flag) 의미{R}
  {cy}  g{R}  global — 줄 내 모든 패턴 치환 (없으면 첫 번째만)
  {cy}  c{R}  confirm — 하나씩 확인하며 치환 (y/n/a/q)
  {cy}  i{R}  ignore case — 대소문자 무시
  {cy}  I{R}  대소문자 구분 (기본)

  {B}📌 실전 예시{R}
{yl}  :%s/foo/bar/g{R}     {DM}# 파일 전체 foo → bar{R}
{yl}  :%s/print(/print3(/g{R} {DM}# Python 2→3 변환{R}
{yl}  :%s/\t/    /g{R}     {DM}# 탭을 스페이스 4개로{R}
{yl}  :%s/  *$//g{R}       {DM}# 줄 끝 공백 제거{R}
{yl}  :%s/old/new/gc{R}    {DM}# 하나씩 확인: y=교체, n=건너뜀, a=전체, q=중단{R}

  {B}💡 팁{R}
  {DM}  치환 전 :%s/foo/bar/gn 으로 개수만 먼저 확인 가능.{R}
  {DM}  정규식을 지원하므로 복잡한 패턴 치환도 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "파일 전체에서 foo를 bar로 치환하는 명령어는?",
                "type": "choice",
                "choices": [":s/foo/bar/g", ":%s/foo/bar/", ":%s/foo/bar/g", ":s/foo/bar/"],
                "answer": 2,
            },
            {
                "q": ":%s/a/b/gc 에서 c 플래그의 의미는?",
                "type": "choice",
                "choices": [
                    "대소문자 무시",
                    "현재 줄만 치환",
                    "하나씩 확인하며 치환",
                    "취소(cancel) 옵션",
                ],
                "answer": 2,
            },
        ],
    },
    {
        "id": "vim_tips",
        "name": "실용 팁 & 치트시트",
        "summary": ":set number, 들여쓰기, 자동완성 등 실용적인 Vim 팁 모음.",
        "content": f"""{MG}{B}  Vim — 실용 팁 & 치트시트{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}📌 유용한 설정{R}
{yl}  :set number{R}     줄 번호 표시 켜기
{yl}  :set nonumber{R}   줄 번호 끄기
{yl}  :set paste{R}      붙여넣기 모드 (들여쓰기 자동 방지)
{yl}  :set expandtab{R}  탭을 스페이스로 변환
{yl}  :syntax on{R}      문법 강조 켜기

  {B}📌 들여쓰기{R}
  {GR}  >>{R}  현재 줄 들여쓰기 (indent)
  {GR}  <<{R}  현재 줄 내어쓰기 (outdent)
  {GR}  3>>{R} 현재 줄부터 3줄 들여쓰기
  {GR}  ={R}   Visual 선택 범위 자동 들여쓰기

  {B}📌 자동완성{R}
  {GR}  Ctrl+n{R}  (Insert 모드) 다음 자동완성 후보
  {GR}  Ctrl+p{R}  이전 자동완성 후보

  {B}📌 .vimrc 기본 설정 예시{R}
{DM}  ~/.vimrc 파일을 만들어 저장하면 항상 적용됩니다:{R}
{yl}  set number          " 줄 번호{R}
{yl}  set expandtab       " 탭 → 스페이스{R}
{yl}  set tabstop=4       " 탭 크기 4칸{R}
{yl}  set shiftwidth=4    " 들여쓰기 4칸{R}
{yl}  syntax on           " 문법 강조{R}
{yl}  set hlsearch        " 검색 강조{R}

  {B}📌 전체 치트시트 요약{R}
  {cy}이동{R}    h j k l  |  w b  |  0 $ gg G
  {cy}입력{R}    i a o O A
  {cy}삭제{R}    x dd dw d$
  {cy}복사{R}    yy yw y$  |  p P
  {cy}취소{R}    u  Ctrl+r  |  .
  {cy}검색{R}    /pat ?pat  |  n N
  {cy}저장{R}    :w :wq :q! ZZ
  {cy}치환{R}    :%s/a/b/g

  {B}💡 팁{R}
  {DM}  .vimrc에 set number 를 넣어두면 항상 줄 번호가 표시됩니다.{R}
""",
        "quizzes": [
            {
                "q": "줄 번호를 표시하는 명령어는?",
                "type": "choice",
                "choices": [":set line", ":set number", ":show number", ":line on"],
                "answer": 1,
            },
            {
                "q": ".vimrc에서 줄 번호를 항상 표시하는 설정을 입력하세요.",
                "type": "input",
                "answer": "set number",
                "validate": lambda s: "set number" in s,
            },
        ],
    },
]

# ── PowerShell lessons ─────────────────────────────────────────────────────────
POWERSHELL_LESSONS = [
    {
        "id": "ps_location",
        "name": "Get-Location: 현재 위치 확인",
        "summary": "Get-Location(pwd)으로 현재 작업 디렉터리를 확인합니다.",
        "content": f"""{CY}{B}  Get-Location — 현재 위치 확인{R}
{DM}  ─────────────────────────────────────────────{R}

  PowerShell에서 현재 위치를 확인할 때 {B}Get-Location{R}을 사용합니다.
  Unix의 {cy}pwd{R}와 동일한 역할을 합니다.

  {B}📌 기본 사용법{R}
{yl}  PS> Get-Location{R}
{gr}  Path
  ----
  C:\\Users\\name\\Documents{R}

  {B}📌 짧은 별칭(alias){R}
{yl}  PS> pwd{R}   ← Unix 스타일로도 동작!
{yl}  PS> gl{R}    ← 더 짧은 별칭

  {B}📌 경로 구조 (Windows){R}
  {DM}C:\\ (드라이브 루트){R}
   └─ {DM}Users\\{R}
       └─ {DM}name\\{R}
           └─ {cy}Documents\\{R}  ← 지금 여기

  {B}💡 팁{R}
  {DM}  PowerShell에서는 Unix 별칭(pwd, ls, cd)도 대부분 동작합니다.{R}
  {DM}  하지만 원래 cmdlet 이름을 익혀두면 더 강력하게 활용할 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "PowerShell에서 현재 디렉터리를 확인하는 cmdlet은?",
                "type": "choice",
                "choices": [
                    "Get-Location",
                    "Show-Directory",
                    "Print-Path",
                    "Current-Dir",
                ],
                "answer": 0,
            },
            {
                "q": "Get-Location의 짧은 별칭(alias)을 입력하세요.",
                "type": "input",
                "answer": "pwd",
                "validate": lambda s: s.strip().lower() in ("pwd", "gl"),
            },
        ],
    },
    {
        "id": "ps_ls",
        "name": "Get-ChildItem: 파일 목록 보기",
        "summary": "Get-ChildItem(ls/dir)으로 디렉터리 내용을 확인합니다.",
        "content": f"""{CY}{B}  Get-ChildItem — 파일 목록 보기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Get-ChildItem{R}은 디렉터리 안의 파일과 폴더를 나열합니다.
  Unix의 {cy}ls{R}, Windows CMD의 {cy}dir{R}와 동일합니다.

  {B}📌 기본 사용법{R}
{yl}  PS> Get-ChildItem{R}
{yl}  PS> ls{R}        ← 별칭
{yl}  PS> dir{R}       ← 별칭

  {B}📌 주요 옵션{R}
{yl}  PS> Get-ChildItem -Force{R}          {DM}# 숨김 파일 포함{R}
{yl}  PS> Get-ChildItem -Recurse{R}        {DM}# 하위 폴더까지{R}
{yl}  PS> Get-ChildItem *.txt{R}           {DM}# .txt 파일만{R}
{yl}  PS> Get-ChildItem -Name{R}           {DM}# 이름만 출력{R}

  {B}📌 별칭 정리{R}
  • {cy}gci{R}  — Get-ChildItem 의 공식 별칭
  • {cy}ls{R}   — Unix 스타일
  • {cy}dir{R}  — CMD 스타일

  {B}💡 팁{R}
  {DM}  Get-ChildItem은 파일시스템뿐 아니라 레지스트리, 인증서 저장소에도{R}
  {DM}  사용할 수 있는 강력한 cmdlet입니다.{R}
""",
        "quizzes": [
            {
                "q": "Get-ChildItem에서 숨김 파일까지 보려면?",
                "type": "choice",
                "choices": [
                    "Get-ChildItem -Force",
                    "Get-ChildItem -Hidden",
                    "Get-ChildItem -All",
                    "Get-ChildItem -a",
                ],
                "answer": 0,
            },
            {
                "q": "현재 폴더의 .log 파일만 나열하는 명령어를 입력하세요.",
                "type": "input",
                "answer": "Get-ChildItem *.log",
                "validate": lambda s: ("*.log" in s or "*.Log" in s) and ("gci" in s.lower() or "ls" in s.lower() or "dir" in s.lower() or "get-childitem" in s.lower()),
            },
        ],
    },
    {
        "id": "ps_cd",
        "name": "Set-Location: 디렉터리 이동",
        "summary": "Set-Location(cd)으로 작업 디렉터리를 변경합니다.",
        "content": f"""{CY}{B}  Set-Location — 디렉터리 이동{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Set-Location{R}은 현재 작업 디렉터리를 변경합니다.
  Unix/CMD 모두에서 쓰는 {cy}cd{R}와 동일합니다.

  {B}📌 기본 사용법{R}
{yl}  PS> Set-Location C:\\Users\\name\\Documents{R}
{yl}  PS> cd Documents{R}   ← 별칭, 상대 경로
{yl}  PS> cd ..{R}           ← 상위 폴더로
{yl}  PS> cd ~{R}            ← 홈 디렉터리로
{yl}  PS> cd -{R}            ← 이전 위치로 (뒤로 가기)

  {B}📌 경로 표현{R}
  • {cy}C:\\folder\\sub{R}     절대 경로
  • {cy}.\\subfolder{R}       현재 폴더 기준 상대 경로
  • {cy}..\\sibling{R}        부모 폴더의 형제 폴더
  • {cy}~{R}                  홈 디렉터리 ($HOME)

  {B}📌 별칭{R}
  • {cy}cd{R}  • {cy}sl{R}  • {cy}chdir{R}

  {B}💡 팁{R}
  {DM}  Tab 키로 경로 자동완성이 됩니다. 파워셸의 강력한 기능!{R}
""",
        "quizzes": [
            {
                "q": "PowerShell에서 홈 디렉터리로 이동하는 명령어는?",
                "type": "choice",
                "choices": [
                    "cd ~",
                    "cd /home",
                    "cd $HOME_DIR",
                    "go home",
                ],
                "answer": 0,
            },
            {
                "q": "Set-Location의 공식 별칭은 무엇인가요?",
                "type": "input",
                "answer": "cd",
                "validate": lambda s: s.strip().lower() in ("cd", "sl", "chdir"),
            },
        ],
    },
    {
        "id": "ps_newitem",
        "name": "New-Item: 파일/폴더 생성",
        "summary": "New-Item으로 파일과 디렉터리를 만듭니다.",
        "content": f"""{CY}{B}  New-Item — 파일/폴더 생성{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}New-Item{R}은 파일이나 폴더를 새로 만듭니다.
  Unix의 {cy}touch{R}(파일) 및 {cy}mkdir{R}(폴더)에 해당합니다.

  {B}📌 폴더 만들기{R}
{yl}  PS> New-Item -ItemType Directory -Name "myfolder"{R}
{yl}  PS> mkdir myfolder{R}   ← 더 짧은 별칭

  {B}📌 파일 만들기{R}
{yl}  PS> New-Item -ItemType File -Name "notes.txt"{R}
{yl}  PS> ni notes.txt{R}     ← 별칭

  {B}📌 내용 포함해서 생성{R}
{yl}  PS> New-Item -Name "hello.txt" -Value "Hello, World!"{R}

  {B}📌 중간 경로 자동 생성{R}
{yl}  PS> New-Item -Path "a\\b\\c" -ItemType Directory -Force{R}
  {DM}  Unix의 mkdir -p 와 동일{R}

  {B}💡 팁{R}
  {DM}  New-Item은 파일시스템 외에도 레지스트리 키 등을 만들 수 있습니다.{R}
""",
        "quizzes": [
            {
                "q": "새 폴더를 만드는 올바른 cmdlet은?",
                "type": "choice",
                "choices": [
                    "New-Item -ItemType Directory",
                    "Create-Folder",
                    "Make-Directory",
                    "New-Folder",
                ],
                "answer": 0,
            },
            {
                "q": "mkdir는 New-Item의 무엇인가요?",
                "type": "choice",
                "choices": [
                    "별칭(alias)",
                    "매개변수(parameter)",
                    "함수(function)",
                    "모듈(module)",
                ],
                "answer": 0,
            },
        ],
    },
    {
        "id": "ps_copy",
        "name": "Copy-Item: 파일 복사",
        "summary": "Copy-Item(cp)으로 파일과 폴더를 복사합니다.",
        "content": f"""{CY}{B}  Copy-Item — 파일 복사{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Copy-Item{R}은 파일이나 폴더를 복사합니다.
  Unix의 {cy}cp{R}, CMD의 {cy}copy{R}에 해당합니다.

  {B}📌 파일 복사{R}
{yl}  PS> Copy-Item file.txt backup.txt{R}
{yl}  PS> cp file.txt C:\\Backup\\{R}   ← 별칭

  {B}📌 폴더 전체 복사{R}
{yl}  PS> Copy-Item -Path .\\src -Destination .\\dst -Recurse{R}
  {DM}  Unix의 cp -r 과 동일{R}

  {B}📌 덮어쓰기 강제{R}
{yl}  PS> Copy-Item file.txt dst.txt -Force{R}

  {B}📌 와일드카드 사용{R}
{yl}  PS> Copy-Item *.txt C:\\Backup\\{R}   {DM}# 모든 .txt 복사{R}

  {B}📌 별칭{R}
  • {cy}cp{R}  • {cy}copy{R}  • {cy}cpi{R}

  {B}💡 팁{R}
  {DM}  -WhatIf 옵션으로 실행 전 결과를 미리 확인할 수 있습니다.{R}
{yl}  PS> Copy-Item *.log C:\\Archive\\ -WhatIf{R}
""",
        "quizzes": [
            {
                "q": "폴더 전체를 복사할 때 필요한 옵션은?",
                "type": "choice",
                "choices": [
                    "-Recurse",
                    "-Folder",
                    "-All",
                    "-Deep",
                ],
                "answer": 0,
            },
            {
                "q": "Copy-Item의 Unix 스타일 별칭은?",
                "type": "input",
                "answer": "cp",
                "validate": lambda s: s.strip().lower() in ("cp", "copy", "cpi"),
            },
        ],
    },
    {
        "id": "ps_move",
        "name": "Move-Item: 파일 이동/이름 변경",
        "summary": "Move-Item(mv)으로 파일을 이동하거나 이름을 바꿉니다.",
        "content": f"""{CY}{B}  Move-Item — 이동 / 이름 변경{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Move-Item{R}은 파일/폴더를 이동하거나 이름을 변경합니다.
  Unix의 {cy}mv{R}와 동일합니다.

  {B}📌 파일 이동{R}
{yl}  PS> Move-Item file.txt C:\\Archive\\{R}
{yl}  PS> mv file.txt C:\\Archive\\{R}   ← 별칭

  {B}📌 파일 이름 변경{R}
{yl}  PS> Move-Item old.txt new.txt{R}
  {DM}  같은 폴더 안에서 이름만 바꾸는 것도 Move-Item으로!{R}

  {B}📌 여러 파일 이동{R}
{yl}  PS> Move-Item *.log C:\\Logs\\{R}

  {B}📌 별칭{R}
  • {cy}mv{R}  • {cy}move{R}  • {cy}mi{R}

  {B}💡 팁{R}
  {DM}  Rename-Item 전용 cmdlet도 있지만, Move-Item으로 이름 변경도 가능합니다.{R}
{yl}  PS> Rename-Item old.txt new.txt{R}
""",
        "quizzes": [
            {
                "q": "Move-Item으로 이름 변경도 할 수 있나요?",
                "type": "choice",
                "choices": [
                    "네, 같은 폴더에서 다른 이름으로 지정하면 됩니다",
                    "아니요, 이름 변경은 Rename-Item만 가능합니다",
                    "아니요, 이동만 가능합니다",
                    "네, 하지만 -Rename 옵션이 필요합니다",
                ],
                "answer": 0,
            },
            {
                "q": "Move-Item의 별칭(Unix 스타일)은?",
                "type": "input",
                "answer": "mv",
                "validate": lambda s: s.strip().lower() in ("mv", "move", "mi"),
            },
        ],
    },
    {
        "id": "ps_remove",
        "name": "Remove-Item: 파일 삭제",
        "summary": "Remove-Item(rm)으로 파일과 폴더를 삭제합니다.",
        "content": f"""{CY}{B}  Remove-Item — 파일/폴더 삭제{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Remove-Item{R}은 파일이나 폴더를 삭제합니다.
  Unix의 {cy}rm{R}, CMD의 {cy}del{R}/{cy}rd{R}에 해당합니다.

  {B}📌 파일 삭제{R}
{yl}  PS> Remove-Item file.txt{R}
{yl}  PS> rm file.txt{R}   ← 별칭

  {B}📌 폴더 삭제 (안의 내용 포함){R}
{yl}  PS> Remove-Item -Path .\\myfolder -Recurse{R}
  {DM}  Unix의 rm -r 과 동일{R}

  {B}📌 확인 없이 강제 삭제{R}
{yl}  PS> Remove-Item *.tmp -Force{R}

  {B}⚠ 주의사항{R}
  {rd}  • PowerShell의 rm은 휴지통을 거치지 않습니다!{R}
  {rd}  • -Recurse -Force 조합은 특히 신중하게 사용하세요.{R}
  {DM}  • -WhatIf 로 먼저 확인하는 습관을 들이세요:{R}
{yl}  PS> Remove-Item *.log -WhatIf{R}

  {B}📌 별칭{R}
  • {cy}rm{R}  • {cy}del{R}  • {cy}erase{R}  • {cy}ri{R}
""",
        "quizzes": [
            {
                "q": "폴더와 그 내용을 모두 삭제하려면?",
                "type": "choice",
                "choices": [
                    "Remove-Item -Recurse",
                    "Remove-Item -Deep",
                    "Remove-Item -All",
                    "Remove-Item -Folder",
                ],
                "answer": 0,
            },
            {
                "q": "삭제 전 결과를 미리 확인하는 안전한 옵션은?",
                "type": "choice",
                "choices": [
                    "-WhatIf",
                    "-Preview",
                    "-DryRun",
                    "-Check",
                ],
                "answer": 0,
            },
        ],
    },
    {
        "id": "ps_content",
        "name": "Get-Content: 파일 내용 보기",
        "summary": "Get-Content(cat)으로 파일 내용을 읽습니다.",
        "content": f"""{CY}{B}  Get-Content — 파일 내용 보기{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Get-Content{R}은 파일의 내용을 읽어 출력합니다.
  Unix의 {cy}cat{R}에 해당합니다.

  {B}📌 기본 사용법{R}
{yl}  PS> Get-Content notes.txt{R}
{yl}  PS> cat notes.txt{R}     ← 별칭

  {B}📌 처음/끝 N줄만 보기{R}
{yl}  PS> Get-Content log.txt -TotalCount 10{R}   {DM}# 처음 10줄 (head){R}
{yl}  PS> Get-Content log.txt -Tail 10{R}          {DM}# 마지막 10줄 (tail){R}

  {B}📌 실시간 모니터링 (tail -f){R}
{yl}  PS> Get-Content log.txt -Wait{R}
  {DM}  새 내용이 추가되면 자동으로 표시됩니다.{R}

  {B}📌 인코딩 지정{R}
{yl}  PS> Get-Content file.txt -Encoding UTF8{R}

  {B}📌 별칭{R}
  • {cy}cat{R}  • {cy}gc{R}  • {cy}type{R}

  {B}💡 팁{R}
  {DM}  Get-Content는 줄 단위 배열로 반환하므로 파이프와 잘 어울립니다.{R}
""",
        "quizzes": [
            {
                "q": "파일의 마지막 5줄을 보는 명령어는?",
                "type": "choice",
                "choices": [
                    "Get-Content file.txt -Tail 5",
                    "Get-Content file.txt -Last 5",
                    "Get-Content file.txt -End 5",
                    "Get-Content file.txt -Bottom 5",
                ],
                "answer": 0,
            },
            {
                "q": "Get-Content의 Unix 스타일 별칭은?",
                "type": "input",
                "answer": "cat",
                "validate": lambda s: s.strip().lower() in ("cat", "gc", "type"),
            },
        ],
    },
    {
        "id": "ps_selectstring",
        "name": "Select-String: 텍스트 검색",
        "summary": "Select-String(grep)으로 파일에서 패턴을 검색합니다.",
        "content": f"""{CY}{B}  Select-String — 텍스트 검색{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Select-String{R}은 파일이나 입력에서 텍스트 패턴을 검색합니다.
  Unix의 {cy}grep{R}에 해당합니다.

  {B}📌 기본 검색{R}
{yl}  PS> Select-String "error" log.txt{R}
{yl}  PS> sls "error" log.txt{R}   ← 별칭

  {B}📌 대소문자 구분 없이{R}
{yl}  PS> Select-String "error" log.txt -CaseSensitive:$false{R}
  {DM}  기본값이 대소문자 무시입니다!{R}

  {B}📌 여러 파일 검색{R}
{yl}  PS> Select-String "TODO" *.ps1{R}

  {B}📌 정규식(Regex) 검색{R}
{yl}  PS> Select-String "[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}" log.txt{R}
  {DM}  날짜 패턴 검색 예시{R}

  {B}📌 파이프와 함께{R}
{yl}  PS> Get-Content log.txt | Select-String "WARN"{R}

  {B}💡 팁{R}
  {DM}  결과는 객체로 반환되어 .LineNumber, .Line 등 속성 활용 가능{R}
{yl}  PS> (sls "error" log.txt).LineNumber{R}
""",
        "quizzes": [
            {
                "q": "Select-String의 짧은 별칭은?",
                "type": "choice",
                "choices": [
                    "sls",
                    "grep",
                    "find",
                    "search",
                ],
                "answer": 0,
            },
            {
                "q": "Select-String에서 대소문자를 구분하여 검색하려면?",
                "type": "choice",
                "choices": [
                    "-CaseSensitive",
                    "-MatchCase",
                    "-Exact",
                    "-Strict",
                ],
                "answer": 0,
            },
        ],
    },
    {
        "id": "ps_pipeline",
        "name": "파이프라인(|): 명령어 연결",
        "summary": "| 연산자로 cmdlet을 연결해 강력한 명령을 만듭니다.",
        "content": f"""{CY}{B}  파이프라인 — 명령어 연결{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}파이프라인({cy}|{B}){R}은 앞 명령의 출력을 다음 명령의 입력으로 전달합니다.
  Unix와 동일한 개념이지만, PowerShell은 {CY}텍스트가 아닌 객체{R}를 전달합니다!

  {B}📌 기본 예시{R}
{yl}  PS> Get-Process | Where-Object CPU -gt 100{R}
  {DM}  CPU 사용량 100 이상인 프로세스만 필터링{R}

{yl}  PS> Get-ChildItem | Sort-Object Length -Descending{R}
  {DM}  파일을 크기 내림차순으로 정렬{R}

{yl}  PS> Get-Content log.txt | Select-String "ERROR" | Measure-Object{R}
  {DM}  ERROR 줄 개수 세기{R}

  {B}📌 자주 쓰는 파이프 대상{R}
  • {cy}Where-Object{R} ({cy}?{R}) — 조건 필터링
  • {cy}Sort-Object{R}  ({cy}sort{R}) — 정렬
  • {cy}Select-Object{R} ({cy}select{R}) — 필드 선택
  • {cy}Measure-Object{R} ({cy}measure{R}) — 개수/합계/평균
  • {cy}Format-Table{R}  ({cy}ft{R}) — 표 형식 출력
  • {cy}Out-File{R}      — 파일로 저장

  {B}💡 파워셸 파이프라인의 특징{R}
  {DM}  일반 텍스트가 아닌 .NET 객체가 전달되므로{R}
  {DM}  속성 이름으로 바로 정렬/필터링이 가능합니다.{R}
""",
        "quizzes": [
            {
                "q": "PowerShell 파이프라인이 Unix와 다른 점은?",
                "type": "choice",
                "choices": [
                    "텍스트가 아닌 .NET 객체를 전달한다",
                    "파이프를 여러 개 연결할 수 없다",
                    "출력을 파일로만 저장할 수 있다",
                    "속도가 더 느리다",
                ],
                "answer": 0,
            },
            {
                "q": "파이프라인에서 조건으로 필터링하는 cmdlet은?",
                "type": "choice",
                "choices": [
                    "Where-Object",
                    "Filter-Object",
                    "Select-Where",
                    "Find-Object",
                ],
                "answer": 0,
            },
        ],
    },
    {
        "id": "ps_process",
        "name": "Get-Process / Stop-Process: 프로세스 관리",
        "summary": "Get-Process(ps)와 Stop-Process(kill)로 프로세스를 관리합니다.",
        "content": f"""{CY}{B}  Get-Process / Stop-Process — 프로세스 관리{R}
{DM}  ─────────────────────────────────────────────{R}

  {B}Get-Process{R}는 실행 중인 프로세스 목록을 보여줍니다.
  {B}Stop-Process{R}는 프로세스를 종료합니다.

  {B}📌 프로세스 목록 보기{R}
{yl}  PS> Get-Process{R}
{yl}  PS> ps{R}         ← 별칭
{yl}  PS> gps{R}        ← 별칭

  {B}📌 특정 프로세스 검색{R}
{yl}  PS> Get-Process notepad{R}
{yl}  PS> Get-Process -Name "chrome*"{R}

  {B}📌 CPU/메모리 정렬{R}
{yl}  PS> Get-Process | Sort-Object CPU -Descending | Select-Object -First 5{R}
  {DM}  CPU 사용량 상위 5개{R}

  {B}📌 프로세스 종료{R}
{yl}  PS> Stop-Process -Name notepad{R}
{yl}  PS> Stop-Process -Id 1234{R}
{yl}  PS> kill 1234{R}    ← 별칭

  {B}⚠ 주의{R}
  {rd}  • -Force 없이 종료하면 저장 확인 대화상자가 뜰 수 있습니다.{R}
  {rd}  • 시스템 프로세스는 관리자 권한이 필요합니다.{R}
""",
        "quizzes": [
            {
                "q": "프로세스를 이름으로 종료하는 명령어는?",
                "type": "choice",
                "choices": [
                    "Stop-Process -Name notepad",
                    "Kill-Process notepad",
                    "End-Process -Name notepad",
                    "Remove-Process notepad",
                ],
                "answer": 0,
            },
            {
                "q": "Get-Process의 Unix 스타일 별칭은?",
                "type": "input",
                "answer": "ps",
                "validate": lambda s: s.strip().lower() in ("ps", "gps"),
            },
        ],
    },
    {
        "id": "ps_env",
        "name": "$env: 환경변수",
        "summary": "$env: 드라이브로 환경변수를 읽고 설정합니다.",
        "content": f"""{CY}{B}  $env: — 환경변수{R}
{DM}  ─────────────────────────────────────────────{R}

  PowerShell에서는 {B}$env:{R} 드라이브를 통해 환경변수에 접근합니다.
  Unix의 {cy}$VARNAME{R} / {cy}export{R}에 해당합니다.

  {B}📌 환경변수 읽기{R}
{yl}  PS> $env:PATH{R}            {DM}# PATH 출력{R}
{yl}  PS> $env:USERNAME{R}        {DM}# 현재 사용자 이름{R}
{yl}  PS> $env:COMPUTERNAME{R}    {DM}# 컴퓨터 이름{R}
{yl}  PS> $env:TEMP{R}            {DM}# 임시 폴더 경로{R}

  {B}📌 모든 환경변수 보기{R}
{yl}  PS> Get-ChildItem Env:{R}
{yl}  PS> ls env:{R}   ← 별칭

  {B}📌 환경변수 설정 (현재 세션){R}
{yl}  PS> $env:MY_VAR = "hello"{R}

  {B}📌 영구적으로 설정{R}
{yl}  PS> [System.Environment]::SetEnvironmentVariable("MY_VAR","hello","User"){R}
  {DM}  "User" 또는 "Machine" (시스템 전체, 관리자 권한 필요){R}

  {B}💡 팁{R}
  {DM}  $env:PATH 에 경로 추가:{R}
{yl}  PS> $env:PATH += ";C:\\mytools"{R}
""",
        "quizzes": [
            {
                "q": "PowerShell에서 PATH 환경변수를 출력하는 방법은?",
                "type": "choice",
                "choices": [
                    "$env:PATH",
                    "echo $PATH",
                    "env PATH",
                    "$PATH",
                ],
                "answer": 0,
            },
            {
                "q": "모든 환경변수를 나열하는 명령어는?",
                "type": "choice",
                "choices": [
                    "Get-ChildItem Env:",
                    "Show-Env",
                    "List-Variables",
                    "Get-Environment",
                ],
                "answer": 0,
            },
        ],
    },
    {
        "id": "ps_compress",
        "name": "Compress-Archive: 압축",
        "summary": "Compress-Archive / Expand-Archive로 ZIP 파일을 만들고 풉니다.",
        "content": f"""{CY}{B}  Compress-Archive — 압축/해제{R}
{DM}  ─────────────────────────────────────────────{R}

  PowerShell 5+ 내장 cmdlet으로 ZIP 파일을 다룰 수 있습니다.
  Unix의 {cy}tar{R}/{cy}zip{R}에 해당합니다.

  {B}📌 압축하기{R}
{yl}  PS> Compress-Archive -Path .\\myfolder -DestinationPath archive.zip{R}
{yl}  PS> Compress-Archive *.log -DestinationPath logs.zip{R}

  {B}📌 기존 ZIP에 파일 추가{R}
{yl}  PS> Compress-Archive -Path new.txt -DestinationPath archive.zip -Update{R}

  {B}📌 압축 해제{R}
{yl}  PS> Expand-Archive -Path archive.zip -DestinationPath .\\output{R}
{yl}  PS> Expand-Archive archive.zip .\\output{R}   ← 간단 버전

  {B}📌 강제 덮어쓰기{R}
{yl}  PS> Expand-Archive archive.zip .\\output -Force{R}

  {B}💡 Unix tar 비교{R}
  {DM}  tar -czf  →  Compress-Archive{R}
  {DM}  tar -xzf  →  Expand-Archive{R}
  {DM}  tar -tf   →  (Get-Archive 없음, 직접 열어야 함){R}
""",
        "quizzes": [
            {
                "q": "ZIP 파일을 만드는 cmdlet은?",
                "type": "choice",
                "choices": [
                    "Compress-Archive",
                    "New-Archive",
                    "Create-Zip",
                    "Pack-Files",
                ],
                "answer": 0,
            },
            {
                "q": "ZIP 파일을 해제하는 cmdlet은?",
                "type": "input",
                "answer": "Expand-Archive",
                "validate": lambda s: "expand-archive" in s.lower(),
            },
        ],
    },
]

# ── Lesson lookup ──────────────────────────────────────────────────────────────
ALL_LESSONS = {"terminal": TERMINAL_LESSONS, "vim": VIM_LESSONS, "powershell": POWERSHELL_LESSONS, "tmux": TMUX_LESSONS}

def get_lesson(ltype: str, lid: str):
    for lesson in ALL_LESSONS[ltype]:
        if lesson["id"] == lid:
            return lesson
    return None

# ── Quiz engine ────────────────────────────────────────────────────────────────
def run_quiz(quiz: dict) -> bool:
    print()
    hr()
    print(f"\n  {B}퀴즈{R}")
    print(f"  {quiz['q']}\n")

    if quiz["type"] == "choice":
        for idx, choice in enumerate(quiz["choices"]):
            print(f"  {cy}{idx+1}.{R} {choice}")
        print()
        while True:
            print(f"  답 입력 (1~{len(quiz['choices'])}): ", end="", flush=True)
            raw = getch()
            print(raw)
            if raw.isdigit() and 1 <= int(raw) <= len(quiz["choices"]):
                chosen = int(raw) - 1
                break
            print(f"  {rd}유효한 번호를 입력하세요.{R}")
        if chosen == quiz["answer"]:
            print(f"\n  {GR}✓ 정답입니다!{R}")
            return True
        else:
            correct_text = quiz["choices"][quiz["answer"]]
            print(f"\n  {RD}✗ 틀렸습니다.{R}")
            print(f"  {DM}정답: {quiz['answer']+1}. {correct_text}{R}")
            return False

    else:  # input type
        raw = input(f"  입력: ").strip()
        if quiz["validate"](raw):
            print(f"\n  {GR}✓ 정답입니다!{R}")
            return True
        else:
            print(f"\n  {RD}✗ 틀렸습니다.{R}")
            print(f"  {DM}정답 예시: {quiz['answer']}{R}")
            return False

# ── Lesson flow ────────────────────────────────────────────────────────────────
def run_lesson_flow(ltype: str, lesson: dict) -> bool:
    """Show lesson, run quizzes. Returns True if passed."""
    while True:
        clr()
        hr()
        print(f"\n  {CY}{B}{lesson['name']}{R}\n")
        typewrite(lesson["content"])
        hr()
        input(f"\n  {DM}Enter를 눌러 퀴즈를 시작하세요...{R}")

        score = 0
        for quiz in lesson["quizzes"]:
            if run_quiz(quiz):
                score += 1
            pause()

        clr()
        hr()
        print(f"\n  {B}결과: {score}/{len(lesson['quizzes'])} 정답{R}\n")

        passed = score >= 1
        if passed:
            mark_learned(ltype, lesson["id"])
            done = learned_count(ltype)
            total = len(ALL_LESSONS[ltype])
            print()
            animate_progress_bar(done, total, f"{GR}완료{R} {done}/{total}")
            print(f"  {GR}✓ 통과! 복습 큐에 추가됨{R}")
            return True
        else:
            print(f"  {RD}아직 조금 더 공부가 필요합니다.{R}")
            print(f"  {DM}점수 {score}/{len(lesson['quizzes'])} — 통과 기준: 1점 이상{R}")
            print(f"\n  레슨을 다시 읽어보시겠습니까? [y/n]: ", end="", flush=True)
            again = getch().lower()
            print(again)
            if again != "y":
                return False

# ── Learning menu ──────────────────────────────────────────────────────────────
def show_lesson_list(ltype: str, lessons: list):
    """Show all lessons with completion status and let user pick one."""
    while True:
        clr()
        label = {"terminal": "터미널", "vim": "Vim", "powershell": "PowerShell", "tmux": "tmux"}.get(ltype, ltype)
        total = len(lessons)
        done = learned_count(ltype)
        print(f"\n  {CY}{B}{label} 레슨 목록 ({done}/{total}){R}\n")
        hr()
        for idx, lesson in enumerate(lessons):
            status = f"{GR}✓{R}" if is_learned(ltype, lesson["id"]) else f"{DM}○{R}"
            print(f"  {status} {cy}{idx+1:2}.{R} {lesson['name']}")
        print(f"\n  {DM}0. 뒤로 가기{R}")
        hr()
        # 다음 미완료 레슨 계산 (Enter 기본값용)
        next_unlearned = next((l for l in lessons if not is_learned(ltype, l["id"])), None)
        hint = f" {DM}(Enter = 다음 레슨){R}" if next_unlearned else ""
        raw = input(f"\n  번호 선택{hint}: ").strip()
        if raw == "0":
            return
        if raw == "" and next_unlearned:
            chosen = next_unlearned
        elif raw.isdigit() and 1 <= int(raw) <= total:
            chosen = lessons[int(raw)-1]
        else:
            continue
        run_lesson_flow(ltype, chosen)
        cont = input(f"\n  계속 학습하시겠습니까? [\033[4mY\033[0m/n]: ").strip().lower()
        if cont not in ("", "y"):
            return

def learning_menu(ltype: str):
    lessons = ALL_LESSONS[ltype]
    label = {"terminal": "터미널 기초", "vim": "Vim 에디터", "powershell": "PowerShell 기초", "tmux": "tmux 터미널 멀티플렉서"}.get(ltype, ltype)
    total = len(lessons)

    while True:
        clr()
        done = learned_count(ltype)
        print(f"\n  {CY}{B}{label} 학습{R}")
        print(f"  진행도: {GR}{done}{R}/{total}\n")

        # find next unlearned
        next_lesson = None
        for lesson in lessons:
            if not is_learned(ltype, lesson["id"]):
                next_lesson = lesson
                break

        hr()
        if next_lesson is None:
            fireworks()
            pause()
            clr()
            done2 = learned_count(ltype)
            total2 = len(lessons)
            print(f"\n  [{GR}{'█' * 38}{R}] {GR}100%{R}  {done2}/{total2}\n")
        else:
            print(f"  {B}다음 레슨:{R} {CY}{next_lesson['name']}{R}\n")
        print(f"  {cy}1.{R} 학습 시작" + (f" — {next_lesson['name']}" if next_lesson else ""))
        print(f"  {cy}2.{R} 레슨 목록 보기")
        print(f"  {cy}0.{R} 뒤로 가기")
        hr()
        print(f"\n  선택: ", end="", flush=True)
        choice = getch()
        print(choice)

        if choice == "0":
            return
        elif choice == "1":
            if next_lesson is None:
                print(f"\n  {GR}이미 모든 레슨을 완료했습니다.{R}")
                pause()
            else:
                run_lesson_flow(ltype, next_lesson)
                print(f"\n  계속 학습하시겠습니까? [\033[4mY\033[0m/n]: ", end="", flush=True)
                cont = getch()
                print(cont if cont not in ("\r", "\n") else "")
                if cont.lower() not in ("y", "\r", "\n"):
                    return
        elif choice == "2":
            show_lesson_list(ltype, lessons)
        else:
            print(f"\n  {rd}올바른 번호를 입력하세요.{R}")
            pause()

# ── Review menu ────────────────────────────────────────────────────────────────
def review_menu():
    clr()
    p = load_progress()
    today = date.today().isoformat()

    t_done = learned_count("terminal")
    v_done = learned_count("vim")
    tm_done = learned_count("tmux")
    t_total = len(TERMINAL_LESSONS)
    v_total = len(VIM_LESSONS)
    tm_total = len(TMUX_LESSONS)

    print(f"\n  {CY}{B}학습 내용 보기 / 복습{R}\n")
    hr()
    print(f"  {B}전체 진행도{R}")
    print(f"  터미널 기초:  {GR}{t_done}{R}/{t_total}")
    print(f"  Vim 에디터:   {GR}{v_done}{R}/{v_total}")
    print(f"  tmux:         {GR}{tm_done}{R}/{tm_total}")
    hr()

    all_learned = []
    for ltype_label, ltype_key, lessons in [("터미널", "terminal", TERMINAL_LESSONS), ("Vim", "vim", VIM_LESSONS), ("tmux", "tmux", TMUX_LESSONS)]:
        for lesson in lessons:
            info = p[ltype_key].get(lesson["id"])
            if info and info.get("learned"):
                all_learned.append((ltype_key, lesson, info))

    if all_learned:
        print(f"\n  {B}학습 완료 항목{R}\n")
        for ltype_key, lesson, info in all_learned:
            nr = info.get("next_review", "없음")
            due_mark = f"  {YL}📌 복습필요{R}" if nr <= today else f"  {DM}(다음 복습: {nr}){R}"
            status = f"{GR}✓ 완료{R}"
            print(f"  {status} {lesson['name']}{due_mark}")
    else:
        print(f"\n  {DM}아직 학습한 항목이 없습니다.{R}")

    due = get_due()

    hr()
    if due:
        due_count = len(due)
        print(f"\n  {YL}📌 오늘 복습할 항목: {due_count}개{R}\n")
        for ltype_key, lid in due:
            lesson = get_lesson(ltype_key, lid)
            if lesson:
                print(f"   • {lesson['name']}")
        print()
        start = input(f"  복습을 시작하시겠습니까? [y/n]: ").strip().lower()
        if start == "y":
            correct_count = 0
            total_count = len(due)
            for ltype_key, lid in due:
                lesson = get_lesson(ltype_key, lid)
                if not lesson:
                    continue
                clr()
                hr()
                print(f"\n  {CY}{B}복습: {lesson['name']}{R}\n")
                print(f"  {DM}{lesson['summary']}{R}\n")
                print(lesson["content"])
                hr()
                pause()
                result = run_quiz(lesson["quizzes"][0])
                update_review(ltype_key, lid, result)
                if result:
                    correct_count += 1
                pause()

            clr()
            hr()
            print(f"\n  {B}복습 완료!{R}")
            print(f"  점수: {GR}{correct_count}{R}/{total_count}\n")
            hr()
    else:
        print(f"\n  {GR}👍 오늘 복습할 항목이 없습니다!{R}\n")
        upcoming = []
        for ltype_key in ("terminal", "vim", "tmux"):
            for lid, info in p[ltype_key].items():
                if info.get("learned"):
                    nr = info.get("next_review", "9999")
                    if nr > today:
                        lesson = get_lesson(ltype_key, lid)
                        if lesson:
                            upcoming.append((nr, lesson["name"]))
        upcoming.sort()
        if upcoming:
            print(f"  {DM}다가오는 복습:{R}")
            for nr, name in upcoming[:5]:
                print(f"  {DM}  {nr} — {name}{R}")
        print()

    pause()

# ── Settings menu ──────────────────────────────────────────────────────────────
def settings_menu():
    cfg = load_config()
    while True:
        clr()
        print(f"\n  {CY}{B}설정{R}\n")
        hr()
        claude_masked = ("*" * (len(cfg["claude_key"])-4) + cfg["claude_key"][-4:]) if len(cfg["claude_key"]) > 4 else ("*" * len(cfg["claude_key"]) if cfg["claude_key"] else "(미설정)")
        openai_masked = ("*" * (len(cfg["openai_key"])-4) + cfg["openai_key"][-4:]) if len(cfg["openai_key"]) > 4 else ("*" * len(cfg["openai_key"]) if cfg["openai_key"] else "(미설정)")
        active = cfg.get("active_ai", "claude")
        print(f"  {cy}1.{R} Claude API 키  [{claude_masked}]")
        print(f"  {cy}2.{R} OpenAI API 키  [{openai_masked}]")
        print(f"  {cy}3.{R} 활성 AI 선택   [{GR}{active}{R}]")
        print(f"  {cy}0.{R} 뒤로 가기")
        hr()
        print(f"\n  선택: ", end="", flush=True)
        choice = getch()
        print(choice)
        if choice == "0":
            return
        elif choice == "1":
            key = getpass.getpass("  Claude API 키 입력 (입력시 숨김): ").strip()
            if key:
                cfg["claude_key"] = key
                save_config(cfg)
                print(f"  {GR}✓ 저장됨{R}")
                pause()
        elif choice == "2":
            key = getpass.getpass("  OpenAI API 키 입력 (입력시 숨김): ").strip()
            if key:
                cfg["openai_key"] = key
                save_config(cfg)
                print(f"  {GR}✓ 저장됨{R}")
                pause()
        elif choice == "3":
            print(f"\n  {cy}1.{R} Claude")
            print(f"  {cy}2.{R} OpenAI")
            print("  선택: ", end="", flush=True)
            sel = getch()
            print(sel)
            if sel == "1":
                cfg["active_ai"] = "claude"
            elif sel == "2":
                cfg["active_ai"] = "openai"
            save_config(cfg)
            print(f"  {GR}✓ 저장됨{R}")
            pause()
        else:
            print(f"  {rd}올바른 번호를 입력하세요.{R}")
            pause()

# ── Main menu ──────────────────────────────────────────────────────────────────
def main_menu():
    ensure_dirs()
    while True:
        clr()
        t_done = learned_count("terminal")
        v_done = learned_count("vim")
        ps_done = learned_count("powershell")
        tm_done = learned_count("tmux")
        t_total = len(TERMINAL_LESSONS)
        v_total = len(VIM_LESSONS)
        ps_total = len(POWERSHELL_LESSONS)
        tm_total = len(TMUX_LESSONS)
        due = get_due()
        due_count = len(due)

        title = "PowerShell 학습 도우미" if IS_WINDOWS else "터미널 학습 도우미 "
        print(f"""
  {CY}{B}┌─────────────────────────────────────────┐{R}
  {CY}{B}│      {title} v2.0           │{R}
  {CY}{B}└─────────────────────────────────────────┘{R}
""")

        if due_count > 0:
            print(f"  {YL}📌 오늘 복습할 항목: {due_count}개{R}\n")

        hr()
        if IS_WINDOWS:
            print(f"  {cy}1.{R} PowerShell 기초 학습   {DM}({GR}{ps_done}{DM}/{ps_total}){R}")
            print(f"  {cy}2.{R} 터미널 기초 학습        {DM}({GR}{t_done}{DM}/{t_total}){R}")
            print(f"  {cy}3.{R} Vim 에디터 학습         {DM}({GR}{v_done}{DM}/{v_total}){R}")
            print(f"  {cy}4.{R} 학습 내용 보기 / 복습   {DM}{'(' + YL + '📌 ' + str(due_count) + '개' + R + DM + ')' if due_count else ''}{R}")
            print(f"  {cy}5.{R} 설정")
            print(f"  {cy}0.{R} 종료")
        else:
            print(f"  {cy}1.{R} 터미널 기초 학습      {DM}({GR}{t_done}{DM}/{t_total}){R}")
            print(f"  {cy}2.{R} Vim 에디터 학습        {DM}({GR}{v_done}{DM}/{v_total}){R}")
            print(f"  {cy}3.{R} tmux 학습              {DM}({GR}{tm_done}{DM}/{tm_total}){R}")
            print(f"  {cy}4.{R} 학습 내용 보기 / 복습  {DM}{'(' + YL + '📌 ' + str(due_count) + '개' + R + DM + ')' if due_count else ''}{R}")
            print(f"  {cy}5.{R} 설정")
            print(f"  {cy}0.{R} 종료")
        hr()

        print(f"\n  선택: ", end="", flush=True)
        choice = getch()
        print(choice)

        if choice == "0":
            print(f"\n  {GR}종료합니다. 오늘도 수고하셨습니다!{R}\n")
            sys.exit(0)
        elif IS_WINDOWS:
            if choice == "1":
                learning_menu("powershell")
            elif choice == "2":
                learning_menu("terminal")
            elif choice == "3":
                learning_menu("vim")
            elif choice == "4":
                review_menu()
            elif choice == "5":
                settings_menu()
            else:
                print(f"\n  {rd}올바른 번호를 입력하세요 (0~5).{R}")
                pause()
        else:
            if choice == "1":
                learning_menu("terminal")
            elif choice == "2":
                learning_menu("vim")
            elif choice == "3":
                learning_menu("tmux")
            elif choice == "4":
                review_menu()
            elif choice == "5":
                settings_menu()
            else:
                print(f"\n  {rd}올바른 번호를 입력하세요 (0~5).{R}")
                pause()


def main():
    """pip install 후 console_scripts 진입점."""
    try:
        splash_screen()
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {GR}종료합니다.{R}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
