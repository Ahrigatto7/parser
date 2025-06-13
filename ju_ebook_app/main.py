
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from ebook_tab import EbookTab
from visualization_tab import VisualizationTab
import sys

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📘 Ebook 통합 분석기")
        self.setGeometry(100, 100, 900, 700)

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(EbookTab(), "📘 Ebook 관리")
        self.tabs.addTab(VisualizationTab(), "📊 시각화")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
