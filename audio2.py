import whisper

# Caminho do arquivo de áudio
audio_path = r"C:\\Users\\Carlos\\OneDrive\\Voz 041.m4a"
wav_path = r"C:\\Users\\Carlos\\OneDrive\\Voz_041.wav"

model = whisper.load_model("base")
result = model.transcribe(audio_path)
# print(result["text"])
with open(r"C:\\Users\\Carlos\\OneDrive\\transcricao.txt", "w", encoding="utf-8") as f:
    f.write(result)
