# Arquitetura inicial do RollOS

## Implementado no protótipo

- **Roll Core:** configuração local em `~/.rollos/config.json` e log de eventos em `events.jsonl`.
- **Roll Shell:** interface desktop PySide6, com cartões e reorganização de colunas.
- **Roll Display:** cálculo de dimensões virtuais e estados compacto/expandido; não aciona hardware.
- **Roll AI:** cliente opcional NVIDIA NIM no protótipo desktop. A chave fica em `.env` local.
- **Roll Storage:** consulta informativa de capacidade e espaço livre, sem apagar ou modificar arquivos.\n- **Roll Cloud (experimental):** cliente da Neon Management API que lista organizações e cria um projeto PostgreSQL na conta Neon autorizada pelo usuário. A chave pessoal é transitória e não é salva.
- **Roll Store:** catálogo estático de aplicativos planejados; instalação ainda não habilitada.
- **Roll Game:** camada futura para entrada, controles e perfis de desempenho.

## Roll Cloud: fluxo e limites atuais\n\n1. O usuário cria uma chave pessoal no Console Neon e a informa no fluxo experimental do Roll Cloud.\n2. O RollOS usa a chave apenas em memória para consultar as organizações e criar um projeto na organização escolhida.\n3. O projeto nasce com branch `production` e banco `rollos`.\n4. O RollOS registra localmente apenas o evento e o ID do projeto, nunca a chave.\n5. A URI de conexão não é persistida nem distribuída nesta etapa; a conexão do app deve passar por backend protegido.\n6. Vídeos e fotos ainda não são enviados: o bucket de Object Storage e os uploads com URLs assinadas serão uma etapa separada.\n\n**OAuth:** a integração oficial OAuth da Neon para aplicativos de terceiros exige parceria comercial ativa. Até haver aprovação e credenciais OAuth próprias do RollOS, não apresentar o fluxo de chave pessoal como login OAuth nem como experiência final de produção.\n\n## Arquitetura móvel pretendida

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
