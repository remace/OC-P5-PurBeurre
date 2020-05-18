# purbeurre

this is a studies project, around databases, and food sanity using openFoodFacts API.

## user story

the user has a choice:

* find a new substitute
* look at my already substituted products

if the user selects option 1, the program asks those following questions:

* select a category
* select an products
* the program prints this product's details (name, components, nutriscore, labels, nutrients, store, barcode, and a link to OpenfoodFacts' dedicated page) 
* then the user can ask for a substitute, see its details or save this one in a favourite list


## features

* get OpenFoodFacts database
* Search ingredients in personnal database database, by category
* display some details about a particular product
* search for substitutes for a given product. 
* save a list of favourite products in personnal database
* user interface with kivy
* database must be on a mysql database

## documentation

### dependencies: 

* python 3.7 (not higher)
* requests
* mysql-connector-python
* docutils
* pygments
* kivy 1.11.1
* kivy.deps.sdl2
* kivy.deps.glew

### setup

#### database

* install Mysql (mariadb)
* execute "/database/off.sql"

#### purbeurre App

* TODO pour fournir une build windows et une build linux
