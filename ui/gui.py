import sys
import os
import subprocess
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QCheckBox, QPushButton, QMessageBox, QDialog,
    QTextEdit, QLineEdit, QScrollArea
)
from PyQt5.QtGui import QPixmap

from extract import adb_connector
from extract import parser
from export import export_csv, export_pdf

def launch_gui():
    app = QApplication(sys.argv)
    window = ForensicTool()
    window.show()
    sys.exit(app.exec_())

class ForensicTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mobile Forensic Triage Tool")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel("Select Data to Extract:")
        self.layout.addWidget(self.label)

        self.sms_cb = QCheckBox("SMS")
        self.calllog_cb = QCheckBox("Call Logs")
        self.photos_cb = QCheckBox("Photos")
        self.whatsapp_cb = QCheckBox("WhatsApp Media")

        for cb in [self.sms_cb, self.calllog_cb, self.photos_cb, self.whatsapp_cb]:
            self.layout.addWidget(cb)

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("🔍 Optional: Enter keyword to filter messages")
        self.layout.addWidget(self.keyword_input)

        self.preview_btn = QPushButton("Preview Selected")
        self.preview_btn.clicked.connect(self.preview_data)
        self.layout.addWidget(self.preview_btn)

        self.extract_btn = QPushButton("Extract & Export")
        self.extract_btn.clicked.connect(self.extract_data)
        self.layout.addWidget(self.extract_btn)

        self.setLayout(self.layout)

    def preview_data(self):
        keyword = self.keyword_input.text().strip()
        preview_text = ""

        if self.sms_cb.isChecked():
            sms = parser.get_sample_sms()
            if keyword:
                sms = parser.filter_messages_by_keyword(sms, keyword)
            preview_text += "📱 SMS:\n" + "\n".join(
                f"{m['Sender']}: {m['Message']} @ {m['Timestamp']}" for m in sms
            ) + "\n\n"

        if self.calllog_cb.isChecked():
            calls = parser.get_sample_call_logs()
            preview_text += "📞 Call Logs:\n" + "\n".join(
                f"{c['Name']} - {c['Type']} - {c['Time']}" for c in calls
            ) + "\n\n"

        if self.photos_cb.isChecked():
            try:
                result = subprocess.run(
                    ["adb", "shell", "ls", "/sdcard/DCIM/Camera"],
                    capture_output=True,
                    text=True
                )
                photo_list = result.stdout.strip().splitlines()
                if photo_list:
                    preview_text += "🖼️ Photos (on device):\n" + "\n".join(photo_list[:100]) + "\n\n"
                else:
                    preview_text += "🖼️ Photos: No files found on device.\n\n"
            except Exception as e:
                preview_text += f"🖼️ Photos: Error listing files.\n{str(e)}\n\n"

        if self.whatsapp_cb.isChecked():
            try:
                result = subprocess.run(
                    ["adb", "shell", "find", "/sdcard/WhatsApp/Media" , "-type", "f"],
                    capture_output=True,
                    text=True
                )
                media_list = result.stdout.strip().splitlines()
                if media_list:
                    preview_text += "🟢 WhatsApp Media (on device):\n" + "\n".join(os.path.basename(f) for f in media_list[:100]) + "\n\n"
                else:
                    preview_text += "🟢 WhatsApp Media: No files found on device.\n\n"
            except Exception as e:
                preview_text += f"🟢 WhatsApp Media: Error listing files.\n{str(e)}\n\n"

        dlg = QDialog(self)
        dlg.setWindowTitle("Preview Data")
        dlg.setGeometry(200, 200, 500, 400)
        layout = QVBoxLayout()
        txt_area = QTextEdit()
        txt_area.setReadOnly(True)
        txt_area.setText(preview_text.strip() or "No data to preview.")
        layout.addWidget(txt_area)
        dlg.setLayout(layout)
        dlg.exec_()

    def extract_data(self):
        if not adb_connector.check_device_connected():
            QMessageBox.critical(self, "Error", "No device connected via ADB.")
            return

        if self.photos_cb.isChecked():
            adb_connector.pull_photos()
        if self.whatsapp_cb.isChecked():
            adb_connector.pull_whatsapp_media()
        if self.sms_cb.isChecked():
            sms = parser.get_sample_sms()
            keyword = self.keyword_input.text().strip()
            if keyword:
                sms = parser.filter_messages_by_keyword(sms, keyword)
            export_csv.export_to_csv(sms, "sms_logs")
        if self.calllog_cb.isChecked():
            calls = parser.get_sample_call_logs()
            export_csv.export_to_csv(calls, "call_logs")

        QMessageBox.information(self, "Done", "Data extraction complete.")
