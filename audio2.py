import whisper

# Caminho do arquivo de áudio
audio_path = r"C:\\Users\\Carlos\\OneDrive\\Voz 041.m4a"

# Carregar o modelo
model = whisper.load_model("base")  # Você pode testar "small", "medium" ou "large" para mais precisão

# Transcrever o áudio
result = model.transcribe(audio_path)

# Salvar a transcrição em um arquivo
txt_path = r"C:\\Users\\Carlos\\OneDrive\\transcricao.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(result["text"])  # Agora estamos acessando apenas o texto

print(f"Transcrição salva em: {txt_path}")