# MOHS_Scraper
:scissors:
MOHS Arcgis Dashboard - Scraping and push the data to MySQL to integrate with PowerBI for visualization

## List to Do 
- [x] MySQL Connection
- [x] Schedule to run script at every 8:30PM
- [] Auto insert into the template
- [] PowerBI visualzation & published

### January 16 - Tasks 
* [x] DF1 from SQL // DF2 from HTML old
* [x] Find duplicates
* [x] Compare the values

### January 18 - Errors & Tasks 
* Today's error is a little different & difficult than the previous ones. I've pcode csv that'd region column which needed to be compared with my SQL data. But the region column from SQL & region column from csv isn't the same. Especially one thing is being different - Bago. In SQL , there's only titled as 'Bago' but in CSV , there're Bago(East) & Bago(West). 
* [x] I still don't have any idea to solve that. But possible way is if I make a dictionary of townships under this two different Bago and then compared with my SQL , titled as the dictionary. I solved that problem by using Merge/Concat in nested ways. 
* [] still need to find a better(shorter) code to solve the above problem.  

## Prerequisites
### Activate Environment 
- (on window) run cmd command >
```console
.\environment\Script\activate.bat
```

### Installing

```console
pip install -r requirements.txt
```

### SQL Commands
- Beware that SQL Table Column names must be the same as pandas dataframe column names. And also the data types. 
- Create Township Table 
```SQL
create table township(id int auto_increment primary key, upload_date DATE DEFAULT (CURRENT_DATE), townships varchar(255), sr varchar(255) not null, cumulative_no int);
```
- Create Overall Table 
```SQL
create table overall(id int auto_increment primary key, upload_date DATE DEFAULT (CURRENT_DATE), index_name varchar(255) not null, total_no float not null);
```


## Running the tests

To run scraping & putting data into database , click to *run another.bat* file or schedule with Window Tasks Scheduler. 
or run python code as below.

```Python
python main.py
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Pandas](https://pandas.pydata.org/) - Data Analysis Framework
* [Selenium](https://selenium-python.readthedocs.io/) - Web Driver
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML paraser

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Thet Paing Myo** - *Personal project* - [Personal Blog](https://paing.me)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Alex from Yangon Data Science Community
    * I got initiated inspiration from YDSC MOHS scraping repo - [Link](https://github.com/Yangon-Data-Science-Community/MM-COVID-19-Surveillance)
    * This repo & code help me a lot to figure out the structure of MOHS website.  
* All Geeks & Instructors from Internet (Especially from StackOverFlow)

