Board Games: PLay Next App
---
## Description
The Play Next app for board games provides a "recommendation engine" (based on cosine similarity vectors) 
to help gamers find their next favorite game based on something they're enjoying now. Built on the open-source data provided 
by BoardGameGeek.com and hosted as a dataset on Kaggle.com from Jesse van Elteren (found [here](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews/data), please look for the 2025 update), 
my app allows the user to find games with mechanics overlap, flavored with game category information, the weight of the game (complexity), 
and a few spices of my own.

---
### Data Model

The Play Next app runs on a machine learning model I developed as a project for my Computer Science degree. The model uses vectorized 
data from the dataset (board game categories, mechanics) as well as a tagging system I developed, stored as TF-IDF vectors in sparce matrix form. 

The model also integrates normalized (using Min-Max scaling) numeric data from the BGG database including average weight of the game (scale of 1-5 
before normalization), average playing time, and potentially minimum or maximum player count.

There are 3 versions of the model at present, and two are integrated into the app: a mechanics-heavy model where the overlap in mechanics drives 45% 
of the recommendations, and an "original recipe" that I developed early on which offers a wider list of results with less precision. I prefer the 
mechanics-weighted model, but the app can fall back to the original recipe if a game is not generating a lot of recommendations. 

----
### Dataset and Pre-processing

##### Data Source
Kaggle.com: from Jesse van Elteren found [here](https://www.kaggle.com/datasets/jvanelteren/boardgamegeek-reviews/data)

Please use the file explorer to locate the file labeled games_detailed_info2025.csv for the raw dataset that I cleaned and processed 
before building my ML model and this app. 

##### Cleaning & Processing
The dataset driving this app includes 25,700 individual games with publication years through 2024. (The data source notes that the most recent pull 
from the BGG API to create this set was done in early 2025.)

The dataset can be explored at its Kaggle home page.  Of note: The data includes no personal user information, only game data. 

**Key changes during pre-processing and cleaning**
* 27.8K entries in the starting set; 25.7K entries remain after cleaning.

**Dropped data**
* About 1,000 games did not have any title information, had no description, or had no reviews. Those games were dropped because it would 
take too long (for the time I had) to fill in that missing data.
* Another 300 games had no category information. When I inspected this small set of games, they were all very low-rated (on a scale of 1-10, ratings were 2.5 or lower) 
and had few individual reviewers. I removed these rows.
* Another 300 games were missing key data such as an average rating or mechanics information. Again, I removed these rows. 
* The remaining games were found through searches of titles and other fields to uncover entries which are not games at all (and some might remain). 
For example, there was an entry in the database for GameTrayz, the maker of plastic game component organizer systems. Some entries were simply not games, and I flagged 
them for deletion as I was inspecting and cleaning the data.

**Cleaning**
* I used the Python library ftfy (fixed that for you) to fix foreign language text, emoji text, or XML leftovers found in the .csv text.
* Games without a publication year were mostly (through visual inspection) historic games from around the world whose origin is unknown. Those values were replaced with zero. 
* Games with no minimum player count were updated to a count of 1. This data may not be accurate; in a later version of the app, I would like 
to find a way to use information from the game's description to correct min and max player counts and playing time data. 
* Games with no maximum player count or maximum playtime were examined (there were several hundred) by searching for games with similar category flags and mechanics. 
For example, many older tabletop wargames had no max player count but their description suggested a 2-person experience, so I filled in "2" as maximum player count. I would 
like to fix this problem in future releases. 
* Playingtime ranged wildly.  Zeroes were replaced with 30 minutes as a reasonable minimum for a short game if the game had no entry.  For very long games with times in the thousands 
of minutes, I capped playtime at 720 minutes. The longest games represent campaigns, where the entire experience would still likely be played in sessions 
rather than a single 20-hour setting. (!)  I think this is reasonable, given that these numbers are scaled (min/max) if incorporated into the model. 

**Data Preparation**
* Data was prepped for modeling by converting strings to an appropriate data type (such as int). 
* Lists of categories and mechanics were unpacked into actual lists that could be accessed by Python. 
* Columns were added to the game data spreadsheet to hold min/max scaled numeric data. 

-----
## License

* The BGG data is used under their license for use of the API, which was handled by the author of the Kaggle dataset.
* This app is made available under an MIT License. 

