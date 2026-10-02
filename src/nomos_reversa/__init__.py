"""NOMOS Reversa — mapeamento e engenharia reversa de ferramentas de terceiros.

Componente do ecossistema NOMOS. Mapeia uma ferramenta de terceiros sem
executá-la: origem, integridade, autoria, superfície, permissões, licença — e
um blueprint de reimplementação, porque a preferência é construir o nosso.

Repositório próprio, licença MIT.
"""

from nomos_reversa.mapa import (
    VERSAO,
    Achado,
    Mapa,
    classificar_licenca,
    mapear,
    para_dict,
    relatorio,
)

__all__ = ["VERSAO", "Achado", "Mapa", "classificar_licenca", "mapear",
           "para_dict", "relatorio"]

__version__ = "1.0.0"
