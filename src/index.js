#!/usr/bin/env node
import chalk from 'chalk'
import inquirer from 'inquirer'
import { createRequire } from 'module'
import { showCommandMenu } from './lessons/commands.js'
import { showVimMenu } from './lessons/vim.js'
import { startAIChat } from './ai/assistant.js'
import { showSettings } from './config.js'

const require = createRequire(import.meta.url)

function printBanner() {
  console.clear()
  console.log()
  console.log(chalk.cyan.bold('  ╔══════════════════════════════════════════════╗'))
  console.log(chalk.cyan.bold('  ║                                              ║'))
  console.log(chalk.cyan.bold('  ║    🖥️   터미널 학습 도우미                    ║'))
  console.log(chalk.cyan.bold('  ║    Terminal & Vim Interactive Learning       ║'))
  console.log(chalk.cyan.bold('  ║                                              ║'))
  console.log(chalk.cyan.bold('  ╚══════════════════════════════════════════════╝'))
  console.log()
  console.log(chalk.dim('  pwd, ls, cd, cal, vim 등 기초부터 차근차근 배워봐요!\n'))
}

async function mainMenu() {
  printBanner()

  const { choice } = await inquirer.prompt([{
    type: 'list',
    name: 'choice',
    message: '무엇을 배우고 싶으신가요?',
    choices: [
      { name: '📚  명령어 학습  (pwd, ls, cd, cal, mail ...)', value: 'commands' },
      { name: '⌨️   Vim 에디터 연습', value: 'vim' },
      { name: '🤖  AI 어시스턴트에게 질문하기', value: 'ai' },
      new inquirer.Separator(),
      { name: '⚙️   설정  (API 키 관리)', value: 'settings' },
      { name: '🚪  종료', value: 'exit' },
    ],
  }])

  switch (choice) {
    case 'commands': await showCommandMenu(); break
    case 'vim':      await showVimMenu();     break
    case 'ai':       await startAIChat();     break
    case 'settings': await showSettings();   break
    case 'exit':
      console.log(chalk.green('\n  안녕히 가세요! 열심히 공부하셨어요 👋\n'))
      process.exit(0)
  }

  await mainMenu()
}

mainMenu().catch(err => {
  if (err.name === 'ExitPromptError') process.exit(0)
  console.error(chalk.red('\n오류가 발생했습니다:'), err.message)
  process.exit(1)
})
