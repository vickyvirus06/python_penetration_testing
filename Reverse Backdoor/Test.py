command = "cd 'Network Scanner'"
command = command.split(" ")
if "'" in command[1]:
    path = ""
    for d in command:
        path = path+" "+d
    path = path.strip("cd ")
    print(path)