#!/bin/bash
set -e

REPO="lemonardo1/Learning-Terminal"
BRANCH="main"
SCRIPT="learning_terminal.py"
INSTALL_DIR="$HOME/.local/bin"
CMD_NAME="terminal"

# ── 배너 ──────────────────────────────────────────────────────────────────────
echo ""
echo "  ┌──────────────────────────────────────────┐"
echo "  │  터미널 학습 도우미 설치                  │"
echo "  │  github.com/$REPO   │"
echo "  └──────────────────────────────────────────┘"
echo ""
echo "  설치 후 'terminal' 명령어로 바로 실행할 수 있습니다."
echo ""

# ── 동의 확인 ─────────────────────────────────────────────────────────────────
echo "  설치 위치: $INSTALL_DIR/$CMD_NAME"
echo "  설정 파일: ~/.config/learning-terminal/"
echo ""
read -rp "  설치하시겠습니까? [y/N] " CONFIRM
echo ""

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "  설치를 취소했습니다."
    echo ""
    exit 0
fi

# ── Python 3 확인 ─────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "  ✗ Python 3가 필요합니다."
    echo ""
    echo "  macOS:  xcode-select --install"
    echo "  또는    https://www.python.org/downloads/"
    echo ""
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 7 ]]; then
    echo "  ✗ Python 3.7 이상이 필요합니다. (현재: $PY_VER)"
    exit 1
fi

echo "  ✓ Python $PY_VER 확인"

# ── 설치 디렉터리 생성 ────────────────────────────────────────────────────────
mkdir -p "$INSTALL_DIR"

# ── 다운로드 ──────────────────────────────────────────────────────────────────
URL="https://raw.githubusercontent.com/$REPO/$BRANCH/$SCRIPT"
DEST="$INSTALL_DIR/$CMD_NAME"

echo "  ↓ 다운로드 중..."

if ! curl -fsSL "$URL" -o "$DEST"; then
    echo "  ✗ 다운로드 실패. 네트워크를 확인해주세요."
    echo "  URL: $URL"
    exit 1
fi

chmod +x "$DEST"
echo "  ✓ 설치 완료: $DEST"

# ── PATH 등록 ─────────────────────────────────────────────────────────────────
RCFILE=""
[[ "$SHELL" == */zsh  ]] && RCFILE="$HOME/.zshrc"
[[ "$SHELL" == */bash ]] && RCFILE="$HOME/.bashrc"
[[ -z "$RCFILE" && -f "$HOME/.zshrc"  ]] && RCFILE="$HOME/.zshrc"
[[ -z "$RCFILE" && -f "$HOME/.bashrc" ]] && RCFILE="$HOME/.bashrc"

PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

if [[ ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
    echo "  ✓ PATH 이미 설정됨"
elif [[ -n "$RCFILE" ]]; then
    # 이미 추가된 줄이 있는지 확인
    if ! grep -qF "$INSTALL_DIR" "$RCFILE" 2>/dev/null; then
        {
            echo ""
            echo "# Learning Terminal"
            echo "$PATH_LINE"
        } >> "$RCFILE"
        echo "  ✓ PATH 추가 ($RCFILE)"
        NEED_SOURCE=1
    else
        echo "  ✓ PATH 이미 $RCFILE 에 설정됨"
    fi
else
    echo "  ⚠  PATH 자동 설정 불가. 아래 줄을 셸 설정 파일에 추가하세요:"
    echo "     $PATH_LINE"
fi

# ── 완료 메시지 ───────────────────────────────────────────────────────────────
echo ""
echo "  ────────────────────────────────────────────"
echo "  설치 완료!"
echo ""

if [[ -n "$NEED_SOURCE" ]]; then
    echo "  ⚠  PATH 적용을 위해 아래 명령어를 실행하세요:"
    echo ""
    echo "     source $RCFILE"
    echo ""
    echo "  이후 새 터미널에서는 자동으로 적용됩니다."
else
    echo "  지금 바로 실행할 수 있습니다:"
    echo ""
    echo "     terminal"
fi

echo "  ────────────────────────────────────────────"
echo ""
