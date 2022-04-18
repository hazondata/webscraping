# webscraping
Scrapes and stores new jobs from a job platform to your datasource.

# Requirements
## Datasources
The web scraper datasource that is written to is suffixed in the filename. 
> ex: **sqlite** is required as the datasource for the indeed-sqlite.py file.
> 
**indeed-sqlite.py** requires a table that has the following text columns:

|JKEY|Url|Title|Salary|Body|Category|Created| 
|--|--|--|--|--|--|--| 
| | | | | | | | 

## VPN
**NordVPN** is used as the vpn but feel free to use any vpn that provides the ability to change servers via code.

# Usage

 ### 1. Establish a connection to your sqlite db  ↓ or wherever the db is located, for example:

> conn = sqlite3.connect("C:/Users/**bobsmith**/ukjobs.db")

### 2. Update line 55 with your local subdomain if international.
Read the inline comment for an example.

### 3. Main(**kwargs)
Input the keyword arguments as defined below:
>main(pages=1,uri='https://uk.indeed.com/jobs?as_and&as_phr&as_any&as_not&as_ttl=data%20engineer&as_cmp&jt=all&st&salary&radius=25&fromage=any&limit=50&sort&psf=advsrch&from=advancedsearch', label='DataEngineer', table='UKjobs', vpn='C:/Program Files/NordVPN/')
#### pages
Set the number of pages you want to read from. I like to pull in batches so I set this number to 100 which will pull ~5k postings. You can estimate how many pages you need by dividing the total number of jobs by 50.  

#### uri
Generate the uri by querying Indeed's **advanced search** for the jobs you are interested in. Then delete the *&vjk=0000000000000000* tail part of the resulting url.

#### label
Categorize your data with a distinct name that summarizes your job query.

#### table
Name of your datasource table.

#### vpn
Path to your vpn.
