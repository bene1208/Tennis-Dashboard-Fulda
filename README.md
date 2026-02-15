# Tennis-Dashboard for the region of Fulda

### Link to Dashboard: https://tennis-dashboard-fulda.streamlit.app 

### Module: Frameworks & Application Development for Data Science

### Name: Benedikt Klüber

### Date: 15.02.2026

### Project Description: 
This dashboard offers an overview over all tennis-clubs in the region of Fulda. The dashboard is made for all people, who are interested in Tennis and are living near Fulda. In particular, the dashboard is directed at beginners and trainers, who are currently searching for a new club and want to get an overview over all clubs in the region. As the dashboard has been made for people living near Fulda in Germany, the dashboard language is German. 

### Fulfilled Complexity Criteria
1. **Data Engineering (Web Scraping):** The database used for the dashboard was gathered by performing **Web Scraping**. The two websites that were scraped are https://www.sportkreis-fulda-huenfeld.de/ and https://htv.liga.nu/. The source code concerning this is contained in the folder `/scraping`.
2. **Advanced Human-Computer Interaction (HCI):** The dashboard implements various features of advanced human-computer interaction such as the interactive map, which shows a tooltip when hovering over the locations of the clubs on the map. Another advanced HCI feature represents the synchronization of the club-selection from the main-page to the club-details page. 

### Limitations:
Originally, it was planned to create a Tennis & Padel-Dashboard. Due to the fact that at the moment only one club in the region of Fulda offers padel courts and as a consequence there is no data for padel courts in the region of Fulda, the padel sport has not been included in the dashboard. Furthermore, it was also planned that prices for tennis courts of club-websites or a rating system could be included in the dashboard. These two features were not included, as the Web Scraping has been a very tough challenge to face. Therefore, I invested a lot of time to extract the information that is now used in the dashboard. As a consequence of the difficulties with Web Scraping and missing other data sources concerning tennis clubs in the region of Fulda, I decided to concentrate on transforming and cleaning the data that I was able to scrape successfully. Furthermore, I also focused on building a dashboard providing a good overview over the tennis clubs in the region of Fulda combined with a good usability.


### Installations & Starting the Dashboard:
1. Unpacking .zip file.
2. Installing necessary requirements:  
   `pip install -r requirements.txt`
3. Starting the dashboard:  
   `streamlit run app.py`

### Structure:
* `app.py`: Main application containing the source code for the dashboard created with streamlit.
* `/data`: Transformed and cleaned CSV-Exports representing the database for the dashboard.
* `/scraping`: Web-Scraping Code used for deriving the database for the dashboard (the two already mentioned CSV-export files).
