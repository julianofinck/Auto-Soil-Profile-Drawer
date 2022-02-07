# Auto-Soil-Profile-Drawer
##### Why?
> Drawing borehole profiles on AutoCAD was too time-consuming in the company. 

###### How was the problem solved?
> AutoCAD's command "script" allowed some time-optimization (2-3 days of work could be reduced to some minutes). Coworkers now fill "1_title_block.csv" with client and project information and "2_borehole_data.csv" with the field data, run "run.bat", which calls interpret.py. Python interprets the data, translates it into the syntax of AutoCAD and saves in "4_script_borehole_acad.scr". On AutoCAD, one must select the "No Template-Metrics" and click on "Start Drawing", use the "script" command, and navigate to "4_script_borehole_acad.scr". The borehole profiles will be drawn.

###### What did you learn?
> I learned how to automatise drawings on AutoCAD and that by running a ".py" from a ".bat" allows me to read any eventual error straight on screen. I developed this tool still in my first month of work and received a big compliment from my boss at the time.
----
##### First time using this tool?
###### 1. "Let AutoCAD know where are the Hatches and the CTB (Color Dependent Plot Style)"
	On AutoCAD, type "_OPTIONS", go to "Files"
	     Under "Support File Search Path", 
	             add a new path to where the HATCES files are stored. (Padrao\HATCHES)
	
	     Under "Printer Support File Path > Plot Style Table Search Path",
	             add a new path to where the CTB file is stored.   (fica em PADRAO\PENA)
	
	2. Set your OS' list separator to ";"
	On Control panel > Region > Additional settings... > list separator -> ;
	
	3. Make sure you have a python.exe set as an environmental variable in PATH
----
##### INSTRUCTIONS:
1. Create a folder in past_projects and copy "1_title_block.csv" and "2_borehole_data.csv" to it.
2. Fill both csv. Copy them to the root "Auto-Soil-Profile-Drawer\", overwriting the existent ones.
3. Run "run.bat" (if any error occurs, check both csv)
4. Start a new drawing from "" teamplate on AutoCAD, use "script" command, select .scr
5. Double-check for minor adjustments, like the figure number in each title.
6. Use publish to export all figures in a single .pdf
	obs¹ Ao preencher, atente ao ponto como separador decimal, vírgula como divisor de elementos, e eventuais colchetes.
	obs² Topo liso acima do solo é digitado com valor negativo.

---
##### Explanation for files and folders:
###### Files:
- 1_title_block.csv\ Generic information of the client and project
- 2_borehole_data.csv\ Field data of the boreholes
- 3_run.bat\ Used to run python
- 4_script_borehole_acad.scr\File to be read in AutoCAD via "script" command.
(several lines of telling what AutoCAD must draw)
- LICENSE\License in GitHub
- README.md\This readme
###### Folders
- past_projects\\\
directory to keep data from past projects
- teamplate\\\
directory where .py and teamplate are stored