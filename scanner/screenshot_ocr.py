import os
import cv2
import easyocr

print("Loading EasyOCR...")

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SCREENSHOT_DIR = os.path.join(
    BASE_DIR,
    "..",
    "storage",
    "screenshots"
)


def ocr_image(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return ""

    print(
        "Original Shape:",
        img.shape
    )

    height, width = img.shape[:2]

    if max(width, height) < 3000:

        img = cv2.resize(
            img,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    try:

        results = reader.readtext(
            gray,
            detail=0
        )

    except Exception as e:

        print(
            f"OCR Failed: {image_path}"
        )

        print(e)

        return ""

    return "\n".join(results)


def run_ocr():

    report = []

    for folder in sorted(os.listdir(SCREENSHOT_DIR)):

        folder_path = os.path.join(
            SCREENSHOT_DIR,
            folder
        )

        if not os.path.isdir(folder_path):
            continue

        report.append("\n" + "=" * 80)
        report.append(folder.upper())
        report.append("=" * 80)

        for file in sorted(os.listdir(folder_path)):

            if not file.lower().endswith(".png"):
                continue

            image_path = os.path.join(
                folder_path,
                file
            )

            print(f"Processing {file}")

            text = ocr_image(image_path)

            report.append(
                f"\n----- {file} -----"
            )

            report.append(text)

    return "\n".join(report)


if __name__ == "__main__":

    print(run_ocr())