from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from PIL import Image 

MODEL = "vikhyatk/moondream2"

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL,
    trust_remote_code=True
)

print("Loading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    trust_remote_code=True
)

model.eval()

print("Moondream Loaded!")

PROMPT = """


"""

def analyze_image():

    image = Image.open(
        "storage/screenshots/Virustotal/virustotal_detection.png"
    )

    w, h = image.size

    image = image.resize(
        (w*3, h*2),
        Image.LANCZOS
    )


    answer = model.query(
        image=image,
        question=PROMPT
    )

    return answer


result = analyze_image()

print(result)