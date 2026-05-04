import time
import argparse
from playwright.sync_api import sync_playwright
import openpyxl

def is_sinhala(text):
    return any("\u0D80" <= c <= "\u0DFF" for c in text)

def run_test():
    parser = argparse.ArgumentParser()
    parser.add_argument('--excel', required=True)
    parser.add_argument('--url', required=True)
    parser.add_argument('--wait-ms', type=int, default=5000)
    parser.add_argument('--type-delay-ms', type=int, default=80)
    parser.add_argument('--slow-mo-ms', type=int, default=200)
    parser.add_argument('--save-every', type=int, default=1)
    parser.add_argument('--keep-open', action='store_true')
    args = parser.parse_args()

    wb = openpyxl.load_workbook(args.excel)
    sheet = wb.active

    headers = [cell.value for cell in sheet[1]]

    tc_id_col = input_col = expected_col = actual_col = status_col = None

    for idx, h in enumerate(headers, start=1):
        if h and 'TC' in str(h):
            tc_id_col = idx
        elif h and 'Input' in str(h) and 'expected' not in str(h).lower():
            input_col = idx
        elif h and 'Expected' in str(h):
            expected_col = idx
        elif h and 'Actual' in str(h):
            actual_col = idx
        elif h and 'Status' in str(h):
            status_col = idx

    print(f"Found columns: TC={tc_id_col}, Input={input_col}, Expected={expected_col}, Actual={actual_col}, Status={status_col}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=args.slow_mo_ms)
        context = browser.new_context()
        page = context.new_page()

        print(f"Loading {args.url}...")
        page.goto(args.url)

        page.wait_for_timeout(args.wait_ms)
        page.wait_for_load_state("networkidle")

        print("Frontend loaded successfully.")

        # find input
        input_box = None
        for selector in ["textarea", "input[type='text']", "div[contenteditable='true']", "div[role='textbox']"]:
            try:
                loc = page.locator(selector).first
                if loc.is_visible():
                    input_box = loc
                    print(f"Found input: {selector}")
                    break
            except:
                continue

        if not input_box:
            print("ERROR: Input not found")
            page.screenshot(path="error.png")
            browser.close()
            return

        total_rows = sheet.max_row
        print(f"Starting test with {total_rows - 1} rows...")

        for row in range(2, total_rows + 1):

            tc_id = sheet.cell(row=row, column=tc_id_col).value
            input_text = sheet.cell(row=row, column=input_col).value
            expected = sheet.cell(row=row, column=expected_col).value

            if not input_text:
                print(f"Row {row}: No input, skipping")
                continue

            print(f"Testing {tc_id}: {input_text[:50]}...")

            try:
                # Clear + type
                input_box.click()
                input_box.fill("")
                input_box.type(input_text, delay=args.type_delay_ms)

                input_box.press("Enter")

                # IMPORTANT WAIT (fix EMPTY issue)
                page.wait_for_timeout(4000)

                # GET LATEST RESPONSE (FIXED LOGIC)
                messages = page.locator("div").all()

                output_text = ""

                for msg in reversed(messages):
                    try:
                        text = msg.inner_text().strip()

                        if text and text != input_text and len(text) > 2:
                            output_text = text
                            break
                    except:
                        continue

                print(f"  Output: {output_text[:80] if output_text else '[EMPTY]'}")

                # PASS / FAIL logic (FIXED)
                if output_text and expected and expected in output_text:
                    status = "PASS"
                elif output_text:
                    status = "FAIL (mismatch)"
                else:
                    status = "FAIL (no output)"

                sheet.cell(row=row, column=actual_col, value=output_text)
                sheet.cell(row=row, column=status_col, value=status)

                print(f"  Status: {status}")

            except Exception as e:
                print(f"  ERROR: {e}")
                sheet.cell(row=row, column=actual_col, value=f"ERROR: {str(e)[:100]}")
                sheet.cell(row=row, column=status_col, value="ERROR")

            if row % args.save_every == 0:
                wb.save(args.excel)
                print(f"  [Saved at row {row}]")

        wb.save(args.excel)
        print(f"\nDone! Results saved to {args.excel}")

        if args.keep_open:
            input("Press Enter to close browser...")

        browser.close()

if __name__ == "__main__":
    run_test()