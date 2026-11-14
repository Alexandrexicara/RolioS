"""Interface desktop do RollOS, integrada aos serviços locais do protótipo."""
from __future__ import annotations

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QPushButton, QSlider, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget, QInputDialog,
)

from .ai_client import NvidiaAssistant
from .apps import AppCatalog
from .core import RollCore
from .display import RollDisplay
from .storage import RollStorage
from .system_info import collect_system_info
from .neon_cloud import (
    NeonProvisioner, NeonProvisioningError,
    initialize_rollos_schema, save_database_credential,
)


class AiWorker(QThread):
    finished_text = Signal(str)

    def __init__(self, assistant: NvidiaAssistant, prompt: str) -> None:
        super().__init__()
        self.assistant = assistant
        self.prompt = prompt

    def run(self) -> None:
        self.finished_text.emit(self.assistant.ask(self.prompt))


class RollShell(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RollOS — protótipo de sistema")
        self.resize(1120, 760)
        self.setMinimumSize(760, 560)
        self.core = RollCore()
        self.display = RollDisplay()
        self.storage = RollStorage()
        self.apps = AppCatalog()
        self.ai = NvidiaAssistant()
        self._workers: list[AiWorker] = []
        self._last_mode = ""
        self.core.log_event("shell_started", {"build": self.core.config.build})
        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet("""
            QMainWindow, QWidget#root { background: #0b1020; color: #edf2ff; }
            QLabel { color: #edf2ff; }
            QLabel#muted { color: #9ba8c7; }
            QLabel#brand { color: #7ce7d5; font-size: 25px; font-weight: 800; }
            QFrame#panel { background: #151e35; border: 1px solid #293653; border-radius: 16px; }
            QPushButton { background: #243451; color: #f4f7ff; border: 1px solid #3b5075;
                          border-radius: 10px; padding: 10px 14px; }
            QPushButton:hover { background: #30466b; }
            QPushButton#primary { background: #087f78; border-color: #16a99d; font-weight: 700; }
            QLineEdit, QTextEdit { background: #0d1528; color: #f4f7ff; border: 1px solid #354565;
                                   border-radius: 9px; padding: 9px; }
            QSlider::groove:horizontal { height: 7px; background: #34425f; border-radius: 3px; }
            QSlider::handle:horizontal { background: #7ce7d5; width: 18px; margin: -6px 0; border-radius: 9px; }
        """)
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(24, 20, 24, 20)
        outer.setSpacing(16)

        header = QHBoxLayout()
        brand = QLabel("RollOS")
        brand.setObjectName("brand")
        tagline = QLabel("UM SISTEMA QUE SE EXPANDE COM A TELA")
        tagline.setObjectName("muted")
        header.addWidget(brand)
        header.addSpacing(14)
        header.addWidget(tagline)
        header.addStretch()
        self.mode_label = QLabel("MODO COMPACTO")
        self.mode_label.setStyleSheet("color: #7ce7d5; font-weight: 700;")
        header.addWidget(self.mode_label)
        outer.addLayout(header)

        panel = QFrame()
        panel.setObjectName("panel")
        controls = QVBoxLayout(panel)
        slider_row = QHBoxLayout()
        slider_row.addWidget(QLabel("Extensão simulada da tela"))
        self.extent = QSlider(Qt.Orientation.Horizontal)
        self.extent.setRange(0, 100)
        self.extent.setValue(35)
        self.extent.valueChanged.connect(self._apply_screen_mode)
        slider_row.addWidget(self.extent, 1)
        self.extent_value = QLabel("35%")
        slider_row.addWidget(self.extent_value)
        controls.addLayout(slider_row)
        self.display_details = QLabel("Resolução virtual: —")
        self.display_details.setObjectName("muted")
        controls.addWidget(self.display_details)
        outer.addWidget(panel)

        self.cards_host = QWidget()
        self.cards = QGridLayout(self.cards_host)
        self.cards.setSpacing(14)
        self.card_widgets: list[QFrame] = []
        outer.addWidget(self.cards_host, 1)

        self._add_card("Roll AI", "Assistente integrado com conexão NVIDIA opcional.", self._show_ai)
        self._add_card("Aplicativos", "Catálogo inicial de aplicativos previstos para o RollOS.", self._show_apps)
        self._add_card("Armazenamento", "Consulta informativa do espaço livre no computador.", self._show_storage)
        self._add_card("Roll Cloud", "Crie um projeto de banco de dados na sua própria conta Neon.", self._show_roll_cloud)
        self._add_card("Sistema", "Informações e versão da camada Roll Core.", self._show_system)

        footer = QHBoxLayout()
        footer.addWidget(QLabel("ROLL CORE • SERVIÇOS LOCAIS ATIVOS"))
        footer.addStretch()
        self.footer_status = QLabel("Inicializando…")
        self.footer_status.setObjectName("muted")
        footer.addWidget(self.footer_status)
        outer.addLayout(footer)
        self._apply_screen_mode(self.extent.value())
        self._refresh_status()

    def _add_card(self, title: str, description: str, callback) -> None:
        card = QFrame()
        card.setObjectName("panel")
        card.setMinimumHeight(150)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout(card)
        heading = QLabel(title)
        heading.setStyleSheet("font-size: 19px; font-weight: 700;")
        desc = QLabel(description)
        desc.setObjectName("muted")
        desc.setWordWrap(True)
        button = QPushButton("Abrir")
        button.clicked.connect(callback)
        layout.addWidget(heading)
        layout.addWidget(desc)
        layout.addStretch()
        layout.addWidget(button)
        self.card_widgets.append(card)

    def _apply_screen_mode(self, value: int) -> None:
        state = self.display.state_for(value / 100)
        self.extent_value.setText(f"{value}%")
        self.mode_label.setText("MODO EXPANDIDO" if state.mode == "expanded" else "MODO COMPACTO")
        self.display_details.setText(
            f"Resolução virtual: {state.width_px} × {state.height_px} px  •  "
            f"Grade: {state.columns} coluna(s)"
        )
        while self.cards.count():
            self.cards.takeAt(0)
        for index, card in enumerate(self.card_widgets):
            self.cards.addWidget(card, index // state.columns, index % state.columns)
        if state.mode != self._last_mode:
            self.core.log_event("display_mode_changed", {
                "mode": state.mode, "expansion": state.expansion,
                "virtual_width": state.width_px,
            })
            self._last_mode = state.mode

    def _refresh_status(self) -> None:
        ai_status = "NVIDIA pronta" if self.ai.configured else "NVIDIA não configurada"
        self.footer_status.setText(f"{self.core.config.build}  •  {ai_status}")

    def _show_ai(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Roll AI")
        dialog.resize(620, 480)
        dialog.setStyleSheet(self.styleSheet())
        layout = QVBoxLayout(dialog)
        status = QLabel(
            f"NVIDIA configurada · modelo {self.ai.model}" if self.ai.configured
            else "NVIDIA não configurada — preencha NVIDIA_API_KEY no arquivo .env"
        )
        status.setObjectName("muted")
        output = QTextEdit()
        output.setReadOnly(True)
        output.setPlainText(
            "Olá! Sou o Roll AI. Faça uma pergunta para testar a conexão. "
            "Sem uma chave configurada, o sistema informa que a conexão está indisponível."
        )
        prompt = QLineEdit()
        prompt.setPlaceholderText("Digite sua pergunta…")
        send = QPushButton("Enviar")
        send.setObjectName("primary")

        def submit() -> None:
            question = prompt.text().strip()
            if not question:
                return
            prompt.clear()
            output.append(f"\nVocê: {question}\nRoll AI: processando…")
            send.setEnabled(False)
            worker = AiWorker(self.ai, question)
            self._workers.append(worker)

            def complete(answer: str) -> None:
                output.append(answer)
                send.setEnabled(True)
                if worker in self._workers:
                    self._workers.remove(worker)

            worker.finished_text.connect(complete)
            worker.start()

        send.clicked.connect(submit)
        prompt.returnPressed.connect(submit)
        layout.addWidget(status)
        layout.addWidget(output, 1)
        layout.addWidget(prompt)
        layout.addWidget(send)
        dialog.exec()

    def _show_apps(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Catálogo RollOS — demonstração")
        dialog.resize(520, 420)
        dialog.setStyleSheet(self.styleSheet())
        layout = QVBoxLayout(dialog)
        intro = QLabel("Catálogo conceitual. Nenhum aplicativo é instalado nesta versão.")
        intro.setObjectName("muted")
        layout.addWidget(intro)
        for app in self.apps.list_apps():
            row = QFrame()
            row.setObjectName("panel")
            row_layout = QVBoxLayout(row)
            name = QLabel(f"{app.name}  ·  {app.category}")
            name.setStyleSheet("font-weight: 700;")
            description = QLabel(app.description)
            description.setObjectName("muted")
            description.setWordWrap(True)
            state = QLabel(app.status.upper())
            state.setStyleSheet("color: #7ce7d5; font-size: 10px;")
            row_layout.addWidget(name)
            row_layout.addWidget(description)
            row_layout.addWidget(state)
            layout.addWidget(row)
        close = QPushButton("Fechar")
        close.clicked.connect(dialog.accept)
        layout.addWidget(close)
        dialog.exec()
        self.core.log_event("app_catalog_opened", {"items": len(self.apps.list_apps())})


    def _show_roll_cloud(self) -> None:
        QMessageBox.information(
            self, "Conectar ao Neon",
            "Esta etapa experimental cria um projeto na sua própria conta Neon. "
            "Você precisa gerar uma chave de API pessoal no Neon (Configurações da conta → API keys). "
            "A chave será usada somente nesta execução e não será gravada pelo RollOS. "
            "A integração OAuth automática depende de aprovação comercial do Neon."
        )
        api_key, accepted = QInputDialog.getText(
            self, "Autorização Neon", "Cole sua chave de API pessoal do Neon:",
            QLineEdit.EchoMode.Password,
        )
        if not accepted or not api_key.strip():
            return
        try:
            provisioner = NeonProvisioner(api_key)
            organizations = provisioner.list_organizations()
        except (NeonProvisioningError, ValueError) as exc:
            QMessageBox.warning(self, "Roll Cloud", str(exc))
            return
        labels = [f"{item['name']} — {item['id']}" for item in organizations]
        selected, accepted = QInputDialog.getItem(
            self, "Conta Neon", "Escolha a organização que será proprietária do projeto:",
            labels, 0, False,
        )
        if not accepted or not selected:
            return
        organization = organizations[labels.index(selected)]
        project_name, accepted = QInputDialog.getText(
            self, "Novo banco RollOS", "Nome do projeto:", text="rollos-cloud"
        )
        if not accepted or not project_name.strip():
            return
        regions = [
            "aws-us-east-1", "aws-us-east-2",
            "aws-eu-central-1", "aws-ap-southeast-1",
        ]
        region, accepted = QInputDialog.getItem(
            self, "Região Neon", "Escolha a região do banco:",
            regions, 0, False,
        )
        if not accepted:
            return
        confirm = QMessageBox.question(
            self, "Confirmar criação",
            f"Criar o projeto '{project_name.strip()}' na organização "
            f"'{organization['name']}' ({region})? Esta ação pode consumir os limites "
            "do plano Neon da sua conta.",
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            project = provisioner.create_project(
                organization["id"], project_name.strip(), region
            )
        except (NeonProvisioningError, ValueError) as exc:
            QMessageBox.warning(self, "Roll Cloud", str(exc))
            return
        self.core.log_event("neon_project_created", {
            "project_id": project.project_id, "region": project.region_id,
        })
        details = (
            f"Projeto criado na sua conta Neon.\\n\\n"
            f"Nome: {project.name}\\nID: {project.project_id}\\n"
            f"Região: {project.region_id}\\n"
        )
        if project.connection_uri:
            try:
                initialize_rollos_schema(project.connection_uri)
                save_database_credential(project.connection_uri)
                details += (
                    "\\nBanco conectado, tabelas iniciais criadas e conexão guardada "
                    "no cofre de credenciais do sistema."
                )
                if project.branch_id:
                    bucket_name = provisioner.create_private_bucket(
                        project.project_id, project.branch_id
                    )
                    details += f"\\nBucket privado de arquivos criado: {bucket_name}."
                else:
                    details += (
                        "\\nA branch não foi retornada pela Neon; o bucket privado "
                        "precisará ser criado depois."
                    )
            except (NeonProvisioningError, ValueError) as exc:
                details += f"\\n\\nProjeto criado, mas a configuração automática não terminou: {exc}"
        else:
            details += (
                "\\n\\nProjeto criado, mas a Neon não forneceu uma URI de conexão. "
                "A conexão e as tabelas precisam ser configuradas depois no Console Neon."
            )
        details += (
            "\\n\\nO armazenamento de vídeos e fotos em bucket ainda será ativado "
            "na próxima etapa do Roll Cloud."
        )
        QMessageBox.information(self, "Roll Cloud", details)

    def _show_storage(self) -> None:
        try:
            snapshot = self.storage.snapshot()
            total = snapshot.total_bytes / (1024 ** 3)
            free = snapshot.free_gb
            used = snapshot.used_percent
            message = (
                f"Local consultado: {snapshot.path}\n\n"
                f"Capacidade: {total:.1f} GB\n"
                f"Em uso: {used:.1f}%\n"
                f"Livre: {free:.1f} GB\n\n"
                "Consulta somente informativa. Nenhum arquivo foi alterado."
            )
            self.core.log_event("storage_snapshot_read", {"free_gb": round(free, 2)})
            QMessageBox.information(self, "Roll Storage", message)
        except OSError as exc:
            QMessageBox.warning(self, "Roll Storage", f"Não foi possível consultar o armazenamento: {exc}")

    def _show_system(self) -> None:
        info = collect_system_info()
        info["RollOS build"] = self.core.config.build
        info["Diretório de dados"] = str(self.core.data_dir)
        info["NVIDIA NIM"] = "Configurada" if self.ai.configured else "Não configurada"
        self.core.log_event("system_info_opened")
        QMessageBox.information(
            self, "Informações do RollOS",
            "\n".join(f"{key}: {value}" for key, value in info.items())
        )
