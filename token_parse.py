
with open("passwords.txt", "r") as f:
    fileText = f.read().split("\n")
    API_TOKEN_WEATHER = fileText[0]
    API_TOKEN_TG = fileText[1]
