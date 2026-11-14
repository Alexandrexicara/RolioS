# RollOS — sistema experimental para tela enrolável

Sistema operacional experimental para dispositivos móveis com tela expansível, interface adaptável e arquitetura de IA híbrida.

## Prévia visual

A interface web de demonstração está publicada em **https://rollios.netlify.app/**. Ela permite navegar pelos módulos, testar a expansão simulada da tela e visualizar os conceitos do Roll AI e do armazenamento.

## Estado atual

- A branch `main` contém a prévia web estática publicada na Netlify.
- A branch `feature/rollos-integrated-preview` reúne a prévia web e o protótipo desktop em Python/PySide6.
- O PR [#2 — integração do protótipo desktop](https://github.com/Alexandrexicara/RolioS/pull/2) está em validação.
- O protótipo inclui Roll Core, Roll Display simulado, Roll Storage somente leitura, cliente NVIDIA NIM opcional, catálogo conceitual e um primeiro fluxo Roll Cloud para criar um projeto na conta Neon do próprio usuário.
- Os testes automatizados ainda precisam passar em Windows e Linux.

## Roll Cloud — estágio experimental\n\nO cartão Roll Cloud permite informar uma chave pessoal da Neon em tempo de execução, listar as organizações autorizadas, criar um projeto PostgreSQL, preparar as tabelas iniciais e guardar a URI do banco no cofre de credenciais do sistema operacional. A chave da API não é gravada pelo RollOS. A criação consome os limites/plano da conta Neon do usuário. Este fluxo ainda não é OAuth integrado: o OAuth oficial da Neon é restrito a parceiros comerciais ativos. Upload de vídeos/fotos em bucket e backend de produção ainda não estão concluídos. Não use uma chave administrativa em dispositivo compartilhado.\n\n## O que ainda não funciona como sistema operacional

Esta versão não é instalável em celular. Ainda não possui kernel próprio, imagem de instalação, boot móvel, drivers, integração com painel flexível, modem, GPU, sensores ou motores. O catálogo não instala aplicativos. A prévia web do Roll AI é demonstrativa; a chave NVIDIA não deve ser publicada no navegador.

## Próximas etapas

1. Corrigir e aprovar os testes em Windows e Linux.
2. Validar a interface desktop em resoluções e escalas diferentes.
3. Proteger a integração NVIDIA e criar um backend autenticado para a interface web.
4. Definir um aparelho ARM de referência e obter documentação do SoC, painel, controlador, modem e sensores.
5. Escolher a base Linux móvel, estratégia de boot, partições, atualização e recuperação.
6. Desenvolver e testar drivers e integração do painel expansível no aparelho escolhido.
7. Implementar loja segura, permissões, instalação/atualização de aplicativos e serviços móveis.

## Executar o protótipo desktop

No Windows, com Python 3.10 ou superior:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

Para executar os testes:

```powershell
python -m unittest discover -s tests -v
```

Para testar a IA no desktop, preencha `NVIDIA_API_KEY` no arquivo local `.env`. Nunca envie esse arquivo ao GitHub.

## Links

- [Prévia web no Netlify](https://rollios.netlify.app/)
- [Painel Netlify](https://app.netlify.com/projects/rollios)
- [Pull request de integração](https://github.com/Alexandrexicara/RolioS/pull/2)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Roteiro de desenvolvimento](docs/ROADMAP.md)
