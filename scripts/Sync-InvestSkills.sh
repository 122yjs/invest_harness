#!/usr/bin/env bash
set -e

# Repository Root 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Python 3 실행 환경 탐색
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "Error: Python 3가 필요하지만 설치되어 있지 않습니다." >&2
        exit 1
    fi
fi

echo "==> Cross-platform sync using Python..."
"$PYTHON_CMD" "$SCRIPT_DIR/sync_invest_skills.py"
