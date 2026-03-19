import chalk from 'chalk'
import inquirer from 'inquirer'
import { spawnSync } from 'child_process'
import { writeFileSync, existsSync } from 'fs'
import { join } from 'path'

const PRACTICE_FILE = join(process.env.HOME || '/tmp', 'vim_practice.txt')

const PRACTICE_CONTENT = `# Vim 연습 파일 (vim_practice.txt)
# 이 파일에서 Vim 명령어를 자유롭게 연습해보세요!
# ─────────────────────────────────────────────

안녕하세요! Vim 연습을 시작합니다.

1. 첫 번째 줄입니다.
2. 두 번째 줄입니다.
3. 세 번째 줄입니다.

The quick brown fox jumps over the lazy dog.
Hello World
Hello Vim
Hello Terminal

# 검색 연습용 텍스트:
ERROR: something went wrong
WARNING: check your config
INFO: everything is fine
ERROR: another error here

# 편집 연습:
apple banana cherry
one two three four five

# 파일 끝
`

const LESSONS = [
  {
    id: 'intro',
    name: 'Vim 소개',
    content: `
${chalk.bold.cyan('Vim이란?')}

Vim은 강력하고 효율적인 텍스트 에디터입니다.
서버 환경에서 거의 항상 사용 가능하며, 손이 키보드에서 떠나지 않아도 되어
숙련되면 매우 빠르게 코드를 작성할 수 있습니다.

${chalk.bold('Vim을 여는 방법:')}
  ${chalk.yellow('vim 파일명')}      파일 열기 (없으면 새로 생성)
  ${chalk.yellow('vim')}            빈 파일로 시작

${chalk.bold.red('⚠️  가장 중요: Vim에서 나가는 방법')}

  1. ${chalk.yellow('Esc')} 를 눌러 일반 모드로 이동
  2. ${chalk.yellow(':q!')} 를 입력하고 Enter → 저장 없이 강제 종료
  3. ${chalk.yellow(':wq')} 를 입력하고 Enter → 저장하고 종료

${chalk.bold('Vim의 핵심: 모드(Mode) 시스템')}
  Vim에는 여러 모드가 있습니다. 처음 열리면 ${chalk.green('일반 모드')}입니다.

  ${chalk.green('일반 모드')}  → 명령어 입력 (기본 상태)
  ${chalk.yellow('입력 모드')}  → 실제 타이핑
  ${chalk.blue('비주얼 모드')} → 텍스트 선택`,
    practice: null,
  },
  {
    id: 'modes',
    name: '모드 전환 (Mode Switching)',
    content: `
${chalk.bold.cyan('Vim의 주요 모드')}

${chalk.bold.green('일반 모드 (Normal Mode)')} — 기본 상태
  • Vim을 열면 이 모드로 시작
  • ${chalk.yellow('Esc')} 를 누르면 언제든지 돌아올 수 있음

${chalk.bold.yellow('입력 모드 (Insert Mode)')} — 타이핑 가능
  화면 하단에 ${chalk.yellow('-- INSERT --')} 표시

  일반 모드에서 진입하는 방법:
  ${chalk.yellow('i')}  현재 커서 위치에서 입력 시작
  ${chalk.yellow('a')}  현재 커서 다음 위치에서 입력 시작
  ${chalk.yellow('o')}  아랫줄에 새 줄 추가하고 입력 시작
  ${chalk.yellow('O')}  윗줄에 새 줄 추가하고 입력 시작
  ${chalk.yellow('A')}  줄의 맨 끝에서 입력 시작

${chalk.bold.blue('비주얼 모드 (Visual Mode)')} — 선택
  ${chalk.yellow('v')}  글자 단위 선택
  ${chalk.yellow('V')}  줄 단위 선택
  ${chalk.yellow('Ctrl+v')}  블록 선택

${chalk.bold.magenta('명령행 모드 (Command-line Mode)')} — : 로 진입
  ${chalk.yellow(':w')}   저장
  ${chalk.yellow(':q')}   종료
  ${chalk.yellow(':wq')}  저장 후 종료
  ${chalk.yellow(':q!')}  강제 종료 (변경 무시)`,
    practice: {
      task: 'Vim을 열고 "Hello, Vim!" 을 타이핑한 후 저장하고 종료해보세요.',
      steps: [
        '아래 "Vim 열기" 를 선택하면 vim_practice.txt 가 열립니다',
        'i 를 눌러 입력 모드로 진입합니다',
        '"Hello, Vim!" 을 타이핑합니다',
        'Esc 를 눌러 일반 모드로 돌아갑니다',
        ':wq 를 입력하고 Enter 를 눌러 저장 후 종료합니다',
      ],
    },
  },
  {
    id: 'navigation',
    name: '이동하기 (Navigation)',
    content: `
${chalk.bold.cyan('커서 이동 명령어')}

${chalk.bold('기본 이동 (방향키 대신 사용):')}
  ${chalk.yellow('h')} ← 왼쪽    ${chalk.yellow('l')} → 오른쪽
  ${chalk.yellow('j')} ↓ 아래    ${chalk.yellow('k')} ↑ 위

${chalk.bold('단어 단위 이동:')}
  ${chalk.yellow('w')}  다음 단어의 시작으로
  ${chalk.yellow('b')}  이전 단어의 시작으로
  ${chalk.yellow('e')}  현재 단어의 끝으로

${chalk.bold('줄 단위 이동:')}
  ${chalk.yellow('0')}  줄의 맨 처음으로
  ${chalk.yellow('$')}  줄의 맨 끝으로
  ${chalk.yellow('^')}  줄의 첫 번째 글자로

${chalk.bold('파일 단위 이동:')}
  ${chalk.yellow('gg')}      파일의 맨 처음으로
  ${chalk.yellow('G')}       파일의 맨 끝으로
  ${chalk.yellow('숫자G')}   특정 줄로 이동 (예: 10G)
  ${chalk.yellow('Ctrl+f')}  한 페이지 아래
  ${chalk.yellow('Ctrl+b')}  한 페이지 위

${chalk.dim('💡 팁: 숫자를 앞에 붙이면 반복됩니다. 5j = 5줄 아래, 3w = 3단어 앞으로')}`,
    practice: {
      task: '다양한 이동 명령어를 연습해보세요.',
      steps: [
        'Vim 열기를 선택하면 vim_practice.txt 가 열립니다',
        'h j k l 로 이동해보세요',
        'gg 로 파일 처음으로, G 로 파일 끝으로 가보세요',
        '5j 처럼 숫자를 붙여서 이동해보세요',
        ':q! 로 종료합니다',
      ],
    },
  },
  {
    id: 'editing',
    name: '편집하기 (Editing)',
    content: `
${chalk.bold.cyan('텍스트 편집 명령어')} (일반 모드에서 사용)

${chalk.bold('삭제:')}
  ${chalk.yellow('x')}    현재 글자 삭제
  ${chalk.yellow('dd')}   현재 줄 삭제 (잘라내기)
  ${chalk.yellow('dw')}   현재 단어 삭제
  ${chalk.yellow('d$')}   현재 위치부터 줄 끝까지 삭제

${chalk.bold('복사 (Yank):')}
  ${chalk.yellow('yy')}   현재 줄 복사
  ${chalk.yellow('yw')}   현재 단어 복사
  ${chalk.yellow('y$')}   현재 위치부터 줄 끝까지 복사

${chalk.bold('붙여넣기:')}
  ${chalk.yellow('p')}    현재 위치 다음에 붙여넣기
  ${chalk.yellow('P')}    현재 위치 앞에 붙여넣기

${chalk.bold('실행 취소 / 재실행:')}
  ${chalk.yellow('u')}        실행 취소 (Undo)
  ${chalk.yellow('Ctrl+r')}   재실행 (Redo)

${chalk.bold('교체:')}
  ${chalk.yellow('r')} + 글자   현재 글자를 교체
  ${chalk.yellow('cw')}        현재 단어를 바꾸기 (입력 모드 진입)

${chalk.dim('💡 팁: 3dd = 3줄 삭제, 5yy = 5줄 복사, 2p = 2번 붙여넣기')}`,
    practice: {
      task: '편집 명령어를 연습해보세요.',
      steps: [
        'Vim 열기를 선택하면 vim_practice.txt 가 열립니다',
        'dd 로 줄 삭제, yy 로 복사, p 로 붙여넣기 연습',
        'u 로 실행 취소, Ctrl+r 로 재실행 연습',
        ':q! 로 저장 없이 종료합니다',
      ],
    },
  },
  {
    id: 'search',
    name: '검색과 치환 (Search & Replace)',
    content: `
${chalk.bold.cyan('검색과 치환')}

${chalk.bold('검색 (일반 모드에서):')}
  ${chalk.yellow('/검색어')}   앞으로 검색 (Enter 로 실행)
  ${chalk.yellow('?검색어')}   뒤로 검색
  ${chalk.yellow('n')}         다음 결과로
  ${chalk.yellow('N')}         이전 결과로
  ${chalk.yellow('*')}         현재 커서의 단어를 검색

${chalk.bold('치환 (명령행 모드):')}
  ${chalk.yellow(':s/원본/대체/')}        현재 줄에서 첫 번째만
  ${chalk.yellow(':s/원본/대체/g')}       현재 줄의 모두
  ${chalk.yellow(':%s/원본/대체/g')}      파일 전체에서 모두
  ${chalk.yellow(':%s/원본/대체/gc')}     파일 전체, 하나씩 확인하며

${chalk.bold('예시:')}
  ${chalk.yellow(':%s/Hello/안녕/g')}     파일의 모든 "Hello" → "안녕"
  ${chalk.yellow(':%s/ERROR/FIXED/gc')}   하나씩 확인하며 교체

${chalk.dim('💡 팁: 검색 하이라이트 제거는 :noh 또는 :nohlsearch')}`,
    practice: {
      task: '검색과 치환을 연습해보세요.',
      steps: [
        'Vim 열기를 선택하면 vim_practice.txt 가 열립니다',
        '/ERROR 로 ERROR를 검색하고 n 으로 다음 결과로 이동해보세요',
        ':%s/Hello/안녕/g 로 Hello를 안녕으로 교체해보세요',
        ':q! 로 저장 없이 종료합니다',
      ],
    },
  },
  {
    id: 'saveclose',
    name: '저장과 종료',
    content: `
${chalk.bold.cyan('Vim 저장과 종료')}

${chalk.bold('저장:')}
  ${chalk.yellow(':w')}           현재 파일에 저장
  ${chalk.yellow(':w 파일명')}    다른 이름으로 저장

${chalk.bold('종료:')}
  ${chalk.yellow(':q')}    종료 (변경사항 없을 때)
  ${chalk.yellow(':q!')}   강제 종료 (변경사항 무시)

${chalk.bold('저장 후 종료:')}
  ${chalk.yellow(':wq')}   저장하고 종료
  ${chalk.yellow(':x')}    변경된 경우에만 저장하고 종료
  ${chalk.yellow('ZZ')}    :wq 와 동일 (빠른 종료)
  ${chalk.yellow('ZQ')}    :q! 와 동일

${chalk.bold('여러 파일 작업:')}
  ${chalk.yellow(':e 파일명')}   다른 파일 열기
  ${chalk.yellow(':sp 파일')}    수평 분할로 열기
  ${chalk.yellow(':vsp 파일')}   수직 분할로 열기
  ${chalk.yellow('Ctrl+w w')}    분할 창 간 이동

${chalk.bold.red('⚠️  Vim에서 나가는 가장 확실한 방법:')}
  ${chalk.yellow('Esc')} → ${chalk.yellow(':q!')} → ${chalk.yellow('Enter')}`,
    practice: null,
  },
  {
    id: 'tips',
    name: '실용적인 팁과 단축키',
    content: `
${chalk.bold.cyan('Vim 실용 팁')}

${chalk.bold('줄 번호 표시:')}
  ${chalk.yellow(':set number')}     줄 번호 켜기
  ${chalk.yellow(':set nonumber')}   줄 번호 끄기
  ${chalk.yellow(':set relativenumber')}  상대적 줄 번호

${chalk.bold('들여쓰기:')}
  ${chalk.yellow('>>')}    현재 줄 들여쓰기
  ${chalk.yellow('<<')}    현재 줄 내어쓰기

${chalk.bold('반복 실행:')}
  ${chalk.yellow('.')}    마지막 명령어 반복

${chalk.bold('자동완성 (입력 모드에서):')}
  ${chalk.yellow('Ctrl+n')}   다음 자동완성 후보
  ${chalk.yellow('Ctrl+p')}   이전 자동완성 후보

${chalk.bold('vimrc 설정 예시 (~/.vimrc):')}
  ${chalk.dim('set number          " 줄 번호 표시')}
  ${chalk.dim('set tabstop=2       " 탭 크기 2칸')}
  ${chalk.dim('set expandtab       " 탭을 스페이스로')}
  ${chalk.dim('syntax on           " 문법 강조')}

${chalk.bold('Vim 치트시트 요약:')}
  ${chalk.yellow('i/a/o')}  입력 모드    ${chalk.yellow('Esc')}   일반 모드
  ${chalk.yellow('hjkl')}   이동         ${chalk.yellow('dd/yy/p')} 삭제/복사/붙여넣기
  ${chalk.yellow('/검색')}  검색         ${chalk.yellow(':%s/a/b/g')} 전체 치환
  ${chalk.yellow(':w')}    저장         ${chalk.yellow(':q!')}  강제 종료`,
    practice: null,
  },
]

// ─── UI ───────────────────────────────────────────────────────────────────────

function ensurePracticeFile() {
  if (!existsSync(PRACTICE_FILE)) {
    writeFileSync(PRACTICE_FILE, PRACTICE_CONTENT, 'utf8')
  }
}

async function openVimPractice(task, steps) {
  console.log('\n  ' + chalk.bold.green('🎯 실습 과제:'))
  console.log(`  ${task}\n`)
  console.log(chalk.bold('  단계:'))
  steps.forEach((step, i) => {
    console.log(`    ${chalk.yellow(`${i + 1}.`)} ${step}`)
  })
  console.log()

  const { openVim } = await inquirer.prompt([{
    type: 'confirm',
    name: 'openVim',
    message: 'vim_practice.txt 파일을 열까요?',
    default: true,
  }])

  if (openVim) {
    ensurePracticeFile()
    console.log(chalk.dim(`\n  파일 위치: ${PRACTICE_FILE}`))
    console.log(chalk.yellow('  Vim이 열립니다. :q! 로 종료하면 돌아옵니다.\n'))
    await new Promise(r => setTimeout(r, 800))
    spawnSync('vim', [PRACTICE_FILE], { stdio: 'inherit' })
    console.log(chalk.green('\n  ✓ Vim에서 돌아왔습니다!\n'))
  }

  await inquirer.prompt([{
    type: 'input', name: '_',
    message: chalk.dim('  Enter를 눌러 계속...'), prefix: '',
  }])
}

async function showVimLesson(lesson) {
  console.clear()
  console.log(chalk.cyan.bold(`\n ⌨️  ${lesson.name}\n`))
  console.log(chalk.dim('─'.repeat(62)))
  console.log(lesson.content)
  console.log(chalk.dim('─'.repeat(62)))

  const choices = []
  if (lesson.practice) {
    choices.push({ name: '🎯 직접 연습해보기 (Vim 열기)', value: 'practice' })
  }
  choices.push({ name: '← 목록으로 돌아가기', value: 'back' })

  const { action } = await inquirer.prompt([{
    type: 'list', name: 'action',
    message: '다음을 선택하세요:',
    choices,
  }])

  if (action === 'practice' && lesson.practice) {
    await openVimPractice(lesson.practice.task, lesson.practice.steps)
  }
}

// ─── Exported Menu ────────────────────────────────────────────────────────────

export async function showVimMenu() {
  while (true) {
    console.clear()
    console.log(chalk.bold('\n ⌨️  Vim 에디터 학습\n'))

    const choices = [
      ...LESSONS.map((l, i) => ({
        name: `  ${i + 1}. ${l.name}`,
        value: l.id,
      })),
      new inquirer.Separator(),
      { name: '← 뒤로 가기', value: 'back' },
    ]

    const { lessonId } = await inquirer.prompt([{
      type: 'list', name: 'lessonId',
      message: 'Vim 레슨을 선택하세요:',
      choices,
      pageSize: 12,
    }])

    if (lessonId === 'back') return

    const lesson = LESSONS.find(l => l.id === lessonId)
    if (lesson) await showVimLesson(lesson)
  }
}
