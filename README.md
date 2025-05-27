# Mobile Forensic Triage Tool

A lightweight cross-platform tool that connects to Android devices using ADB (Android Debug Bridge) to extract and preview forensic data such as SMS messages, call logs, photos, and WhatsApp media. This project is ideal for forensic triage in cybercrime investigations or during digital evidence collection.

---

## 📦 Features

* Preview and extract:

  * SMS (with keyword filtering)
  * Call logs
  * Photos (DCIM folder)
  * WhatsApp media files
* GUI built with PyQt5
* Export data to CSV format
* Auto-detects connected Android device using ADB

---

## 🛠️ Requirements

* Python 3.6+
* Android device with USB debugging enabled
* ADB installed and added to PATH

### Python Dependencies

Install with:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
PyQt5
```

---

## 🚀 How to Run

1. Connect an Android device via USB and ensure ADB detects it:

```bash
adb devices
```

2. Launch the tool:

```bash
python main.py
```

---

## 📁 Project Structure

```
mobile-forensic-tool/
├── main.py                   # Entry point
├── extract/
│   ├── adb_connector.py      # Pulls data using ADB
│   └── parser.py             # Parses SMS, call logs
├── export/
│   ├── export_csv.py         # CSV export
│   └── export_pdf.py         # (Optional) PDF export
├── ui/
│   └── gui.py                # PyQt5 GUI logic
├── output/                   # Output directory for extracted files
├── assets/                   # Icons, images
└── requirements.txt          # Python dependencies
```

---

## ✅ Checklist Functionality

The GUI provides checkboxes to:

* Select which data to preview/extract
* Filter SMS by keyword
* Preview the first 100 entries before extraction

---

## ⚠️ Disclaimer

This tool is intended for ethical use only. Ensure you have permission before accessing data from any mobile device.

---

## 📌 License

MIT License
