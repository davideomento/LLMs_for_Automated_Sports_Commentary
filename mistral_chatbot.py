import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
from shutil import copytree
from transformers.utils import cached_file



# Directory dove vuoi salvare il modello su Drive
drive_model_path = "/content/drive/MyDrive/mistral_model"

# Nome del modello Hugging Face
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

# Inserisci il tuo token
hf_token = "hf_..."  # Inserisci il tuo token HF qui
login(hf_token)

# Se il modello è già presente su Drive, lo carico da lì
if os.path.exists(drive_model_path):
    print(f"✅ Modello già presente in {drive_model_path}, lo carico da lì.")
    tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
    model = AutoModelForCausalLM.from_pretrained(drive_model_path, device_map="auto")
else:
    print("⬇️ Modello non trovato su Drive, scarico da Hugging Face...")

    # Scarica tokenizer e modello
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", token=hf_token)

    # Trova percorso locale della cache HF
    print("📁 Copio i file dalla cache locale al Drive...")
    cache_path = os.path.dirname(
        cached_file(model_name, "model.safetensors.index.json", token=hf_token)
    )
    
    # Copia il contenuto su Drive
    copytree(cache_path, drive_model_path, dirs_exist_ok=True)
    tokenizer.save_pretrained(drive_model_path)

# Inferenzia un prompt
prompt = "Hi! What is the capital of France?"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("🧠 Risposta:", response)
