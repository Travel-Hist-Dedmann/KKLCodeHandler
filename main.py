import re 
from json import load as jsonLoad 

def KKLcode_to_Dict(input:str)->dict[dict[str]]:
    with open("KKL_Parts_Names.json","r") as file:
        KKL_Parts_Names =  jsonLoad(fp = file)
    #put part values in ths dictionary
    operant_dict:dict = {}

    #String allcode handling is future

    
    #Version handling
    version_index:int = input.find("**") + 1
    version:str = input[:version_index]
    input:str = input.lstrip(version)
    operant_dict["ver"] = version.rstrip("**")

    #Imported image handling
    importObjects_regex:re = re.compile(r"/#].+",re.DOTALL)
    importObjectsAddress:str = "".join(re.findall(importObjects_regex,input))
    
    if importObjectsAddress!= None:
        print(importObjectsAddress)
        input:str = input.rstrip("_"+importObjectsAddress)
    
    count_iter = 0
    count_alpha = 0
    #Split @input by "_" into operant_list
    operant_list:list[str]  = re.split("[_]",input)


    alphaNum_regex = re.compile(r"[a-z]{1,2}[0-9]+|[a-z]{2}")
    for i in operant_list:
        count_iter += 1
        alphaNum:str = re.findall(alphaNum_regex,i)[0]

        #if the part value is alphabet + number, change into alphabet + "." + number
        if alphaNum.isalpha()==False:
            
            alpha = re.findall(r"[a-z]{1,2}",alphaNum)[0]
            num   = re.findall(r"[0-9]+",alphaNum)[0]

            match alpha:
                case "r"|"m"|'t'|'s'|'a'|'b'|'c'|'d'|'w'|'x'|'e'|'y'|'z'|'v':
                    num1,num2 = num[:1],num[2:]
                    dot_added_alphaNumeric = f"{alpha}.{num1}.{num2}"
                    i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                case _:
                    dot_added_alphaNumeric = f"{alpha}.{num}"
                    i:str = i.replace(alphaNum,dot_added_alphaNumeric)
        #Split element i of operant list by "."    
        i = i.split(".")
        
        part_dict_name:str = i[0]
        part_vals:list = i[1:]
        
        #matches:
    
    

        
        #Part val_names must be replaced with KKL codenames.
        
        
        part_val_names = KKL_Parts_Names[part_dict_name][:]
        
        if part_vals == []:
            operant_dict[part_dict_name] = dict.fromkeys(part_val_names,"")
        else:
            operant_dict[part_dict_name] = dict(zip(part_val_names,part_vals))  
    #End of for loop
    """for x in KKL_Parts_Names.keys(): 
        if x not in operant_dict.keys():
            operant_dict[x] = dict.fromkeys(KKL_Parts_Names[x],"")
      """
        
    if not(importObjectsAddress==""):
        operant_dict["importObjects"] = importObjectsAddress 
    
    #operant_list:list[list[str]] = [re.split("[.]",x) for x in operant_list] 
    

    output_dict:dict[dict[str]] = operant_dict.copy()

    
    return output_dict



def dict_to_KKLCode(input:dict[dict[str]])->str:
        operant_dict:dict[dict[str]] = input.copy()
        Version     = operant_dict["ver"] 
        del operant_dict["ver"]
        
        output:str  = ''
        for (partname,part_values) in operant_dict.items():
            
            part_string:str  = ".".join([x for x in part_values.values() if x !=""])
            output      += partname+ part_string + "_"

       
        #match Version_ then atleast 2 digits
        output = Version + "**" + output
        output = output.rstrip("_")
        return output


class KKLCodeCovertor_Object:
             
    def __init__(self,compare:str) -> None:
        
        """For future
        ,names_list:list[str],convert_list:list[str]
        self.dict:dict[dict[str]] = {}
        for index,name in enumerate(names_list):
            self.dict[name] = KKLcode_to_Dict(convert_list[index])
        """    
            
        
        self.compare:str = compare
        self.comparedict:dict = KKLcode_to_Dict(self.compare)

        with open("KKL_Menu_names.json","r") as file:
            self.KKL_Menu_Names =  jsonLoad(fp = file)
        Menunames:dict[str] = self.KKL_Menu_Names.copy()
        with open("KKL_Parts_Names.json","r") as file:
            self.KKL_Parts_Names =  jsonLoad(fp = file)
        Partnames:dict[list[str]] = self.KKL_Parts_Names.copy()
        
        
        self.Menu_and_Part_names  = {}
        for keys in Menunames.keys():
            self.Menu_and_Part_names[keys] = dict.fromkeys(Menunames[keys],'')
            for valkey in self.Menu_and_Part_names[keys].keys():
                try:
                    self.Menu_and_Part_names[keys][valkey] = Partnames[valkey]
                except KeyError:
                    pass
    

    def create_covertor(self):
        
        keys:set[str] = set()
        self.help()
        temp_comma_sep_String:str= ",".join(self.Menu_and_Part_names.keys())
       
        Run = True
        print("1) Choose whate you want to covert")
        while Run :
            print(keys) if len(keys)>0 else ""
            key = input("1a)Please enter a single Part menu from list. Leave blank or type exit to exit.")
            if key == "" or key.lower()== "exit": 
                Run = False 
                break
            
            key_regex = re.findall(r"[a-z0-9]*"+key+r"[a-z0-9]*",temp_comma_sep_String,re.IGNORECASE)
            match len(key_regex):
                case 0:
                    print("1)No match")
                    self.help()
                case 1:
                    keys.add(key_regex[0])
                    
                case _:
                    print(list(enumerate(key_regex)))
                    choice = input("1b) Please choose a part by it's index number, or leave blank/type non numbers to restart.")
                    if choice == "" or not choice.isnumeric():
                        continue
                    keys.add(key_regex[int(choice)])



        print(keys)
        change_dict:dict[dict[str]] = {}
        
        for element in keys:
            print(f"For {element}")
            for x in self.Menu_and_Part_names[element].keys():
                
                if x in set(self.comparedict)and self.comparedict[x] != None and '' not in self.comparedict[x].values() :
                    change_dict[x] = self.comparedict[x]
                    self.search(x,"2a)Please select part from list.","2b)Select value label","2)Please choose value",change_dict)
                else:
                    print("2)No such part exists,skipped.")
        
        compare_dict = self.comparedict
        for x,y in change_dict.items():
            compare_dict[x] = y             
        
        convertstring:str = dict_to_KKLCode(compare_dict)
        print(convertstring)
        return convertstring           
                   


                        
                              
    def help(self,*tablist:tuple[str])->None:
        if tablist ==():
            print(f"""Type menu names for the tabgroups.
Options: 
{list(self.Menu_and_Part_names.keys())[:10]}
{list(self.Menu_and_Part_names.keys())[10:23]}
{list(self.Menu_and_Part_names.keys())[23:30]}
{list(self.Menu_and_Part_names.keys())[30:41]}
""")    

        else:
            for index in tablist:
                print(self.Menu_and_Part_names[index])


    def search(self,iter,input1:str,input2:str,input3:str,dict:dict[dict[str]]) ->dict[dict[str]]:
        Running = True
        change_list:set[dict:str] = set()
        if iter in list(dict):
            print(list(dict[iter]))
            while Running :
                print(change_list) if len(change_list)>0 else ""
                
                part = input(input1 + "Type Exit or leave plank to exit this loop")
                if part == "" or part.lower()== "exit": 
                    Running = False 
                    break
                
                part_regex = re.findall(r"[a-z0-9_\-]*"+part+r"[_\-a-z0-9]*",",".join(list(dict[iter])),re.IGNORECASE)
                match len(part_regex):
                    case 0:
                        print("No match")
                        print(list(dict.values()))
                    case 1:
                        change_list.add(part_regex[0])
                        
                    case _:
                        print(list(enumerate(part_regex)))
                        choice = input(input2 + "Type Non numeric or leave blank to skip this.")
                        if choice == "" or not choice.isnumeric():
                            continue
                        else:    
                            change_list.add(part_regex[int(choice)])
            print(change_list)
            
            for item in change_list:
                print(f"{item}: {dict[iter][item]}")
                changevalue = input(input3)
                dict[iter][item] = changevalue
            return dict.copy()

def main():
    
    code = input("Your convertor string here.")

    code_convertor = KKLCodeCovertor_Object(code)

    string = code_convertor.create_covertor()

    input()

main()