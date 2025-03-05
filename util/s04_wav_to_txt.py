# encoding: utf-8
from config import logger
import os
import whisper
from whisper.utils import get_writer
import zhconv
#from tqdm import tqdm


device = "cuda:0"
model_large_v3 = whisper.load_model("D:/svc/whisper/v3/_models/large-v3/large-v3.pt").to(device)
#model_large_v3 = whisper.load_model("D:/svc/whisper/v3/_models/large-v3-turbo/large-v3-turbo.pt").to(device)


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

            dsrt = os.path.join(output_dir.replace("_txt", "srt"))
            if not os.path.exists(dsrt):
                os.makedirs(dsrt)

            try:
                result = model_large_v3.transcribe(fpath, language='zh', fp16="False")
                srt_writer = get_writer("srt", dsrt) 
                txt_writer = get_writer("txt", dsrt)  
                srt_writer(result, fpath,{"max_line_width":150, "max_line_count":1, "highlight_words":False})
                txt_writer(result, fpath,{"max_line_width":150, "max_line_count":1, "highlight_words":False})

                if min_words > 0:
                    if len(result["text"]) < min_words:
                        logger.debug(f'SKIP: too short({len(result["text"])} < {min_words}): result["text"]')
                        continue
                if max_words > 0:
                    if len(result["text"]) > max_words:
                        logger.debug(f'SKIP: too long({len(result["text"])} > {max_words}): ')
                        continue      
                
                text_sep = ""
                for segment in result["segments"]:
                    text_sep = "，".join([text_sep, segment["text"].strip()])

                text_sep = text_sep.strip("，")
                text_sep = text_sep.replace(",","，")

                text_sep = zhconv.convert(text_sep, 'zh-cn')
                logger.info(f'result: {len(result["text"])}: {text_sep}')
                with open(txt_file,'w', encoding="utf-8") as f:
                    f.write(text_sep)
            except Exception as err:
                logger.error(f'ERROR:{0}'.format(err))
                continue
