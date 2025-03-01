from config import logger
import os
from tqdm import tqdm
from ffmpeg import FFmpeg
#pip install python-ffmpeg
 
def wav_to_441000_pcm_s16le(fpath: str, output_dir: str):
    fpath = os.path.abspath(fpath)
    if not os.path.isfile(fpath):
        print(f'file does not exist: {fpath}')
        return None
    fout = os.path.join(output_dir, os.path.basename(fpath))
    logger.debug(f'fout: {fout}')
    os.makedirs(os.path.dirname(fout), exist_ok=True)
    ffmpeg = (FFmpeg()
        .option("y")
        .input(fpath)
        .output(
            fout, 
            ar=44100, 
            ac=1, 
            acodec="pcm_s16le",
            )
        )

    ffmpeg.execute()

def wav_normalize(mp3_dir: str = "", output_dir: str = ""):
    for root, dirs, files in os.walk(mp3_dir, True):
        for file in tqdm(files):
            if file[-4:].lower() != ".wav":
                #print(file)
                continue
            fpath = os.path.join(root, file)
            #print(f'{fpath}')
            wav_to_441000_pcm_s16le(fpath, output_dir)

#print(config.DIR_ROOT)

#melotts_wav_normalize(mp3_dir=f"{config.DIR_ROOT}/02_slice", output_dir=f"{config.DIR_ROOT}/_wav")


#ar=44100, ac=1, acodec='pcm_s16le'