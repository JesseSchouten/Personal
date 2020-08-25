cd "C:/Users/Jesse/Anaconda3"
call condabin\activate.bat
cd C:\Users\Jesse\OneDrive\Bureaublad laptop Jesse\Beleggen\data
runas /profile /env /user:Jesse /savecred "cmd.exe /c python get_yahoo_data.py 2>> std_output_errors.log"
