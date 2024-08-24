import re 
from json import load as jsonLoad, dump as jsondump 
from csv import reader, writer
from operator import itemgetter
from os import path



current_dir = path.dirname(__file__)
def KKLcode_to_Dict(input:str)->dict[dict[str]]:
    
    with open(path.join(current_dir,"KKL_Menu_names.json"),"r") as file:
        KKL_Menu_Names =  jsonLoad(fp = file)
    
    with open(path.join(current_dir,"KKL_Parts_Names.json"),"r") as file:
        KKL_Parts_Names =  jsonLoad(fp = file)

    
    #put part values in ths dictionary
    operant_dict:dict = {}
    #String allcode handling is future
    #Version handling
    version_index:int = input.find("**") + 1
    version:str = input[:version_index]
    input:str = input.lstrip(version)
    name_dict:dict = dict()
    operant_dict["ver"] = {"ver":{"ver":version.rstrip("**")}}

    #Imported image handling
    importObjects_regex:re = re.compile(r"/#].+",re.DOTALL)
    importObjectsAddress:str = re.search(importObjects_regex,input) 
    
    if importObjectsAddress!= None:
        print(importObjectsAddress.group())
        importObjectsAddress = importObjectsAddress.group()
        input:str = input.rstrip("_"+importObjectsAddress)
    
        
    #Split @input by "_" into operant_list
    operant_list:list[str]  = re.split("[_]",input)
    
    
    alphaNum_regex = re.compile(r"^[a-zA-Z0-9]+")
    dict_name:str = ""
    for i in operant_list:
        
        alphaNum:str = i.split(".",maxsplit=1)[0]        #if the part value is alphabet + number, change into alphabet + "." + number
        
        alpha = re.match(r"^[a-z]{1,2}",alphaNum).group(0)    
        numa_a   = re.search(r"[0-9]+",alphaNum)
           
        if bool(numa_a): 
            num = numa_a.group(0)
        else: 
            num = ""
        match alpha:
            #These are of the form [a-z]{1}[0-9]{1}[0-9]+
            case "r"|"m"|'t'|'s'|'a'|'b'|'c'|'d'|'w'|'x'|'e'|'y'|'z'|'v'|'f':
                num1,num2 = num[:2],num[2:]
                dot_added_alphaNumeric = f"{alpha}{num1}.{num1}.{num2}"
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                alphaNum = f"{alpha}{num1}"
                dict_name = f"{alpha}"
                
            case  'xm'|'xr':
                dot_added_alphaNumeric = f"{alpha}{num}.{num}"
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                alphaNum = f"{alpha}{num}"
                dict_name =f"{alpha}"
            case 'dh'|'da':
                
                alphaNum1,alphaNum2 = alphaNum[:2],alphaNum[2:]
                dot_added_alphaNumeric = f"{alphaNum1}.{alphaNum2}"
                
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                
                alphaNum = f"{alphaNum1}"
                dict_name = f"{alphaNum1}"
            case _:
                dot_added_alphaNumeric = f"{alpha}.{num}"
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                alphaNum = f"{alpha}"
                dict_name =f"{alpha}"
    
            #Split element i of operant list by "."    
        
       
        i = i.split(".")
         
        
        part_vals:list = i[1:]
        
        part_val_names = KKL_Parts_Names[dict_name]
        
        #print(part_val_names)
        
        if part_vals == []:
            
            name_dict[alphaNum] = dict.fromkeys(part_val_names,"")
            
        else:
            name_dict[alphaNum] = dict(zip(part_val_names,part_vals))
        

        key_regex = re.compile("[0-9]+")  # Matches one or more digits

        for menukey in KKL_Menu_Names.keys():
            # Construct the new dictionary with filtered keys
            operant_dict[menukey] = {
                key: val
                for key, val in name_dict.items()
                if re.sub(key_regex, "", key) in KKL_Menu_Names[menukey] 
                
            }
            
    #End of for loop
        
    if not(importObjectsAddress== None):
        operant_dict["importObjects"] = {"importObjects":{"importObjects":importObjectsAddress}} 
    
    
    output_dict:dict[dict[str]] = operant_dict.copy()

    return output_dict

def dict_to_KKLCode(input:dict[dict[dict[str]]])->str:
        operant_dict:dict[dict[dict[str]]] = input.copy()
       
        
        Version     = operant_dict["ver"]["ver"]["ver"]
        del operant_dict["ver"]
        if "importObjects" in operant_dict:
            Imported_objects = operant_dict["importObjects"]["importObjects"]["importObjects"] 
            print("These are imported",operant_dict["importObjects"])
            del operant_dict["importObjects"]
        else:
            Imported_objects = ""
        
        output:str  = ''
        for values in operant_dict.values():
            for partname,part_values in values.items():
                joiner:list = [x for x in part_values.values() if x !=""]
                part_string:str = ""
               
                if bool(joiner) ==False:
                    part_string:str = partname
                else:
                    partname_clean = re.match(r"^[a-z]{1,2}",partname).group(0)
                    match partname_clean:
                        case "r"|"m"|'t'|'s'|'a'|'b'|'c'|'d'|'w'|'x'|'e'|'y'|'z'|'v'|'f': 
                            part_string:str = partname_clean + joiner[0] + ".".join(joiner[1:]) 
                        case 'xm'|'xr':
                            part_string:str = partname +"."+".".join(joiner[1:])
                        case 'dh': 
                            part_string:str = partname +joiner[0] +"."+ ".".join(joiner[1:])   
                            print("Dict to code string",part_string)
                        case'da':
                            part_string:str = partname + joiner[0]
                            print("Dict to code string",part_string) 
                        case _:
                            part_string:str = partname_clean + ".".join(joiner)
                    
                
                output+= part_string + "_"

       
        #match Version_ then atleast 2 digits
        output = Version + "**" + output
        output = output.rstrip("_")
        output = output+Imported_objects
        return output


class KKLCodeCovertor_Object:
             
    def __init__(self,compare:str,names_list:list[str],convert_list:list[str]) -> None:
        
        if type(names_list) is not list or type(convert_list) is not list:
            raise ValueError("MAKE SURE INPUT IS A LIST") 
        self.convertlist = convert_list
        self.convertdict:dict[dict[dict[dict[str]]]] = {}
        for index,name in enumerate(names_list):
            if bool(name) and convert_list[index] != "":
                print(name)
                self.convertdict[name] = KKLcode_to_Dict(convert_list[index])
                       
            else:
                print("skipped due to no name." )
        
        self.compare:str = compare
        self.comparedict:dict = KKLcode_to_Dict(self.compare)


        with open(path.join(current_dir,"KKL_Menu_names.json"),"r") as file:
            self.KKL_Menu_Names =  jsonLoad(fp = file)
        

        with open(path.join(current_dir,"KKL_Parts_Names.json"),"r") as file:
            self.KKL_Parts_Names =  jsonLoad(fp = file)
        
        

    

    

    def convert(self):
        
        #Get the dictionaries
        convert_objects_dict:dict = self.convertdict.copy()
        
        compare_dict:dict = self.comparedict.copy()
        
        #Cleaning the comapare_dict of empty values. And removing version.
        
        version = compare_dict.pop("ver")
        importObjects = compare_dict.pop("importObjects") if "importObjects" in compare_dict else ""
        
        #get list of changes.
        
        menuOptions:list[str] = list()
        partOptions:list[str] = list()
        labelOptions:list[str] = list()
        
       
        #Break dictionary into 3 ordered lists
   
        for menukey,menuvalue in compare_dict.items():
            for partkey,partvalue in menuvalue.items():
                for labelkey,labelvalue in partvalue.items():
                    if bool(menuvalue):  
                        menuOptions.append([menukey]) if [menukey] not in menuOptions else ''
                        if bool(partvalue):
                            partOptions.append([menukey,partkey]) if [menukey,partkey] not in partOptions else ''
                            if bool(labelvalue):
                                labelOptions.append([menukey,partkey,labelkey])           
                                    
        
        
        def regsearch(Options_list:list[str],list_length:int,inputname:str = "menu"):    
            menu_excluded = []
            Options = Options_list[:]
            Options_clean = list(map(itemgetter(list_length),Options))
            
            while True:
                print(menu_excluded)
                print("            ") 
                menuInput = input(f"""1){Options}  
                                Choose {inputname} names. """)
                print("            ")
                if menuInput =="":
                    #If Nothing entered, end whole function
                    break
                
                menuregex = re.findall(r"[a-z0-9_]{0,}"+menuInput+r"[a-z0-9_]{0,}","~".join(Options_clean),re.IGNORECASE) 
                if menuregex == []:  
                    print("Value not found.")
                    print("            ")
                    continue
                while len(menuregex)>0:    
                    menu_choice = input(f""" {list(enumerate(menuregex,start=1))}
                    Choose option by index(integer only): """)
                    print("            ")
                    if menu_choice == "" or not menu_choice.isnumeric() or int(menu_choice)>len(menuregex):
                        print("Input Outside of expected value, restart." )
                        print("            ")
                        break
                    menu_choice = menuregex.pop(int(menu_choice)-1)
                    
                    #Regex helper
                    remove_index = Options_clean.index(menu_choice)
                    Options_clean.pop(remove_index)
                    Options.pop(remove_index)
                    menu_excluded.append(menu_choice)
                    
            
            return menu_excluded[:]
        #cleaning the lists
        
        menu_exclude = regsearch(menuOptions,0,"menu")
        print(menu_exclude)
        
        [partOptions.remove(x) 
        for x in partOptions[:] 
        if x[0] not in menu_exclude]
        
        
        part_exclude = regsearch(partOptions,1,"part")
        print(partOptions)
        
 
        [labelOptions.remove(x)
        for x in labelOptions[:] 
        if x[1] not in part_exclude]

       

        label_exclude = regsearch(labelOptions,2,"label")
        print(label_exclude)    


         


       
        
        list_of_strings = []      
        count = 0
        for key in self.convertdict.keys():
            count+=1
            for menukey,menuvalue in compare_dict.items():
                for partkey,partvalue in menuvalue.items():
                    for labelkey,labelvalue in partvalue.items():
                        if menukey not in menu_exclude: 
                            #print("Menukey found:",menukey)
                            if partkey not in part_exclude:  
                                print("Partkey found:",partkey) if partkey == "da" else ""
                                if labelkey not in label_exclude:
                                    #print("Labelkey found:",labelkey)
                                    convert_objects_dict[key][menukey] = compare_dict[menukey] if bool(self.convertdict[key].get(menukey)) else convert_objects_dict[key][menukey]
                                    convert_objects_dict[key][menukey][partkey] = compare_dict[menukey][partkey] if bool(self.convertdict[key][menukey].get(partkey)) else convert_objects_dict[key][menukey][partkey]
                                    convert_objects_dict[key][menukey][partkey][labelkey] = compare_dict[menukey][partkey][labelkey] if bool(self.convertdict[key][menukey][partkey].get(labelkey)) else convert_objects_dict[key][menukey][partkey][labelkey]
            print(key)                
                            
                            
            convert_objects_dict[key].update({'importObjects':importObjects}) if 'importObjects' in compare_dict else ''
            convert_objects_dict[key].update({"ver":version})
            list_of_strings.append(dict_to_KKLCode(convert_objects_dict[key]))
            

        return list_of_strings






                              
    def help(self,*tablist:tuple[str])->None:
        if tablist ==():
            print(f"""Type menu names for the tabgroups.
Options: 
{list(self.KKL_Parts_Names)[:10]}   
{list(self.KKL_Parts_Names)[10:23]}
{list(self.KKL_Parts_Names)[23:30]}
{list(self.KKL_Parts_Names)[30:41]}
""")    

        else:
            for index in tablist:
                print(f"{self.KKL_Menu_Names[index]}:{[self.KKL_Parts_Names[i] for i in self.KKL_Menu_Names[index]]}")



try:
    with open(path.join(current_dir,"KKLcode loader and dumper.csv"),"r",newline="") as f:
        file = reader(f,delimiter=",")
        header = next(file)
        rows = []
        Id,names,codes,output,convertor_list =[],[],[],[],[] 
        for i in file:
            rows.append(i)
except PermissionError:
    input("Close the csv file or this won't work. ")



Id = list(map(itemgetter(0),rows))
names= list(map(itemgetter(1),rows))
codes= list(map(itemgetter(2),rows))
output = list(map(itemgetter(3),rows))
convertor_list= list(map(itemgetter(4),rows))
convertor = convertor_list[0]





working_Object = KKLCodeCovertor_Object(convertor,names,codes)

output = working_Object.convert()



out = list(zip(Id,names,codes,output,convertor_list))

with open(path.join(current_dir,"KKLcode loader and dumper.csv"),"w",newline="") as f:
    rows = writer(f,dialect="excel",delimiter=",")
    rows.writerow(header)
    rows.writerows(out)





