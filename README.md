## UserSim

This is a collection of Python code that was developed to act as dumb simulated user on the 2015 Palmetto Cyber Defense Competition network. I have taken out some of the configuration, but if you read through the code it shouldn't be too hard to figure out what needs to be added. Also, there is some left over settings from this year's competition (specifically for email). Change these to suit your needs. If you have any questions, feel free to ask. The following are some host configutation options that the UserSim is expecting.

* IP Addresses should be static if you want to score them

* Users should be part of the domain to make them a viable pivot point

* Need to have the file shares mounted
	* Path MUST be ```Z:\SimResources\<username>\Files\```

* The simulator program will not run unless they get logged into.
	* Recommened to change the Windows registry key to autologin and set the scripts to autorun, this way if the machine reboots, the UserSim will keep working

* Each of the scripts will score one of the simulated services. Just pass them an IP address of the target
	* Returns 0 for success
	* Returns 1 for failure
	* Shutdown script will start everything and retrieve the log file

* To score the web traffic, the simulator will reach out to ```http://x.x.x.x/score-bot-page``` (this is to make sure they can still reach Internet facing resources)
	- They are looking for the following string: “score-bot-traffic-nothing-to-see-here”

* To score the file share, the sims will look for a file called “score.txt” on the share
	* The string “score-bot-readme” must be in the first line!
	* Path to this file MUST be ```Z:\SimResources\<username>\Files\score.txt```


## UserSim Setups

* Set Windows Power Settings to high power so VMs don’t go to sleep

* Install VMware Tools (if running on VM)

* Install Firefox
	* Not default browser
	* Install Adblock Plus
	* No warnings for default browser (check the box to 'not show this option again')
	* No warnings to closing multiple tabs (check the box to 'not show this option again')
	* Google default search engine

* Install Python-2.7.9

* Turn off Windows Firewall (optional, but recommended)

* Install Selenium
	* ```cmd> pip install -U selenium```

* Download Selenium IEDriver
	* [Selenium Download](http://selenium-release.storage.googleapis.com/2.44/IEDriverServer_Win32_2.44.0.zip)
	* Extract to ```C:\SeleniumResources\iedriverserver.exe```
	* Add ```‘C:\SeleniumResources\’``` to your path

* Make sure start_simulator.bat is in the auto run folder
