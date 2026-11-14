# Arquitetura inicial do RollOS

## Camadas implementadas no protótipo

- **Roll Core:** configuração local em `~/.rollos/config.json` e log de eventos em `events.jsonl`.
- **Roll Shell:** interface desktop PySide6, com cartões e reorganização de colunas.
- **Roll Display:** cálculo de dimensões virtuais e estados compacto/expandido, sem acionar hardware.
- **Roll AI:** cliente opcional NVIDIA NIM no protótipo desktop. A chave fica no arquivo `.env` local.
- **Roll Storage:** consulta informativa de capacidade e espaço livre, sem apagar ou modificar arquivos.
- **Roll Store:** catálogo estático de aplicativos planejados; instalação ainda não habilitada.
- **Roll Game:** camada futura para entrada, controles e perfis de desempenho.

## Estratégia técnica

O primeiro marco é um protótipo desktop em Python/PySide6. A etapa móvel deverá escolher uma base Linux móvel compatível com o dispositivo alvo. O kernel e os drivers só podem ser definidos com o SoC, painel, controlador, modem e documentação do fabricante.

## Segurança

Chaves de API ficam em `.env`, fora do controle de versão. Não incluir tokens, senhas ou chaves nos commits. O catálogo de aplicativos desta fase não executa downloads nem comandos de instalação.
