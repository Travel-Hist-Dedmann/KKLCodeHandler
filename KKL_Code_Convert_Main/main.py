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
    KKL_Menu_Names_reversed:dict ={}
    for  key,value in KKL_Menu_Names.items():     
        for i in value:
                KKL_Menu_Names_reversed[i] = key 
    
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
    
    for i in operant_list:
        
        alphaNum:str = re.search(alphaNum_regex,i).group()  
        #if the part value is alphabet + number, change into alphabet + "." + number
           
        alpha = re.search(r"[a-z]{1,2}",alphaNum).group(0)    
        numa_a   = re.search(r"[0-9]+",alphaNum)
           
        if numa_a != None: 
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
            case  'xm'|'xr':
                dot_added_alphaNumeric = f"{alpha}{num}.{num}"
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                alphaNum = f"{alpha}{num}"
            case 'dh'|'da':
                alphaNum1,alphaNum2 = alphaNum[:2],alphaNum[2:]
                dot_added_alphaNumeric = f"{alphaNum1}.{alphaNum2}"
                
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
            case _:
                dot_added_alphaNumeric = f"{alpha}.{num}"
                i:str = i.replace(alphaNum,dot_added_alphaNumeric)
                alphaNum = f"{alpha}"
    
            #Split element i of operant list by "."    
        
       
        i = i.split(".")
        part_dict_name:str = re.sub(r"[0-9]+", "", i[0])
         
        
        part_vals:list = i[1:]
        
        part_val_names = KKL_Parts_Names[part_dict_name][:]
        
        #print(part_val_names)
        """if len(part_dict_name)<=2 and len(part_dict_name)>0:    
            
            part_val_names = KKL_Parts_Names[part_dict_name][:]
        elif len(part_dict_name)>2 and len(part_dict_name)<=3:
            print(part_dict_name)
            part_val_names = KKL_Parts_Names[part_dict_name[0]][:]
        elif len(part_dict_name)>3:
            print(part_dict_name)
            part_val_names = KKL_Parts_Names[part_dict_name[0:1]][:]
        else:
            print("Found problem" +part_dict_name)
            continue """
        
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
                partname = re.sub(r"[0-9]+","",partname)
                part_string:str  = ".".join(joiner)
                output      += partname+ part_string + "_"

       
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
            if bool(menuvalue):  
                menuOptions.append([menukey])
            for partkey,partvalue in menuvalue.items():
                if bool(partvalue):
                    partOptions.append([menukey,partkey])
                for labelkey,labelvalue in partvalue.items():
                    if bool(labelvalue):
                        labelOptions.append([menukey,partkey,labelkey])           
                                    
        
        
        def regsearch(Options:list[str],list_length:int,inputname:str = "menu"):    
            menu_excluded = []
            Options_clean = list(map(itemgetter(list_length),Options))
            
            while True:
                print(menu_excluded)
                 
                menuInput = input(f"""1){Options}  
                                Choose {inputname} names. """)
                if menuInput =="":
                    break
                
                menuregex = re.findall(r"[a-z0-9_]{0,}"+menuInput+r"[a-z0-9_]{0,}","~".join(Options_clean),re.IGNORECASE) 
                if menuregex == []:  
                    print("Value not found.")
                    
                    continue
                while len(menuregex)>0:    
                    menu_choice = input(f""" {list(enumerate(menuregex,start=1))}
                    Choose option by index(integer only): """)
                    if menu_choice == "" or not menu_choice.isnumeric() or int(menu_choice)>len(menuregex):
                        print("Input Outside of expected value, restart." )
                        
                        break
                    menu_choice = menuregex.pop(int(menu_choice)-1)
                    
                    #Regex helper
                    remove_index = Options_clean.index(menu_choice)
                    Options_clean.pop(remove_index)
                    Options.pop(remove_index)
                    menu_excluded.append(menu_choice)
                    
                    
                    
                        
                        
                
            
            return menu_excluded
        #cleaning the lists
        
        menu_exclude = regsearch(menuOptions,0,"menu")
        print(menu_exclude)
        
        [partOptions.remove(x) for x in partOptions[:] if x[0] not in menu_exclude]
        
        
        part_exclude = regsearch(partOptions,1,"part")
        print(part_exclude)
        
        [labelOptions.remove(x) for x in labelOptions[:] if x[1] not in part_exclude]        

        label_exclude = regsearch(labelOptions,2,"label")
        print(label_exclude)    


         
        menuOptions =  [x for x in list(map(itemgetter(0),menuOptions)) if x not in menu_exclude]
        partOptions =  [x for x in list(map(itemgetter(1),partOptions)) if x not in part_exclude]
        labelOptions = [x for x in list(map(itemgetter(2),labelOptions)) if x not in label_exclude]
      
       
        
        list_of_strings = []      
        count = 0
        for key in self.convertdict.keys():
            count+=1
            for menukey,menuvalue in compare_dict.items():
                if menukey in menuOptions: 
                    convert_objects_dict[key][menukey] = compare_dict[menukey]
               
        
                for partkey,partvalue in menuvalue.items():
                    
                    if partkey in partOptions:
                        convert_objects_dict[key][menukey][partkey] = compare_dict[menukey][partkey]
                    
                       
                    for labelkey,labelvalue in partvalue.items():
                        
                        if labelkey in labelOptions:
                            convert_objects_dict[key][menukey][partkey][labelkey] = compare_dict[menukey][partkey][labelkey]
                        
                            
                            
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
code = ["108**aa11.350.1.0.50.19.60.0.3.72.0.0_ab41.57.58.49_ac29.57.56.21_ba50_bb5.1_bc675.510.8.0.1.0_bd5_be1800_bi0.0.100.100_bf_bg_bh1_ca590.13.590.590.350.450.80.400.560.0.70.80.1.1_cc500.500.500.500.500.500.500.500.1.1.0.0_cd500.500.500.500.500.500.500.500.1.1.0.0_ce500.500.500.500.500.500.500.500.1.1.1.1_cf0.500.500.500.500.0.500.500.500.500.1.1.1.1_cg0.500.500.500.500.0.500.500.500.500.1.1_ch0.500.500.500.500.0.500.500.500.500.1.1_da8_db_dd0.0.340.500.500.500.1.1_dh8.30.50.50.4_di10_qa6.8.8.50.50.5.0.0.0.50.11.0.1.50.50.50.50_qb1.100_dc_eh_ea9.25.25.56.0.0_ec4.500.25.25.56.470.620.0_ed25.0.1.1.25.56_ef_eg_r00_fa1.500.500.610.350.65.473F30.0_fb7_fh_fk136_fc0.43.55.0.43.55.500.61.61.500.500.500_fj0.0.0_fd1.0.50.25.56.75.50_fe50.61_ff0000000000_fg0.50.56.0.0.1.0.0_fi_pa0.0.0.0.40.50.85.85.0.0_t00_pb7.25.26.50.0_pc_pd_pe2.25.26.0.2.0.53_ga0_gb1.0.10.40.65_gc1.0_ge0000000000_gh0_gf_gg_gd000000_ha92.92_hb490.1.500.990.990.490.500_hc1.54.10.1.54.10.500.500_hd4.1.590.690.2.600.500.50.1.61_ad0.0.0.0.0.0.0.0.0.0_ae1.0.0.0.0_ia_if6.55.55.19.1.2.49.0.2.49.0.0.0.1.0.0.0.0.1.0.0.0.0.0_ib_id_ic_jc_ie8.57.57.57.1.55.19.0.1.55.19.0.0_ja15.55.2.0_jb15.55.2.0_jf_jg_jd0.55.55.57.0.19.0.0_je0.55.55.57.0.19.0.0_ka_kb_kc_kd_ke_kf_kg_la_lb_oa_os_ob_oc_od_oe_of_lc_m00_s00_og_oh_oo_op_oq_or_om_on_ok_ol_oi19.55.60.0.1_oj19.55.60.0.1_f00_fv1.0"]
compare = "108**aa7.0.0.8.50.7.0.0.0.50.0.0_ab36.24.55.0_ac_ba50_bb5.1_bc150.510.4.0.1.0_bd5_be1800_bi0.0.100.100_bf_bg_bh1_ca510.0.450.510.340.340.34.0.0.0.60.80.1.1_cc500.500.500.500.500.500.500.500.1.1.0.0_cd500.500.500.500.500.500.500.500.1.1.0.0_ce500.500.500.500.500.500.500.500.1.1.1.1_cf0.500.500.500.500.0.500.500.500.500.1.1.1.1_cg0.500.500.500.500.0.500.500.500.500.1.1_ch0.500.500.500.500.0.500.500.500.500.1.1_da1_db_dd0.0.340.500.500.500.1.1_dh1.30.50.50.0_di5_qa_qb_dc0.1.1.1.1.0_eh4.32.100_ea11.32.32.56.0.0_ec2.500.32.32.56.380.620.0_ed20.1000.1.1.32.56_ef_eg_r00_fa0.500.500.500.500.65.56.0_fb7_fh_fk_fc0.18.55.0.18.55.500.61.61.500.500.500_fj0.0.0_fd1.0.50.32.56.75.50_fe50.61_ff0000000000_fg0.50.56.0.0.1.0.0_fi_pa0.0.0.0.40.50.85.85.0.0_t00_pb_pc_pd_pe_ga0_gb1.0.10.40.65_gc0.0_ge0000000000_gh0_gf_gg_gd000000_ha92.92_hb490.1.500.990.990.490.500_hc0.59.390.0.59.390.500.500_hd0.1.590.550.2.600.500.50.1.61_ad0.0.0.0.0.0.0.0.0.0_ae1.0.0.0.0_ia_if_ib_id3.55.55.19.0.0.1.30.55.0.30.55.0.26.0.0.0.0.1.0.0.0.0.0_ic_jc_ie_ja9.55.18.55_jb9.55.18.55_jf_jg_jd5.59.59.54.1.53.0.0_je5.59.59.54.1.53.0.0_ka8.55.55.33.0_kb8.55.55.33.0_kc_kd_ke_kf_kg_la_lb_oa_os_ob36.57.0.0_oc_od_oe7.55.60.55.0_of_lc_m00_s00_og_oh_oo_op_oq_or_om_on_ok_ol_oi_oj_f00_fv1.0"
working_Object = KKLCodeCovertor_Object(compare,["Sable"],code)

output = working_Object.help("Pose")

"""
with open(path.join(current_dir,"KKLcode loader and dumper.csv"),"r",newline="") as f:
    file = reader(f,delimiter=",")
    header = next(file)
    rows = []
    Id,names,codes,output,convertor_list =[],[],[],[],[] 
    for i in file:
        rows.append(i)

Id = list(map(itemgetter(0),rows))
names= list(map(itemgetter(1),rows))
codes= list(map(itemgetter(2),rows))
output = list(map(itemgetter(3),rows))
convertor_list= list(map(itemgetter(4),rows))
convertor = convertor_list[0]





working_Object = KKLCodeCovertor_Object(convertor,names,codes)

output = working_Object.convert()



out = list(zip(Id,names,codes,output,convertor_list))
try:
    with open(path.join(current_dir,"KKLcode loader and dumper.csv"),"w",newline="") as f:
        rows = writer(f,dialect="excel",delimiter=",")
        rows.writerow(header)
        rows.writerows(out)
except PermissionError:
    input("Close the csv file or this won't work. ")"""





