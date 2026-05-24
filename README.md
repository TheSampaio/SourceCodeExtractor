# Source Code Extractor

Source Code Extractor is a clean desktop application built with Python that streamlines the process of gathering source code context from projects. It allows you to select a project directory, filter files by extension, ignore irrelevant paths (such as `bin`, `node_modules`, or `.git`), and instantly copy the formatted output to your clipboard.

This tool is especially useful for sharing project context with AI assistants and LLMs without manually opening and copying dozens of files.

---

## Features

* **Visual Interface**
  Easy-to-use desktop GUI for selecting folders and configuring extraction rules.

* **Smart Filtering**
  Built-in toggles for common file extensions such as `.cs`, `.css`, `.html`, `.js`, `.json`, `.py`, `.sql`, and `.ts`.

* **Noise Reduction**
  Automatically ignores heavy and irrelevant directories like `.git`, `.vs`, `.vscode`, `node_modules`, `bin`, `obj`, `build`, `dist` and `platform`,.

* **Advanced Customization**
  Add custom relative paths to ignore directly through the interface.

* **One-Click Clipboard Export**
  Formats extracted code with clear file headers:

  ```text
  // ==== path/to/file ====
  ```

  Then copies everything directly to your clipboard.

---

## Prerequisites

* Python 3.x
* `pyperclip` (used for clipboard management)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/thesampaio/SourceCodeExtractor.git
```

### 2. Navigate to the project directory

```bash
cd SourceCodeExtractor
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application with:

```bash
python src/main.py
```

---

## Powered by Kroma UI

This application's graphical interface is built using **Kroma**.

Kroma is a lightweight object-oriented GUI framework built on top of Tkinter, designed to simplify the creation of graphical user interfaces in Python. It provides an intuitive API for building windows, managing widgets, and handling events efficiently.

### Kroma Features

* Simplified window and widget management
* Predefined color and alignment options
* Message box utilities
* Screen resolution retrieval
* Customizable widget properties
* Event-driven architecture

> Kroma is built on top of Tkinter, which comes pre-installed with Python.
> No additional installation is required.
> It is open-source and distributed under the BSD 2-Clause License.

---

## License

This project is open-source and available under the MIT License. See the `LICENSE` file for more information.
