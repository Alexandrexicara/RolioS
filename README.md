# RollOS — sistema experimental para tela enrolável

O RollOS é um projeto experimental de sistema operacional móvel com interface que se adapta à expansão física da tela e camada de IA híbrida.

## Estado desta versão
Esta branch contém o primeiro **protótipo desktop em Python/PySide6**. Ele oferece uma interface inicial, alternância simulada entre modo compacto e expandido, painel de informações do ambiente e integração opcional com NVIDIA NIM.

> **Importante:** isto ainda não é uma imagem instalável em celular nem um kernel móvel. Drivers do painel flexível, motores, modem, GPU, sensores e gerenciamento real de energia dependem do SoC e do hardware escolhidos.

## Requisitos
- Python 3.10 ou superior
- Windows, Linux ou macOS para executar o protótipo

## Instalação no Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

No Linux/macOS, crie e ative um ambiente virtual com `python3 -m venv .venv` e instale `requirements.txt`.

## NVIDIA NIM (opcional)
Edite `.env` e informe `NVIDIA_API_KEY`. O modelo e a URL base podem ser ajustados em `NVIDIA_MODEL` e `NVIDIA_BASE_URL`. Nunca envie o arquivo `.env` para o GitHub.

## Estrutura
- `main.py`: inicialização da interface.
- `rollos/shell.py`: shell gráfico e simulador de extensão da tela.
- `rollos/ai_client.py`: cliente opcional NVIDIA NIM.
- `rollos/system_info.py`: informações básicas do ambiente de prototipagem.
- `docs/ARCHITECTURE.md`: arquitetura planejada e limites técnicos.

## Próximos marcos
1. Executar e validar o protótipo desktop.
2. Desenvolver os serviços Roll Core, Roll Display e Roll Storage.
3. Implementar testes automatizados e integração contínua.
4. Selecionar a plataforma ARM e o dispositivo de referência.
5. Portar o shell para uma base Linux móvel compatível e iniciar o trabalho de kernel/drivers com documentação do fabricante.
