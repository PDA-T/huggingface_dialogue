import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from model import ChatModel


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hugging Face模型对话")
        self.resize(700, 340)
        self.model = ChatModel()
        self.setup_ui()
        self.model_loaded = False
        self.setStyleSheet(self.qss_style())

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(24, 22, 24, 18)

        # 顶部
        top_row = QHBoxLayout()

        # 居中
        self.status_label = QLabel("未装载模型", self)
        self.status_label.setFont(QFont("微软雅黑", 10))
        self.status_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.status_label.setMinimumWidth(180)
        self.status_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        top_row.addWidget(self.status_label, 2)

        self.model_input = QLineEdit(self)
        self.model_input.setPlaceholderText("输入模型名称(如:Qwen/Qwen3-0.6B)")
        self.model_input.setFont(QFont("微软雅黑", 11))
        self.model_input.setMinimumWidth(220)
        self.model_input.setMaximumWidth(320)
        self.model_input.setMinimumHeight(38)
        top_row.addWidget(self.model_input, 3)

        self.load_btn = QPushButton("检测并装载", self)
        self.load_btn.setFont(QFont("微软雅黑", 11, QFont.Bold))
        self.load_btn.setMinimumHeight(38)
        self.load_btn.clicked.connect(self.load_model)
        top_row.addWidget(self.load_btn, 1)

        main_layout.addLayout(top_row)

        # 输入和发送按钮
        mid_row = QHBoxLayout()
        self.input_edit = QLineEdit(self)
        self.input_edit.setPlaceholderText("请输入你的问题")
        self.input_edit.setFont(QFont("微软雅黑", 12))
        self.input_edit.setMinimumHeight(40)
        mid_row.addWidget(self.input_edit)

        self.send_btn = QPushButton("发送", self)
        self.send_btn.setFont(QFont("微软雅黑", 12, QFont.Bold))
        self.send_btn.setMinimumHeight(40)
        self.send_btn.setMaximumWidth(88)
        self.send_btn.clicked.connect(self.send_question)
        self.send_btn.setEnabled(False)
        mid_row.addWidget(self.send_btn)
        main_layout.addLayout(mid_row)

        # 聊天回复
        self.reply_label = QLabel("AI回复将在这里显示", self)
        self.reply_label.setFont(QFont("微软雅黑", 13))
        self.reply_label.setWordWrap(True)
        self.reply_label.setMinimumHeight(100)
        self.reply_label.setFrameShape(QFrame.Box)
        self.reply_label.setFrameShadow(QFrame.Raised)
        self.reply_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.reply_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.reply_label)

        self.setLayout(main_layout)

    def qss_style(self):
        return """
        QWidget {
            background-color: #23272E;
            color: #F1F1F1;
            font-family: 微软雅黑, Arial;
        }
        QLineEdit {
            background-color: #353B48;
            color: #F1F1F1;
            border: 2px solid #242830;
            border-radius: 11px;
            padding: 8px;
            font-size: 15px;
        }
        QLineEdit:focus {
            border: 2px solid #00B8B8;
        }
        QPushButton {
            background-color: #00ADB5;
            color: #222831;
            border: none;
            border-radius: 13px;
            padding: 8px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:pressed {
            background-color: #00888f;
        }
        QPushButton:disabled {
            background-color: #444a53;
            color: #888;
        }
        QLabel {
            background: transparent;
            color: #F1F1F1;
            font-size: 14px;
        }
        QFrame {
            border: 2px solid #393E46;
            border-radius: 16px;
            background-color: #393E46;
            padding: 14px;
            font-size: 16px;
        }
        """

    def load_model(self):
        model_name = self.model_input.text().strip()
        if not model_name:
            self.status_label.setText("请输入模型名称")
            return
        self.status_label.setText("正在检测/下载模型，请稍等...")
        QApplication.processEvents()
        try:
            msg = self.model.load_model(model_name)
            self.status_label.setText(msg)
            self.model_loaded = True
            self.send_btn.setEnabled(True)
        except Exception as e:
            self.status_label.setText(f"模型加载失败: {str(e)}")
            self.model_loaded = False
            self.send_btn.setEnabled(False)

    def send_question(self):
        user_text = self.input_edit.text().strip()
        if not user_text:
            self.reply_label.setText("请输入内容")
            return
        self.reply_label.setText("AI正在思考...")
        QApplication.processEvents()
        try:
            reply = self.model.chat(user_text)
            self.reply_label.setText(reply)
        except Exception as e:
            self.reply_label.setText(f"对话出错: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
