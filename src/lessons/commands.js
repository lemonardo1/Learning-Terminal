import chalk from 'chalk'
import inquirer from 'inquirer'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

// ─── Lesson Data ──────────────────────────────────────────────────────────────

const CATEGORIES = [
  { name: '🗺️   기초 탐색     (pwd, ls, cd)', value: 'navigation' },
  { name: '📁  파일 조작     (mkdir, touch, cp, mv, rm)', value: 'files' },
  { name: '📄  파일 보기     (cat, head, tail)', value: 'viewing' },
  { name: '📅  날짜 / 달력   (date, cal)', value: 'datetime' },
  { name: '🔍  텍스트 처리   (echo, grep, wc)', value: 'text' },
  { name: '📧  메일          (mail)', value: 'mail' },
  { name: '🛠️   시스템 도구   (man, which, history)', value: 'system' },
  new inquirer.Separator(),
  { name: '← 뒤로 가기', value: 'back' },
]

const LESSONS = {
  navigation: [
    {
      id: 'pwd',
      name: 'pwd — 현재 위치 확인',
      description:
        chalk.bold('pwd') + ' (Print Working Directory)\n' +
        '현재 내가 있는 디렉터리의 전체 경로를 출력합니다.\n' +
        '터미널을 열면 어디에 있는지 모를 때 가장 먼저 쓰는 명령어입니다.',
      syntax: 'pwd',
      examples: [
        { cmd: 'pwd', desc: '현재 디렉터리의 절대 경로 출력' },
      ],
      exercise: '현재 디렉터리 경로를 출력해보세요.',
      hint: 'pwd 를 입력하고 Enter를 누르세요.',
      safe: true,
      validate: cmd => /^pwd$/.test(cmd.trim()),
    },
    {
      id: 'ls',
      name: 'ls — 파일 목록 보기',
      description:
        chalk.bold('ls') + ' (List)\n' +
        '디렉터리 안의 파일과 폴더 목록을 보여줍니다.\n\n' +
        '자주 쓰는 옵션:\n' +
        `  ${chalk.yellow('ls -l')}   자세한 정보 (권한, 크기, 날짜)\n` +
        `  ${chalk.yellow('ls -a')}   숨김 파일도 표시 (. 으로 시작하는 파일)\n` +
        `  ${chalk.yellow('ls -la')}  위 두 옵션 합치기\n` +
        `  ${chalk.yellow('ls -lh')}  파일 크기를 K/M/G 단위로 표시`,
      syntax: 'ls [옵션] [경로]',
      examples: [
        { cmd: 'ls', desc: '현재 폴더 목록' },
        { cmd: 'ls -la', desc: '상세 목록 (숨김 파일 포함)' },
        { cmd: 'ls -lh /tmp', desc: '/tmp 폴더 상세 목록 (용량 단위 표시)' },
      ],
      exercise: 'ls -la 로 상세 파일 목록을 출력해보세요.',
      hint: '-l 은 상세, -a 는 숨김 파일 포함입니다.',
      safe: true,
      validate: cmd => /^ls(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'cd',
      name: 'cd — 디렉터리 이동',
      description:
        chalk.bold('cd') + ' (Change Directory)\n' +
        '현재 위치를 다른 폴더로 이동합니다.\n\n' +
        '자주 쓰는 경로:\n' +
        `  ${chalk.yellow('cd ~')}       홈 디렉터리로\n` +
        `  ${chalk.yellow('cd ..')}      한 단계 위 폴더로\n` +
        `  ${chalk.yellow('cd -')}       이전 위치로 돌아가기\n` +
        `  ${chalk.yellow('cd /경로')}   절대 경로로 이동`,
      syntax: 'cd [경로]',
      examples: [
        { cmd: 'cd ~',    desc: '홈 디렉터리로 이동' },
        { cmd: 'cd ..',   desc: '상위 폴더로 이동' },
        { cmd: 'cd /tmp', desc: '/tmp 폴더로 이동' },
        { cmd: 'cd -',    desc: '이전 위치로 돌아가기' },
      ],
      exercise: '홈 디렉터리로 이동하는 명령어를 입력해보세요.',
      hint: '~ 는 홈 디렉터리를 의미합니다.',
      safe: true,
      validate: cmd => /^cd(\s|$)/.test(cmd.trim()),
    },
  ],

  files: [
    {
      id: 'mkdir',
      name: 'mkdir — 폴더 만들기',
      description:
        chalk.bold('mkdir') + ' (Make Directory)\n' +
        '새 디렉터리를 생성합니다.\n\n' +
        `  ${chalk.yellow('mkdir -p a/b/c')}  중간 경로도 한 번에 생성`,
      syntax: 'mkdir [옵션] 디렉터리명',
      examples: [
        { cmd: 'mkdir test_dir', desc: 'test_dir 폴더 생성' },
        { cmd: 'mkdir -p a/b/c', desc: 'a, a/b, a/b/c 폴더를 한 번에 생성' },
      ],
      exercise: 'test_dir 라는 폴더를 만들어보세요.',
      hint: 'mkdir test_dir 을 입력해보세요.',
      safe: true,
      validate: cmd => /^mkdir(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'touch',
      name: 'touch — 빈 파일 만들기',
      description:
        chalk.bold('touch') + '\n' +
        '빈 파일을 만들거나, 이미 있는 파일의 수정 시간을 현재로 업데이트합니다.',
      syntax: 'touch 파일명',
      examples: [
        { cmd: 'touch hello.txt',    desc: '빈 hello.txt 파일 생성' },
        { cmd: 'touch a.txt b.txt',  desc: '여러 파일을 한 번에 생성' },
      ],
      exercise: 'hello.txt 파일을 만들어보세요.',
      hint: 'touch hello.txt 를 입력하면 됩니다.',
      safe: true,
      validate: cmd => /^touch(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'cp',
      name: 'cp — 파일/폴더 복사',
      description:
        chalk.bold('cp') + ' (Copy)\n' +
        '파일이나 폴더를 복사합니다.\n\n' +
        `  ${chalk.yellow('cp -r')}  폴더를 복사할 때 필요한 옵션`,
      syntax: 'cp [옵션] 원본 대상',
      examples: [
        { cmd: 'cp a.txt b.txt',  desc: 'a.txt를 b.txt로 복사' },
        { cmd: 'cp a.txt /tmp/',  desc: 'a.txt를 /tmp 폴더에 복사' },
        { cmd: 'cp -r 폴더1 폴더2', desc: '폴더1을 폴더2로 복사' },
      ],
      exercise: 'cp 명령어의 도움말을 확인해보세요.',
      hint: 'cp --help 를 입력해보세요.',
      safe: true,
      validate: cmd => /^cp(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'mv',
      name: 'mv — 파일/폴더 이동 또는 이름 변경',
      description:
        chalk.bold('mv') + ' (Move)\n' +
        '파일이나 폴더를 이동하거나 이름을 변경합니다.',
      syntax: 'mv 원본 대상',
      examples: [
        { cmd: 'mv old.txt new.txt', desc: '파일 이름 변경' },
        { cmd: 'mv a.txt /tmp/',     desc: 'a.txt를 /tmp로 이동' },
      ],
      exercise: 'mv 명령어의 도움말을 확인해보세요.',
      hint: 'mv --help 를 입력해보세요.',
      safe: true,
      validate: cmd => /^mv(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'rm',
      name: 'rm — 파일/폴더 삭제 ⚠️',
      description:
        chalk.bold.red('rm') + ' (Remove)\n' +
        chalk.red('삭제된 파일은 휴지통 없이 영구 삭제됩니다! 신중하게 사용하세요.\n\n') +
        `  ${chalk.yellow('rm -i')}    삭제 전 확인 (권장)\n` +
        `  ${chalk.yellow('rm -r')}    폴더 삭제\n` +
        `  ${chalk.yellow('rm -rf')}   강제 삭제 (매우 위험!)`,
      syntax: 'rm [옵션] 파일명',
      examples: [
        { cmd: 'rm -i a.txt',  desc: '확인 후 삭제 (안전)' },
        { cmd: 'rm -rf 폴더',  desc: '폴더 강제 삭제 (위험!)' },
      ],
      exercise: 'rm --help 로 도움말을 확인해보세요.',
      hint: 'rm --help 를 입력해보세요.',
      safe: true,
      validate: cmd => /^rm(\s|$)/.test(cmd.trim()),
    },
  ],

  viewing: [
    {
      id: 'cat',
      name: 'cat — 파일 내용 보기',
      description:
        chalk.bold('cat') + '\n' +
        '파일의 전체 내용을 터미널에 출력합니다.\n\n' +
        `  ${chalk.yellow('cat -n')}  줄 번호와 함께 출력`,
      syntax: 'cat [옵션] 파일명',
      examples: [
        { cmd: 'cat /etc/hostname',   desc: '호스트 이름 파일 보기' },
        { cmd: 'cat -n /etc/hosts',   desc: '줄 번호와 함께 보기' },
      ],
      exercise: '/etc/hostname 파일의 내용을 출력해보세요.',
      hint: 'cat /etc/hostname 을 입력해보세요.',
      safe: true,
      validate: cmd => /^cat(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'head',
      name: 'head — 파일 앞부분 보기',
      description:
        chalk.bold('head') + '\n' +
        '파일의 처음 N줄을 출력합니다. 기본값: 10줄\n\n' +
        `  ${chalk.yellow('head -n 5')}  처음 5줄만 출력`,
      syntax: 'head [옵션] 파일명',
      examples: [
        { cmd: 'head /etc/hosts',       desc: '처음 10줄 출력' },
        { cmd: 'head -n 5 /etc/hosts',  desc: '처음 5줄만 출력' },
      ],
      exercise: 'head -n 5 /etc/hosts 를 입력해보세요.',
      hint: '-n 뒤에 출력할 줄 수를 입력합니다.',
      safe: true,
      validate: cmd => /^head(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'tail',
      name: 'tail — 파일 뒷부분 보기',
      description:
        chalk.bold('tail') + '\n' +
        '파일의 마지막 N줄을 출력합니다.\n\n' +
        `  ${chalk.yellow('tail -f')}  파일에 내용 추가될 때 실시간으로 보기 (로그 모니터링)`,
      syntax: 'tail [옵션] 파일명',
      examples: [
        { cmd: 'tail /etc/hosts',         desc: '마지막 10줄 출력' },
        { cmd: 'tail -n 3 /etc/hosts',    desc: '마지막 3줄만 출력' },
        { cmd: 'tail -f /var/log/system.log', desc: '로그 실시간 보기 (Ctrl+C로 종료)' },
      ],
      exercise: 'tail -n 3 /etc/hosts 를 입력해보세요.',
      hint: '-n 뒤에 줄 수를 입력합니다.',
      safe: true,
      validate: cmd => /^tail(\s|$)/.test(cmd.trim()),
    },
  ],

  datetime: [
    {
      id: 'date',
      name: 'date — 날짜와 시간 보기',
      description:
        chalk.bold('date') + '\n' +
        '현재 날짜와 시간을 출력합니다.\n\n' +
        '형식 지정:\n' +
        `  ${chalk.yellow('date "+%Y-%m-%d"')}         2024-01-15\n` +
        `  ${chalk.yellow('date "+%H:%M:%S"')}         14:30:00\n` +
        `  ${chalk.yellow('date "+%Y년 %m월 %d일"')}   2024년 01월 15일`,
      syntax: 'date ["+형식"]',
      examples: [
        { cmd: 'date',                    desc: '현재 날짜와 시간' },
        { cmd: 'date "+%Y-%m-%d %H:%M"', desc: '날짜와 시간을 특정 형식으로' },
      ],
      exercise: '현재 날짜와 시간을 출력해보세요.',
      hint: 'date 명령어를 그냥 입력하면 됩니다.',
      safe: true,
      validate: cmd => /^date(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'cal',
      name: 'cal — 달력 보기',
      description:
        chalk.bold('cal') + '\n' +
        '터미널에서 달력을 보여줍니다.\n\n' +
        `  ${chalk.yellow('cal')}           이번 달 달력\n` +
        `  ${chalk.yellow('cal 2026')}      2026년 전체 달력\n` +
        `  ${chalk.yellow('cal 3 2026')}    2026년 3월 달력`,
      syntax: 'cal [월] [연도]',
      examples: [
        { cmd: 'cal',          desc: '이번 달 달력' },
        { cmd: 'cal 12 2026',  desc: '2026년 12월 달력' },
        { cmd: 'cal 2026',     desc: '2026년 전체 달력' },
      ],
      exercise: '이번 달 달력을 출력해보세요.',
      hint: 'cal 명령어를 입력하면 됩니다.',
      safe: true,
      validate: cmd => /^cal(\s|$)/.test(cmd.trim()),
    },
  ],

  text: [
    {
      id: 'echo',
      name: 'echo — 텍스트 출력',
      description:
        chalk.bold('echo') + '\n' +
        '텍스트를 화면에 출력합니다.\n\n' +
        `  ${chalk.yellow('echo $HOME')}           환경 변수 출력\n` +
        `  ${chalk.yellow('echo "text" > file')}   파일에 쓰기\n` +
        `  ${chalk.yellow('echo "text" >> file')}  파일에 추가`,
      syntax: 'echo [텍스트]',
      examples: [
        { cmd: 'echo "Hello, World!"', desc: 'Hello, World! 출력' },
        { cmd: 'echo $HOME',            desc: '홈 디렉터리 경로 출력' },
        { cmd: 'echo $USER',            desc: '현재 사용자 이름 출력' },
      ],
      exercise: '"안녕하세요!" 를 출력해보세요.',
      hint: 'echo "안녕하세요!" 를 입력해보세요.',
      safe: true,
      validate: cmd => /^echo(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'grep',
      name: 'grep — 텍스트 검색',
      description:
        chalk.bold('grep') + '\n' +
        '파일에서 특정 패턴을 검색합니다.\n\n' +
        `  ${chalk.yellow('grep -i')}  대소문자 무시\n` +
        `  ${chalk.yellow('grep -n')}  줄 번호 표시\n` +
        `  ${chalk.yellow('grep -r')}  폴더 내 모든 파일 검색\n` +
        `  ${chalk.yellow('grep -v')}  패턴이 없는 줄만 출력`,
      syntax: 'grep [옵션] 패턴 [파일]',
      examples: [
        { cmd: 'grep "localhost" /etc/hosts',   desc: '/etc/hosts에서 localhost 검색' },
        { cmd: 'grep -n "root" /etc/passwd',    desc: '줄 번호와 함께 root 검색' },
        { cmd: 'grep -rn "TODO" ~/',            desc: '홈 폴더에서 TODO 검색' },
      ],
      exercise: 'grep "localhost" /etc/hosts 를 입력해보세요.',
      hint: 'grep "검색어" 파일명 형식으로 입력합니다.',
      safe: true,
      validate: cmd => /^grep(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'wc',
      name: 'wc — 글자/줄 수 세기',
      description:
        chalk.bold('wc') + ' (Word Count)\n' +
        '파일의 줄 수, 단어 수, 글자 수를 셉니다.\n\n' +
        `  ${chalk.yellow('wc -l')}  줄 수만\n` +
        `  ${chalk.yellow('wc -w')}  단어 수만\n` +
        `  ${chalk.yellow('wc -c')}  바이트 수만`,
      syntax: 'wc [옵션] 파일',
      examples: [
        { cmd: 'wc /etc/hosts',    desc: '줄·단어·글자 수 모두 출력' },
        { cmd: 'wc -l /etc/hosts', desc: '줄 수만 출력' },
      ],
      exercise: 'wc -l /etc/hosts 로 줄 수를 출력해보세요.',
      hint: 'wc -l 파일명 형식으로 입력합니다.',
      safe: true,
      validate: cmd => /^wc(\s|$)/.test(cmd.trim()),
    },
  ],

  mail: [
    {
      id: 'mail',
      name: 'mail — 이메일 보내기/받기',
      description:
        chalk.bold('mail') + '\n' +
        '터미널에서 이메일을 보내거나 받는 명령어입니다.\n' +
        chalk.dim('⚠️  서버 환경에 따라 설치/설정이 필요할 수 있습니다.\n\n') +
        '기본 사용법:\n' +
        `  ${chalk.yellow('mail 받는사람@email.com')}\n` +
        '  제목과 내용 입력 후 Ctrl+D 로 전송\n\n' +
        '자주 쓰는 옵션:\n' +
        `  ${chalk.yellow('mail -s "제목" 받는사람')}   제목 지정\n` +
        `  ${chalk.yellow('echo "내용" | mail -s "제목" 받는사람')}  파이프로 전송`,
      syntax: 'mail [-s 제목] 받는사람',
      examples: [
        { cmd: 'mail -s "안녕" user@example.com',                    desc: '이메일 보내기' },
        { cmd: 'echo "본문내용" | mail -s "제목" user@example.com',  desc: '파이프로 내용 전달' },
        { cmd: 'mail',                                                 desc: '받은 메일함 확인' },
      ],
      exercise: 'mail 명령어의 도움말을 확인해보세요.',
      hint: 'mail --help 또는 man mail 을 입력해보세요.',
      safe: true,
      validate: cmd => /^mail(\s|$)/.test(cmd.trim()),
    },
  ],

  system: [
    {
      id: 'man',
      name: 'man — 명령어 설명서 보기',
      description:
        chalk.bold('man') + ' (Manual)\n' +
        '명령어의 공식 사용 설명서를 엽니다.\n\n' +
        '조작 방법:\n' +
        `  ${chalk.yellow('↑ ↓')}   스크롤\n` +
        `  ${chalk.yellow('q')}     종료\n` +
        `  ${chalk.yellow('/')}     검색 (입력 후 Enter)\n` +
        `  ${chalk.yellow('n')}     다음 검색 결과`,
      syntax: 'man 명령어',
      examples: [
        { cmd: 'man ls',  desc: 'ls 명령어 설명서 보기' },
        { cmd: 'man man', desc: 'man 자체의 설명서 보기' },
      ],
      exercise: 'man ls 를 입력해서 ls 설명서를 확인해보세요.',
      hint: '보고 나면 q 를 눌러 종료합니다.',
      safe: false,   // man opens interactive pager
      validate: cmd => /^man(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'which',
      name: 'which — 명령어 위치 찾기',
      description:
        chalk.bold('which') + '\n' +
        '명령어가 저장된 파일의 경로를 출력합니다.',
      syntax: 'which 명령어',
      examples: [
        { cmd: 'which node',    desc: 'node 명령어의 경로' },
        { cmd: 'which python3', desc: 'python3의 경로' },
        { cmd: 'which ls',      desc: 'ls 명령어의 경로' },
      ],
      exercise: 'which ls 로 ls 명령어의 위치를 확인해보세요.',
      hint: 'which 다음에 명령어 이름을 입력합니다.',
      safe: true,
      validate: cmd => /^which(\s|$)/.test(cmd.trim()),
    },
    {
      id: 'history',
      name: 'history — 명령어 기록 보기',
      description:
        chalk.bold('history') + '\n' +
        '이전에 입력한 명령어 목록을 보여줍니다.\n\n' +
        `  ${chalk.yellow('history 20')}   최근 20개만 보기\n` +
        `  ${chalk.yellow('!123')}         히스토리 번호 123번 명령어 재실행\n` +
        `  ${chalk.yellow('!!')}           마지막 명령어 재실행\n` +
        `  ${chalk.yellow('Ctrl+R')}       히스토리 검색`,
      syntax: 'history [숫자]',
      examples: [
        { cmd: 'history',           desc: '전체 히스토리' },
        { cmd: 'history 20',        desc: '최근 20개만' },
        { cmd: 'history | grep ls', desc: 'ls가 포함된 명령어만' },
      ],
      exercise: 'history 20 으로 최근 명령어를 확인해보세요.',
      hint: 'history 를 입력하면 됩니다.',
      safe: true,
      validate: cmd => /^history(\s|$)/.test(cmd.trim()),
    },
  ],
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const DANGEROUS = /^(rm\s+-rf|sudo\s+rm|dd\s+if|mkfs|:(){ :|:& };:)/

async function runCommand(cmd) {
  if (DANGEROUS.test(cmd.trim())) {
    return { stdout: '', stderr: '⚠️  위험한 명령어는 실행하지 않습니다.', success: false }
  }
  try {
    const { stdout, stderr } = await execAsync(cmd, {
      shell: process.env.SHELL || '/bin/zsh',
      cwd: process.env.HOME,
      timeout: 5000,
    })
    return { stdout: stdout || '', stderr: stderr || '', success: true }
  } catch (err) {
    return { stdout: err.stdout || '', stderr: err.stderr || err.message, success: false }
  }
}

// ─── UI ───────────────────────────────────────────────────────────────────────

async function showLesson(lesson) {
  console.clear()
  console.log(chalk.cyan.bold(`\n 📖 ${lesson.name}\n`))
  console.log(chalk.dim('─'.repeat(62)))
  console.log('\n' + lesson.description + '\n')
  console.log(chalk.bold('문법:'))
  console.log(`  ${chalk.yellow(lesson.syntax)}\n`)
  console.log(chalk.bold('예시:'))
  for (const ex of lesson.examples) {
    console.log(`  ${chalk.yellow('$')} ${chalk.bold(ex.cmd)}`)
    console.log(`    ${chalk.dim(ex.desc)}`)
  }
  console.log('\n' + chalk.dim('─'.repeat(62)))

  const choices = [
    { name: '✏️  직접 명령어 입력해보기', value: 'practice' },
    { name: '▶️  예시 명령어 실행해보기', value: 'demo' },
    { name: '← 목록으로 돌아가기',       value: 'back' },
  ]

  const { action } = await inquirer.prompt([{
    type: 'list', name: 'action',
    message: '다음을 선택하세요',
    choices,
  }])

  if (action === 'practice') await practiceMode(lesson)
  if (action === 'demo')     await demoMode(lesson)
}

async function practiceMode(lesson) {
  console.log(`\n  💪 연습: ${chalk.bold(lesson.exercise)}`)
  if (lesson.hint) console.log(`  ${chalk.dim('💡 힌트: ' + lesson.hint)}`)
  console.log(chalk.dim('\n  (q 입력 시 종료)\n'))

  while (true) {
    const { cmd } = await inquirer.prompt([{
      type: 'input', name: 'cmd',
      message: chalk.yellow('  $ '), prefix: '',
    }])

    const trimmed = cmd.trim()
    if (!trimmed) continue
    if (trimmed === 'q' || trimmed === 'exit') break

    const { stdout, stderr, success } = await runCommand(trimmed)
    if (stdout) {
      console.log(chalk.dim('\n  출력:'))
      stdout.trim().split('\n').slice(0, 25).forEach(l => {
        console.log(chalk.green('  ' + l))
      })
    }
    if (stderr) {
      const firstLine = stderr.trim().split('\n')[0]
      console.log(chalk.red('\n  ' + firstLine))
    }
    console.log()

    if (lesson.validate && lesson.validate(trimmed)) {
      console.log(chalk.green('  ✓ 잘 하셨습니다! (q 입력 시 종료)\n'))
    }
  }
}

async function demoMode(lesson) {
  console.log('\n  ▶️  예시 명령어 실행:\n')
  for (const ex of lesson.examples) {
    if (DANGEROUS.test(ex.cmd)) {
      console.log(`  ${chalk.yellow('$')} ${chalk.bold(ex.cmd)}`)
      console.log(chalk.dim(`    ${ex.desc}`))
      console.log(chalk.dim('    (안전을 위해 실행하지 않습니다)\n'))
      continue
    }
    console.log(`  ${chalk.yellow('$')} ${chalk.bold(ex.cmd)}`)
    console.log(chalk.dim(`    ${ex.desc}`))
    const { stdout, stderr } = await runCommand(ex.cmd)
    if (stdout) {
      stdout.trim().split('\n').slice(0, 10).forEach(l => {
        if (l) console.log(chalk.green('  ' + l))
      })
    }
    if (stderr) console.log(chalk.dim('  ' + stderr.trim().split('\n')[0]))
    console.log()
  }
  await inquirer.prompt([{
    type: 'input', name: '_',
    message: chalk.dim('  Enter를 눌러 계속...'), prefix: '',
  }])
}

// ─── Exported Menu ────────────────────────────────────────────────────────────

export async function showCommandMenu() {
  console.clear()
  console.log(chalk.bold('\n 📚 명령어 학습\n'))

  const { category } = await inquirer.prompt([{
    type: 'list', name: 'category',
    message: '배울 카테고리를 선택하세요:',
    choices: CATEGORIES,
    pageSize: 12,
  }])

  if (category === 'back') return

  const lessons = LESSONS[category]
  if (!lessons) return

  while (true) {
    console.clear()
    console.log(chalk.bold('\n 📚 명령어 목록\n'))

    const { lessonId } = await inquirer.prompt([{
      type: 'list', name: 'lessonId',
      message: '배울 명령어를 선택하세요:',
      choices: [
        ...lessons.map(l => ({ name: `  ${l.name}`, value: l.id })),
        new inquirer.Separator(),
        { name: '← 카테고리 목록으로', value: 'back' },
      ],
    }])

    if (lessonId === 'back') break

    const lesson = lessons.find(l => l.id === lessonId)
    if (lesson) await showLesson(lesson)
  }

  await showCommandMenu()
}
