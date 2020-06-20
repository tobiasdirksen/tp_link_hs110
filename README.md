 # Getting data from TP Link Hs110
 This script collects data from a TP Link Hs110 power plug and returns a data frame. 
 
 Simple run the function ```run(address)``` with the ip address of the Hs110 as input, and it returns a data frame.
 
 If you do not know how to find the ip addres of the Hs110, you can use an app like Fing. 
 
 I run the script on my raspberry pi 4, and save date in postgres, which also runs on my raspberry. 
 
 References:
 * https://gist.github.com/rbaarda/22deebc5612938f442dfdd7f5ebba3e1
 * https://github.com/softScheck/tplink-smartplug/blob/master/tplink_smartplug.py
 * https://www.softscheck.com/en/reverse-engineering-tp-link-hs110/
