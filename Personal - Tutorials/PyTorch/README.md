# Description
This tutorial consists of basic PyTorch tutorials. It consists of a series of videos:
   * part_1: https://www.youtube.com/watch?v=BzcBsTou0C0
   
The series provides the basics of using Pytorch.

## Tools used:
   * Python
   * PyTorch
   
## Methodology

## Reproducing the results:
Note: the tutorial was followed on a windows machine, thus the steps might not translate 
1:1 to linux or MacOS. My apologies! Installment of docker is assumed. If this is not installed
on the machine, tutorials are widely available on the web.

	*step 1: Open the terminal.
	*step 2: Navigate to the directory including the Dockerfile and docker-compose.ylm, probably ./Pytorch
	*step 3: docker build . -t custom_notebook
	*step 4: docker run -p 8888:8888 -t .:custom_notebook . [OR: docker-compose up]
	*step 5: paste the url to your browser of choice, I picked chrome.
	*step 6: import the jupyter notebook of choice.
Congratulations, you can now rerun the cells using the docker container!

## Result snapshot


