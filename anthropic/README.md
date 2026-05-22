# Anthropic Agent HQ

This file supports 5 languages: English, Francais, Korean, Chinese, and Spanish.
Support de 5 langues: anglais, francais, coreen, chinois et espagnol.
5개 언어 지원: 영어, 프랑스어, 한국어, 중국어, 스페인어.
本文件支持 5 种语言：英语、法语、韩语、中文、西班牙语。
Este archivo admite 5 idiomas: ingles, frances, coreano, chino y espanol.

---

## English

### What this folder is

`anthropic/` is the Claude-native side of this agent system. It is designed for automatic routing, specialist selection, and operational work without requiring users to manually call agents by name every time.

### What makes it different

- It is Claude-first, not OpenAI-first.
- It prefers auto-routing from task intent.
- It combines agents, context files, skills, hooks, plugins, and workflow logic in one place.

### What is inside

- `CLAUDE.md`: the root operating file for Anthropic workflows
- `agents/`: core and specialist agent definitions
- `context/`: routing rules, project context, and tooling notes
- `skills/`: reusable skills for documents, automation, design, testing, and more
- `hooks/` and `plugins/`: operational extensions and integrations

### Quick start

1. Read `CLAUDE.md`.
2. Check `context/project_context.md` and `context/routing_rules.md`.
3. Let Claude choose the narrowest useful agent.
4. For meaningful build or modify work, wait for approval before execution.

### Best for

- Claude-centric multi-agent workflows
- auto-routing with specialist bias
- skills-heavy operational setups
- automation, growth, monetization, and implementation work

---

## Francais

### A quoi sert ce dossier

`anthropic/` est la partie native Claude de ce systeme d'agents. Il est concu pour le routage automatique, le choix du bon specialiste et le travail operationnel sans devoir nommer chaque agent a la main.

### Ce qui le distingue

- Systeme pense d'abord pour Claude.
- Routage base sur l'intention de la tache.
- Agents, contexte, skills, hooks, plugins et logique operationnelle dans un seul ensemble.

### Ce que vous y trouvez

- `CLAUDE.md` : fichier racine de fonctionnement
- `agents/` : definitions des agents principaux et specialises
- `context/` : regles de routage, contexte projet, notes outils
- `skills/` : competences reutilisables pour documents, automatisation, design, tests, etc.
- `hooks/` et `plugins/` : extensions et integrations

### Demarrage rapide

1. Lire `CLAUDE.md`.
2. Consulter `context/project_context.md` et `context/routing_rules.md`.
3. Laisser Claude choisir l'agent le plus pertinent.
4. Pour un vrai build ou une modification, attendre l'approbation avant execution.

### Ideal pour

- workflows multi-agents centres sur Claude
- routage automatique avec specialistes
- environnements riches en skills
- automatisation, croissance, monetisation et implementation

---

## 한국어

### 이 폴더가 하는 일

`anthropic/`는 Claude 네이티브 운영 폴더다. 사용자가 매번 에이전트 이름을 직접 부르지 않아도, 작업 의도에 맞춰 자동 라우팅하고 적절한 전문 역할을 고르도록 설계돼 있다.

### 어떤 점이 다르나

- OpenAI용이 아니라 Claude 중심 구조다.
- 작업 의도 기반 auto-routing을 선호한다.
- agents, context, skills, hooks, plugins, 운영 로직이 한 폴더 체계 안에 모여 있다.

### 들어 있는 것

- `CLAUDE.md`: Anthropic 쪽 루트 운영 파일
- `agents/`: 코어 및 전문 에이전트 정의
- `context/`: 라우팅 규칙, 프로젝트 문맥, 툴링 메모
- `skills/`: 문서, 자동화, 디자인, 테스트 등에 쓰는 재사용 스킬
- `hooks/`, `plugins/`: 확장 기능과 통합 레이어

### 빠른 시작

1. `CLAUDE.md`를 읽는다.
2. `context/project_context.md`, `context/routing_rules.md`를 본다.
3. Claude가 가장 맞는 에이전트를 고르도록 둔다.
4. 중요한 생성/수정 작업은 승인 후 실행한다.

### 잘 맞는 용도

- Claude 중심 멀티에이전트 운영
- specialist 기반 auto-routing
- skill이 많은 실전형 환경
- 자동화, 성장, 수익화, 구현 작업

---

## 中文

### 这个文件夹是什么

`anthropic/` 是这套系统里偏 Claude 原生的一侧。它的目标是根据任务意图自动路由，并选择合适的专家角色，而不是要求用户每次都手动点名代理。

### 它的特点

- 以 Claude 为中心，而不是 OpenAI。
- 更强调按任务意图自动路由。
- 把 agents、context、skills、hooks、plugins 和运营逻辑放在同一套结构里。

### 里面有什么

- `CLAUDE.md`：Anthropic 侧根操作文件
- `agents/`：核心与专家代理定义
- `context/`：路由规则、项目背景、工具说明
- `skills/`：可复用技能，覆盖文档、自动化、设计、测试等
- `hooks/` 与 `plugins/`：扩展与集成层

### 快速开始

1. 先读 `CLAUDE.md`。
2. 再看 `context/project_context.md` 和 `context/routing_rules.md`。
3. 让 Claude 选择最合适的代理。
4. 重要创建或修改任务先批准，再执行。

### 适合什么

- Claude 导向的多代理工作流
- 带专家倾向的自动路由
- skill 很丰富的实战环境
- 自动化、增长、商业化和实现工作

---

## Espanol

### Que es esta carpeta

`anthropic/` es el lado nativo de Claude dentro de este sistema. Esta pensado para ruteo automatico, seleccion de especialistas y trabajo operativo sin obligar al usuario a invocar agentes manualmente cada vez.

### Que la hace diferente

- Esta centrada en Claude.
- Prefiere auto-routing basado en la intencion de la tarea.
- Une agents, context, skills, hooks, plugins y logica operativa en una sola estructura.

### Que contiene

- `CLAUDE.md`: archivo raiz de operacion para Anthropic
- `agents/`: definiciones de agentes base y especialistas
- `context/`: reglas de ruteo, contexto del proyecto y notas de herramientas
- `skills/`: skills reutilizables para documentos, automatizacion, diseno, testing y mas
- `hooks/` y `plugins/`: extensiones e integraciones

### Inicio rapido

1. Lee `CLAUDE.md`.
2. Revisa `context/project_context.md` y `context/routing_rules.md`.
3. Deja que Claude elija el agente mas adecuado.
4. Para trabajo importante de creacion o cambio, espera aprobacion antes de ejecutar.

### Ideal para

- workflows multiagente centrados en Claude
- auto-routing con sesgo a especialistas
- entornos ricos en skills
- automatizacion, crecimiento, monetizacion e implementacion
