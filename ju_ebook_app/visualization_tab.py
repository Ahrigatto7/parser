
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from ebook_manager import EbookManager

class VisualizationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = EbookManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)

        self.plot_button = QPushButton("📊 개념별 사례 수 시각화")
        self.plot_button.clicked.connect(self.plot_data)

        layout.addWidget(self.plot_button)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        concept_counts = {
            concept: len(data["사례"])
            for concept, data in self.manager.ebook_data.items()
        }

        if concept_counts:
            concepts = list(concept_counts.keys())
            counts = list(concept_counts.values())
            ax.barh(concepts, counts)
            ax.set_xlabel("사례 수")
            ax.set_title("개념별 사례 분포")
        else:
            ax.text(0.5, 0.5, "데이터 없음", ha="center")

        self.canvas.draw()
