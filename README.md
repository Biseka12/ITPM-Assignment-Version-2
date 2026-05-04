# Assignment 1 – Transliteration Accuracy Testing (Option 1)

**Unit:** IT3040 – ITPM | **Year:** 3 | **Semester:** 1

## Overview

This repository contains a Playwright-based automation suite that tests the Chat Sinhala transliteration accuracy of [https://www.pixelssuite.com/chat-translator](https://www.pixelssuite.com/chat-translator).

Fifty negative test cases (Neg_0001–Neg_0050) are recorded in the Excel file, covering all 24 Singlish input types specified in Appendix 1 of the assignment brief.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11 or 3.12 |
| pip | Latest |
| Google Chrome (recommended) | Any recent version |

---

## Installation

### 1. Clone or extract the project

Place the `test_automation` folder on your **D: drive** so that the path is:

```
D:\test_automation\
```

### 2. Open Command Prompt and navigate to the folder

```cmd
cd /d D:\test_automation
```

### 3. Install dependencies (one-time)

```cmd
pip install -U pip
pip install playwright openpyxl
playwright install
```

---

## Running the Tests

From the `D:\test_automation` directory, run:

```cmd
python test_automation.py --excel "test_automation/Assignment 1 - Test cases.xlsx" --url "https://www.pixelssuite.com/chat-translator" --wait-ms 5000 --type-delay-ms 80 --slow-mo-ms 200 --save-every 1 --keep-open
```

### Command-line Options

| Flag | Default | Description |
|---|---|---|
| `--excel` | Auto-detected | Path to the Excel test case file |
| `--url` | Pixelssuite chat-translator | URL of the application under test |
| `--wait-ms` | 5000 | Milliseconds to wait after each transliteration |
| `--type-delay-ms` | 80 | Typing delay per character (ms) |
| `--slow-mo-ms` | 200 | Playwright slow-motion delay (ms) |
| `--save-every` | 1 | Save Excel after every N rows |
| `--keep-open` | false | Keep browser open after run |
| `--headless` | false | Run without browser UI |

---

## Checking Results

After the script completes:

1. Open `Assignment 1 - Test cases.xlsx` from the `test_automation` folder.
2. Verify the **Actual output** (column E) and **Status** (column F) columns are populated.
3. Review the **Singlish input types covered** (column G) and **Evidence or rationale** (column H) columns which were manually filled in.

---

## Project Structure

```
test_automation/
├── test_automation.py           # Main Playwright automation script
├── Assignment 1 - Test cases.xlsx  # Test cases with results
└── README.md                    # This file
```

---

## Test Case Design

- **Total test cases:** 50 negative test cases (Neg_0001 – Neg_0050)
- **Coverage:** All 24 Singlish input types from Appendix 1, with ≥ 2 test cases per type
- **TC ID format:** `Neg_XXXX` (negative test cases — cases where the system is expected to fail)
- **Input length categories:** S (≤ 30 chars), M (31–299 chars), L (300–450 chars)
