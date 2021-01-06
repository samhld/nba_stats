
![Architecture](https://github.com/samhld/nba_stats/blob/main/imgs/nba_app.png)

# What will it do?

## __Backend should support__
__API for UI__
* Most if not all functionality below should be exposed to UI

__Return time series by player__
* By between 1 and all stats (basic and advanced)
* By date range
* By datetime unit (day, month, year/season)
* By regular season and playoffs...or combined
* Available parameters
  - Date range / specific date or game / season
  - Regular season / playoffs

__Return time series by team__
* By between 1 and all stats (basic and advanced)
* By date range
* By datetime unit (day, month, year/season)
* By regular season and playoffs...or combined

__Supported analytics__
* Forecasting by player/team


__(Optional) Return time series by conference__
* By between 1 and all stats (basic and advanced)
* By date range
* By datetime unit (day, month, year/season)
* By regular season and playoffs...or combined


## __UI should support__
 __Show time series (line graph) by player__
* Players should be searchable
* Stats should be searchable and selectable in a dropdown
* Teams should be searchable and selectable in a dropdown
* Year/season should be selectable in a dropdown
* Time sampling should support ranges and units by day, year, and month [and pre-/post-allstar break? (probably hardcoded each season)]

__Player comparisons__
* Support side by side tables of basic or advanced stats given parameters for players or teams

# Data tables
* Players
  - Table of all players and their per-game stats (basic and advanced) at the season level
* Gamelog
  - Each player will have their own gamelog table with a foreign key to the players table
* Shot chart
  - Each player will have shot

# Work to be done
Select a method of "querying".   
