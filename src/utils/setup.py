import os,config

if not os.path.exists(config.INPUTS_DIR): 
    os.makedirs(config.INPUTS_DIR) 

open(config.SESSION_ID_FILE, 'a').close()

print(f"You can now set your session id in the {config.SESSION_ID_FILE} file")
print("Don't forget to change the year in the config file")
