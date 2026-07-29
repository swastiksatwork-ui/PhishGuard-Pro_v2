import json
import sys
import subprocess

INPUT_FILE = "storage/moondream_dump.json"
OUTPUT_FILE = "storage/moondream_report.txt"


def try_parse(value):
    """Recursively parse JSON strings."""
    while isinstance(value, str):
        value = value.strip()

        if not value:
            break

        if value[0] not in "{[":
            break

        try:
            value = json.loads(value)
        except Exception:
            break

    return value


def write_section(file, obj, indent=0):
    obj = try_parse(obj)

    prefix = "    " * indent

    if isinstance(obj, dict):
        for key, value in obj.items():

            value = try_parse(value)

            if isinstance(value, dict):
                file.write(f"{prefix}{key}\n")
                file.write(f"{prefix}{'-' * len(key)}\n")
                write_section(file, value, indent + 1)
                file.write("\n")

            elif isinstance(value, list):
                file.write(f"{prefix}{key}:\n")

                for item in value:

                    item = try_parse(item)

                    if isinstance(item, (dict, list)):
                        write_section(file, item, indent + 1)
                    else:
                        file.write(f"{prefix}  • {item}\n")

                file.write("\n")

            else:
                file.write(f"{prefix}{key}: {value}\n")

    elif isinstance(obj, list):

        for item in obj:

            item = try_parse(item)

            if isinstance(item, dict):
                file.write("----------------------------------------\n")
                write_section(file, item, indent + 1)
            else:
                file.write(f"{prefix}- {item}\n")

    else:
        file.write(f"{prefix}{obj}\n")


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        out.write("=" * 80 + "\n")
        out.write("MOONDREAM CYBERSECURITY REPORT\n")
        out.write("=" * 80 + "\n\n")

        for section, content in data.items():

            out.write("\n")
            out.write("=" * 80 + "\n")
            out.write(section.replace("_", " ").upper() + "\n")
            out.write("=" * 80 + "\n\n")

            answer = content.get("answer", "")

            write_section(out, answer)

            out.write("\n")

    print(f"[+] Human-readable report saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

subprocess.run(
    [
        sys.executable,
        "-m",
        "ai.phi3_json"
    ],
    check=True
)