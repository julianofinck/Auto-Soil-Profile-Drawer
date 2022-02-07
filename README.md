# Auto-Desenhar-Perfil

> Why?
It used to take a long time to prepare figures from boreholes on AutoCAD in the company. Once I
learned from the command "script" on AutoCAD, I realised I could bring much to the company.

> How was the problem solved?
This tool reduced a work of 2-3 days to some minutes. Since then, instead of drawing on AutoCAD,
coworkers can fill a default "borehole_data.csv" with the field data and run "run.bat", which
then calls "Padrao\interpret.py". "interpret.py" translates what it finds in "borehole_data.csv"
to AutoCAD syntax, creating "perfil.scr". On AutoCAD, one must select the "No Template-Metrics" and
click on "Start Drawing", type scr, hit enter and navigate to "perfil.scr".

> What did you learn?
Developing this tool, I learned that I can automatise drawings on AutoCAD and that using ".bat" 
to run a ".py", I can read any error straight on screen. I developed this tool still in my first
month of work and that made my first stating "Now I am 100% sure I made the right choice choosing you"
----------------------------------------------------------------------------------------------------------
FIRST TIME USING THE TOOL: 
"Let AutoCAD know where are the Hatches and the CTB (Color Dependent Plot Style)"

On AutoCAD, type "_OPTIONS", go to "Files"
     Under "Support File Search Path", 
             add a new path to where the HATCES files are stored. (Padrao\HATCHES)

     Under "Printer Support File Path > Plot Style Table Search Path",
             add a new path to where the CTB file is stored.   (fica em PADRAO\PENA)
----------------------------------------------------------------------------------------------------------
INSTRUCTIONS:

 PREPARAR DADOS
(1) Preencha "DADOS.xlsx" (obs¹), salve como .csv (15a opção)
  * Na ausência do NA estabilizado, usar os do FT-01 de água.
(2) Preencha "INFO_GERAIS.txt"	(Informação do projeto, do cliente, escala, sist de coordenadas)

 PROCESSAMENTO
(3) Abra "1. Perfil v1.py" com python.exe (clique em Propriedades e navegue até o python.exe na pasta do Python)

 CONFERIR ENTRADAS
(4) Havendo avisos de erros, volte para (1) e revise "DADOS.xlsx".

 AUTODESENHAR
(5) Abra AutoCAD, digite "scr", enter, selecione perfil.scr

 AJUSTES FINAIS
(6) Checar se o desenho está correto, fazer pequenos ajustes e adicionar granulometria

 GERAR PDF PARA FIGURAS/IMPRESSÃO
(7) Ctrl+P em cada Layout, salvar como .pdf (já está configurado pela rotina o tipo de exportação). Combinar em um .pdf único.
    Alternativamente, digite PUBLISH, remova Model, desmarque "include plot stamp", clique publish (não precisa salvar lista de plotagem)

   *NÃO NECESSÁRIO, mas se quiser visualizar com as cores de impressão, clicar com botão direito em cada aba de Layout, "modificar/modify", marcar "plot with style"
 
 PRONTO!

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

------------------------------------------------------------------------------------------------------------------------------------------------
control panel (view by> category)
change the date, time or number formats
additional settings
list separator -> ;