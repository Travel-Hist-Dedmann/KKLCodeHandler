import re ,copy
from json import load as jsonLoad, dump as jsondump 
from csv import reader, writer
from operator import itemgetter
from os import path

current_dir = path.dirname(__file__)

def update_nested_dict(values_dict:dict,keys:list[str],operant_dict:dict)-> None:
    """Recursive function. Changes the value of the operant_dict to the values in the values dicionary. Keys required are the Menu keys and the labelkeyes. 
    Used in code_to_Dict function.

    @values_dict:dict[dict...]: Should cotaint a dictionary. It wil replace the dictionary in the operant dict.

    @Operant_dict:dict: The nest dictinary whose values you want changed.
    
    @keys:list[str]: A list of Keys.
    """
    
    if len(keys) == 1:
        if bool(operant_dict.get(keys[0])):
            operant_dict[keys[0]] = {}
        operant_dict[keys[0]] = values_dict[keys[0]].copy()
        #print("Done")
    else:
        key = keys[0]
        #print("Looped")
        if key in operant_dict:
            update_nested_dict(values_dict,keys[1:],operant_dict[keys[0]])


all_code_exception_list = set(["a","b","c","d","w","x","e","y","z","ua","uf","ue","ub","u","u0","u1","u2","u3","u4","u5","u6","u7","u8","u9","v","ud","ug","uc"]) 
with open(path.join(current_dir,"KKL_Menu_names.json"),"r") as file:
        KKL_Menu_Names =  jsonLoad(fp = file)
    
with open(path.join(current_dir,"KKL_Parts_Names.json"),"r") as file:
    KKL_Parts_Names =  jsonLoad(fp = file)

menu_and_partnames_list:list = []
name_dict ={}
for menukey,menuvalue in KKL_Menu_Names.items():
    name_dict[menukey] = {}
    if bool(set(menuvalue).intersection(all_code_exception_list)):
        name_dict.pop(menukey)
    else:
        for element in menuvalue:
            name_dict[menukey][element] = {} 
            menu_and_partnames_list.append([menukey,element])
        #print(menukey,":",name_dict[menukey])            

                     
helper_dict =    {k:dict.fromkeys(v,"") 
                      for k,v in KKL_Parts_Names.items()
                      if k not in all_code_exception_list }



#print(name_dict["Pose"]["aa"])
for key in name_dict:
    for partkey in name_dict[key]:
        name_dict[key][partkey].update(helper_dict[partkey]) if partkey not in all_code_exception_list else ""
        #print(key,":",helper_dict[key])
        #print(key,":",partkey,":",name_dict[key][partkey])
KKL_Names_reversed = {}
for key,value in KKL_Menu_Names.items():
    for element in value:
        KKL_Names_reversed[element] = key if element not in all_code_exception_list else ""



def KKLcode_to_Dict(input:str)->dict[dict[str]]:
    
    #Copy name dict to this operant dict.
    operant_dict:dict = copy.deepcopy(name_dict)
    
    #Version handling
    version_index:int = input.find("**") + 1
    version:str = input[:version_index]
    input:str = input.lstrip(version)
    
    
    operant_dict["ver"] = {"ver":{"ver":version.rstrip("**")}}

    #Imported image handling
    
    importObjectsAddress:list = input.split("/#]",1) 
    
    if len(importObjectsAddress)>1:
        print(importObjectsAddress)
        input:str = input.rstrip("_"+importObjectsAddress[0])
    
    
    #Split @input by "_" into operant_list
    operant_list:list[str]  = input.split("_")
    print("This list doesn't exist") if operant_list =="" else ""   
    #print("First split", operant_list)
    #add to set if there are taken partnames in case1.
    list_of_dicts_to_use:list =[]
    list_of_parts_to_pop:list = menu_and_partnames_list[:]
    extra_part_catch_set:set = set() 
    for i in operant_list:
            
        splitBy_List = i
        #print(splitBy_List) if splitBy_List =="da" else ""
        alphaNum:str = splitBy_List.split(".",maxsplit=1)[0]        #if the part value is alphabet + number, change into alphabet + "." + number
        #print("|",alphaNum,"|") if len(alphaNum) ==8  else ""
        part_name ="Error in KKLcode_to_dict"
        alpha =re.match(r"([a-z]{1,2})",alphaNum).group(1)
        #print("|",alpha.strip(),"|") if len(alphaNum) ==8  else ""
        #Remove the Part name at the start of the  SliptBy_List nd then splt it by .
        splitBy_dot_List = splitBy_List.removeprefix(alpha).split(".")
        #print("|",splitBy_dot_List,"|") if len(alphaNum) ==8  else ""
        splitter_help_dict = {}
        ####TestStart
        #print(splitBy_dot_List) if alpha =="da" else ""
        if len(alphaNum)<=2:
            part_name = alpha
            splitter_help_dict = {part_name : dict.fromkeys(helper_dict[alpha].keys(),"")} 
            
        else:
        ####Testend
            num = alphaNum.removeprefix(alpha)    
            #print("|",num,"|") if len(alphaNum) ==8  else ""
            
            #print(alpha,":",num,":",splitBy_dot_List)
            match alpha:
                #These are of the form [a-z]{1}[0-9]{1}[0-9]+
                case "a"|"b"|"c"|"d"|"w"|"x"|"e"|"y"|"z"|"ua"|"uf"|"ue"|"ub"|"u"|"v"|"ud"|"ug"|"uc":
                    continue
                case "r"|"m"|'t'|'s'|'a'|'b'|'c'|'d'|'w'|'x'|'e'|'y'|'z'|'v'|'f':
                    #form r00.000...

                    part_name = alpha + num[:2]
                    if part_name in extra_part_catch_set:
                      # print(part_name,splitBy_dot_List)
                       continue 
                    

                    #print(part_name,":",splitBy_dot_List)
                        
                    else:
                        #print(part_name,":",splitBy_dot_List)
                        splitBy_dot_List[0] = splitBy_dot_List[0][2:]  
                    splitter_help_dict = {part_name : dict(zip(helper_dict[alpha].keys(),splitBy_dot_List))}    
                    #print("case1 :",len(name_dict[part_name]) == len(KKL_Parts_Names[alpha]))
                case  'xm'|'xr':
                    #form = xm000.---
                    part_name = alpha + num
                   
                    if len(splitBy_dot_List) <=1:
                        continue
                    splitBy_dot_List.pop(0)
                    #print(splitBy_dot_List)
                    splitter_help_dict = {part_name : dict(zip(helper_dict[alpha].keys(),splitBy_dot_List))}
                    #print("case2 :",len(name_dict[part_name]) == len(KKL_Parts_Names[alpha])) 
                    #print(name_dict[part_name]) if alpha in ["da,dh"] else ""
                    #print(part_name,":",num,";",splitBy_dot_List)
                case 'dh'|'da':
                    part_name = alpha
                    #print(part_name)
                    if part_name in extra_part_catch_set:
                       #print(part_name,splitBy_dot_List)
                       continue 
                    #print(helper_dict[alpha])
                    splitter_help_dict = {part_name : dict(zip(helper_dict[alpha].keys(),splitBy_dot_List))}  
                    #print(splitter_help_dict)
                    #print("case3 :",len(name_dict[part_name]) == len(KKL_Parts_Names[alpha])) 
                case _:
                    part_name = alpha
                    
                    if part_name in extra_part_catch_set:
                       #print(part_name,splitBy_dot_List)
                       continue 
                    splitter_help_dict = {part_name : dict(zip(helper_dict[alpha].keys(),splitBy_dot_List))}
                    
            
        #print(part_name,splitBy_dot_List,sep="||") if part_name in ["xm202","ac"] else ""
        """splitter_help_dict = {}
            
            #print(helper_dict[alpha].keys())
            splitter_help_dict = dict(zip(helper_dict[alpha].keys(),splitBy_dot_List))
"""            
            #print(splitter_help_dict)
         
            #print(alpha,';',operant_dict[KKL_Names_reversed[alpha]][alpha])
        
        list_of_parts_to_pop.remove([KKL_Names_reversed[alpha],part_name]) if [KKL_Names_reversed[alpha],part_name] in list_of_parts_to_pop else ""
        list_of_dicts_to_use.append(splitter_help_dict) 
        update_nested_dict(splitter_help_dict,[KKL_Names_reversed[alpha],part_name],operant_dict)
        #print(operant_dict[KKL_Names_reversed[alpha]][part_name]) if part_name == "da" else ""
       
        
    #print("Here +",list_of_parts_to_pop)    
    [[operant_dict[x].pop(y) 
      for y in ["r", 'm', 't', 's', 'a', 'b', 'c', 'd', 'w', 'x', 'e', 'y', 'z', 'v', "f",'xm','xr'] if y in operant_dict[x]]
     for x in operant_dict]
    
  
    for menukey,partkey in list_of_parts_to_pop:
        operant_dict[menukey].pop(partkey) if bool(operant_dict[menukey].get(partkey,False)) else ""
    #print(operant_dict)


    #End of for loop
        
    if len(importObjectsAddress)>1:
        operant_dict["importObjects"] = {"importObjects":{"importObjects":importObjectsAddress[0]}} 
    
    
    

    return operant_dict.copy()

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
            #print("NEW:  ",values)
            for partname,part_values in values.items():
                 
                joiner:list = [x for x in part_values.values() if x!=""]
                #print(partname,":",joiner) if partname in ["da"] else ""
                part_string:str = ""
               #If joiner list is empty
                if joiner==[]:
                    part_string:str = partname
                else:
                    partname_clean = re.match(r"^[a-z]{1,2}",partname).group(0)
                    match partname_clean:
                        case "r"|"m"|'t'|'s'|'a'|'b'|'c'|'d'|'w'|'x'|'e'|'y'|'z'|'v'|'f': 
                            if joiner == ["00"]:
                                #If the part value is empty, then it shoes ["00"] as a value. This  is removed if we want an empty values. 
                                #Eg. only r00 is return as part string if this condition is true
                                part_string:str = partname
                            else:    
                                part_string:str = partname +".".join(joiner) 
                               #print(part_string, joiner)
                        case 'xm'|'xr':
                            part_string:str = partname +"."+".".join(joiner)
                        case 'dh': 
                            part_string:str = partname +".".join(joiner)   
                            #print(part_string,joiner)
                        case'da':
                            #da is Body colour. It only has 1 value thta can be from 0-9 or a hexdecimal colour value.
                            part_string:str = partname + joiner[0]
                            #print(part_string,joiner)
                        case _:
                            #print(partname,":",joiner) if partname in ["og","ab","ac"] else ""
                            part_string:str = partname_clean + ".".join(joiner)
                    
                
                output+= part_string + "_" 
                del joiner
       
        #match Version_ then atleast 2 digits
        output = Version + "**" + output
        output = output.rstrip("_")
        output = output+Imported_objects
        #print(output)
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
        print(self.convertdict["Snatcher golem"]["Tan"]["da"])
        self.compare:str = compare
        print("compare_dict")
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
        
        menuOptions:list[list[str]] = list()
        partOptions:list[list[str,str]] = list()
        labelOptions:list[list[str,str,str]] = list()
        labelEmptyVals:list[list[str,str,str]] = list()
        
        
        label_name_dict:list[list[str,str,str]] = list()
        
        #Break dictionary into 3 ordered lists
        #print(self.comparedict)
        for menukey in compare_dict:
                for partkey in compare_dict[menukey]:
                        for labelkey in compare_dict[menukey][partkey]:  
                                label_name_dict.append([menukey,partkey,labelkey])
       

        for menukey,menuvalue in compare_dict.items():
            for partkey,partvalue in menuvalue.items():
                for labelkey,labelvalue in partvalue.items():
                    if labelvalue!= "":  
                        menuOptions.append([menukey]) if [menukey] not in menuOptions[:] else ''
                            
                    labelOptions.append([menukey,partkey,labelkey])
                    partOptions.append([menukey,partkey]) if [menukey,partkey] not in partOptions[:] else ''
                    
                    

        #for x,y,z in  labelOptions
        #    print(x,y,z, sep="||") if compare_dict[x][y][z] != "" else ""                      
        label_compare_list = labelOptions[:]
        #print()
        #print(labelEmptyVals)
       # print(partOptions)
        #print(compare_dict_popped_labelvalues)
        
        
        def regsearch(Options_list:list[str],list_length:int,inputname:str = "menu"):    
            menu_excluded = []
            Options = Options_list[:]
            Options_clean = list(map(itemgetter(list_length),Options))
            
            while True:
                print(menu_excluded)
                print("            ") 
                menuInput = input(f"""NAMES:  {Options}  
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
                    menu_choice = input(f"""      VALUES : 
{list(enumerate(menuregex,start=1))}
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
                    
            
            return menu_excluded,Options
        #cleaning the lists
        
        menu_exclude,a = regsearch(menuOptions,0,"menu")
        del a
        print(menu_exclude)
        
    
        
        
        [partOptions.remove(x) 
        for x in partOptions[:] 
        if x[0] not in menu_exclude]
        
        
        part_exclude,a= regsearch(partOptions,1,"part")
        del a
        print(part_exclude)
    
        
 
        [labelOptions.remove(x)
        for x in labelOptions[:] 
        if x[1] not in part_exclude]

        
        label_exclude,labelOptions = regsearch(labelOptions,2,"label")
        print(label_exclude)    
        


        #print(labelEmptyVals)
  
        
        
        list_of_strings = []
        for key in self.convertdict:
            print(key) 
            for menukey,partkey,labelkey in label_name_dict:
                #Check if there are partkeys to be excluded that don't have associaed labelkeys. If so, stop excution immediatley. 
                """if partkey in part_exclude and labelkey in label_exclude:
                    print(menukey,partkey,labelkey,sep="||")
                    continue"""

                #update the values in the convert_dict    
                if labelkey not in label_exclude: 
                    #print(menukey,partkey,labelkey,sep="||")
                    if partkey not in self.convertdict[key][menukey]:
                        convert_objects_dict[key][menukey][partkey] = {}

                    convert_objects_dict[key][menukey][partkey][labelkey] = compare_dict[menukey][partkey][labelkey]
                """elif partkey in part_exclude:
                    print(menukey,partkey,labelkey,sep="||")
                    pass """
            #print(convert_objects_dict[key])                
            #print(labelOptions)
            convert_objects_dict[key].update({'importObjects':importObjects}) if 'importObjects' in compare_dict else ''
            convert_objects_dict[key].update({"ver":version})
            list_of_strings.append(dict_to_KKLCode(convert_objects_dict[key]))
                
       
        return list_of_strings        


        """for key in self.convertdict.keys():
            for labels in label_name_dict:
                if labels[0] in menu_exclude:
                    for partkey,partvalue in compare_dict[labels[0]].items(): 
                            for labelkey,labelvalue in partvalue.items():
                                #print(labelkey,labelvalue)
                                if partkey not in part_exclude and labelkey not in label_exclude:
                                    convert_objects_dict[key][labels[0]][partkey] = compare_dict[la]labelvalue  
                     
                     
            
                if not bool(convert_objects_dict[key][labels[0]].get(labels[1])):
                    #print("No part key for =",labels[1] )
                    convert_objects_dict[key][labels[0]][labels[1]] = {}
                if labels[2] not in label_exclude:
                    #print(labels)
                    convert_objects_dict[key][labels[0]][labels[1]][labels[2]] = compare_dict[labels[0]][labels[1]][labels[2]]
        """    

        
        
        

        




                              
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

#[print(y,":",x,":",x==y) for x,y in zip(working_Object.convertdict["SiegeGolem"]["BodyHeight"]["ca"].keys(),working_Object.KKL_Parts_Names["ca"])]
#print(dict_to_KKLCode(output))


#print(dict_to_KKLCode(working_Object.comparedict))



out = list(zip(Id,names,codes,output,convertor_list))

try:

    with open(path.join(current_dir,"KKLcode loader and dumper.csv"),"w",newline="") as f:
        rows = writer(f,dialect="excel",delimiter=",")
        rows.writerow(header)
        rows.writerows(out)
except PermissionError:
    input(f"""'''CLOSE THE GODDAMN CSV FILE OR SO HELP GOD.....
          
          
          
          Sorry, got heated a bit there.Close the CSV and then press Enter.'''""")
finally:
    with open(path.join(current_dir,"KKLcode loader and dumper.csv"),"w",newline="") as f:
        rows = writer(f,dialect="excel",delimiter=",")
        rows.writerow(header)
        rows.writerows(out)

