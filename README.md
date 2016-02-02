# Fantasy Hockey Gems

This is a little Python script designed to help organize and view hockey stats so users can hopefully find some hidden gems for their fantasy hockey pool. I haven't had a chance to do any programming in a while, and since I've fallen behind in all my pools, I decided to make something that would give me an edge when looking for additions to my teams. 

# About

The script downloads the JSON data that NHL.com uses to display regular season stats for skaters and goalies. After that, it creates individual JSON files for each player and keeps track of popular fantasy statistics in the file. If the script is run daily, the new stats are compared to the stats of the JSON file, and a game by game snapshot is generated for each player. These differences are output as a series of reports in 3, 5, or 10 game spans. For example, the script is able to output the statistical leader in save percentage over the last 5 games, and lists in descending order the goalies' names. The script is best used everyday at a set time for consistent results. Because I'm not providing a database of NHL stats, the first run of the script will only provide the regular season stats. As the database grows, the reports will look more like game by game stats instead of the accumulated season stats.

# Usage

I wrote the script using Python 3.4, but by replacing the statistics module with the stats module, it will likely be able to run on Python 3.X. I haven't had any issues running this on Ubuntu 12.04 LTS or Windows 8.1.

# Statistics 

* Goals
* Assists
* Points
* Save Percentage
* Wins
* Shots Against
* Goals Against
* Saves
* Time on Ice (goalies)
* Goals Against Average

# Future Features

I'd like to throw in some testing sometime in the near future. I'd also like to do something with shutouts, but since that stat doesn't pop up consistently, I didn't feel like it was worth it to track too much.

# Legal Stuff

I'm a big fan of the NHL, so I'd like to formally recognize that all NHL stats, logo, players, copyright, trademark etc etc are their own. I'm not trying to make any money off their name by selling this or anything, I'm just doing this for fun and programming practice. I'm also licensing this under Apache License, version 2.0 so I'm releasing this "as is", without warranties or conditions.

