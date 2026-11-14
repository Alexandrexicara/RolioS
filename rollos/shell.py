from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .ai_client import NvidiaAssistant
from .system_info import collect_system_info


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
        self.ai = NvidiaAssistant()
        self._workers: list[AiWorker] = []
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
        self.extent.setRange(35, 100)
        self.extent.setValue(35)
        self.extent.valueChanged.connect(self._apply_screen_mode)
        slider_row.addWidget(self.extent, 1)
        self.extent_value = QLabel("35%")
        slider_row.addWidget(self.extent_value)
        controls.addLayout(slider_row)
        outer.addWidget(panel)

        self.cards_host = QWidget()
        self.cards = QGridLayout(self.cards_host)
        self.cards.setSpacing(14)
        self.card_widgets: list[QFrame] = []
        outer.addWidget(self.cards_host, 1)

        self._add_card("Roll AI", "Assistente integrado com conexão NVIDIA opcional.", self._show_ai)
        self._add_card("Aplicativos", "Base para aplicativos nativos e web apps.", self._show_apps)
        self._add_card("Arquivos", "Ponto inicial do gerenciador de arquivos.", self._show_files)
        self._add_card("Sistema", "Informações do computador que executa o protótipo.", self._show_system)
        footer = QHBoxLayout()
        footer.addWidget(QLabel("ROLL CORE • PROTÓTIPO DE SOFTWARE"))
        footer.addStretch()
        footer.addWidget(QLabel("Hardware físico ainda não conectado"))
        outer.addLayout(footer)
        self._apply_screen_mode(35)

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
        self.extent_value.setText(f"{value}%")
        expanded = value >= 68
        self.mode_label.setText("MODO EXPANDIDO" if expanded else "MODO COMPACTO")
        while self.cards.count():
            self.cards.takeAt(0)
        columns = 2 if expanded else 1
        for index, card in enumerate(self.card_widgets):
            self.cards.addWidget(card, index // columns, index % columns)

    def _show_ai(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Roll AI")
        dialog.resize(620, 480)
        dialog.setStyleSheet(self.styleSheet())
        layout = QVBoxLayout(dialog)
        status = QLabel(
            "NVIDIA configurada" if self.ai.configured
            else "NVIDIA não configurada — edite o arquivo .env"
        )
        status.setObjectName("muted")
        output = QTextEdit()
        output.setReadOnly(True)
        output.setPlainText("Olá! Sou o Roll AI. Faça uma pergunta para testar a integração.")
        prompt = QLineEdit()
        prompt.setPlaceholderText("Digite sua pergunta...")
        send = QPushButton("Enviar")
        send.setObjectName("primary")

        def submit() -> None:
            question = prompt.text().strip()
            if not question:
                return
            prompt.clear()
            output.append(f"\nVocê: {question}\nRoll AI: processando...")
            send.setEnabled(False)
            worker = AiWorker(self.ai, question)
            self._workers.append(worker)
            def complete(answer: str) -> None:
                output.append(answer)
                send.setEnabled(True)
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
        QMessageBox.information(
            self, "Aplicativos",
            "O catálogo e o instalador de aplicativos serão implementados após definir o formato de pacotes."
        )

    def _show_files(self) -> None:
        QMessageBox.information(self, "Arquivos", "O gerenciador de arquivos será conectado na próxima etapa.")

    def _show_system(self) -> None:
        info = collect_system_info()
        QMessageBox.information(
            self, "Informações do protótipo",
            "\n".join(f"{key}: {value}" for key, value in info.items())
        )
