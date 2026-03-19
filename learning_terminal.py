#!/usr/bin/env python3
"""터미널 학습 도우미 | Python 3 only — stdlib only"""

import os, sys, json, re
from datetime import date, timedelta
import getpass

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
    os.system("clear")

def hr():
    print(f"{DM}{'─'*60}{R}")

def pause():
    input(f"\n{DM}  Enter를 눌러 계속...{R}")

# ── Storage paths ─────────────────────────────────────────────────────────────
CFG_DIR      = os.path.expanduser("~/.config/learning-terminal")
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
    default = {"terminal": {}, "vim": {}}
    p = load_json(PROGRESS_FILE, default)
    if "terminal" not in p: p["terminal"] = {}
    if "vim" not in p: p["vim"] = {}
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
    for ltype in ("terminal", "vim"):
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

# ── Lesson lookup ──────────────────────────────────────────────────────────────
ALL_LESSONS = {"terminal": TERMINAL_LESSONS, "vim": VIM_LESSONS}

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
            raw = input(f"  답 입력 (1~{len(quiz['choices'])}): ").strip()
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
        print(lesson["content"])
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
            print(f"  {GR}✓ 통과! 복습 큐에 추가됨{R}")
            return True
        else:
            print(f"  {RD}아직 조금 더 공부가 필요합니다.{R}")
            print(f"  {DM}점수 {score}/{len(lesson['quizzes'])} — 통과 기준: 1점 이상{R}")
            again = input(f"\n  레슨을 다시 읽어보시겠습니까? [y/n]: ").strip().lower()
            if again != "y":
                return False

# ── Learning menu ──────────────────────────────────────────────────────────────
def show_lesson_list(ltype: str, lessons: list):
    """Show all lessons with completion status and let user pick one."""
    while True:
        clr()
        label = "터미널" if ltype == "terminal" else "Vim"
        total = len(lessons)
        done = learned_count(ltype)
        print(f"\n  {CY}{B}{label} 레슨 목록 ({done}/{total}){R}\n")
        hr()
        for idx, lesson in enumerate(lessons):
            status = f"{GR}✓{R}" if is_learned(ltype, lesson["id"]) else f"{DM}○{R}"
            print(f"  {status} {cy}{idx+1:2}.{R} {lesson['name']}")
        print(f"\n  {DM}0. 뒤로 가기{R}")
        hr()
        raw = input(f"\n  번호 선택: ").strip()
        if raw == "0":
            return
        if raw.isdigit() and 1 <= int(raw) <= total:
            chosen = lessons[int(raw)-1]
            run_lesson_flow(ltype, chosen)
            cont = input(f"\n  계속 학습하시겠습니까? [y/n]: ").strip().lower()
            if cont != "y":
                return

def learning_menu(ltype: str):
    lessons = ALL_LESSONS[ltype]
    label = "터미널 기초" if ltype == "terminal" else "Vim 에디터"
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
            print(f"\n  {GR}🎉 모두 완료! 모든 레슨을 학습했습니다.{R}\n")
        else:
            print(f"  {B}다음 레슨:{R} {CY}{next_lesson['name']}{R}\n")
        print(f"  {cy}1.{R} 학습 시작" + (f" — {next_lesson['name']}" if next_lesson else ""))
        print(f"  {cy}2.{R} 레슨 목록 보기")
        print(f"  {cy}0.{R} 뒤로 가기")
        hr()
        choice = input(f"\n  선택: ").strip()

        if choice == "0":
            return
        elif choice == "1":
            if next_lesson is None:
                print(f"\n  {GR}이미 모든 레슨을 완료했습니다.{R}")
                pause()
            else:
                run_lesson_flow(ltype, next_lesson)
                cont = input(f"\n  계속 학습하시겠습니까? [y/n]: ").strip().lower()
                if cont != "y":
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
    t_total = len(TERMINAL_LESSONS)
    v_total = len(VIM_LESSONS)

    print(f"\n  {CY}{B}학습 내용 보기 / 복습{R}\n")
    hr()
    print(f"  {B}전체 진행도{R}")
    print(f"  터미널 기초: {GR}{t_done}{R}/{t_total}")
    print(f"  Vim 에디터:  {GR}{v_done}{R}/{v_total}")
    hr()

    all_learned = []
    for ltype_label, ltype_key, lessons in [("터미널", "terminal", TERMINAL_LESSONS), ("Vim", "vim", VIM_LESSONS)]:
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
        for ltype_key in ("terminal", "vim"):
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
        choice = input(f"\n  선택: ").strip()
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
            sel = input("  선택: ").strip()
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
        t_total = len(TERMINAL_LESSONS)
        v_total = len(VIM_LESSONS)
        due = get_due()
        due_count = len(due)

        print(f"""
  {CY}{B}┌─────────────────────────────────────────┐{R}
  {CY}{B}│      터미널 학습 도우미  v2.0           │{R}
  {CY}{B}└─────────────────────────────────────────┘{R}
""")

        if due_count > 0:
            print(f"  {YL}📌 오늘 복습할 항목: {due_count}개{R}\n")

        hr()
        print(f"  {cy}1.{R} 터미널 기초 학습      {DM}({GR}{t_done}{DM}/{t_total}){R}")
        print(f"  {cy}2.{R} Vim 에디터 학습        {DM}({GR}{v_done}{DM}/{v_total}){R}")
        print(f"  {cy}3.{R} 학습 내용 보기 / 복습  {DM}{'(' + YL + '📌 ' + str(due_count) + '개' + R + DM + ')' if due_count else ''}{R}")
        print(f"  {cy}4.{R} 설정")
        print(f"  {cy}0.{R} 종료")
        hr()

        choice = input(f"\n  선택: ").strip()

        if choice == "0":
            print(f"\n  {GR}종료합니다. 오늘도 수고하셨습니다!{R}\n")
            sys.exit(0)
        elif choice == "1":
            learning_menu("terminal")
        elif choice == "2":
            learning_menu("vim")
        elif choice == "3":
            review_menu()
        elif choice == "4":
            settings_menu()
        else:
            print(f"\n  {rd}올바른 번호를 입력하세요 (0~4).{R}")
            pause()


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {GR}종료합니다.{R}\n")
        sys.exit(0)
