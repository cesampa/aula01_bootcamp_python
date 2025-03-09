import whisper
import re

# Caminho do arquivo de áudio
audio_path = r"C:\\Users\\Carlos\\OneDrive\\Voz 041.m4a"

# Carregar o modelo
model = whisper.load_model("base")  # Teste "small", "medium" ou "large" para mais precisão

# Transcrever o áudio, forçando o idioma para português
result = model.transcribe(audio_path, language="pt")

# Ajuste para quebrar frases em linhas separadas
text = result["text"]
formatted_text = re.sub(r'([.!?])\s+', r'\1\n', text)  # Adiciona quebra de linha após pontuação

# Salvar a transcrição formatada em um arquivo
txt_path = r"C:\\Users\\Carlos\\OneDrive\\transcricao.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(formatted_text)

print(f"Transcrição salva em: {txt_path}")
