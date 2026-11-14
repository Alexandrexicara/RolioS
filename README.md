# RollOS — sistema experimental para tela enrolável

Sistema operacional experimental para dispositivos móveis com tela expansível, interface adaptável e arquitetura de IA híbrida.

## Prévia visual

A interface está publicada em https://rollios.netlify.app/. A área de IA foi atualizada para **Jarvis**, com chat conectado à função segura do Netlify, entrada por microfone e leitura das respostas em voz alta nos navegadores compatíveis.

## Estado atual

- A branch `main` contém a prévia web e o protótipo desktop em Python/PySide6.
- O protótipo inclui Roll Core, simulação de expansão, consulta local de armazenamento, catálogo conceitual e Roll Cloud experimental.
- O Jarvis usa por padrão o modelo `nvidia/nemotron-3.5-bolt-e4b` pela API NVIDIA NIM.
- A chave NVIDIA é lida somente no backend Netlify pela variável secreta `NVIDIA_API_KEY`; nunca deve ser colocada no navegador ou no Git.
- O microfone e a leitura de voz do site usam as APIs de fala do navegador. O suporte depende do navegador, das permissões e da disponibilidade de voz em português.
- A variável `NVIDIA_API_KEY` ainda precisa ser cadastrada no Netlify para ativar as respostas reais. Sem ela, a função retorna aviso de serviço não configurado.
- A interface de voz web não significa que o sistema operacional móvel ou o protótipo desktop já tenham integração de áudio nativa.

## Configuração NVIDIA no Netlify

No painel do site `rollios`, cadastre `NVIDIA_API_KEY` como variável **secreta**, com escopo para Functions e contexto Production. As variáveis `NVIDIA_MODEL` e `NVIDIA_BASE_URL` já estão configuradas:

- Modelo: `nvidia/nemotron-3.5-bolt-e4b`
- Base URL: `https://integrate.api.nvidia.com/v1`

Depois de cadastrar ou alterar a chave, publique um novo deploy. A função `/.netlify/functions/ai` chama a NVIDIA sem expor a chave ao navegador. O limite simples por IP incluído nesta prévia é uma proteção básica, não substitui autenticação, quotas persistentes e controle de abuso antes de abrir o serviço ao público.

## Roll Cloud — estágio experimental

O cartão Roll Cloud permite informar uma chave pessoal da Neon em tempo de execução, listar organizações autorizadas, criar um projeto PostgreSQL, preparar tabelas iniciais, criar um bucket privado e guardar a URI do banco no cofre de credenciais do sistema operacional. A chave da API não é gravada pelo RollOS. Este fluxo ainda não é OAuth integrado. Upload/download de vídeos e fotos, URLs assinadas, quotas e backend móvel de produção ainda não estão concluídos.

## O que ainda não funciona como sistema operacional

Esta versão não é instalável em celular. Ainda não possui imagem de instalação móvel, boot próprio, drivers, integração com painel flexível, modem, GPU, sensores ou motores. O catálogo não instala aplicativos. A prévia web e o protótipo desktop não equivalem a um sistema operacional móvel completo.

## Executar o protótipo desktop

No Windows, com Python 3.10 ou superior:

```powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

Para testar:

```powershell
python -m unittest discover -s tests -v
```

Para ativar a NVIDIA no desktop, preencha `NVIDIA_API_KEY` no arquivo local `.env`. Nunca envie esse arquivo ao GitHub.

## Links

- [Prévia web no Netlify](https://rollios.netlify.app/)
- [Painel Netlify](https://app.netlify.com/projects/rollios)
- [Repositório GitHub](https://github.com/Alexandrexicara/RolioS)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Roteiro](docs/ROADMAP.md)
