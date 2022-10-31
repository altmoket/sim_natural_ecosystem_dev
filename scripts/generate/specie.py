import sys
def generate_specie(name:str):
    fileName = name.lower()
    with open(f"src/species/classes/{fileName}.py", 'w') as f:
        text = get_specie_text()
        result = replace_name_in_text(name, text)
        f.write(result)

def get_specie_text():
    with open("scripts/generate/texts/subclass.txt") as f:
        text = f.read()
        return text

def replace_name_in_text(name:str, text:str):
    old_str = '${class_name}'
    result = text.replace(old_str, name)
    return result

def main():
    args = sys.argv
    len_args = len(args)
    if len_args == 2:
        name = args[1]
        generate_specie(name)


if __name__ == "__main__":
    main()

