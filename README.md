# RollOS — sistema experimental para tela enrolável

Sistema operacional experimental para dispositivos móveis com tela expansível, interface adaptável e arquitetura de IA híbrida.

## Prévia visual
A interface web de demonstração está publicada em **https://rollios.netlify.app/**. Ela permite navegar pelos módulos, testar a expansão simulada da tela, visualizar o conceito do Roll AI e consultar um painel ilustrativo de armazenamento.

## Estado atual
O repositório contém o preview web estático para Netlify. A implementação desktop em Python/PySide6 e os primeiros serviços Roll Core, Roll Display e Roll Storage estão sendo desenvolvidos na branch `feature/rollos-desktop-prototype`.

## Limites técnicos
O preview web é uma demonstração visual, não o sistema operacional móvel. Não controla painel flexível, motores, modem, GPU ou sensores. O protótipo desktop também roda em espaço de usuário. Kernel, drivers e integração de hardware exigem a escolha do dispositivo ARM e documentação do fabricante.

## Segurança
Chaves de API devem ficar em variáveis locais/servidor e nunca em JavaScript publicado. O arquivo `.env` não deve ser enviado ao GitHub.

## Links
- [Preview no Netlify](https://rollios.netlify.app/)
- [Painel Netlify](https://app.netlify.com/projects/rollios)
- [Arquitetura](docs/ARCHITECTURE.md)


## Protótipo desktop (em desenvolvimento)

A branch `feature/rollos-integrated-preview` também inclui uma versão desktop em Python/PySide6:
- Roll Core: configurações e log local de eventos.
- Roll Display: simulação da expansão e reorganização do layout.
- Roll Storage: leitura informativa do armazenamento, sem apagar arquivos.
- Roll AI: cliente opcional NVIDIA NIM para o protótipo desktop.
- Roll Store: catálogo conceitual, sem instalação de aplicativos nesta fase.

Para executar no Windows, consulte as instruções de instalação abaixo:

```powershell
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

Para executar os testes:

```powershell
python -m unittest discover -s tests -v
```

O protótipo desktop ainda não é um sistema operacional móvel instalável. O kernel, drivers e controle físico da tela dependem da escolha e documentação do hardware.
