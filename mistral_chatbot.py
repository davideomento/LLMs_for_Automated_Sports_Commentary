import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch
from shutil import copytree

# Monta Google Drive (esegui solo se non montato)
# from google.colab import drive
# drive.mount('/content/drive')

# Directory dove vuoi salvare il modello su Drive
drive_model_path = "/content/drive/MyDrive/mistral_model"

# Nome del modello Hugging Face
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

# Log in a Hugging Face (usa la tua variabile d'ambiente o inserisci direttamente)
hf_token = "YOUR_HUGGING_FACE_TOKEN"  # Replace with your actual token

login(hf_token)

# Controlla se modello già scaricato su Drive
if os.path.exists(drive_model_path):
    print(f"Modello già presente in {drive_model_path}, lo carico da lì.")
    tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
    model = AutoModelForCausalLM.from_pretrained(drive_model_path, device_map="auto")
else:
    print("Modello non trovato su Drive, scarico da Hugging Face...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", use_auth_token=hf_token)
    
    print("Salvo il modello su Drive per usi futuri...")
    # Salva tokenizer e modello sul Drive
    tokenizer.save_pretrained(drive_model_path)
    model.save_pretrained(drive_model_path)

# Usa il modello per fare inferenza
prompt = "Hi! What is the capital of France?"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)
