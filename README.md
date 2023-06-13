# Python Web Scraper
Created using BeautifulSoup library.
Extracts data from specified website and saves it to JSON file.

### Feed the script with website data:
Save the website as .html file and copy the website to:
```
/input/
```

### Run script using:
```
python webscraper.py
```

### Script Output:
The script will create (if folders don't exist):
```
/output/
/images/
```

### Output folder:
A JSON file similar to the one in the example below:
```
{
    "QuestionID": 0,
    "TxtLine_0": "You have a table in an Azure Synapse Analytics dedicated SQL pool. The table was created by using the following Transact-SQL statement.",
    "Image_1": "URL: `IMAGE URL`",
    "TxtLine_2": "You need to alter the table to meet the following requirements:",
    "TxtLine_3": "Ensure that users can identify the current manager of employees.",
    "TxtLine_4": "Support creating an employee reporting hierarchy for your entire company.",
    "TxtLine_5": "Provide fast lookup of the managers' attributes such as name and job title.",
    "TxtLine_6": "Which column should you add to the table?",
    "Variant_A": "[ManagerEmployeeID] [smallint] NULL",
    "Variant_B": "[ManagerEmployeeKey] [smallint] NULL",
    "Variant_C": "[ManagerEmployeeKey] [int] NULL",
    "Variant_D": "[ManagerName] [varchar](200) NULL",
    "Correct Answer:": "C",
    "Explanation:": "We need an extra column to identify the Manager. Use the data type as the EmployeeKey column, an int column.Reference: `WEBSITE LINK`"
}
```

### Images folder:
Saved images from website.