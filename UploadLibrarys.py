import os

def create_folder():
    try:
        os.mkdir("/flash/libraries")
    except Exception:
        pass
    
    
def upload_file(code: str):
    with open('/flash/libraries/DriveBase.py', 'w+t') as DriveBase:
        char = DriveBase.write(code)
    
    

create_folder()
upload_file("import os")
