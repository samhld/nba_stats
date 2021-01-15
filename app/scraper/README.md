## Scraper

Scraper is responsible for obtaining data from webpages.  This is where the raw data supporting the application comes from.  The Preprocessor is designed to take the returns of Scraper and handle processing that data.  DBs is responsible for persisting the results.

### High level functions
* Scrapes all necessary pages for all available tables with them
* Montitors pages for changes.  When changes have occurred, pulls the latest records from the available tables.

