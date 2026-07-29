from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

MODEL = "vikhyatk/moondream2"

print("Loading Moondream tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL,
    trust_remote_code=True
)

print("Loading Moondream model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    trust_remote_code=True
)

model.eval()

print("Moondream Core Loaded Successfully!")