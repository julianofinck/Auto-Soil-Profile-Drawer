@REM Set the path to the Python interpreter
set PYTHON="python"

@REM Set the path to the main script
set SCRIPT="template\translate_csv_2_acad_drawing.py"

@REM Call the Python interpreter on the main script
%PYTHON% -B %SCRIPT%

@REM Wait for the user to press a key before closing the window
pause

