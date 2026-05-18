#!/bin/bash
# Tworzy nową paczkę na bazie _template
# Użycie: ./scripts/new-pack.sh <folder> "<Nazwa>" [mc-version] [loader]

FOLDER=$1
NAME=$2
MC_VER=${3:-"1.21.1"}
LOADER=${4:-"neoforge"}

if [ -z "$FOLDER" ] || [ -z "$NAME" ]; then
  echo "Użycie: $0 <folder> <nazwa> [mc-version] [loader]"
  echo "Przykład: $0 create-s2ep5 'FFTV Create S2 Ep5' 1.21.1 neoforge"
  exit 1
fi

if [ -d "$FOLDER" ]; then
  echo "Błąd: folder '$FOLDER' już istnieje!"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cp -r "$REPO_ROOT/_template" "$REPO_ROOT/$FOLDER"

sed -i "s/NAZWA_ODCINKA/$NAME/g" "$REPO_ROOT/$FOLDER/pack.toml"
sed -i "s/minecraft = \"1.21.1\"/minecraft = \"$MC_VER\"/g" "$REPO_ROOT/$FOLDER/pack.toml"

case "$LOADER" in
  neoforge) sed -i "s/# neoforge/neoforge/" "$REPO_ROOT/$FOLDER/pack.toml" ;;
  forge)    sed -i "s/# forge/forge/"       "$REPO_ROOT/$FOLDER/pack.toml" ;;
  fabric)   sed -i "s/# fabric/fabric/"     "$REPO_ROOT/$FOLDER/pack.toml" ;;
  quilt)    sed -i "s/# quilt/quilt/"       "$REPO_ROOT/$FOLDER/pack.toml" ;;
esac

echo "✓ Nowa paczka gotowa: $FOLDER"
echo ""
echo "Następne kroki:"
echo "  cd $FOLDER"
echo "  packwiz refresh"
echo "  packwiz modrinth add <mod>"
