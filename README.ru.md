🌐 **Язык:** [English](README.md) | Русский

# Claude Code Project Framework

**От идеи до работающего кода за один разговор.**

```
Вы: /prd CLI-утилита для конвертации markdown в PDF
     ↓
Claude: Создаёт требования, техническую спецификацию, задачи
     ↓
Вы: /autonomous-development
     ↓
Claude: Пишет код, проверяет качество, коммитит каждый шаг
     ↓
Вы: Готовый код с тестами ✓
```

Больше никаких «Claude забыл, что мы обсуждали». Никаких сломанных коммитов. Не вы управляете ИИ — он управляет проектом.

[![Version](https://img.shields.io/badge/version-2.0.1-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)

---

## Быстрый старт

**Установка** (выберите один вариант):

```bash
# Новый проект
git clone https://github.com/1sergeykuzmin/claude-code-project-start-pack.git my-app
cd my-app && rm -rf .git && git init

# Существующий проект
curl -fsSL https://raw.githubusercontent.com/1sergeykuzmin/claude-code-project-start-pack/main/install.sh | bash
```

**Попробуйте:**

```bash
claude
```

```
Вы: /prd Трекер личных финансов

Claude: Создаю Product Requirements Document.
        Сначала несколько вопросов...
```

Готово. Вы уже используете фреймворк.

---

## 5 основных команд

Эти команды формируют основной рабочий процесс:

```
/prd → /trd → /to-do → /autonomous-development
                              ↓
                        /codex-review (автоматически)
```

---

### `/prd` — Опишите вашу идею

Превращает идею в структурированный Product Requirements Document.

```
Вы: /prd Мобильное приложение для отслеживания потребления воды

Claude: Помогу создать PRD. Сначала несколько вопросов:

        1. Целевые платформы? (iOS, Android, web?)
Вы: iOS и Android

Claude: 2. Ключевые функции помимо базового трекинга?
Вы: Напоминания, дневные цели, недельная статистика

Claude: 3. Нужны ли интеграции?
Вы: Apple Health и Google Fit

Claude: ✓ Создан dev-docs/prd.md

        Итого:
        - 8 функциональных требований
        - 4 нефункциональных требования
        - 3 user personas
        - Метрики успеха определены
```

**Что вы получаете:** `dev-docs/prd.md` — полная спецификация продукта, которую можно показать стейкхолдерам или использовать как источник истины.

---

### `/trd` — Спланируйте техническую реализацию

Превращает PRD в Technical Requirements Document.

```
Вы: /trd

Claude: Анализирую PRD...

        ✓ Создан dev-docs/trd.md

        Архитектурные решения:
        - Framework: React Native + Expo
        - Database: SQLite (локально) + опциональная cloud sync
        - APIs: HealthKit, Google Fit
        - Auth: Biometric + email fallback

        Security review:
        - Шифрование health data: Обязательно
        - Хранение API keys: Secure keychain
        - Data retention: Контролируется пользователем
```

**Что вы получаете:** `dev-docs/trd.md` — технический план с архитектурой, dependencies и анализом безопасности.

---

### `/to-do` — Разбейте на задачи

Превращает TRD в приоритизированный список задач.

```
Вы: /to-do

Claude: Разбиваю технические требования на задачи...

        ✓ Создан dev-docs/to-do.md

        Phase 1: Foundation (4 задачи)
        - [ ] Инициализировать React Native project (TRD 2.1)
        - [ ] Настроить SQLite schema (TRD 3.1)
        - [ ] Создать navigation structure (TRD 2.2)
        - [ ] Реализовать auth flow (TRD 4.1)

        Phase 2: Core Features (5 задач)
        - [ ] Экран логирования воды (PRD FR-001)
        - [ ] Система дневных целей (PRD FR-002)
        - [ ] Notifications (PRD FR-003)
        ...

        Всего 12 задач в 3 фазах
```

**Что вы получаете:** `dev-docs/to-do.md` — каждая задача связана с разделами PRD/TRD, так что всегда понятно *почему* что-то делается.

---

### `/autonomous-development` — Постройте всё

Выполняет ВСЕ задачи автоматически в непрерывном цикле.

```
Вы: /autonomous-development

Claude: Запускаю continuous execution...

        ┌──────────────────────────────────────────────────┐
        │ LOOP: Найти задачу → Сделать → Review → Commit  │
        │       ↑________________________________________↓  │
        └──────────────────────────────────────────────────┘

        → Task 1/12: Инициализировать React Native project
          Создаю структуру проекта...
          Добавляю dependencies...
          Запускаю /codex-review... ✓ Passed
          Committed: "feat: Initialize React Native with Expo"

        → Task 2/12: Настроить SQLite schema
          Пишу database models...
          Запускаю /codex-review... ⚠ Issue found
          Auto-fixing: Добавлен недостающий index
          Запускаю /codex-review... ✓ Passed
          Committed: "feat: Add SQLite database schema"

        → Task 3/12: Создать navigation structure
          ...

        [Продолжает пока ВСЕ задачи не выполнены]

        ✓ Все 12 задач выполнены
        ✓ Создано 12 commits
        ✓ Готово к release
```

**Ключевое поведение:**
- Работает пока ВСЕ задачи не выполнены (не только одна)
- Автоматически запускает code review после каждой задачи
- Автоматически исправляет проблемы (до 3 попыток)
- Останавливается только когда: всё готово, unfixable error, или вы прервали

---

### `/codex-review` — Quality Gate

Проверяет код перед каждым commit. Запускается автоматически в `/autonomous-development`, но можно запустить и вручную.

```
Вы: /codex-review

Claude: Запускаю code review...

        Checking:
        ✓ Syntax valid
        ✓ Security vulnerabilities не найдены
        ✓ Hardcoded secrets нет
        ✓ Tests pass (14/14)
        ⚠ Warning: Function 'processData' — 67 строк

        Recommendation: Рассмотрите разбиение на меньшие функции.

        Result: PASS (1 warning)
```

**Это обязательно.** Каждая задача должна пройти review перед commit — без исключений, независимо от настроек.

---

## Session Management

Framework помнит, где вы остановились.

### Начало сессии

```
Вы: start

Claude: Загружаю ваш проект...

        ✓ Context загружен (3,241 tokens)
        ✓ Git status: clean
        ✓ Осталось 4 задачи в Phase 2

        Готов продолжить. Запустите /autonomous-development
        или спросите что угодно о проекте.
```

Другие triggers: `resume`, `continue`, `begin`

### Завершение сессии

```
Вы: done

Claude: Завершаю...

        ✓ Все changes committed
        ✓ Snapshot обновлён
        ✓ Session сохранена

        Progress: 8/12 задач выполнено
        Next time: Phase 2, Task 5 (Notifications)
```

Другие triggers: `finish`, `/fi`, `end session`

### Почему это важно

| Без Session Management | С Session Management |
|------------------------|----------------------|
| Claude загружает весь codebase (~15k tokens) | Загружает smart summary (~3k tokens) |
| Не помнит предыдущую работу | Точно знает, где вы остановились |
| Потеря работы при забытом commit | Автоматическое crash recovery |

### Crash Recovery

Забыли сказать `done`? Не проблема.

```
Вы: start

Claude: ⚠ Найдена incomplete session со вчера

        Uncommitted changes:
        - src/notifications.ts (new)
        - src/api/health.ts (modified)

        Что хотите сделать?
        1. Commit и продолжить
        2. Stash и начать заново
        3. Сначала посмотреть changes

Вы: 1

Claude: ✓ Committed: "feat: Add notification system"
        Продолжаю с места остановки...
```

---

## Другие полезные команды

### Добавление features в существующий код

```
Вы: /feature Добавить dark mode

Claude: Спланирую эту feature. Несколько вопросов...
        [Задаёт 2-3 уточняющих вопроса]

        ✓ Обновлён PRD с новыми requirements
        ✓ Обновлён TRD с implementation approach
        ✓ Добавлено 4 задачи в to-do.md

        Запускаю /autonomous-development...
```

### Quick Fixes

| Command | Что делает |
|---------|------------|
| `/fix "не работает login"` | Debug и исправление проблем |
| `/refactor auth.ts` | Улучшение структуры кода |
| `/explain api/` | Объяснение как работает код |
| `/optimize utils.ts` | Performance optimization |
| `/test users` | Написание tests для module |

### Git Commands

| Command | Что делает |
|---------|------------|
| `/commit` | Structured commit с правильным message |
| `/pr` | Создание pull request |
| `/release` | Version management |

### Security

| Command | Что делает |
|---------|------------|
| `/security` | OWASP security audit |
| `/security-dialogs` | Проверка на leaked credentials в диалогах |

### Для существующих проектов

```
Вы: /migrate-legacy

Claude: Анализирую ваш codebase...

        ✓ Найдено: Next.js 14, 47 components, PostgreSQL
        ✓ Generated dev-docs/prd.md (reverse-engineered)
        ✓ Generated dev-docs/trd.md (architecture analysis)

        Готов к /feature или /autonomous-development
```

---

## Configuration

### Presets

Выберите, сколько Claude будет подтверждать с вами:

| Preset | Поведение | Для чего |
|--------|-----------|----------|
| `balanced` | Подтверждает важные actions | Ежедневная работа (default) |
| `autopilot` | Минимум confirmations | Быстрое prototyping |
| `paranoid` | Подтверждает всё | Production code |
| `verbose` | Полный output, все confirmations | Debugging |
| `silent` | Минимальный output | CI/CD pipelines |

Установите в `.claude/settings.json`:

```json
{
  "preset": "balanced"
}
```

**Важно:** Code review **всегда обязателен** независимо от preset.

### Ключевые файлы

| File | Назначение |
|------|------------|
| `dev-docs/prd.md` | Product requirements |
| `dev-docs/trd.md` | Technical specification |
| `dev-docs/to-do.md` | Task breakdown |
| `dev-docs/snapshot.md` | Текущее состояние проекта |
| `.claude/settings.json` | Framework configuration |

---

## Installation

### Новый проект

```bash
git clone https://github.com/1sergeykuzmin/claude-code-project-start-pack.git my-project
cd my-project && rm -rf .git && git init
```

### Существующий проект

```bash
curl -fsSL https://raw.githubusercontent.com/1sergeykuzmin/claude-code-project-start-pack/main/install.sh | bash
```

### Installer Options

| Flag | Effect |
|------|--------|
| `--dry-run` | Preview без изменений |
| `--minimal` | Установить только `.claude/` folder |
| `--update` | Обновить существующую installation |
| `--force` | Overwrite без вопросов |
| `--no-hooks` | Skip git hooks |

### Requirements

**Обязательно:**
- Claude Code CLI
- Python 3.8+
- Git

**Опционально:**
- Node.js 18+ (для dialog web UI)

---

## Origins & Credits

Этот framework объединяет два подхода к AI-assisted development:

### Planning Skills

Pipeline от идеи до execution:

| Skill | Назначение |
|-------|------------|
| `/prd` | Generate Product Requirements из идеи |
| `/trd` | Generate Technical Specification из PRD |
| `/to-do` | Разбиение на actionable tasks |
| `/autonomous-development` | Execute все tasks в continuous loop |
| `/codex-review` | Mandatory code review gate |

### Starter Architecture

Session management и operational commands основаны на [claude-code-starter](https://github.com/alexeykrol/claude-code-starter) от [Alexey Krol](https://github.com/alexeykrol):

- Session protocols (Cold Start, Completion, crash recovery)
- Operational commands (`/commit`, `/pr`, `/fix`, `/refactor`)
- Document conventions (`snapshot.md`, `architecture.md`)
- Security layers (pre-commit hooks, commit policies)

### The Combination

```
┌─────────────────────────────────────────────────────┐
│         Claude Code Project Framework               │
├─────────────────────────────────────────────────────┤
│  PLANNING                                           │
│  /prd → /trd → /to-do → /autonomous-development    │
├─────────────────────────────────────────────────────┤
│  SESSIONS (based on claude-code-starter)            │
│  start → work → done (with crash recovery)          │
├─────────────────────────────────────────────────────┤
│  COMMANDS                                           │
│  /commit, /pr, /fix, /refactor, /security           │
└─────────────────────────────────────────────────────┘
```

---

## License

MIT

---

*Built for AI-assisted development with Claude Code*
