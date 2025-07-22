from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Percorso modello Mistral salvato su Drive
drive_model_path = "/content/drive/MyDrive/mistral_model"

# Carica tokenizer e modello
tokenizer = AutoTokenizer.from_pretrained(drive_model_path)
model = AutoModelForCausalLM.from_pretrained(drive_model_path, device_map="auto")  # o device_map={"": "cuda"} se singola GPU

model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Usa la tua funzione di prompt
def format_prompt(event, context):
    player = context["name"]
    minute = event["minute"]
    event_type = event["type"].replace("_", " ").capitalize()

    base = f"Minute {minute}': {event_type} involving {player}.\n"
    stats = (
        f"{player} has scored {context['goals']} goals and provided {context['assists']} assists this season. "
        f"He's played {context['minutes_played']} minutes and shows an influence score of {context['influence']}, "
        f"threat of {context['threat']}, and creativity of {context['creativity']}."
    )

    instruction = (
        "\nYou are a football commentator tasked with generating a realistic commentary for a match event. "
        "You are given the player's stats and the event details and you have to tell as a commentator would do these events. "
        "Write an exciting and realistic football commentary based on this event and context. "
        "Mention the minute and player's name clearly."
    )

    return base + stats + instruction

# Input di esempio
event = {"minute": "67", "type": "goal", "player": "Gabriel Jesus"}
context = {
    "name": "Gabriel Jesus",
    "position": "FWD",
    "goals": 3,
    "assists": 2,
    "minutes_played": 600,
    "goals_conceded": 5,
    "clean_sheets": 2,
    "yellow_cards": 4,
    "red_cards": 0,
    "influence": 154.4,
    "threat": 255.0,
    "creativity": 119.5,
    "total_points": 42
}

prompt = format_prompt(event, context)

# Tokenizza il prompt
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Genera output
outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=150,  # attenzione a non esagerare, max tokens modello
    do_sample=True,
    top_p=0.9,
    temperature=0.8,
    pad_token_id=tokenizer.eos_token_id,
    no_repeat_ngram_size=2,
)

# Decodifica e stampa
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
