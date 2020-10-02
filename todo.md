# To-do list: 

## Scraping: 
- [x] Set warning `if response.status != 200`
- [x] Use time/sleep to slow down requests
- [x] Figure out pagination, and use `pd.concat(dfs)` where `dfs` is a list of dfs
- [x] Scrape all available pages
- [x] Scrape SFBay postings (bc location is a set field, plus I know it better): SF
- [x] Export scrape to CSV

## Data Cleaning: 
- [ ] Deal with duplicate listings (unique URLs bc posted multiple times)
- [ ] Deal with missing information (esp. sqft)
- [ ] Save clean CSV file
- [ ] If BR = NaN, convert to 0 (assume Studio)
- [ ] Amenities: create groupings 
- [ ] Neighborhoods: create groupings

## Regression
- [ ] feature selection
- [ ] ... 
