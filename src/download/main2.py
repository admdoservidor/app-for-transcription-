import os
import yt_dlp
from faster_whisper import WhisperModel

def transcrever_link_instagram(url):
    arquivo_audio = "audio_temp.mp3"
    
    # 1. Baixar apenas o áudio via yt-dlp
    opcoes_download = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio_temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    print("Baixando áudio do Instagram...")
    with yt_dlp.YoutubeDL(opcoes_download) as ydl:
        ydl.download([url])

    # 2. Carregar o modelo otimizado para CPU (int8)
    print("Transcrevendo áudio com Faster-Whisper...")
    modelo = WhisperModel("small", device="cpu", compute_type="int8")
    
    # O beam_size=5 melhora a precisão da transcrição
    segmentos, info = modelo.transcribe(arquivo_audio, language="pt", beam_size=5)

    # Junta todos os trechos transcritos em um texto completo
    texto_completo = "".join([segmento.text for segmento in segmentos])

    # 3. Remover o arquivo temporário
    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)

    return texto_completo.strip()

# Exemplo de uso
link_video = "https://www.instagram.com/reel/Dfr5zZCKopm/?utm_source=ig_web_copy_link&cplk=NTc4MTIwNjQ2YQ=="
texto_final = transcrever_link_instagram(link_video)

print("\n--- TRANSCRIÇÃO ---")
print(texto_final)
