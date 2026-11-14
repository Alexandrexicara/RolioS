# Arquitetura inicial do RollOS

## Implementado no protótipo

- **Roll Core:** configuração local em `~/.rollos/config.json` e log de eventos em `events.jsonl`.
- **Roll Shell:** interface desktop PySide6, com cartões e reorganização de colunas.
- **Roll Display:** cálculo de dimensões virtuais e estados compacto/expandido; não aciona hardware.
- **Roll AI:** cliente opcional NVIDIA NIM no protótipo desktop. A chave fica em `.env` local.
- **Roll Storage:** consulta informativa de capacidade e espaço livre, sem apagar ou modificar arquivos.
- **Roll Store:** catálogo estático de aplicativos planejados; instalação ainda não habilitada.
- **Roll Game:** camada futura para entrada, controles e perfis de desempenho.

## Arquitetura móvel pretendida

1. **Boot e recuperação:** bootloader suportado pelo aparelho, imagem assinada, partições de sistema e recuperação/rollback.
2. **Kernel e drivers:** kernel Linux compatível com o SoC e drivers para GPU, painel, toque, áudio, modem, sensores e energia.
3. **Roll Core:** serviços de sistema, configurações, eventos, permissões e atualização.
4. **Roll Display:** recebe dimensões reais e eventos do controlador do painel; calcula layout adaptativo.
5. **Roll Shell:** interface móvel com estados compacto, intermediário e expandido, acessibilidade e rotação.
6. **Roll AI:** roteador híbrido entre serviço em nuvem e modelos locais, com política de privacidade e limites de consumo.
7. **Roll Store:** catálogo assinado, verificação de origem, permissões e atualizações.
8. **Roll Game:** integração com GPU, controles e perfis térmicos/energéticos.

## Estratégia de desenvolvimento

A primeira entrega é um protótipo desktop e web, não um firmware. A etapa móvel deve selecionar primeiro um aparelho ARM de referência. A compatibilidade de kernel e drivers varia por fabricante e modelo; não se deve prometer suporte genérico a qualquer celular.

O mecanismo de expansão exige documentação do painel/controlador, sensores e limites físicos. O software deve reagir ao estado informado pelo hardware e nunca comandar motores sem camada de segurança e testes específicos.

## Segurança

- Chaves de API ficam em variáveis locais ou em backend protegido, nunca em JavaScript publicado.
- Não incluir tokens, senhas ou chaves nos commits.
- Atualizações do sistema e aplicativos devem ter origem verificável e integridade criptográfica.
- O catálogo desta fase não executa downloads nem comandos de instalação.
- Serviços com privilégios devem ser separados da interface e validar cada solicitação.
