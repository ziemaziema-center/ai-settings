#!/bin/bash
python3 -c "
import json
with open('/home/ubuntu/.claude/settings.json','r') as f: s=json.load(f)
s['env']['ANTHROPIC_MODEL']='qwen/qwen3-coder:free'
with open('/home/ubuntu/.claude/settings.json','w') as f: json.dump(s,f,indent=2)
"
exec /usr/bin/claude "$@"
