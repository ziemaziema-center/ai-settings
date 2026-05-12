# Claude Code + OpenRouter Setup

## Models
- Default: deepseek/deepseek-v3.2 (paid, ~$0.02/session)
- Free: qwen/qwen3-coder:free (free tier, 200 req/day)

## Commands
- `claude` → deepseek/deepseek-v3.2
- `claude-qwen` → qwen/qwen3-coder:free

## EC2 Setup
1. Copy settings.json to ~/.claude/settings.json
2. Copy claude-ds.sh to /usr/local/bin/claude-ds && chmod +x
3. Copy claude-qwen.sh to /usr/local/bin/claude-qwen && chmod +x

## OpenRouter
- Requires $10 credit for 1000 req/day free tier
- API key: stored in settings.json (never commit real key)
