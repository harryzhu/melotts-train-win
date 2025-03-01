# encoding: utf-8
from config import logger
import os
import math
from tqdm import tqdm	


def melotts_gen_train_metalist(mp3_dir="", txt_dir="", voice_name="zh_harry", language_code="ZH", meta_path=""):
	with open(meta_path,"w", encoding="utf-8") as fmeta:
		for root,dirs,files in os.walk(mp3_dir,True):
			for file in tqdm(files):
				if file[-4:].lower() != ".wav":
					continue
				fwav = os.path.abspath(os.path.join(root,file))
				ftxt = os.path.abspath(os.path.join(txt_dir,os.path.basename(file).replace(".wav",".txt")))
				if not os.path.isfile(ftxt):
					logger.debug("SKIP(not exist):", ftxt)
					os.rename(fwav,fwav.replace("_wav","_bak"))
					continue
				logger.debug(f'{fwav} => {ftxt}')
				txt_content = ""
				with open(ftxt,'r', encoding="utf-8") as f1:
					txt_content = f1.read()
				txt_content = txt_content.replace("\n","").replace("\r","")
				fwav_unix = fwav.replace("\\","/")
				line = f'{fwav_unix}|{voice_name}|{language_code}|{txt_content}\n'
				logger.debug(line)
				fmeta.write(line)
	logger.debug(f'\npython preprocess_text.py --metadata {meta_path}')
				

			
#melotts_gen_train_metalist(mp3_dir=f"{config.DIR_ROOT}/_wav", txt_dir=f"{config.DIR_ROOT}/_txt", meta_path = f"{config.DIR_ROOT}/metadata.list")


