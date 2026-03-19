import Conf from 'conf'
import inquirer from 'inquirer'
import chalk from 'chalk'
import boxen from 'boxen'

const store = new Conf({ projectName: 'learning-terminal' })

export function getConfig(key) {
  return store.get(key)
}

export function setConfig(key, value) {
  store.set(key, value)
}

export async function showSettings() {
  console.clear()
  console.log('\n' + boxen(chalk.bold('⚙️   설정'), {
    padding: { top: 0, bottom: 0, left: 2, right: 2 },
    borderColor: 'cyan',
    borderStyle: 'round',
  }))
  console.log()

  const claudeKey = store.get('claudeApiKey') || ''
  const openaiKey = store.get('openaiApiKey') || ''
  const activeAI  = store.get('activeAI') || 'claude'

  console.log('  현재 설정:')
  console.log(`    Claude API 키 : ${claudeKey ? chalk.green('✓ 설정됨') : chalk.red('✗ 미설정')}`)
  console.log(`    OpenAI API 키 : ${openaiKey ? chalk.green('✓ 설정됨') : chalk.red('✗ 미설정')}`)
  console.log(`    사용 중인 AI  : ${chalk.cyan(activeAI === 'claude' ? 'Claude (Anthropic)' : 'GPT (OpenAI)')}`)
  console.log()

  const { action } = await inquirer.prompt([{
    type: 'list',
    name: 'action',
    message: '설정 항목을 선택하세요',
    choices: [
      { name: 'Claude API 키 설정', value: 'claude' },
      { name: 'OpenAI API 키 설정', value: 'openai' },
      { name: '사용할 AI 선택', value: 'selectAI' },
      new inquirer.Separator(),
      { name: '← 뒤로 가기', value: 'back' },
    ],
  }])

  if (action === 'claude') {
    const { key } = await inquirer.prompt([{
      type: 'password',
      name: 'key',
      message: 'Claude API 키를 입력하세요 (sk-ant-...):',
    }])
    if (key) {
      store.set('claudeApiKey', key.trim())
      console.log(chalk.green('\n  ✓ Claude API 키가 저장되었습니다.\n'))
    }
  } else if (action === 'openai') {
    const { key } = await inquirer.prompt([{
      type: 'password',
      name: 'key',
      message: 'OpenAI API 키를 입력하세요 (sk-...):',
    }])
    if (key) {
      store.set('openaiApiKey', key.trim())
      console.log(chalk.green('\n  ✓ OpenAI API 키가 저장되었습니다.\n'))
    }
  } else if (action === 'selectAI') {
    const { ai } = await inquirer.prompt([{
      type: 'list',
      name: 'ai',
      message: '사용할 AI를 선택하세요:',
      choices: [
        { name: 'Claude (Anthropic) — 권장', value: 'claude' },
        { name: 'GPT (OpenAI)', value: 'openai' },
      ],
    }])
    store.set('activeAI', ai)
    console.log(chalk.green(`\n  ✓ ${ai === 'claude' ? 'Claude' : 'GPT'}로 설정되었습니다.\n`))
  }

  if (action !== 'back') {
    await inquirer.prompt([{
      type: 'input', name: '_',
      message: chalk.dim('Enter를 눌러 계속...'), prefix: '',
    }])
    await showSettings()
  }
}
