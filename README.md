To run project use command "uv run fastapi dev"
Then go to browser and open localhost with port 8000 (probably another port, check output when u ran command)
There is 3 endpoints:
- /rss - shows list of rss sources and allows add/delete sources
- /keywords - shows list of keywords and allows add/delete keywords
- /news - shows news where keywords were met into title

Database contains 3 tables:
- keywords
- news
- rss

Table news consists title(header of news), magazin(link to source), url(link to news)