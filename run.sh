#!/usr/bin/env bash
# Launch script for the Document Chatbot
# Sets required environment variables BEFORE Python/Streamlit starts
# to prevent segfaults from tokenizers/OpenMP/MPS threading conflicts.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Prevent segfaults from forked threads on macOS
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Activate virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

exec streamlit run app.py "$@"
