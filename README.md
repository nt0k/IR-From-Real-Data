# IR-From-Real-Data

This is an queryable index built using my youtube search history as the corpus and TF-IDF for retrieval.


### Data

I used google takeout for 3 of my gmail accounts to get json data on my youtubw watch history from 2016-2023. I got additional data
for each video using the youtube API with a script that chatGPT wrote for me (fetch_video_info). I did not know how to use the
API so chatGPT was a big help for that task.

### Implementation

Using previous code from another assignment, I built an index with a TF-IDF Matrix of Vectors for each term. The matrix is stored
in a pickle file, running main with arguments for number of threads and location of the pickle file will ask for input to search
for in the corpus and then return the ten most relevant documents.

### Running on the cloud
