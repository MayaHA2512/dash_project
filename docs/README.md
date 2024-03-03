**Dash Student Finance Tracker**

**RESEARCH**

**Background information**

Financial literacy is often quite low among students and this leads to difficulty
when trying to manage student finances and budgeting. Studies have even shown that improved money
management can reduce stress and lead to better financial futures which tends to provide a better quality of life. 

**Problem statement**

The problem mentioned above inspired me to develop an app that allows students to keep track of their expenses and view stats such as which payment 
method is being used the most and what category of spending is most prevalent so that they can highlight where they can minimise expenses and save more.

**Objectives:**
- Develop an app that allows students to easily track expenses 
- Allow students to view various statistics e.g. what category is taking lots of 'hidden expenses'
- Enhance financial literacy of students 
 
**Language and frameworks**

I developed my app using Python along with the dash web framework. In short - Dash is a web framework  primarily used to develop web applications. I felt this would be a great opportunity to test its capabilities to set up a financial tracker as it requires little to no CSS and is fully Python based. This makes it a great tool to use alongside the Object Orientated Programming (OOP)
paradigm as you can separate the different components of the application using the model view controller (MVC) structure and pull methods from the Model class(business logic) and View class(UI) into the controller when creating your callbacks. Please note - callbacks are what make components such as toggles and graphs in your UI interactive. 

**ANALYSIS** 

**Data storage**

From the beginning stages, it was obvious that a system for saving data was going to be required, to hold the transactions 
from previous sessions and the balance value. For this purpose, I used Python's 'sqlite3' library and put together an entity relationship model as such:
[UPDATE]: Decided to hard code temporary login credentials whilst exploring ways of encrypting passwords to maintain user integrity.

![ERD.png](..%2Fimages%2FERD.png)

**Model View Controller (MVC)**

I decided to use the model view controller to organise my code. This keeps the UI, data handing and interactions between the two separate. This proved to be 
view useful when locating the source of bugs  and errors and matched well with the nature of the dash framwork. File structuring was kept as such:

![file_org.png](..%2Fimages%2Ffile_org.png)

**Flowchart**

![flowchart2.png](..%2Fimages%2Fflowchart2.png)
The flowchart above provides a general depiction of the workings of the app and how data is pulled from the database to form the dashboard page and how the dash app interacts with user input.

**Workflow**

I decided to use the jira board system by Atlassian to manage my tasks - this was very useful to keep track of little changes I was 
hoping to make once I had developed the bulk of the app and wanted to take a bit of time to refine a few features and make them more robust.
Provided below is a screenshot of the task manager I used:

![jira-board.png](../images/jira-board.png)

**Implementation**
Here I will dicuss features I used to develop my application:

1. OOP - OOP composition was major to keeping my code organised as I maintained the Model and View class of which instances were created and used in the controller file (Controller.py).
below are a breakdown of the classes created:
![class_diagram.png](..%2Fimages%2Fclass_diagram.png)

I also used composition and inheritance for the Card base class that created to have the default styling pre-set and reduce duplicate code:
![card class.png](..%2Fimages%2Fcard%20class.png)

This is an example of how I used this card to reduce duplicate code in my project:
![example_Card.png](..%2Fimages%2Fexample_Card.png)

As you can see I only need to create an instance of the card and then set the card content.




OOP
ADVANCED OOP
REFACTORING
CALLBACKS
PLOTLY
SQL
config

IMPLEMENTATION 

TESTING 

REVIEW