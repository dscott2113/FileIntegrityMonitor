import hashlib
from datetime import datetime
import os

#Hash a file
def hash_file(filename):
    hashalgo = hashlib.sha256()

    try:
        #Opens file in binary mode.
        with open(filename, 'rb') as file:
            for byte_block in iter(lambda: file.read(4096), b""):
                hashalgo.update(byte_block)
    except FileNotFoundError:
        return None

    return hashalgo.hexdigest()

#Hash all files in a directory individually and get a combined hash of all the files together
def hash_directory(directory):
    file_hashes = {}
    combined_hash = hashlib.sha256()

    try:
        for root, dirs, files in os.walk(directory):
            files.sort()
            for filename in files:
                filepath = os.path.join(root, filename)
                file_hash = hash_file(filepath)
                if file_hash:
                    file_hashes[filepath] = file_hash
                    #combined hash for files in the folder
                    combined_hash.update(file_hash.encode())
    except FileNotFoundError:
        return None, None

    return file_hashes, combined_hash.hexdigest()

print ("Welcome to FIM: File Integrity Monitor.")

#Loop until a valid file is provided
hashes = None
combined_hash = None
while hashes is None:
    path2hash = input("Input the path to the file or folder you wish to hash: ")

    #checks if the requested path is for a file or a folder
    if os.path.isfile(path2hash):
        file_hash = hash_file(path2hash)
        if file_hash:
            hashes = {path2hash: file_hash}
        else:
            print(f"Error: The file '{path2hash}' was not found!\nPlease try again...")


    elif os.path.isdir(path2hash):
        result = hash_directory(path2hash)  # Get both file hashes and combined hash
        if result[0] is not None:  # Check if the first element is not None
           hashes, combined_hash = result  # Unpack the tuple
        else:
            print(f"Error: The file '{path2hash}' was not found!\nPlease try again...")
    else:
        print(f"Error: The file '{path2hash}' was not found!\nPlease try again...")

timeofhash = datetime.now()

#chnages output based on if it was a file or folder
if len(hashes) == 1:
    file_path = list(hashes.keys())[0]
    file_hash = hashes[file_path]
    print(f"The hash of your file is: {file_hash}")

else:
    print(f"Combined Folder SHA256 Hash: {combined_hash}")
    for path, file_hash in hashes.items():
        print(f"{path} SHA256 Hash: {file_hash}")

#asks the user for the directory they want to save the file
save_dir = input("Please enter the directory where you would like to save the text file: ")

# Default to the current directory if no directory is provided
if not save_dir:
    save_dir = os.getcwd()

# Ensure the directory exists
if not os.path.exists(save_dir):
    print(f"Error: The directory '{save_dir}' does not exist. Please try again.")
else:
    savetotxtname = input("Name your file: ")
    file_path = os.path.join(save_dir, savetotxtname)

#Saves txt file of results
with open(file_path, "w") as file:
    file.write(f"""\
FIM: File Integrity Monitor.
Path Hashed: {path2hash}
Time Stamp: {timeofhash}\n""")
    if combined_hash is not None:
        file.write(f"\nCombined Folder SHA256 Hash: {combined_hash}\n\n")
    for path, file_hash in hashes.items():
        file.write(f"{path}\nSHA256 Hash: {file_hash}\n\n")


print ("Your file has been written!")



