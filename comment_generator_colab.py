from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

# Funzione per ritagliare fino all'ultima frase completa
def trim_to_last_complete_sentence(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return " ".join(sentences[:-1]) if len(sentences) > 1 else text

# Percorso del modello sul tuo Drive
drive_model_path = "/content/drive/MyDrive/mistral_model"

# Carica tokenizer e modello
tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
model = AutoModelForCausalLM.from_pretrained(
    drive_model_path,
    device_map="auto",
    torch_dtype=torch.float16
)
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def genera_frase(prompt: str, max_length: int = 200) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=max_length)
    testo_completo = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Rimuove il prompt e prende solo il testo generato
    testo_generato = testo_completo[len(prompt):].strip()
    
    # Applica il trimming solo alla parte generata
    return trim_to_last_complete_sentence(testo_generato)


# Loop interattivo
def main():
    while True:
        prompt = input("Inserisci il prompt (o 'exit' per uscire): ")
        if prompt.lower() == "exit":
            break
        frase = genera_frase(prompt)
        print("\n--- Output ---")
        print(frase)
        print("--------------\n")

if __name__ == "__main__":
    main()
