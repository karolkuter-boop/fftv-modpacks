# FFTV Modpacks

Repozytorium paczek modów Minecraft dla kanału Fabryka Filmów TV.

## Struktura

```
fftv-modpacks/
├── _template/              ← punkt startowy dla nowej paczki
├── scripts/
│   └── new-pack.sh        ← tworzenie nowej paczki jedną komendą
├── neofftv-cml-ep1/       ← CML NeoFFTV v1.6.28 (MC 1.21.1 + NeoForge)
└── ...kolejne paczki
```

## Nowa paczka

```bash
./scripts/new-pack.sh ep42-create "FFTV Create S2" 1.21.1 neoforge
cd ep42-create
packwiz refresh
```

## Zarządzanie modami

```bash
cd nazwa-paczki
packwiz modrinth add sodium        # Modrinth
packwiz curseforge add jei         # CurseForge
packwiz update --all               # aktualizuj wszystko
packwiz remove sodium              # usuń mod
```

## URL paczki (GitHub Pages)

```
https://karolkuter-boop.github.io/fftv-modpacks/NAZWA-PACZKI/pack.toml
```

## Konwencja nazewnictwa folderów

`TEMAT-ep##` lub `TEMAT-sezon`
Przykłady: `neofftv-cml-ep1`, `create-s2ep5`, `techno-ep12`
