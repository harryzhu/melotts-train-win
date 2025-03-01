# encoding: utf-8
import os
import argparse
import util
from util.s00_wav_rename_batch import wav_rename_with_index_in_place
from util.s01_wav_split_every_n_second import mp3_dir_split_nsec
from util.s02_wav_split_on_silence import mp3_dir_split_on_silence
from util.s03_wav_normalize import wav_normalize

from util.s05_rm_wav_without_pair_txt import rm_wav_without_pair_txt
from util.s06_melotts_gen_train_metalist import melotts_gen_train_metalist
from util.s08_rm_wav_without_pair_bert_pt import melotts_rm_wav_without_pair_bert_pt
from util.s09_copy_wav_to_data import melotts_copy_wav_to_data

DATASET_DIR_ROOT="D:/dataset/_test"


#
TRAIN_DATA_DIR='D:/svc/_train/MeloTTS/melo/data'
TRAIN_DATA_WAV_DIR=f'{TRAIN_DATA_DIR}/_wav'
TRAIN_DATA_TXT_DIR=f'{TRAIN_DATA_DIR}/_txt'
TRAIN_DATA_CFG_DIR=f'{TRAIN_DATA_DIR}/harry'

#
parser = argparse.ArgumentParser()
parser.add_argument('--step', type=int, help='run step: 0,1,2,3,4,5,6')
parser.add_argument('--debug', type=bool, help='if show debug messages')
args = parser.parse_args()

util.config.withDebug(args.debug)

print(f'run step: {args.step} IN: {DATASET_DIR_ROOT}')


# step 0
if args.step == 0:
    print(f'rename source wav files:')
    wav_rename_with_index_in_place(wav_dir=f"{DATASET_DIR_ROOT}/source")


# step 1
if args.step == 1:
    print(f'split wav file into n-seconds segments:')
    mp3_dir_split_nsec(mp3_dir=f"{DATASET_DIR_ROOT}/source", output_dir=f"{DATASET_DIR_ROOT}/01_nsec")

# step 2
if args.step == 2:
    print(f'split wav file on silent:')
    mp3_dir_split_on_silence(mp3_dir=f"{DATASET_DIR_ROOT}/01_nsec", output_dir=f"{DATASET_DIR_ROOT}/02_slice")

# step 3
if args.step == 3:
    print(f'normalize wav files:')
    wav_normalize(mp3_dir=f"{DATASET_DIR_ROOT}/02_slice", output_dir=f"{DATASET_DIR_ROOT}/_wav")

# step 4
if args.step == 4:
    print(f'run this step with whisper conda env')
    from util.s04_wav_to_txt import wav_dir_transcribe
    wav_dir_transcribe(f"{DATASET_DIR_ROOT}/_wav", f"{DATASET_DIR_ROOT}/_txt", min_words = 10, max_words = 150)

# step 5
if args.step == 5:
    print(f'delete wav files which cannot be transribled by whisper')
    rm_wav_without_pair_txt(mp3_dir=f"{DATASET_DIR_ROOT}/_wav")

# step 6
if args.step == 6:
    print(f'generate metadata.list: {DATASET_DIR_ROOT}/metadata.list')
    melotts_gen_train_metalist(mp3_dir=f"{DATASET_DIR_ROOT}/_wav", 
        txt_dir=f"{DATASET_DIR_ROOT}/_txt", 
        voice_name="harry", 
        language_code="ZH",
        meta_path = f"{DATASET_DIR_ROOT}/metadata.list")

# step 7
if args.step == 7:
    print(f'conda activate your melotts env, then cd melo dir, then run:')
    print(f'python ./preprocess_text.py --metadata {DATASET_DIR_ROOT}/metadata.list, it will generate the .bert.pt')

# step 8
if args.step == 8:
    print(f'delete wav files which cannot generate .bert.pt by preprocess_text.py')    
    melotts_rm_wav_without_pair_bert_pt(mp3_dir=f"{DATASET_DIR_ROOT}/_wav")

# step 9
if args.step == 9:
    print(f'copy valid wav files into train data_dir:') 
    os.makedirs(TRAIN_DATA_WAV_DIR,exist_ok=True)
    os.makedirs(TRAIN_DATA_TXT_DIR,exist_ok=True)
    os.makedirs(TRAIN_DATA_CFG_DIR,exist_ok=True)       
    melotts_copy_wav_to_data(mp3_dir=f"{DATASET_DIR_ROOT}/_wav", 
        wav_dir=TRAIN_DATA_WAV_DIR, 
        txt_dir=TRAIN_DATA_TXT_DIR)

# step 10
if args.step == 10:
    print(f'same as step 6, but re-generate the metadata.list without invalid *.wav files(which cannot generate .bert.pt)')
    melotts_gen_train_metalist(mp3_dir=f"{TRAIN_DATA_WAV_DIR}", 
        txt_dir=f"{TRAIN_DATA_TXT_DIR}", 
        voice_name="harry", 
        language_code="ZH",
        meta_path = f"{TRAIN_DATA_CFG_DIR}/metadata.list")
    print(f're-generate metadata.list: ')
    print(f'python ./preprocess_text.py --metadata {TRAIN_DATA_CFG_DIR}/metadata.list')
    print(f'then train: ')
    print(f'python ./train.py --config {TRAIN_DATA_CFG_DIR}/config.json --model harry')
