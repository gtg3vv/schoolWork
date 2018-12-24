import  json
def countLines(fileName):
    with open(fileName, "r") as f:
        count = 0
        for line in f:
            count += 1
            
    return count


files = None
with open("file_info.txt","r") as f:
    files = json.load(f)
    
for file in files:
    print("Local count:", countLines(file), "Info count:", files[file])

