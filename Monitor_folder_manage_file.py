import os
import time
import schedule
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
import pandas as pd
import shutil
import re
from xls2xlsx import XLS2XLSX

# define the path you want to monitor and the destination path if you want to move the upcoming files
path_to_watch='C:/Users/..'
path_to_dest='C:/Users/dest_eg..'

# we will deal with two cases:
# 1. the name pattern of the upcoming file is fixed and you simply need to move it
# 2. the name of the upcoming file is also fixed, but you need to transform it before move it to the destination. 
#    Here are two example cases: convert csv and xls to xlsx format.


name_patterns = {r'^file_\d{8}.*.xlsx$':'new_name.xlsx',
                'pattern_2':'new_name2'
                }
special_case = [r'^file.*.csv$',
                r'^file.*.xls$'
               ]

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        src_file=event.src_path
        dest_folder=path_to_dest
        original_file_name=os.path.basename(src_file)

        if re.match(special_case[0], original_file_name):
            new_file_name = 'new_file_name_1.xlsx'
            df = pd.read_csv(src_file, sep='|')
            df.to_excel(os.path.join(path_to_watch, new_file_name), sheet_name='New_sheet', index=None, header=True)
            shutil.move(os.path.join(path_to_watch, new_file_name), os.path.join(path_to_dest, new_file_name))

        elif re.match(special_case[1], original_file_name):
            original_xls = XLS2XLSX(src_file)
            new_xlsx_name = 'new_file_name_2.xlsx'
            new_xlsx_path = os.path.join(path_to_watch, new_xlsx_name)
            new_xlsx = original_xls.to_xlsx(new_xlsx_path)
            shutil.move(new_xlsx_path, os.join.path(path_to_dest, new_xlsx_name))
            

        for pattern, new_name in name_patterns:
            if re.match(pattern, original_file_name):
                new_file_name=new_name
                shutil.move(src_file, os.path.join(dest_folder, new_file_name))
                
# the following code makes sure that if some files are already added before we run the code, we simulate all these files as just created/ added
    
    def process_existing_files(self, path_to_watch):
        for filename in os.listdir(path_to_watch):
            file_path = os.path.join(path_to_watch, filename)
            if os.path.isfile(file_path):
                event = FileCreatedEvent(file_path)
                self.on_created(event)


def run_observer(path_to_watch):
    event_handler = MyHandler()
    event_handler.process_existing_files(path_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

run_observer(path_to_watch)


#--------------------------------------------------------------------#

# If you don't want to monitor the folder all the time, you can alternatively, monitor the file every, say, 15 minutes using the following code snippet. 
# At the same time, please also comment out the above code from try till run_observer(path_to_watch)


#------------------- Monitor with time interval ---------------------#

#schedule.every(15).minutes.do(run_observer, path_to_watch)
#try:
#    while True:
#        time.sleep(1)
#except KeyboardInterrupt:
#    pass