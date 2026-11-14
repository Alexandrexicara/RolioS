"""Catálogo informativo de aplicativos planejados para o RollOS."""
from dataclasses import dataclass


@dataclass(frozen=True)
class AppEntry:
    app_id: str
    name: str
    category: str
    description: str
    status: str = "planejado"


class AppCatalog:
    """Lista estática e segura; instalação/atualização ainda não habilitadas."""

    def __init__(self) -> None:
        self._apps = (
            AppEntry("browser", "Navegador", "Internet", "Navegação web com layout adaptável."),
            AppEntry("files", "Arquivos", "Sistema", "Gerenciador de arquivos e pastas do usuário."),
            AppEntry("media", "Mídia", "Entretenimento", "Reprodução de áudio e vídeo."),
            AppEntry("camera", "Câmera", "Multimídia", "Captura de fotos e vídeos quando houver hardware compatível."),
            AppEntry("roll-ai", "Roll AI", "Inteligência artificial", "Assistente híbrido com provedor local ou serviço em nuvem.", "protótipo"),
            AppEntry("games", "Jogos", "Entretenimento", "Área para jogos e perfis de desempenho."),
        )

    def list_apps(self) -> tuple[AppEntry, ...]:
        return self._apps

    def get(self, app_id: str) -> AppEntry | None:
        return next((app for app in self._apps if app.app_id == app_id), None)
