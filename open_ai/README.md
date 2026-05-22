# OpenAI Agent HQ

This file supports 5 languages: English, Francais, Korean, Chinese, and Spanish.
Support de 5 langues: anglais, francais, coreen, chinois et espagnol.
5개 언어 지원: 영어, 프랑스어, 한국어, 중국어, 스페인어.
本文件支持 5 种语言：英语、法语、韩语、中文、西班牙语。
Este archivo admite 5 idiomas: ingles, frances, coreano, chino y espanol.

---

## English

### What this folder is

`open_ai/` is the OpenAI-side control center for agent work. It is built for people who want a clean flow:

`classify -> plan -> approval -> execute -> verify`

### What is inside

- `AGENTS.md`: the OpenAI root operating file
- `agents/`: specialist roles such as Strategist, Builder, Reviewer, and Automation Engineer
- `context/`: workflows, templates, routing notes, and prompt support files

### Why it is useful

- You get explicit routing instead of fuzzy assistant behavior.
- Meaningful build or modify work stops for approval before implementation.
- Handoffs between ChatGPT-style planning and Codex-style execution stay structured.

### Quick start

1. Read `AGENTS.md`.
2. Pick the right route with `context/agent_map.md` and `context/workflows.md`.
3. Use `context/templates.md` for clean handoffs.
4. Execute only after approval exists.

### Best for

- structured planning
- technical implementation handoff
- workflow and automation design
- review-first execution

---

## Francais

### A quoi sert ce dossier

`open_ai/` est le centre de pilotage cote OpenAI pour le travail avec agents. Il suit un flux simple:

`classifier -> planifier -> approuver -> executer -> verifier`

### Ce que vous y trouvez

- `AGENTS.md` : fichier principal de fonctionnement
- `agents/` : roles specialises comme Strategist, Builder, Reviewer et Automation Engineer
- `context/` : workflows, modeles, regles de routage et supports de prompt

### Pourquoi c'est utile

- Le routage est explicite, pas flou.
- Les vraies modifications attendent une approbation avant execution.
- Le passage entre planification et implementation reste propre.

### Demarrage rapide

1. Lire `AGENTS.md`.
2. Choisir la bonne route avec `context/agent_map.md` et `context/workflows.md`.
3. Utiliser `context/templates.md` pour les transferts.
4. N'executer qu'apres approbation.

### Ideal pour

- planification structuree
- passage vers l'implementation
- automatisation et workflows
- verification avant livraison

---

## 한국어

### 이 폴더가 하는 일

`open_ai/`는 OpenAI 계열 작업을 위한 에이전트 HQ 폴더다. 핵심 흐름은 아래처럼 명확하다.

`분류 -> 계획 -> 승인 -> 실행 -> 검증`

### 들어 있는 것

- `AGENTS.md`: OpenAI용 루트 운영 파일
- `agents/`: Strategist, Builder, Reviewer, Automation Engineer 같은 역할별 에이전트
- `context/`: 워크플로, 템플릿, 라우팅 기준, 프롬프트 보조 문서

### 왜 편한가

- 애매한 챗봇식 응답 대신 명시적 라우팅을 쓴다.
- 중요한 생성/수정 작업은 승인 전 실행하지 않는다.
- ChatGPT식 계획과 Codex식 실행 handoff가 깔끔하다.

### 빠른 시작

1. `AGENTS.md`부터 읽는다.
2. `context/agent_map.md`, `context/workflows.md`로 경로를 정한다.
3. `context/templates.md`로 handoff 블록을 재사용한다.
4. 승인 후에만 실행한다.

### 잘 맞는 용도

- 구조화된 기획
- 구현 handoff
- 자동화/워크플로 설계
- 검증 중심 실행

---

## 中文

### 这个文件夹是什么

`open_ai/` 是面向 OpenAI 工作流的代理 HQ。它强调一条清晰流程：

`分类 -> 计划 -> 批准 -> 执行 -> 验证`

### 里面有什么

- `AGENTS.md`：OpenAI 侧的根操作文件
- `agents/`：如 Strategist、Builder、Reviewer、Automation Engineer 等角色
- `context/`：工作流、模板、路由规则和提示支持文件

### 为什么好用

- 路由明确，不是模糊的助手模式。
- 重要修改必须先批准再执行。
- 从规划到实现的交接更稳定。

### 快速开始

1. 先读 `AGENTS.md`。
2. 用 `context/agent_map.md` 和 `context/workflows.md` 选择路径。
3. 用 `context/templates.md` 做干净的交接。
4. 只有在批准后再执行。

### 适合什么

- 结构化规划
- 技术实现交接
- 自动化与工作流设计
- 先验证再交付

---

## Espanol

### Que es esta carpeta

`open_ai/` es el centro de control para trabajo con agentes del lado OpenAI. Sigue un flujo claro:

`clasificar -> planear -> aprobar -> ejecutar -> verificar`

### Que contiene

- `AGENTS.md`: archivo raiz de operacion
- `agents/`: roles como Strategist, Builder, Reviewer y Automation Engineer
- `context/`: workflows, plantillas, reglas de ruteo y soporte de prompts

### Por que sirve

- El ruteo es explicito y facil de seguir.
- El trabajo importante espera aprobacion antes de ejecutarse.
- El paso entre planificacion e implementacion queda ordenado.

### Inicio rapido

1. Lee `AGENTS.md`.
2. Elige la ruta correcta con `context/agent_map.md` y `context/workflows.md`.
3. Usa `context/templates.md` para handoffs limpios.
4. Ejecuta solo despues de la aprobacion.

### Ideal para

- planificacion estructurada
- handoff tecnico
- automatizacion y workflows
- ejecucion con verificacion
