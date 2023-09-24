import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QTextBrowser
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
import re

class HTMLAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HTML Analyzer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.code_editor = QTextEdit()
        self.code_editor.setFont(QFont("Arial", 14))
        layout.addWidget(self.code_editor)

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setFont(QFont("Arial", 14))
        self.analyze_button.clicked.connect(self.analyze_html)
        layout.addWidget(self.analyze_button)

        self.output_label = QLabel("Output:")
        self.output_label.setFont(QFont("Arial", 14))
        layout.addWidget(self.output_label)

        self.output_browser = QTextBrowser()
        self.output_browser.setFont(QFont("Arial", 14))
        layout.addWidget(self.output_browser)

        self.setLayout(layout)

        self.set_styles()

    def set_styles(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(15, 15, 15))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        self.analyze_button.setStyleSheet("QPushButton { background-color: #357ABD; color: white; }")

    def analyze_html(self):
        html_content = self.code_editor.toPlainText()
        tags = self.extract_tags(html_content)
        self.display_output(tags)

    def extract_tags(self, conteudo_html):
        tags = re.findall(r'<\s*([a-zA-Z0-9]+)\s*(.*?)\s*>|</\s*([a-zA-Z0-9]+)\s*>|<\s*([a-zA-Z0-9]+)\s*/\s*>|([^<]*)', conteudo_html)
        return tags

    def display_output(self, tags):
        output = ""
        pilha_de_tags = []

        for tag in tags:
            tag_abertura, atributos, tag_fechamento, tag_self_closing, conteudo_interno = tag
            if tag_abertura or tag_self_closing:
                nivel = len(pilha_de_tags)
                tag_name = tag_abertura if tag_abertura else tag_self_closing
                tag_obj = {
                    "name": tag_name,
                    "level": nivel,
                    "attributes": re.findall(r'([a-zA-Z0-9-]+)="(.*?)"', atributos),
                    "inner_html": [],
                }
                if not tag_self_closing:
                    pilha_de_tags.append(tag_obj)
                recuo = '  ' * nivel
                output += f"{recuo}<span style='color: blue'>&lt;{tag_name}</span>, Nível {nivel}<br>"
                for attr in tag_obj["attributes"]:
                    output += f"{recuo}  <span style='color: green'>Atributo:</span> {attr[0]}<br>"
                    output += f"{recuo}    <span style='color: red'>Valor:</span> {attr[1]}<br>"
            elif tag_fechamento:
                while pilha_de_tags:
                    last_tag = pilha_de_tags.pop()
                    if last_tag["name"] == tag_fechamento:
                        recuo = '  ' * last_tag['level']
                        for inner in last_tag["inner_html"]:
                            output += f"{recuo}  <span style='color: purple'>Conteúdo:</span> {inner.strip()}<br>"
                        output += f"{recuo}<span style='color: blue'>&lt;/{tag_fechamento}</span> (Tag de fechamento)<br>"
                        break
            elif conteudo_interno.strip():
                if pilha_de_tags:
                    pilha_de_tags[-1]["inner_html"].append(conteudo_interno.strip())

        self.output_browser.setHtml(output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HTMLAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
