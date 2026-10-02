#!/usr/bin/env python3
"""NOMOS Reversa — linha de comando.

Mapeia uma ferramenta de terceiros **sem executá-la**.

Modos:
- `--mapa ALVO`          mapeia diretório, repositório git, skill ou arquivo.
                         Padrão: diretório atual.
- `--mapa ALVO --json`   mapa em JSON determinístico (gate de CI, contrato estável).
- `--saida DIR`          única escrita: grava `mapa.md` + `mapa.json` em DIR,
                         indicado explicitamente pelo humano.
- `--version`            imprime a versão.

Contrato de segurança (verificado por testes):
- o alvo NUNCA é executado, importado nem instalado — só lido;
- `--saida` é a única escrita, e acontece fora do alvo;
- links simbólicos não são seguidos na varredura;
- git só é consultado por verbos de LEITURA, com `core.hooksPath` e
  `core.fsmonitor` neutralizados: repositório hostil não ganha execução;
- não existe flag que mute o alvo, instale algo ou publique nada.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from nomos_reversa import VERSAO, mapear, para_dict, relatorio

AGENT_VERSION = VERSAO


def _cmd_mapa(args) -> int:
    mapa = mapear(args.mapa)

    if args.saida:
        destino = Path(args.saida).expanduser()
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "mapa.md").write_text(relatorio(mapa) + "\n", encoding="utf-8")
        (destino / "mapa.json").write_text(
            json.dumps(para_dict(mapa), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"mapa gravado em {destino}", file=sys.stderr)

    if args.json:
        print(json.dumps(para_dict(mapa), ensure_ascii=False, indent=2))
    elif not args.saida:
        print(relatorio(mapa))

    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="nomos-reversa",
        description="NOMOS Reversa — mapeia uma ferramenta de terceiros sem executá-la.",
    )
    parser.add_argument("--mapa", metavar="ALVO", default=".",
                        help="diretório, repositório, skill ou arquivo a mapear")
    parser.add_argument("--json", action="store_true",
                        help="saída JSON determinística")
    parser.add_argument("--saida", metavar="DIR",
                        help="grava mapa.md e mapa.json em DIR (única escrita)")
    parser.add_argument("--version", action="version", version=AGENT_VERSION)
    args = parser.parse_args(argv)
    return _cmd_mapa(args)


if __name__ == "__main__":
    sys.exit(main())
