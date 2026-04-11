# 터미널 학습 도우미

[![PyPI version](https://img.shields.io/pypi/v/learning-terminal)](https://pypi.org/project/learning-terminal/)
[![Python](https://img.shields.io/pypi/pyversions/learning-terminal)](https://pypi.org/project/learning-terminal/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

터미널 명령어 · Vim · tmux · Git을 **대화형 퀴즈**로 배우는 CLI 학습 프로그램입니다.  
간격 반복(Spaced Repetition) 알고리즘으로 효율적인 복습을 지원합니다.

---

## 설치

### pip (권장)

```bash
pip install learning-terminal
learning-terminal
```

### 원클릭 설치 — macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/lemonardo1/Learning-Terminal/main/install.sh | bash
```

설치 후 `terminal` 명령어로 실행합니다.

### 원클릭 설치 — Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/lemonardo1/Learning-Terminal/main/install.ps1 | iex
```

> Windows Terminal 또는 PowerShell 7 이상을 권장합니다.

### 직접 실행

```bash
git clone https://github.com/lemonardo1/Learning-Terminal.git
cd Learning-Terminal
python3 learning_terminal.py
```

---

## 특징

- **대화형 퀴즈** — 선택형 + 직접 입력형으로 개념을 바로 확인
- **간격 반복 복습** — 학습 주기를 1 → 3 → 7 → 30 → 90일로 자동 관리
- **TUI 애니메이션** — 스플래시 화면, 진행률 바, 완료 폭죽 애니메이션
- **진도 저장** — 학습 기록이 로컬에 저장되어 이어서 공부 가능
- **외부 의존성 없음** — Python 3 표준 라이브러리만 사용

---

## 커리큘럼

### 터미널 기초 (33개 레슨)

| 카테고리 | 레슨 |
|----------|------|
| 탐색 | `pwd` `ls` `cd` `find` |
| 파일 관리 | `mkdir` `touch` `cp` `mv` `rm` |
| 내용 보기 | `cat` `head` `tail` `less` |
| 텍스트 처리 | `grep` `sed` `awk` `sort` `uniq` `wc` `xargs` |
| 파이프·리디렉션 | 파이프(`\|`) `>` `>>` `<` `2>&1` |
| 시스템 | `ps` `kill` `env` `export` `chmod` `chown` `df` `du` |
| 네트워크 | `ssh` `curl` `rsync` |
| 유틸리티 | `tar` `date` `man` `history` `alias` `echo` `jq` `crontab` |
| Git | `init` `add` `commit` `log` · 브랜치 `branch` `merge` |

### Vim 에디터 (12개 레슨)

모드 · 이동 · 삽입 · 저장/종료 · 삭제 · 복사/붙여넣기 · 되돌리기 · 검색 · 치환 · 팁

### tmux 터미널 멀티플렉서 (6개 레슨)

소개 · 세션 · 윈도우 · 패인 · 복사 모드 · 설정

---

## 메뉴 구조

```
  1. 터미널 기초 학습
  2. Vim 에디터 학습
  3. tmux 학습
  4. 학습 내용 보기 / 복습
  5. 설정
  0. 종료
```

레슨 목록에서 **Enter** 를 누르면 다음 미완료 레슨으로 자동 이동합니다.

---

## 데이터 저장 위치

**macOS / Linux**
```
~/.config/learning-terminal/
├── config.json      # 설정
└── progress.json    # 학습 진도
```

**Windows**
```
%APPDATA%\learning-terminal\
├── config.json      # 설정
└── progress.json    # 학습 진도
```

---

## Thanks to

Vim 아이디어를 준 [서울대학교 차수현](https://github.com/soohyuncha), [연세대학교 이경민](https://github.com/margaretlee35)에게 감사를 표합니다.

## 라이선스

[MIT License](LICENSE)
