# encoding: utf-8
from config import logger
import os
import math
from tqdm import tqdm
				
def melotts_rm_wav_without_pair_bert_pt(mp3_dir=""):
	os.makedirs(mp3_dir.replace("_wav","_bak"), exist_ok=True)
	for root,dirs,files in os.walk(mp3_dir,True):
		for file in tqdm(files):
			if file[-4:].lower() != ".wav":
				continue
			fwav = os.path.join(root,file)
			fbert = fwav.replace(".wav",".bert.pt")
			if not os.path.isfile(fbert):
				logger.debug("SKIP(not exist):", fbert)
				os.rename(fwav,fwav.replace("_wav","_bak"))
				continue	


#print(config.DIR_ROOT)

#melotts_rm_wav_without_pair_bert_pt(mp3_dir=f"{config.DIR_ROOT}/_wav")

