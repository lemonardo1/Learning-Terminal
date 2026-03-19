import chalk from 'chalk'
import inquirer from 'inquirer'
import Anthropic from '@anthropic-ai/sdk'
import { OpenAI } from 'openai'
import { getConfig } from '../config.js'

const SYSTEM_PROMPT = `당신은 터미널과 Vim을 가르치는 친절하고 유능한 선생님입니다.

규칙:
- 항상 한국어로 답변하세요
- 명령어나 코드는 실제로 실행 가능한 예시를 제공하세요
- 초보자도 이해할 수 있도록 쉽고 친절하게 설명하세요
- 필요하면 단계별로 나누어 설명하세요
- 명령어는 \`백틱\`으로 감싸서 표시하세요
- macOS와 Linux 환경을 모두 고려해 설명하세요`

async function askClaude(messages, apiKey) {
  const client = new Anthropic({ apiKey })
  let fullText = ''

  const stream = client.messages.stream({
    model: 'claude-opus-4-6',
    max_tokens: 2048,
    thinking: { type: 'adaptive' },
    system: SYSTEM_PROMPT,
    messages,
  })

  for await (const event of stream) {
    if (
      event.type === 'content_block_delta' &&
      event.delta.type === 'text_delta'
    ) {
      process.stdout.write(event.delta.text)
      fullText += event.delta.text
    }
  }

  return fullText
}

async function askGPT(messages, apiKey) {
  const client = new OpenAI({ apiKey })
  const formattedMessages = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...messages,
  ]
  let fullText = ''

  const stream = await client.chat.completions.create({
    model: 'gpt-4o',
    messages: formattedMessages,
    stream: true,
  })

  for await (const chunk of stream) {
    const text = chunk.choices[0]?.delta?.content || ''
    if (text) {
      process.stdout.write(text)
      fullText += text
    }
  }

  return fullText
}

export async function startAIChat() {
  console.clear()
  console.log(chalk.bold('\n 🤖 AI 어시스턴트\n'))

  const activeAI = getConfig('activeAI') || 'claude'
  const apiKey   = activeAI === 'claude'
    ? getConfig('claudeApiKey')
    : getConfig('openaiApiKey')

  if (!apiKey) {
    console.log(chalk.red(`\n  ⚠️  ${activeAI === 'claude' ? 'Claude' : 'OpenAI'} API 키가 설정되지 않았습니다.`))
    console.log(chalk.dim('  설정 메뉴(⚙️)에서 API 키를 입력해주세요.\n'))
    await inquirer.prompt([{
      type: 'input', name: '_',
      message: chalk.dim('Enter를 눌러 계속...'), prefix: '',
    }])
    return
  }

  const aiName = activeAI === 'claude' ? 'Claude' : 'GPT'
  console.log(chalk.dim(`  ${aiName}에게 터미널, Vim에 대해 무엇이든 물어보세요.`))
  console.log(chalk.dim('  종료하려면 "exit" 또는 빈 줄에서 Enter 두 번.\n'))

  const messages = []
  let emptyCount = 0

  while (true) {
    const { question } = await inquirer.prompt([{
      type: 'input',
      name: 'question',
      message: chalk.green('나  > '),
      prefix: '',
    }])

    if (!question.trim()) {
      emptyCount++
      if (emptyCount >= 2) break
      continue
    }
    emptyCount = 0

    if (['exit', 'quit', 'q', '종료', ':q'].includes(question.trim().toLowerCase())) break

    messages.push({ role: 'user', content: question })

    console.log()
    process.stdout.write(chalk.cyan(`${aiName} > `))

    try {
      const answer = activeAI === 'claude'
        ? await askClaude(messages, apiKey)
        : await askGPT(messages, apiKey)

      console.log('\n')
      messages.push({ role: 'assistant', content: answer })
    } catch (err) {
      console.log()
      if (err.status === 401 || err.message?.includes('401')) {
        console.log(chalk.red('  ⚠️  API 키가 유효하지 않습니다. 설정에서 확인해주세요.'))
      } else {
        console.log(chalk.red(`  오류: ${err.message}`))
      }
      console.log()
    }
  }
}
