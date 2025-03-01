# encoding: utf-8
from config import logger
import os
import whisper
#from tqdm import tqdm


device = "cuda:0"
#model_large_v3 = whisper.load_model("D:/svc/whisper/v3/_models/large-v3/large-v3.pt").to(device)
model_large_v3 = whisper.load_model("D:/svc/whisper/v3/_models/large-v3-turbo/large-v3-turbo.pt").to(device)


def wav_dir_transcribe(wav_dir="", output_dir="", min_words = 0, max_words = 0):
    os.makedirs(output_dir, exist_ok=True)
    for root,dirs,files in os.walk(wav_dir,True):
        for file in files:
            if file[-4:].lower() != ".wav":
                continue
            fpath = os.path.abspath(os.path.join(root,file))
            txt_file = os.path.join(output_dir,os.path.basename(fpath).replace(".wav", ".txt"))
            if os.path.isfile(txt_file):
                continue
            try:
                result = model_large_v3.transcribe(fpath,fp16="False")                
                if min_words > 0:
                    if len(result["text"]) < min_words:
                        logger.debug(f'SKIP: too short({len(result["text"])} < {min_words}): result["text"]')
                        continue
                if max_words > 0:
                    if len(result["text"]) > max_words:
                        logger.debug(f'SKIP: too long({len(result["text"])} > {max_words}): ')
                        continue      
                
                logger.info(f'result: {len(result["text"])}: {result["text"]}')
                with open(txt_file,'w', encoding="utf-8") as f:
                    f.write(result["text"])
            except Exception as err:
                logger.error(f'ERROR:{0}'.format(err))
