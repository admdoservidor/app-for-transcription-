import os
import yt_dlp
import whisper

def transcrever_link_instagram(url):
    arquivo_audio = "audio_temp.mp3"
    
    # 1. Configurações para baixar apenas o áudio via yt-dlp
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

    # 2. Carregar o modelo Whisper e transcrever
    print("Transcrevendo áudio...")
    modelo = whisper.load_model("small")
    resultado = modelo.transcribe(arquivo_audio, language="pt", fp16=False)

    # 3. Remover o arquivo temporário
    if os.path.exists(arquivo_audio):
        os.remove(arquivo_audio)

    return resultado["text"]

# Exemplo de uso
link_video = "https://www.instagram.com/reel/Dfr5zZCKopm/?utm_source=ig_web_copy_link&cplk=NTc4MTIwNjQ2YQ=="
texto_final = transcrever_link_instagram(link_video)

print("\n--- TRANSCRIÇÃO ---")
print(texto_final)

