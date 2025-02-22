from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton,
    QWidget, QLineEdit, QLabel, QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QMovie, QColor, QPalette
import os
import sys

# Define directories
CURRENT_DIR = os.getcwd()
GRAPHICS_DIR = os.path.join(CURRENT_DIR, "Frontend/Graphics")
GIF_PATH = os.path.join(GRAPHICS_DIR, "original-865936c8666c1f5112b28efad81084c3.gif")  # Update with correct path

class ChatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton,
    QWidget, QLineEdit, QLabel, QFrame, QHBoxLayout,QCheckBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QMovie, QColor, QPalette
import os
import sys

# Define directories
CURRENT_DIR = os.getcwd()
GRAPHICS_DIR = os.path.join(CURRENT_DIR, "Frontend/Graphics")
GIF_PATH = os.path.join(GRAPHICS_DIR, "original-865936c8666c1f5112b28efad81084c3.gif")  # Update with correct path



class ChatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 600, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        
        # Set background color matching GIF
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))  # Adjust this color if needed
        self.setPalette(palette)

        # **GIF in Center**
        self.gif_label = QLabel(self.central_widget)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(GIF_PATH)
        self.gif_label.setMovie(self.movie)
        self.movie.setScaledSize(QSize(300, 300))  # Adjust size dynamically
        self.movie.start()

        # **Close Button**
        self.close_button = QPushButton("✖")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background-color: transparent; color: white; font-size: 16px; border: none;")
        self.close_button.clicked.connect(self.close)

        # **Chat Box UI**
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: rgba(255,255,255,0.1); color: white; border-radius: 10px; font-size: 14px; padding: 10px;")
        self.chat_display.setFont(QFont("Arial", 10))

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message here...")
        self.input_box.setStyleSheet("background-color: rgba(255,255,255,0.8); border-radius: 5px; padding: 5px;")
        self.input_box.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: rgba(0,0,0,0.6); color: white; padding: 8px; border-radius: 5px;")
        self.send_button.clicked.connect(self.send_message)

        # **Layouts**
        self.header_layout = QHBoxLayout()
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.close_button)

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.gif_label)
        self.layout.addWidget(self.chat_display)
        self.layout.addWidget(self.input_box)
        self.layout.addWidget(self.send_button)

        self.central_widget.setLayout(self.layout)

    def send_message(self):
        user_text = self.input_box.text().strip()
        if user_text:
            self.chat_display.append(f"<b>You:</b> {user_text}")
            response = self.get_chatbot_response(user_text)
            self.chat_display.append(f"<b>Bot:</b> {response}")
            self.input_box.clear()

    def get_chatbot_response(self, message):
        # Placeholder for chatbot response logic
        return "This is an AI-generated response."

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGUI()
    window.show()
    sys.exit(app.exec_())

