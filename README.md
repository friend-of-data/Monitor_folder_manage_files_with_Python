# Monitor folder and manage files with Python

Oftentimes, different teams will collaborate in the same folder on cloud. So it is efficient to monitor the folder and take relevant actions automatically.

This code snippet helps realise this funcitonality by mainly using Watchdog module in Python.

The code will automatically monitor a folder ('path_to_watch' in the code) and detects any file creation activity. If some team members add or create a file in the folder, depending on the name or name pattern of the file, operation will be executed automatically. 

Specifically, these files will be moved to the destination folder ('path_to_dest'). If the file format is csv or xls, it will be converted to xlsx fisrt while keeping all formats intact before being moved to the other folder. The conversion is achieved through pandas (for csv) and xls2xlsx modules.

In addition, one can also choose to monitor the folder all the time or with a time interval, eg. every 15 minutes, which makes it more flexible and saves computation power.

Of course, some more functionalities could be added to make the code more powerful and versatile and not only constrained to only moving or converting files.

More use cases could be:
* perform specific operations only on the first working day of the month
* ask the user for input and based on returned value to perform differnt operations

P.S. the code could also be saved as .py file and run directly using cmd prompt.
