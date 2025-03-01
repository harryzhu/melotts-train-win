# Environment
* Windows 11
* python 3.10 (conda)
* pytorch 2.4.1 + cuda12.1
* whisper

# Install
1. using conda, create a python 3.10 venv: `conda create -n winmelotts python=3.10`
2. activate winmelotts: `conda activate winmelotts	`
3. clone this repo:

```
git clone https://github.com/harryzhu/melotts-train-win.git
cd melotts-train-win
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
python ./02_unidic_fix_download.py
python ./03_nltk_data_fix.py
cd MeloTTS
pip install .
```

4. prepare your dataset, i.e.: put your wav files in: `D:/dataset/_test/source`
5. open `melotts-train-win/melosteps.py`, update the following vars as yours:

```
DATASET_DIR_ROOT='D:/dataset/_test'
#
TRAIN_DATA_DIR='D:/svc/_train/MeloTTS/melo/data'
TRAIN_DATA_WAV_DIR=f'{TRAIN_DATA_DIR}/_wav'
TRAIN_DATA_TXT_DIR=f'{TRAIN_DATA_DIR}/_txt'
TRAIN_DATA_CFG_DIR=f'{TRAIN_DATA_DIR}/harry'
```

5. run the following steps:

```
# step 0: rename the files, format: foldername_num.wav
python melosteps.py --step=0

# step 1: split long wav file into 10-second segments
python melosteps.py --step=1

#  step 2: split the silence of the 10-second wav file
python melosteps.py --step=2

# step 3: normalize the wav files: 44.1k, pcm_s16le, 1
python melosteps.py --step=3

# step 4: go to your whisper env, run this step only, wav to txt
python melosteps.py --step=4

# step 5: delete wav files which cannot be transribled by whisper
python melosteps.py --step=5

# step 6: generate metadata.list
python melosteps.py --step=6

# step 7: generate *.bert.pt
# python preprocess_text.py --metadata D:/dataset/_test/metadata.list 
python melosteps.py --step=7

# step 8: delete wav files which cannot generate .bert.pt by preprocess_text.py
python melosteps.py --step=8

# step 9: copy valid wav files into train data_dir: melotts-train-win/MeloTTS/melo/data/[_wav, _txt]
python melosteps.py --step=9

# step 10: re-generate metadata.list, start train, results will be in melotts-train-win/MeloTTS/melo/logs
# python preprocess_text.py --metadata data/harry/metadata.list 
python melosteps.py --step=10
```
Notice: step 7 and step 10, preprocess the wav and txt files, but in different folder:

```
python preprocess_text.py --metadata D:/dataset/_test/metadata.list 
```

6. train:

```
python ./train.py --config D:/svc/_train/MeloTTS/melo/data/harry/config.json --model harry
```

6. use your trained model:
```
python infer.py --text "你好，世界" -m melotts-train-win/MeloTTS/melo/logs/G_<iter>.pth -o <output_dir>
```