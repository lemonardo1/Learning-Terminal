# 터미널 학습 도우미

터미널 명령어와 Vim을 대화형으로 배우는 Python 학습 프로그램입니다.
간격 반복(Spaced Repetition) 알고리즘으로 효율적인 복습을 지원합니다.

## 특징

- **터미널 명령어 학습** — `pwd`, `ls`, `cd`, `cp`, `mv`, `rm` 등 필수 명령어
- **Vim 학습** — 기본 조작부터 실전 단축키까지
- **간격 반복 복습** — 학습한 내용을 최적의 주기(1→3→7→30→90일)로 자동 복습
- **퀴즈** — 선택형 및 직접 입력형 문제로 확인
- **진도 저장** — 학습 기록이 로컬에 저장되어 이어서 공부 가능
- **외부 의존성 없음** — Python 3 표준 라이브러리만 사용

## 요구 사항

- Python 3.7 이상
- macOS / Linux

## 설치

### 원클릭 설치 (권장)

```bash
curl -fsSL https://raw.githubusercontent.com/lemonardo1/Learning-Terminal/main/install.sh | bash
```

설치 후 `terminal` 명령어로 바로 실행할 수 있습니다.

### 직접 실행

```bash
git clone https://github.com/lemonardo1/Learning-Terminal.git
cd Learning-Terminal
python3 learning_terminal.py
```

## 사용법

```bash
terminal
```

메인 메뉴에서 원하는 항목을 선택합니다.

```
  1. 터미널 명령어 배우기
  2. Vim 배우기
  3. 오늘의 복습
  4. 진도 확인
  0. 종료
```

## 데이터 저장 위치

학습 진도와 설정은 아래 경로에 저장됩니다.

```
~/.config/learning-terminal/
├── config.json      # 설정
└── progress.json    # 학습 진도
```

## Thanks to.

Vim 아이디어를 준 (서울대학교 차수현)[https://github.com/soohyuncha], 연세대학교 이경민에게 감사를 표합니다.

## 라이선스

[MIT License](LICENSE)
