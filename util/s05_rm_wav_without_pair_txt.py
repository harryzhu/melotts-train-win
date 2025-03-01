# encoding: utf-8
from config import logger
import os
import re
import math
from tqdm import tqdm
				
def rm_wav_without_pair_txt(mp3_dir=""):
	os.makedirs(mp3_dir.replace("_wav","_bak"), exist_ok=True)
	for root,dirs,files in os.walk(mp3_dir,True):
		for file in tqdm(files):
			if file[-4:].lower() != ".wav":
				continue
			fwav = os.path.join(root,file)
			ftxt = fwav.replace("_wav","_txt").replace(".wav",".txt")
			if os.path.isfile(ftxt):
				with open(ftxt, 'r', encoding='utf-8') as f:
					fcnt = f.read()
					f.close()
					if is_having_chinese(fcnt) != True:
						os.rename(ftxt,ftxt.replace("_txt","_bak"))

			if not os.path.isfile(ftxt):
				logger.debug("SKIP(not exist):", ftxt)
				os.rename(fwav,fwav.replace("_wav","_bak"))
				continue	



def is_having_chinese(words=""):
	for word in words:
		if '\u4e00' <= word <= '\u9fa5':
			return True
	return False


