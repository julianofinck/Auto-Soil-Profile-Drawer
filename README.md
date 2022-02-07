## Auto-Soil-Profile-Drawer
#### Why?
> Drawing borehole profiles on AutoCAD was too time-consuming in the company. 
#### How was the problem solved?
> AutoCAD's command "script" allowed some time-optimization (2-3 days of work could be reduced to some minutes). Coworkers now fill "1_title_block.csv" with client and project information and "2_borehole_data.csv" with the field data, run "run.bat", which calls interpret.py. Python interprets the data, translates it into the syntax of AutoCAD and saves in "4_script_borehole_acad.scr". On AutoCAD, one must select the "No Template-Metrics" and click on "Start Drawing", use the "script" command, and navigate to "4_script_borehole_acad.scr". The borehole profiles will be drawn.
#### What did you learn?
> I learned how to automatise drawings on AutoCAD and that by running a ".py" from a ".bat" allows me to read any eventual error straight on screen. I developed this tool still in my first month of work and received a big compliment from my boss at the time.
---
#### FIRST TIME USING IT?
1. "Let AutoCAD know where are the Hatches and the CTB (Color Dependent Plot Style)"
```
On AutoCAD, type "_OPTIONS", go to "Files"
    Under "Support File Search Path",
        add a new path to where the hatches files are stored. (teamplate\hatches\)
    Under "Printer Support File Path > Plot Style Table Search Path",
        add a new path to where the ctb file is stored.   (teamplate\ctb)
```
2. Set your OS' list separator to ";"
```
Control panel > Region > Additional settings... > list separator -> ;
```
3. Make sure you have a python.exe set as an environmental variable in PATH
```
Control panel > System > Advanced system settings > Environment Variables
Under "User variables", select "Path" > Edit > New > 
Type the path to your python.exe
Move this path to the top of the list
```
---
#### INSTRUCTIONS:
1. Create a folder in past_projects and copy "1_title_block.csv" and "2_borehole_data.csv" to it.
2. Fill both csv. Copy them to the root "Auto-Soil-Profile-Drawer\", overwriting the existent ones.
3. Run "run.bat" (if any error occurs, check both csv)
4. Start a new drawing with "No Template-Metric" teamplate on AutoCAD, use "script" command, select "4_script_borehole_acad.scr"
5. Double-check for minor adjustments, like the figure number in each title.
6. Use publish to export all figures in a single .pdf
- ¹When filling both csv, mind the formatting: point as decimal sepator, comma as elements separator, semicolon as list separator, and brackets to certain variables
- ²Topo liso above ground must be written negative.

---
#### EXPLANATION TO FILES AND FOLDERS:
##### Files:
- **1_title_block.csv**\
_Generic information (client and project)_
- **2_borehole_data.csv**\
_Field data of the boreholes_
- **3_run.bat**\
_Used to run python_
- **4_script_borehole_acad.scr**\
_File to be read in AutoCAD via "script" command.(several lines of telling what AutoCAD must draw)_
- **LICENSE**\
_License in GitHub_
- **README.md**\
_This readme_
##### Folders
- **past_projects\\**\
_directory to keep data from past projects_
- **teamplate\\**\
_directory where .py and teamplate are stored_