import lexer

file_path = 'input_file.txt'

with open(file_path, 'r') as file:
    lines = file.readlines()

text = ''.join(lines).replace('\n', '')

result, error = lexer.run('<stdin>', text)

if error:
    print(" ___ _   ___     ___    _     ___ ____    ___ _   _ ____  _   _ _____ ")
    print("|_ _| \ | \ \   / / \  | |   |_ _|  _ \  |_ _| \ | |  _ \| | | |_   _|")
    print(" | ||  \| |\ \ / / _ \ | |    | || | | |  | ||  \| | |_) | | | | | |  ")
    print(" | || |\  | \ V / ___ \| |___ | || |_| |  | || |\  |  __/| |_| | | |  ")
    print("|___|_| \_|  \_/_/   \_\_____|___|____/  |___|_| \_|_|    \___/  |_|  ", '\n')
    
    print("Text in file has incorrect sintax")
    
    info = input("If you want to see more info type 'yes': ")
    if info == "yes":
        print(error.as_string())

elif result:
    print("__     ___    _     ___ ____    ___ _   _ ____  _   _ _____ ")
    print("\\ \\   / / \\  | |   |_ _|  _ \\  |_ _| \\ | |  _ \\| | | |_   _|")
    print(" \\ \\ / / _ \\ | |    | || | | |  | ||  \\| | |_) | | | | | |  ")
    print("  \\ V / ___ \\| |___ | || |_| |  | || |\\  |  __/| |_| | | |  ")
    print("   \\_/_/   \\_\\_____|___|____/  |___|_| \\_|_|    \\___/  |_|  ", '\n')
    print("Text in file has proper syntax!")
