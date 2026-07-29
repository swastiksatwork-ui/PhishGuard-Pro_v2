import os
import json
from pathlib import Path
from PIL import Image
from ai.moondream_core import model

BASE_DIR = Path(__file__).resolve().parent

PROMPTS_DIR = BASE_DIR / "prompts"

def load_prompt(prompts_file):

    prompt_path = PROMPTS_DIR / prompts_file

    with open(
        prompt_path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()
    


def analyze_image(

    image_path,

    prompts_file,

    output_json,

    resize_x=1,

    resize_y=1

):

    image = Image.open(image_path).convert("RGB")

    w, h = image.size

    if resize_x != 1 or resize_y != 1:

        image = image.resize(

            (

                int(w * resize_x),

                int(h * resize_y)

            ),

            Image.LANCZOS

        )

    prompt = load_prompt(prompts_file)

    answer = model.query(

        image=image,

        question=prompt

    )

    Path(output_json).parent.mkdir(

        parents=True,

        exist_ok=True

    )


    with open(

        output_json,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            answer,

            f,

            indent=4

        )

    return answer
    

def merge_moondream_jsons():

    folder = "storage/moondream"

    merged = {}

    for file in os.listdir(folder):

        if not file.endswith(".json"):
            continue

        file_path = os.path.join(folder, file)

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            merged[
                os.path.splitext(file)[0]
            ] = json.load(f)

    with open(

        "storage/moondream_dump.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            merged,

            f,

            indent=4

        )

    print(
        "Moondream dump created successfully."
    )


if __name__ == "__main__":

    result = analyze_image(

    image_path="storage/screenshots/cloudflare/cloudflare_summary.png",

    prompts_file="cloudflare_summary_links.txt",

    output_json="storage/moondream/cloudflare_1_summary.json",

    resize_x=3,

    resize_y=2

)
    
    print(result)


if __name__ == "__main__":

    result = analyze_image(

    image_path="storage/screenshots/cloudflare/cloudflare_security.png",

    prompts_file="cloudflare_security.txt",

    output_json="storage/moondream/cloudflare_2_security.json",

    resize_x=3,

    resize_y=2

)
    
    print(result)

if __name__ == "__main__":

    result = analyze_image(

    image_path="storage/screenshots/cloudflare/cloudflare_indicators.png",

    prompts_file="cloudflare_indicators.txt",

    output_json="storage/moondream/cloudflare_3_indicators.json",

)
    
    print(result)


if __name__ == "__main__":

    result = analyze_image(

    image_path="storage/screenshots/cloudflare/cloudflare_links.png",

    prompts_file="cloudflare_summary_links.txt",

    output_json="storage/moondream/cloudflare_4_links.json",

)
    
    print(result)


if __name__ == "__main__":

    result = analyze_image(

    image_path="storage/screenshots/cloudflare/cloudflare_behavior.png",

    prompts_file="cloudflare_behavior.txt",

    output_json="storage/moondream/cloudflare_5_behavior.json",

    resize_x=3,

    resize_y=2

)

    print(result)


if __name__ == "__main__":

    result = analyze_image(

    image_path="storage/screenshots/cloudflare/cloudflare_network.png",

    prompts_file="cloudflare_network.txt",

    output_json="storage/moondream/cloudflare_6_network.json",

    resize_x=3,

    resize_y=2

)
    
    print(result)


def merge_moondream():

    folder = "storage/moondream"

    merged = {}

    for file in os.listdir(folder):

        if file.endswith(".json"):

            with open(

                os.path.join(folder, file),

                "r",

                encoding="utf-8"

            ) as f:

                merged[file.replace(".json", "")] = json.load(f)

    with open(

        "storage/moondream_dump.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            merged,

            f,

            indent=4

        )

    print("Moondream dump created!")

merge_moondream()

print(".Jsons merged")