import os
import zipfile
import getpass

nltk_data_zip = "3rd/nltk_data/nltk_data.zip"

cur_user = getpass.getuser()
extract_dir = "D:/"
if not os.path.isdir(extract_dir):
	extract_dir = f'C:/Users/{cur_user}'

print(f'will extract "{nltk_data_zip}" into: {extract_dir}')

if not os.path.isfile(nltk_data_zip):
 	print(f'ERROR: please download nltk_data.zip first, and put it: "{nltk_data_zip}"')
else:
	zip = zipfile.ZipFile(nltk_data_zip)
	output = f"{extract_dir}/nltk_data"
	zip.extractall(output)
	zip.close()
		
