from youtube_transcript_api import YouTubeTranscriptApi
import json
import math
import re 
import os


# Function to create a safe filename by removing/replacing invalid characters
def safe_filename(s):
    return re.sub(r'[^\w\-]', '_', s)

video_id = "uSAbUjzFqMg"

# Define match metadata
match_name = "Atletico Madrid vs Real Madrid"
match_date = "2025-03-12"
competition_stage = "Champions League Round of 16"

# Define start and end times in seconds
start_seconds = 16 * 60 + 2  # 24 minutes 45 seconds
end_seconds = (3 * 3600) + (4 * 60) + 2  # 2 hours 17 minutes 36 seconds

# Fetch available transcripts for the video
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

try:
    # Try to get manually created English transcript
    transcript = transcript_list.find_transcript(['en'])
except:
    # If not available, fallback to auto-generated English transcript
    transcript = transcript_list.find_generated_transcript(['en'])

# Fetch the transcript data (list of transcript entries)
transcript_data = transcript.fetch()

commentary_by_minute = {}

# Iterate over each transcript snippet
for entry in transcript_data:
    start_time = entry.start  # start time in seconds

    # Skip entries outside the desired time range
    if start_time < start_seconds or start_time > end_seconds:
        continue

    # Calculate minute relative to video start time
    minute = math.floor((start_time - start_seconds) / 60) + 1

    # Clean subtitle text (remove line breaks)
    text = entry.text.replace('\n', ' ')

    # Group subtitles by minute
    if minute not in commentary_by_minute:
        commentary_by_minute[minute] = []
    commentary_by_minute[minute].append(text)

# Prepare final commentary list combining texts per minute
commentary_list = []

for minute, texts in sorted(commentary_by_minute.items()):
    combined_comment = " ".join(texts)

    # Determine half based on minute number
    half = "1st half" if minute <= 55 else "2nd half"

    commentary_list.append({
        "minute": f"{minute}'",
        "half": half,
        "comment": combined_comment
    })

# Combine metadata and commentary in one dictionary
output = {
    "metadata": {
        "match_name": match_name,
        "match_date": match_date,
        "competition_stage": competition_stage,
        "start_time_seconds": start_seconds,
        "end_time_seconds": end_seconds
    },
    "commentary": commentary_list
}

filename = f"{safe_filename(match_name)}_{match_date}_{safe_filename(competition_stage)}.json"



# Ensure the 'data' folder exists
os.makedirs("data", exist_ok=True)

# Save dataset as JSON file inside the 'data' folder
filepath = os.path.join("data", filename)
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Saved commentary for {len(commentary_list)} minutes ({match_name} on {match_date}, {competition_stage}).")
print(f"File saved as: {filepath}")