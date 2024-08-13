import glob
import os
import time
start_time = time.time()



def find_RS_files_recursive(PATH):
	# rs_files = glob.glob()
	# list_all_files = []
	rs_files = []

	for root, dirs, files in os.walk(PATH):
		# list_all_files.append()
		# print(root,len(files))
		# print(os.path.join(root, file))

		for file in [f for f in files if f[0:2]=='RS']:
			rs_files.append(os.path.join(root, file))
		#     print(os.path.join(root, file))

	# rs_files = glob.glob(os.path.join(PATH, '**', 'RS*'), recursive=True)
	# for file in rs_files:
	# 	print(file)
	return rs_files

rs_files = find_RS_files_recursive('/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/')
print(rs_files)
print("*********", time.time() - start_time,  "*********")