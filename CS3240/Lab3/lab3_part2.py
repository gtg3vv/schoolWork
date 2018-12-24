import  os
import json

files = {}

for file in os.listdir():
    with open(file, "r") as f:
        countLines = 0
        for line in f:
            countLines +=1
            
    files[file] = countLines
    
    
with open("file_info.txt", "w") as f:
    json.dump(files, f)
    
           
           
print(files)
    
        