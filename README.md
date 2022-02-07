# Auto-Soil-Profile-Drawer
> Why?
Drawing borehole profiles on AutoCAD was too time-consuming in the company. 

> How was the problem solved?
AutoCAD's command "script" allowed some time-optimization (2-3 days of work could be reduced to some minutes).
Now coworkers fill "1_title_block.csv" with client and project information and "2_borehole_data.csv" with the
field data, run "run.bat", which calls interpret.py. 
Python interprets the data, translates it into the syntax of AutoCAD and saves in "4_script_borehole_acad.scr".
On AutoCAD, one must select the "No Template-Metrics" and click on "Start Drawing", use the "script" command,
and navigate to "4_script_borehole_acad.scr". The borehole profiles will be drawn.

> What did you learn?
I learned how to automatise drawings on AutoCAD and that by running a ".py" from a ".bat" allows me to read 
any eventual error straight on screen. I developed this tool still in my first month of work and received a 
big compliment from my boss at the time.
----------------------------------------------------------------------------------------------------------
> First time using this tool?
1. "Let AutoCAD know where are the Hatches and the CTB (Color Dependent Plot Style)"
On AutoCAD, type "_OPTIONS", go to "Files"
     Under "Support File Search Path", 
             add a new path to where the HATCES files are stored. (Padrao\HATCHES)

     Under "Printer Support File Path > Plot Style Table Search Path",
             add a new path to where the CTB file is stored.   (fica em PADRAO\PENA)

2. Set your OS' list separator to ";"
On Control panel > Region > Additional settings... > list separator -> ;

3. Make sure you have a python.exe set as an environmental variable in PATH
----------------------------------------------------------------------------------------------------------
INSTRUCTIONS:
 Create a folder in past_projects and copy "1_title_block.csv" and "2_borehole_data.csv" to it.
 Fill both csv. Copy them to the root "Auto-Soil-Profile-Drawer\", overwriting the existent ones.
 Run "run.bat"
 If any error occurs, check both csv
 Start a new drawing from "" teamplate on AutoCAD, use "script" command, select .scr
 Double-check for minor adjustments, like the figure number in each title.
 Use publish to export all figures as one .pdf
 DONE!
	obs¹ Ao preencher, atente ao ponto como separador decimal, vírgula como divisor de elementos, e eventuais colchetes.
	obs² Topo liso acima do solo é digitado com valor negativo.

----------------------------------------------------------------------------------------------------------
O QUE É CADA ARQUIVO??

DADOS ANTIGOS
 Cada novo projeto tem sua pasta. Dentro de cada pasta há um "DADOS.csv" e um "INFO_GERAIS.txt"

PADRAO
 Aqui ficam salvos o logo, os padrões de pena para impressão, e as hachuras que utilizamos.
 Para adicionar as hachuras, abra o AutoCad, digite _OPTIONS, enter. Na aba "Files", clique sobre "Support File Search Path", na direita clique em "Add..." e depois "Browse...", selecione a pasta das hachuras.
 Para mim o caminho é "T:\Tecnico POA\Projetos\1_AutoDesenhar\PADRAO\HATCHES". Pode fechar as opções.

1. LEIAME
 Esse arquivo

2. Python 3.bat 
 É um arquivo com comandos simples em DOS: (1) Abrir Python nessa pasta; (2) rodar rotina perfil.py; (3) manter o prompt aberto para leitura)

DADOS.csv
 Derivado do .xlsx

DADOS.xlsx
 Preenchido com as informações dos perfis

INFO_GERAIS
 Preenchido com as informações do projeto

perfil.py
 É a rotina de programação, onde as ordens de processamento estão armazenadas: "ler CSV -> interpretar no Python -> salvar como .scr do AutoCAD"

perfil.scr
 Produto de saída do processamento que será aberto no AutoCAD via comando SCRIPT.
 (Em suma, diversas linhas de comandos para o AutoCAD desenhar nossos perfis)