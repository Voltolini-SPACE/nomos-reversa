# NOMOS Reversa

**Mapeie antes de adotar.** Mapeamento e engenharia reversa de ferramentas de
terceiros — **sem executá-las**.

Componente do ecossistema [NOMOS](https://github.com/Voltolini-SPACE/nomos).
Repositório próprio, licença MIT.

---

## O que faz

Dado um alvo (repositório git, pasta de skills, binário ou arquivo), o NOMOS
Reversa produz um **mapa** que responde às perguntas de uma validação de
verdade — e termina num **blueprint de reimplementação**, porque a preferência
do ecossistema é construir a nossa própria ferramenta em vez de adotar código de
terceiros.

O mapa cobre:

| Dimensão | O que entrega |
|---|---|
| **Origem** | remote, branch, HEAD, se é repositório git |
| **Inventário** | contagem de arquivos, bytes, distribuição por extensão |
| **Superfície** | pontos de entrada, dependências declaradas, saída de rede |
| **Autoria** | assinatura por skill (e registro explícito quando **não** existe) |
| **Licença** | classificação SPDX, copyleft e cláusulas restritivas |
| **Risco** | achados classificados e gravidade consolidada |
| **Blueprint** | passos para reimplementar dentro do NOMOS |

### Categorias de achado

`execucao` · `rede` · `credencial` · `injecao` · `empacotamento` · `git` ·
`skill` · `licenca`

Exemplos do que é detectado: `curl … | bash`, shell reverso, avaliação dinâmica,
ofuscação por base64, pedido de privilégio, URL externa, variável de segredo,
chave privada embutida, gancho de instalação, **hooks git ativos**,
`core.hooksPath` customizado, filtros `clean`/`smudge`, submódulos, skill sem
assinatura, injeção de prompt em arquivo de instrução, copyleft forte e cláusula
restritiva.

## Contrato de segurança

Verificado por testes, não por promessa:

- O alvo **nunca é executado, importado nem instalado** — só lido.
- **Nada é escrito dentro do alvo.** `--saida` é a única escrita, e vai para um
  diretório indicado explicitamente, fora do alvo.
- **Links simbólicos não são seguidos** na varredura; um alvo que é link é
  recusado explicitamente.
- **git é tratado como código, não configuração.** Só verbos de leitura
  (`rev-parse`, `remote`, `log`, `describe`, `symbolic-ref`), com
  `core.hooksPath` e `core.fsmonitor` neutralizados — repositório hostil não
  ganha execução só por ser mapeado.
- **Não existe flag de mutação ou publicação.** O agente é incapaz de alterar o
  alvo por construção.
- **Saída determinística**: mesma entrada, mesmo JSON (própria para gate de CI).
- **Fail-closed**: alvo inexistente, alvo que é link e manifesto ilegível viram
  risco alto, nunca silêncio.

## Instalação

```bash
pip install -e .
# ou, para desenvolver:
pip install -e ".[dev]"
```

## Uso

```bash
nomos-reversa --mapa ./ferramenta-de-terceiro            # relatório legível
nomos-reversa --mapa ./ferramenta-de-terceiro --json     # contrato estável
nomos-reversa --mapa ./ferramenta-de-terceiro --saida ./evidencias
nomos-reversa --version
```

Como biblioteca:

```python
from nomos_reversa import mapear, para_dict, relatorio, classificar_licenca

mapa = mapear("./alvo")
print(mapa.risco, len(mapa.achados))
print(relatorio(mapa))
```

## Integração com o NOMOS

O comando do ecossistema é:

```bash
nomos reversa <alvo>
```

O NOMOS consome este pacote como componente. A classificação de licença é
compartilhada — o gate de SBOM do NOMOS usa o **mesmo** `classificar_licenca`,
para não haver duas verdades.

## Desenvolvimento

```bash
python -m pytest -q
ruff check .
```

Ambos devem ficar 100% limpos.

## Origem

Extraído do monorepo NOMOS (missão MC65) para repositório próprio, conforme a
regra do ecossistema: toda ferramenta nossa carrega o nome NOMOS, tem
repositório git próprio e licença MIT.

## Licença

MIT — ver [LICENSE](LICENSE). Copyright (c) 2026 Se7enpay.
