@echo off
REM Define the number of times you want to run the script
set NUM_RUNS=50

REM Create or truncate the output CSV file
echo Output > output.csv

REM Loop to run the script multiple times
for /L %%i in (1,1,%NUM_RUNS%) do (
    echo Running iteration %%i...
    python main.py >> output.csv
)

echo All iterations completed.

