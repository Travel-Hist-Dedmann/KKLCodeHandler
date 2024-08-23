My first real python project. I will appriciate harsh criticism since I am still new. 



The main.py file automatically converts KKL codes to a reference a convertor code. You can exclude parts of the code that you want preserved. For example, if you want to copy an eye shape enmass but want to preserve the eye colours of the characters being changes, this is what you need.

***Components***
#Jsons used as general refrence.
1) KKL_Menu_names.json
2) KKL_Parts_Names.json

#CSV where the results of the con=nversion will appear.
3) KKLcode loader and dumper.csv

#Code. Please critique if you are able.
4) main.py

******ONLY SUPPORTS CODES FOR KKL 108, DOES NOT SUPPORT ALLCODES RIGHT NOW*****
Please import your character into KKL version 108 and then export it to use. It does support imported images, as long as they are imported from web or you have the images with  

***How to use
1) Open the "KKLcode loader and dumper.csv".Copy the codes you want to convert under the **Input column**, below the headings.
**Make sure to fill out the Name column(You can simply number the Name column. Ensure the columns are of same Length.)**. You can ignore the id column if you wish, but I will judge you.

2) Next, paste the string containing the character you want to convert to the place shown (E2). For ease, I recommend exporting only the relevant parts of the convertor string. *For example*, If I only want to change the eye color of the characters, I will select the Eye tab and export only that.
Then I can exclude everything but eye color.

3) **Close the CSV file after saving.**

4) Now run the program by double clicking it or through commandline. **The Choice you choose next will be excluded from the conversion.**

5) **The program will ask you to type in a choice from the given list**(*Case is ignored.*). It will also try to match you inputs by order of letters, so feel free to only type parts of the word. 
**Press enter to confirm.Leave empty to move to next step** 
Eg: a)[[Pose],[FootPose],[Eye],[Hair]....]
    b)[[Pose,aa],[Pose,ab],.....]
    c[[Pose,aa,LeftArmLength_0],.....]

6) Now, a list of numbered matches will be shown. Type in the number  of the option you want and press enter to confirm. **Here, you can make multiple choices. Leave empty and press enter to continue. You will return to the above choice.**   
Eg:*for "foot"  typed=*
    [(1,Pose),(2,FootPose)]

7) This process will repeat 2 more times. 

8) Once the process ends, your output will be added to the output column in the Csv, with the character converted except for the exclusions you have made. Enjoy.


**Notes**
Please give me critcism. From code improvements to advice on writing quality help docs.  
Use it for whatever, alter it if you want.

Special Thanks to KisekaeJade for the explaination of how the Save system works, and also for stopping me from chasing deadends.

