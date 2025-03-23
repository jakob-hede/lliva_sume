import yt_dlp
from pathlib import Path


def download_best_pristine(url: str, target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': str(target_dir / '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'restrictfilenames': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    # url = 'https://www.dailymotion.com/video/x8md1k0'  # specify URL here
    # target_dir = Path('/opt/projects/liva_sume/media/2.Inuit_Nunaat_Rock.1974/down')  # specify target directory here

    url = 'https://www.dailymotion.com/video/x8mhnx7'
    target_dir = Path('/opt/projects/liva_sume/media/3.Sume_3/down')

    download_best_pristine(url, target_dir)


if __name__ == "__main__":
    main()
