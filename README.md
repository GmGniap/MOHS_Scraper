# MOHS_Scraper
:scissors:
MOHS Arcgis Dashboard - Scraping and push the data to MySQL to integrate with PowerBI for visualization

## List to Do 
- [x] MySQL Connection
- [] Schedule to run script at every 8:30PM
- [] Auto insert into the template
- [] PowerBI visualzation & published 

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

Explain how to run the automated tests for this system

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

