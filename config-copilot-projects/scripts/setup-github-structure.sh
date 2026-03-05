#!/usr/bin/env bash
# =============================================================================
# setup-github-structure.sh
#
# Genera la estructura profesional de .github/ para cualquier proyecto.
# Delega en gen_github.py para construir los archivos con logica compleja.
#
# Uso:
#   bash setup-github-structure.sh [--lang python|node|java] [--coverage 80]
#
# Ejemplos:
#   bash setup-github-structure.sh
#   bash setup-github-structure.sh --lang python --coverage 90
#   bash setup-github-structure.sh --lang node --coverage 75
#   bash setup-github-structure.sh --lang java
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="$SCRIPT_DIR/gen_github.py"

# Verificar que Python3 esta disponible
if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 no encontrado. Instala Python 3.8+ para continuar." >&2
  exit 1
fi

# Verificar que el generador existe
if [ ! -f "$GENERATOR" ]; then
  echo "ERROR: No se encuentra gen_github.py en $SCRIPT_DIR" >&2
  echo "Asegurate de que ambos archivos esten en el mismo directorio." >&2
  exit 1
fi

# Lanzar el generador Python pasando todos los argumentos
python3 "$GENERATOR" "$@"
