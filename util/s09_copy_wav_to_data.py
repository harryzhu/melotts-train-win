# encoding: utf-8
from config import logger
import os
import math
from tqdm import tqdm
import shutil
				
def melotts_copy_wav_to_data(mp3_dir="", wav_dir="" , txt_dir=""):
	for root,dirs,files in os.walk(mp3_dir,True):
		for file in tqdm(files):
			if file[-4:].lower() != ".wav":
				continue
			fwav = os.path.join(root,file)
			fbert = fwav.replace(".wav",".bert.pt")
			ftxt = fwav.replace("_wav","_txt").replace(".wav",".txt")
			#
			fwav_dst = os.path.join(wav_dir,file)
			ftxt_dst = os.path.join(txt_dir,file.replace(".wav",".txt"))
			logger.debug(f'{fwav}: {fbert}: {ftxt} ==> {fwav_dst}: {ftxt_dst}')
			if os.path.isfile(fbert) and os.path.isfile(ftxt) and os.path.isfile(fwav):
				shutil.copyfile(fwav, fwav_dst)
				shutil.copyfile(ftxt, ftxt_dst)



