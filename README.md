# Folder Archaeologist

<img width="902" height="385" alt="image" src="https://github.com/user-attachments/assets/3b7ecf12-28ee-446a-85e7-45382c48e82a" />

---

## Overview

**Folder Archaeologist** is an advanced command-line utility built for digital explorers, developers, and data professionals who want to analyze, categorize, and manage large folders and file collections. Harnessing the power of Python and the `rich` library, Folder Archaeologist turns directory scanning and file forensics into an accessible, visual, and highly interactive process.

---

## Features

- **Categorize by Extension:** Instantly group files by type to discover common or rare digital “materials.”
- **Search by Size:** Find and display files exceeding custom size thresholds, complete with live scanning progress.
- **Filter by Age:** Locate “ancient” files using flexible date/age queries.
- **Detect Naming Patterns:** Uncover file name patterns and clusters, revealing related artifacts or dataset outliers.
- **Interactive CLI:** Visually navigate results through rich menus, colored tables, and text-based dashboards.
- **Progress Bars Everywhere:** User feedback for every scan, so you’re never left guessing about progress.
- **Cross-Platform:** Supports Linux, macOS, and Windows out of the box.
- **Safe, Efficient, and Modern:** No destructive defaults, modular design, and beautiful output for real work.

---

## Installation

Install via pip:

```
pip install folderarchaeologist
```

Or install directly from source:

```
git clone https://github.com/koffandaff/folderarchaeologist.git
cd folderarchaeologist
pip install -r requirements.txt
```

---

## Quick Start

Simply run from your terminal:

```
python main.py directory\
```

Or, if installed as a package:

```
folderarchaeologist directory\
```

Select a directory, pick your exploration mode, and follow the prompts to scan, filter, and interact with your files—all in style.

---

## Usage

1. **Choose a target folder** when prompted.
2. **Pick an exploration mode:**
   - By extension
   - By file size (with user-defined thresholds)
   - By age (custom year cutoff)
   - By naming pattern (clusters)
3. **View and filter results** using the rich terminal UI.
4. **Export, archive, or perform next actions**—with confidence.

---

## Screenshots

<!-- Paste screenshot or demo GIFs here after using the tool in the CLI -->

### Categories Menu

<img width="902" height="385" alt="image" src="https://github.com/user-attachments/assets/3b7ecf12-28ee-446a-85e7-45382c48e82a" />

---

### File Operations Menu

<img width="760" height="408" alt="image" src="https://github.com/user-attachments/assets/962cea99-bbae-45ca-9776-dcab5fbf229b" />

---

## Development

- Completely written in Python.
- Modular, extensible code structure (`main.py`, `categories.py`, `features.py`, `utilities.py`).
- Clean separation of UI and data logic.
- Powered by [`rich`](https://github.com/Textualize/rich) for all terminal visualization.

---

## Contributions

Contributions and suggestions are welcome!
Please open issues or submit pull requests via GitHub. See the [issues page](https://github.com/koffandaff/folderarchaeologist/issues) for outstanding tasks.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Authors & Contributors

This project is made by:

* Dhruvil (`koffandaff`)
* Kirtan   (`bond0707`)

It is submitted in "for the love of code 2025" hackathon.

---