# IR-From-Real-Data

This is an queryable index built using my youtube search history as the corpus and TF-IDF for retrieval.

Presentation [Link](https://docs.google.com/presentation/d/1JP4ePJKuDL1_OLdN8UUiXaqD-wTPbrmYDQlTBEjzUfQ/edit?usp=sharing)

Author: Nathan Kirk (nkirk.tech@gmail.com)
License: GPL-3.0 license

## Project Structure

The src folder contains all python files and tests, the data folder contains json and pickle data files. The runner files are used to run
the program, the other files are there to help set up the project (data_maker.py) or help structure how the index is calculated and stored
(models.py).

## How to use this software

The main branch is a fully functioning local version, the shooting for the clouds branch is adapted to run on google cloud for bigger data sets. 
To run the main branch create a run config that passes in path to the pickle file, then enter the search term of your choice in the console. 
The results will be limited because it is based on a small dataset of 300 videos that I watched. The more interesting branch is the cloud capable one.
The cloud runner file takes in file paths to a google bucket for json input and pickle file output. Once the pickle file is created it can be passed
into the regular runner file and takes in search terms from the user in the terminal. The current way that it is set up will not work in the future
if my educational account is closed, which will likely happen when I graduate in 2025, but paths to another cloud bucket could be passed in.

### Citations

The fetch_video_info script was written entirely by ChatGPT with the prompt "write me a function that will grab the title, description,
channel name and tags given a youtube url"

I heavily utilized google's documentation to understand how to use Pyspark, Dataproc, and Bucket.
Data was collected through Google's Takeout, and added to with the Youtube API.

Prototype.py is from Professor Mike Ryu at Westmont College.
