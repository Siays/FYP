import torch
import transformers
from transformers import LlamaForCausalLM, LlamaTokenizer

# Ensure we're using a CUDA-capable GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_dir = "./llama/llama-2-7b-chat-hf"
model = LlamaForCausalLM.from_pretrained(model_dir).to(device)

tokenizer = LlamaTokenizer.from_pretrained(model_dir)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",  # Use device_map instead of device
)

sequences = pipeline(
    "I have tomatoes, basil and cheese at home. What can I cook for dinner?\n",
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=400,
    truncation=True,  # Explicitly activate truncation
    pad_token_id=tokenizer.eos_token_id,  # Set pad_token_id to eos_token_id
)

for seq in sequences:
    print(f"{seq['generated_text']}")
