# encoding: utf-8
from config import logger
import os
import math
import random
from tqdm import tqdm
import shutil
import zhconv

alt_text = {
	"辛基吉": "辛弃疾",
	"星期几": "辛弃疾",
	"辛其吉": "辛弃疾",
	"辛继吉": "辛弃疾",
	"辛继续": "辛弃疾",
	"新七级": "辛弃疾",
	"心积极": "辛弃疾",
	"辛绩吉": "辛弃疾",	
	"《新奇集》": "辛弃疾",
	"新奇籍": "辛弃疾",
	"辛琪琪": "辛弃疾",
	"辛弃习": "辛弃疾",
	"生生慢": "声声慢",
	"赵阔": "赵扩",
	"韩托周": "韩侂胄",
	"韩拓胄": "韩侂胄",
	"苏氏": "苏轼",
	"王国威": "王国维",
	"清光": "清官",
	"灰清二帝": "徽钦二帝",
	"皇帝召善": "皇帝赵昚",
	"人间词画": "人间词话",
	"牵生": "迁升",
	"爱信无鸡吞，废吃乔木，游艳严兵": "百姓无集屯，废池乔木，犹厌言兵",
	"出州": "滁州",
	"健康赏心亭": "建康赏心亭",
	"赵邝胤": "赵匡胤",
	"赵沟": "赵构",
	"邪风细雨": "斜风细雨",
	"平南北望": "凭栏北望",
	"兵不削刃": "兵不血刃",
	"刘玉熙": "刘禹锡",
	"刘雨昕": "刘禹锡",
	"刘雨曦": "刘禹锡",
	"范忠焉": "范仲淹",
	"苏哲": "苏辙",
	"韩玉": "韩愈",
	"李玉": "李煜",
	"白居毅": "白居易",
	"白鞠一": "白居易",
	"柳三面": "柳三变",
	"刘勇": "柳三变",
	"柳三便": "柳三变",
	"刘三便": "柳三变",
	"刘三边": "柳三变",
}

del_text = [
	"独播剧场"
]

				
def melotts_zh_clean(txt_dir=""):
	idx = 0
	alt_keys = alt_text.keys()
	for root,dirs,files in os.walk(txt_dir,True):
		#random.shuffle(files)
		sorted(files, key=lambda x: os.path.basename(x))
		for file in tqdm(files):
			if file[-4:].lower() != ".txt":
				continue
			# if idx > batch:
			# 	break
			fpath = os.path.join(root,file)
			
			with open(fpath, 'r', encoding='utf-8') as fr:
				fcontent = fr.read()
				fr.close()			
			fcontent = zhconv.convert(fcontent, 'zh-cn')
			
			print(f'{file[file.index("_")+1:]}: {fcontent}')
			is_alted = False
			for k in alt_keys:
				if fcontent.find(k) >= 0:
					logger.warning(f'\033[95m=={k}=={file[file.index("_")+1:]}: {fcontent} \033[00m')
					fcontent = fcontent.replace(k, alt_text[k])
					is_alted = True

			if is_alted:
				print(f'\033[92m{fcontent}\033[00m')
			
			with open(fpath, 'w', encoding="utf-8") as falt:
				falt.write(fcontent)
				falt.close()		
		
			for d in del_text:
				if fcontent.find(d) >= 0:
					logger.error(f'\033[91m=={d}=={file[file.index("_")+1:]}: {fcontent} \033[00m')
					os.rename(fpath,fpath.replace("_txt","_bak"))
					

			idx += 1

melotts_zh_clean("D:/dataset/dongxinggoushisan/_txt")
