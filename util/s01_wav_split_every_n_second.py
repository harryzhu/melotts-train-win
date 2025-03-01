#import config
from config import logger
import os
import math
import shutil
from tqdm import tqdm
from pydub import AudioSegment
	
def mp3_split_every_n_second(fpath="", export_dir="", n_duration=10.0, min_skip = 5.0):
	sound = AudioSegment.from_file(fpath)
	sound_time = math.floor(sound.duration_seconds)
	#print(f'sound duration: {sound_time}')
	if not os.path.isdir(export_dir):
		os.makedirs(export_dir, exist_ok = True)

	if sound_time < min_skip:
		return None
	if sound_time >= min_skip and sound_time <= n_duration:
		shutil.copyfile(fpath, os.path.join(export_dir,os.path.basename(fpath)))
		return None

	n_count = math.floor(sound_time / n_duration)
	logger.debug(f'n_count: {n_count}')

	n_duration_ms = n_duration * 1000

	try:
		for i in range(n_count):
			out_sound = sound[i*n_duration_ms: i*n_duration_ms+n_duration_ms]
			out_fname = os.path.join(export_dir,os.path.basename(fpath).replace(".wav",f'_{i}.wav'))
			if out_sound.duration_seconds >= min_skip:
				out_sound.export(out_fname,format='wav')
				logger.debug(f'n_fname: {out_fname}')
			else:
				logger.debug(f'SKIP: {out_sound.duration_seconds}')
	except Exception as err:
		logger.error("ERROR:{0}".format(err))
		return None	

def mp3_dir_split_nsec(mp3_dir="", output_dir=""):
	for root,dirs,files in os.walk(mp3_dir,True):
		for file in tqdm(files):
			if file[-4:].lower() != ".wav":
				continue
			fpath = os.path.abspath(os.path.join(root,file))
			mp3_split_every_n_second(fpath, output_dir)
	
			

