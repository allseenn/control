import pandas as pd
import random
import datetime
import os

MENU = "\
0. Create notebook\n\
1. Open notebook\n\
2. Save notebook\n\
3. Find note\n\
4. Add note\n\
5. Update note\n\
6. Delete note\n\
7. Delete notebook\n\
8. List all notes\n\
9. Import/Export\n\
Enter a number or q(uit): "

SUBMENU = "\
i. set id\n\
c. set create date\n\
m. set modify date\n\
s. set subject\n\
b. set body\n\
k. kill buffer\n\
BUF: "

PORT = "\
ic. imports csv to notebook\n\
ij. import json to notebook\n\
ec. export to csv file\n\
ej. export to json file\n\
bc. buffer to csv file\n\
bj. buffer to json file\n\
BUF: "

NOTEBOOK = "notebook.csv"

record = ["", "", "", "", ""]

# 0 Create NoteBook
def new_base() -> pd.DataFrame :
    base = pd.DataFrame( columns=['id', 'created', 'modified', 'subject', 'body'] )
    return base

# 1 Open notebook
def open_base(filename: str = NOTEBOOK) -> pd.DataFrame:
    if os.path.isfile(filename):
        try:
            base = pd.read_csv(filename, dtype=str)
        except BaseException as error:
            return f"Error! {error}"
        return base
    else:
        return "File not found, make new one or save base"
# 2. Save notebook
def save_base(base: pd.DataFrame, filename: str = NOTEBOOK) -> str:
    if os.path.isfile(filename):
        try:
           base.to_csv(filename, index=False)
        except BaseException as error:
            return f"Error! {error}"
        return f"File {filename} is updated"
    else:
        try:
           base.to_csv(filename, index=False)
        except BaseException as error:
            return f"Error! {error}"
        return f"File {filename} is created"
# 3. Find note
def find_record(base: pd.DataFrame) -> pd.DataFrame:
    columns = list(base.columns.values)
    que = " & ".join([f'{columns[i]} == "{record[i]}"' for i in range(len(columns)) if record[i] != ""])
    try:
        find = base.query(que)
    except BaseException as error:
            return f"Error! {error}"
    return "Not found" if find.empty else find
# 4. Add note
def add_record(base: pd.DataFrame) -> pd.DataFrame:
    record[0] = str(random.randint(22222,99999))
    record[1] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    base.loc[record[0]] = record
    return base
# 5. Update note
def update_record(base: pd.DataFrame) -> pd.DataFrame:
    record[2] =  datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    for i in range(len(record)):
        if record[i] != "":
            base.loc[base['id'] == record[0], list(base.columns.values)[i]] = record[i]
    return base
# 6. Delete note
def del_record(base: pd.DataFrame) -> pd.DataFrame:
    if record[0] != "":
        base.drop(base[base.id == record[0]].index, inplace=True)
    else:
        return f"Введите id для удаления"
    return base
# 7. Delete notebook
def del_file(filename: str) -> str:
    if os.path.isfile(filename):
        os.remove(filename)
        return f"{filename} deleted"
    else:
        return f"{filename} not found"
# buffer
def buffer(base: pd.DataFrame, number: int) -> None: 
    for i in range(len(record)):
        record[i] = base.loc[number].tolist()[i]
    return
#kill set
def kill_buffer() -> None:
    for i in range(len(record)):
        record[i] = ""
    return
# main menu 10 digits
def menu():
    base = pd.DataFrame()
    choice = ""
    msg = "Main NoteBook menu"
    while choice != "q":
        print("\033c", end="")
        print(f"MSG: {msg}")
        choice = input(MENU)
        match choice:
            case "0": # create NoteBook
                base = new_base()
                msg = f"NoteBook created in memory, don't forget to save it" if type(base) != str else base
            case "1": # open notebook
                filename = input("Enter "+ NOTEBOOK + " name: ")
                filename = NOTEBOOK if filename == "" else filename
                base = open_base(filename)
                msg = "NoteBook is open" if type(base) != str else base
            case "2": # save NoteBook
                filename = input("Enter "+ NOTEBOOK + " name: ")
                filename = NOTEBOOK if filename == "" else filename 
                msg = save_base(base, filename)
            case "3": # Find note
                submenu(base, "Set one or more elements\nexecute find with first key\nf. find note")
            case "4": # Add  note 
                submenu(base, "Set all elements\nexecute adding with first key\na. add note")
            case "5": # Update note
                submenu(base, "Set any element for update\nexecute del with first key\nu. update note") 
            case "6": # Delete note
                submenu(base, "Set id only for deletion\nexecute del with first key\nd. delete note")   
            case "7": # delete NoteBook
                filename = input("Enter filename to delete: ") 
                msg = del_file(filename)
            case "8": # Clean NoteBook
                print("\033c", end="")
                print(base) 
                foo = input(f"Total is {base.shape[0]} notes\nPress Enter to return menu: ")
            case "9": # Import / Export
                base = port(base)
    print("\033c", end="")
    return print("Have a nice day!\nGood Bye!")
# Submenu 10 chars
def submenu(base: pd.DataFrame , msg: str) -> pd.DataFrame:
    choice = ""
    while choice != "r":
        print("\033c", end="")
        print(f"{msg}")
        print(SUBMENU, end="")
        print(*record)
        choice = input("f(ill), r(eturn) or q(uit): ")
        match choice:
            case "i": # i. set id
                record[0] = input("edit id: ")
            case "c": # c. set create date
                record[1] = input("edit create date: ")
            case "m": # m. set modify date
                record[2] = input("edit modify date: ")
            case "s": # s. set subject
                record[3] = input("edit subject: ")
            case "b": # b. set body
                record[4] = input("edit body: ")
            case "k": # k. kill buffer
                kill_buffer()
            case "f": # f. search records
                print("\033c", end="")
                print(find_record(base))
                try:
                    number = int(input("enter line number to copy in BUF\nor hit Enter to return: "))
                    buffer(base, number)
                except BaseException as error:
                    print(f"enter line number to copy in BUF\nor hit Enter to return: ")
            case "a": # a. add note
                base = add_record(base)
                print("Note was added") if type(base) != str else print(base)
                choice = input("a(ny) key to return:")
            case "d": # d. delete note
                base = del_record(base)
                print("Note was deleted") if type(base) != str else print(base)
                choice = input("a(ny) key to return:")
            case "u": # u. update note
                print("\033c", end="")
                print(f"The BUFF:", end="")
                print(*record, end="")
                print(f' was in this note\n{base.loc[base["id"]==record[0]]}')
                base = update_record(base)
                print("Note was updated") if type(base) != str else print(base)
                print(base.loc[base["id"]==record[0]])
                choice = input("a(ny) key to return:")
            case "q":
                print("\033c", end="")
                print("Have a nice day!\nGood Bye!")
                exit()
    return base
# 10 Import/Export
def port(base: pd.DataFrame) -> pd.DataFrame:
    choice = ""
    while choice != "r":
        print("\033c", end="")
        #print(f"{msg}")
        print(PORT, end="")
        print(*record)
        choice = input("fi(ll), r(eturn) or q(uit): ")
        match choice:
            case "ic": # ic. imports csv to base
                print("\033c", end="")
                sep = input("Enter separator , or t(ab): ")
                encoding = input("Enter encoding utf8: ")
                if sep == "t":
                    sep ="\t"
                filename = input("Enter name.csv to import: ")
                chunk = pd.read_csv(filename, sep=sep, encoding=encoding, dtype=str)
                base = pd.concat([base, chunk], ignore_index=True)
                print(f"{len(chunk)} row from {filename} imported\nnew base have {len(base)} rows")
                choice = input("press a(ny) key to return: ")
            case "ij": # ij. import json to base
                print("\033c", end="")
                filename = input("Enter name.csv to import: ")
                chunk = pd.read_json(filename, orient='split')
                base = pd.concat([base, chunk], ignore_index=True)
                print(f"{len(chunk)} row from {filename} imported\nnew base have {len(base)} rows")
                choice = input("press a(ny) key to return: ")
            case "ec": # ic. export to csv file
                print("\033c", end="")
                sep = input("Enter separator , or t(ab): ")
                encoding = input("Enter encoding utf8: ")
                if sep == "t":
                    sep ="\t"
                filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S.csv')
                base.to_csv(filename, sep=sep, encoding=encoding, index=False)
                print(f"{len(base)} row exported to {filename}")
                choice = input("press a(ny) key to return: ")
            case "ej": # ij. export to json file
                print("\033c", end="")
                filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S.json')
                base.to_json(filename, orient='split', index=False)
                print(f"{len(base)} row exported to {filename}")
                choice = input("press a(ny) key to return: ")
            case "bc": # bc. buffer to csv file
                print("\033c", end="")
                sep = input("Enter separator , or t(ab): ")
                encoding = input("Enter encoding utf8: ")
                if sep == "t":
                    sep ="\t"
                filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S.csv')
                found = find_record(base)
                found.to_csv(filename, sep=sep, encoding=encoding, index=False)
                print(f"{len(found)} row exported to {filename}")
                choice = input("press a(ny) key to return: ")
            case "bj": # bj. buffer to json file
                print("\033c", end="")
                filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S.json')
                found = find_record(base)
                found.to_json(filename, orient='split', index=False)
                print(f"{len(found)} row exported to {filename}")
                choice = input("press a(ny) key to return: ")
            case "q":
                print("\033c", end="")
                print("Have a nice day!\nGood Bye!")
                exit()
    return base

menu()