import csv
import sys
import shutil


filename = sys.argv[1]
source_folder = sys.argv[2]
destination_folder = sys.argv[3]

# python copy_attachments.py /home/juliank/temp/data_test.csv /home/juliank/work/sites/site1/attachments/source_attachment/ /home/juliank/work/sites/site1/attachments/dest_attachment

try:
    print 'attempting to read csv'
    mycsv = csv.reader(open(filename))
    print 'successfully read csv'
    for row in mycsv:
		# print row[0]
		source_dest = row[0].split(";")
		source_id = source_dest[0]
		destination_id = source_dest[1]
		print source_id
		print destination_id
		# break
		if "NULL" in source_id:
			print 'skipping copy since source_id is null'
			continue
		elif "NULL" in destination_id:
			print 'skipping copy since source_id is null'
			continue
		else:
			source_folder_with_id = source_folder + source_id
			destination_folder_with_id = destination_folder + destination_id
			print source_folder_with_id
			print destination_folder_with_id
			for files in source_folder_with_id:
				print 'attempting to copy files'
                shutil.copy(files,destination_folder_with_id)
                print 'file copy successful'
		   
    print 'copy is complete'
except Exception, e:
	print "Could not read or copy files \n", e
