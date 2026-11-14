# Arquitetura inicial do RollOS

## Camadas planejadas

- **Roll Core:** serviços de sessão, configuração, logs e ciclo de vida.
- **Roll Shell:** interface adaptável ao espaço disponível da tela.
- **Roll Display:** abstração para dimensões, orientação e estados do painel.
- **Roll AI:** roteador híbrido entre inferência local e NVIDIA NIM.
- **Roll Storage:** políticas de dados, cache e armazenamento persistente.
- **Roll Store:** catálogo, instalação e atualização de aplicativos.
- **Roll Game:** serviços de entrada, controles e perfil de desempenho.

## Estratégia técnica

O primeiro marco é um protótipo desktop em Python/PySide6. A etapa móvel deverá escolher uma base Linux móvel compatível com o dispositivo alvo. O kernel e os drivers só podem ser definidos com o SoC, painel, controlador, modem e documentação do fabricante.

## Segurança

Chaves de API ficam em `.env`, fora do controle de versão. Não incluir tokens, senhas ou chaves nos commits.
