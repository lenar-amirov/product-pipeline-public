#!/bin/bash
# Создаёт новую папку инициативы из шаблона
# Использование: ./new-initiative.sh "название-инициативы"

if [ -z "$1" ]; then
  echo "Использование: ./new-initiative.sh \"название-инициативы\""
  echo "Пример:        ./new-initiative.sh checkout-redesign"
  exit 1
fi

NAME="$1"
PM="$(whoami)"
BASE="$HOME/pipeline"
TEMPLATE="$BASE/template"
TARGET="$BASE/$NAME"

if [ -d "$TARGET" ]; then
  echo "Папка '$NAME' уже существует"
  exit 1
fi

cp -r "$TEMPLATE" "$TARGET"

# Создаём симлинк ~/.claude/skills → ~/pipeline/.claude/skills (один раз)
if [ ! -e ~/.claude/skills ]; then
  mkdir -p ~/.claude
  ln -sf ~/pipeline/.claude/skills ~/.claude/skills
  echo "✓ Skills linked: ~/.claude/skills → ~/pipeline/.claude/skills"
fi

# Подставляем название и продакта в CONTEXT.md
sed -i "s/\[НАЗВАНИЕ\]/$NAME/g" "$TARGET/CONTEXT.md"
sed -i "s/\[ИМЯ\]/$PM/g" "$TARGET/CONTEXT.md"

# Инициализируем трекер статуса (v2 — с полем steps)
python3 -c "
import json, sys
from datetime import date
d = {
  'pm': sys.argv[1],
  'initiative': sys.argv[2],
  'created': str(date.today()),
  'steps': {str(i): {'status': 'pending', 'date': None, 'summary': None} for i in range(1, 16)},
  'pending': {
    'analytics_brief': None, 'survey_brief': None, 'audience_brief': None,
    'analytics_results': None, 'survey_results': None,
    'design_brief': None, 'gate1_challenge': None, 'gate2_challenge': None
  }
}
print(json.dumps(d, indent=2, ensure_ascii=False))
" "$PM" "$NAME" > "$TARGET/output/status.json"

# Инициализируем decisions.md
echo "# Лог решений: $NAME" > "$TARGET/output/decisions.md"

# Создаём CJM папку
mkdir -p "$TARGET/CJM"

echo "✓ Инициатива создана: $TARGET"
echo ""
echo "Дальше:"
echo "  1. Заполни $TARGET/CONTEXT.md"
echo "  2. Положи скрины CJM в $TARGET/CJM/ (формат: 01_шаг.png, 02_шаг.png...)"
echo "  3. Открой Claude Code в папке $TARGET"
echo ""
echo "Пайплайн команд:"
echo ""
echo "  ── Phase 1: Исследование проблемы + Образ решения → Problem Research Report ──"
echo "  1.  /analyze-cjm             → гипотезы проблем из CJM"
echo "  2.  /synthetic-research      → синтетика или задача на реальное исследование"
echo "  3.  /competitor-research     → конкурентный анализ"
echo "  4.  /generate-research       → бриф аналитику + опрос"
echo "  5.  /create-survey-audience  → выборка для опроса"
echo "  6.  /validate-problems       → валидация гипотез по данным"
echo "  7.  /solution-hypotheses     → гипотезы решений"
echo "  8.  /sketch-solution         → образ решения + Figma"
echo "  9.  /review-design           → ревью дизайна"
echo "  10. /create-presentation     → Problem Research Report (.md + .pptx)"
echo ""
echo "  ── Phase 2: Проработка решения → Solution Research Report ──"
echo "  11. /create-design-brief     → задача дизайнеру + UX-исследование"
echo "  12. /estimate-with-dev       → оценка с разработкой"
echo "  13. /finalize-prd            → финализация PRD"
echo "  14. /design-ab-test          → дизайн AB-теста"
echo "  15. /create-gate2-presentation → Solution Research Report (.md + .pptx)"
echo ""
echo "      /create-jira             → Jira тикеты (после Solution Research Report)"
