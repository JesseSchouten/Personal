cd "C:/Users/Jesse/Anaconda3"
call condabin\activate.bat
cd C:\Users\Jesse\OneDrive\Bureaublad laptop Jesse\Beleggen\data
cmd.exe /c python get_yahoo_data.py --load_daily_stats True 2>> std_output_errors.log
