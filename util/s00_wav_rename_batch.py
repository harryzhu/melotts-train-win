#import config
from config import logger
import os
from tqdm import tqdm
 
def file_rename(fpath, fnew):
    fpath = os.path.abspath(fpath)
    if not os.path.isfile(fpath):
        logger.debug(f'file does not exist: {fpath}')
        return None
    os.makedirs(os.path.dirname(fnew), exist_ok=True)
    os.rename(fpath, fnew)
    

def wav_rename_with_index_in_place(wav_dir= "", prefix=""):
    wav_dir = wav_dir.replace("\\","/")
    if not os.path.isdir(wav_dir):
        logger.debug(f'wav_dir cannot be empty: {wav_dir}')
        return None
    if prefix == "":
        arr_wav_dir = wav_dir.split("/")
        if arr_wav_dir[-1] == "source":
            prefix = arr_wav_dir[-2]
    if prefix == "" or prefix is None:
        logger.debug(f'prefix cannot be empty')
        return None

    logger.debug(f'wav_dir; {wav_dir}, prefix: {prefix}')
    
    filelist = []
    for root, dirs, files in os.walk(wav_dir, True):        
        for file in files:
            if file[-4:].lower() != ".wav":
                logger.debug(file)
                continue
            fpath = os.path.join(root, file)
            filelist.append(fpath)

    file_total = len(filelist)
    index_width = len(str(file_total))

    i: int = 1
    for fpath in tqdm(filelist):
        newbasename = "".join([prefix,"_",str(i).zfill(index_width),".wav"]).lower()
        fnew = os.path.join(os.path.dirname(fpath), newbasename)
        logger.debug(f'{fnew}')
        file_rename(fpath, fnew)
        i += 1



