from config import logger
import os
from tqdm import tqdm
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil
	
def mp3_split_on_silence(fpath="", export_dir="", export_chunk_len=3000):
	#print(f'processing: {fpath}')
	sound = AudioSegment.from_file(fpath)
	chunks = split_on_silence(sound, 
		silence_thresh = sound.dBFS - 16,
		min_silence_len=500, 
		keep_silence=500)
	if not os.path.isdir(export_dir):
		os.makedirs(export_dir)

	if len(chunks) < 1:		
		shutil.copyfile(fpath,os.path.join(export_dir, os.path.basename(fpath)))
		logger.debug(f'copy file: {fpath}')
		return None
	else:
		pass
		#print(f'chunks: {len(chunks)}')

	output_chunks = [chunks[0]]
	for chunk in chunks[1:]:
		if len(output_chunks[-1]) < export_chunk_len:
			output_chunks[-1] += chunk
		else:
			output_chunks.append(chunk)			

	#print(f'output_chunks: {len(chunks)}')
	for i, audio_chunk in enumerate(output_chunks, start=1):
		bname = os.path.basename(fpath).replace(".wav","")
		chunk_fname = os.path.join(export_dir, f"{bname}_{i}.wav")
		audio_chunk.export(chunk_fname, format="wav")
		logger.debug(f'export name: {chunk_fname}')

def mp3_clean_short(output_dir="", min_sec = 5.0):
	print(f'cleaning the short audio: < {min_sec} seconds')
	for root,dirs,files in os.walk(output_dir,True):
		for file in tqdm(files):
			if file[-4:].lower() != ".wav":
				continue
			fpath = os.path.abspath(os.path.join(root,file))
			sound = AudioSegment.from_file(fpath)
			if sound.duration_seconds < min_sec:
				os.remove(fpath)
				#print(f'{fpath}: {sound.duration_seconds}')

def mp3_dir_split_on_silence(mp3_dir="", output_dir=""):
	for root,dirs,files in os.walk(mp3_dir,True):
		for file in tqdm(files):
			if file[-4:].lower() != ".wav":
				continue
			fpath = os.path.abspath(os.path.join(root,file))
			mp3_split_on_silence(fpath,output_dir)
	# clean
	mp3_clean_short(output_dir)
			




