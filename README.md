# Printer Service 🖨️

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

A lightweight Python service to manage printer operations: **Scan**, **Copy**, and **Print** documents easily.

---

## 🚀 Features

- Scan documents directly
- Copy multiple copies easily
- Print files with page selection
- Configurable via `config.json`
- Detailed logging for debugging

---

## 📋 Requirements

- Python 3.10+
- Windows OS (with printer properly installed and accessible)
- A `config.json` file with your printer configuration

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/JahongirHakimjonov/printer-service.git
cd printer-service
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Configuration

Create a `config.json` file in the project root:

```json
{
  "printer_name": "Canon iR2006/2206 UFRII LT"
}
```

> Make sure the printer name matches exactly as it appears in Windows Printer Settings.

---

## 🏃 Usage

Run the service:

```bash
python main.py
```

You will be prompted to select an operation:

| Type   | Description                  |
|--------|-------------------------------|
| SCAN   | Start scanning a document     |
| COPY   | Make multiple copies          |
| PRINT  | Print a file (PDF, etc.)       |

Example flow:

```bash
$ python main.py
Type input (SCAN, COPY, PRINT): PRINT
How many pages to print?: 1-3
Enter the file path: D:\files\example.pdf
```

---

## 🔥 Advanced Usage

You can automate configurations or pass parameters using environment variables (future feature planned).

Planned CLI support:

```bash
python main.py --type PRINT --file_path "D:\docs\test.pdf" --pages "1-2"
```

_(Not available yet — currently interactive mode only.)_

---

## 📂 Project Structure

```bash
├── config/                # Configuration files (e.g., config.json)
├── resources/
│   └── output/            # Scanned/copied/printed file outputs
├── src/
│   ├── controller/        # Handles user inputs and flow control
│   ├── exceptions/        # Custom exception classes
│   ├── services/          # Core printer services
│   │   ├── copy/          # Copy service logic
│   │   ├── print_file/    # Print service logic
│   │   └── scan/          # Scan service logic
│   ├── utils/             # Utilities (logger, enums, etc.)
│   └── __pycache__/       # Python cache files (ignored)
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚡ Error Handling

- Invalid operation type → error logged, program exits.
- Missing file or incorrect printer → critical error logged.
- Bad config format → immediate crash with readable error.

---

## 👨‍💻 Author

**Ryan Gosling** — Backend Developer

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

# ✅ Summary of Improvements

- Added **badges** (Python version, License, Build Status)
- Added **Features** section
- Cleaned **Usage** into a table
- **Advanced Usage** preview (for future CLI expansion)
- Clear **Error Handling** expectations
- **Project Structure** tree
- **Professional formatting** — easy to scan