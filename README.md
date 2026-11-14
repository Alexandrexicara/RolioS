# RollOS — sistema experimental para tela enrolável

O RollOS é um projeto experimental de sistema operacional móvel com interface que se adapta à expansão física da tela e camada de IA híbrida.

## Estado desta versão

Esta branch contém o **protótipo desktop em Python/PySide6** e os serviços iniciais:
- Roll Core: configurações e registro local de eventos.
- Roll Display: simulação de tela compacta/expandida e reorganização da interface.
- Roll Storage: consulta informativa de espaço em disco, sem alterar arquivos.
- Roll AI: cliente opcional NVIDIA NIM no protótipo desktop.
- Roll Store: catálogo informativo de aplicativos planejados, ainda sem instalação.

A interface web de apresentação está na branch `main` e publicada em https://rollios.netlify.app/.

> **Importante:** isto ainda não é uma imagem instalável em celular nem um kernel móvel. Drivers do painel flexível, motores, modem, GPU, sensores e gerenciamento real de energia dependem do SoC e do hardware escolhidos.

## Requisitos

- Python 3.10 ou superior
- Windows, Linux ou macOS para executar o protótipo desktop

## Instalação no Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

No Linux/macOS, crie e ative um ambiente virtual com `python3 -m venv .venv` e instale `requirements.txt`.

## NVIDIA NIM (opcional)

Edite `.env` e informe `NVIDIA_API_KEY`. O modelo e a URL base podem ser ajustados em `NVIDIA_MODEL` e `NVIDIA_BASE_URL`. Nunca envie o arquivo `.env` para o GitHub.

## Testes

```powershell
python -m unittest discover -s tests -v
```

O workflow do GitHub Actions também executa os testes nas atualizações da branch.

## Estrutura principal

- `main.py`: inicialização da interface.
- `rollos/shell.py`: shell gráfico integrado aos serviços.
- `rollos/core.py`: configuração e eventos locais.
- `rollos/display.py`: modelo de tela adaptável simulado.
- `rollos/storage.py`: leitura informativa de armazenamento.
- `rollos/apps.py`: catálogo inicial de aplicativos.
- `rollos/ai_client.py`: cliente opcional NVIDIA NIM.
- `docs/ARCHITECTURE.md`: arquitetura e limites técnicos.
- `docs/ROADMAP.md`: etapas de desenvolvimento.

## Próximos marcos

1. Validar os testes e a interface em Windows e Linux.
2. Criar backend seguro para a IA da interface web.
3. Definir a plataforma ARM e o dispositivo de referência.
4. Selecionar a base Linux móvel compatível.
5. Iniciar integração de kernel, drivers, painel, sensores e gerenciamento de energia com documentação do fabricante.
