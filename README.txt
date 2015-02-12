by ostein
mail: oliver.stein@cern.ch

Goal:
Connecting to Cividec Readout system.

06.02.2015
 - main script: client.py
	additional scripts in sub_script folder
	log files are written in log_files folder
 
 - Connection established
	TCP/IP connection
	simple string communication
	command strings in the scripts or in ROSY_Server_102014.pf

 - ROSY modes can be set
	Post Mortem
	Histogram

 - Problems:
	- Can not set threshold for histogram -> time out
	- When setting the Post Mortem parameters -> server response: 
	  I didn't understand you. (This message is not expected)
	- Further commands lead to time out error 

12.02.2015
- Problem:
	time out or error message when setting up post mortem or histogram mode 
	SOLVED

- Solution:
	forcing the script to sleep for a short time (1 second) before requesting the server answer

- Modes and parameters can be set

- Device can be armed

- Status of the device can be requested

- Problem:
	No data transfer, device doesn't trigger