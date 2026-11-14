# Arquitetura RollOS

## Protótipo atual

- **Roll Core:** configuração e registro de eventos locais.
- **Roll Display:** simulação da expansão e adaptação do layout.
- **Roll Storage:** consulta somente leitura do armazenamento local.
- **Roll AI / Jarvis:** cliente NVIDIA NIM compatível com Chat Completions.
- **Jarvis Web Voice:** captura de fala e síntese de voz pelas APIs nativas do navegador; reconhecimento em português depende do suporte do navegador.
- **Netlify Function `/.netlify/functions/ai`:** recebe texto do navegador, chama NVIDIA NIM e mantém `NVIDIA_API_KEY` no servidor.
- **Roll Cloud:** provisionamento experimental de projeto e metadados Neon na conta autorizada do usuário.

## Modelo NVIDIA

O modelo padrão atual é `nvidia/nemotron-3.5-bolt-e4b`, escolhido para tarefas de assistente com baixa latência e uso cotidiano. A integração usa `POST /v1/chat/completions` em `https://integrate.api.nvidia.com/v1`.

A chave deve existir apenas em variável secreta de backend ou no arquivo local `.env` do protótipo desktop. Nunca incluir a chave em JavaScript, HTML, logs, repositório ou armazenamento do navegador.

## Voz Jarvis

No site, `SpeechRecognition` / `webkitSpeechRecognition` recebe fala e converte para texto; `SpeechSynthesis` lê a resposta em voz alta. O idioma solicitado é pt-BR. Essas APIs são fornecidas pelo navegador e podem variar por dispositivo, navegador, permissões e vozes instaladas. A voz web atual não é um canal de áudio full-duplex NVIDIA nem uma integração de voz nativa do futuro sistema móvel.

## Segurança e limitações do preview

A função Netlify limita tamanho de mensagem e aplica limitação simples em memória por IP. Como funções serverless podem reiniciar e não compartilham estado entre instâncias, isso não é uma quota confiável para produção. Antes de acesso público, implementar autenticação por usuário, limites persistentes, quotas, monitoramento, proteção contra abuso e política de privacidade.

A variável secreta `NVIDIA_API_KEY` ainda precisa ser cadastrada no Netlify para a IA responder de verdade. Sem ela, a função informa que o serviço não foi configurado.

## Arquitetura móvel pretendida

O sistema móvel futuro precisará de kernel e boot compatíveis com um aparelho ARM específico, drivers de tela/toque, modem, áudio, câmera, sensores e mecanismo físico de expansão. Nada disso é fornecido pelo protótipo web atual.
