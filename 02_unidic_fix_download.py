import os
import site
import shutil

site_packages_path = site.getsitepackages()
unidic_download_py = "3rd/unidic/download.py"
unidic_zip = "3rd/unidic/unidic.zip"
unidic_download_py_replace = f'{site_packages_path[0]}/unidic/download.py'
unidic_zip_replace = f'{site_packages_path[0]}/unidic/unidic_zip'
unidic_dicdir = "3rd/unidic/dicdir"

if not os.path.isfile(unidic_download_py_replace):
 	print(f'please run "pip install unidic" first, file does not exist: {unidic_download_py_replace}')
else:
	if os.path.isfile(unidic_download_py):
		print(f'target: {unidic_download_py_replace}')
		shutil.copyfile(unidic_download_py,unidic_download_py_replace)

	if os.path.isfile(unidic_zip) and not os.path.isdir(unidic_dicdir):
		shutil.copyfile(unidic_zip,unidic_zip_replace)
	else:
		print(f'download unidic.zip and put it: "{unidic_zip}", then re-run this script.')


	if os.path.isfile(unidic_zip_replace):
		os.system('python -m unidic download')