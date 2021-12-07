# purbeurre

this is a studies project, around databases, and food sanity using openFoodFacts API.

## user story

the user has a choice:

* find a new substitute
* look at my already substituted products

if the user selects option 1, the program asks those following questions:

* select a category
* select a products
* the program prints this product's details (name, components, nutriscore, labels, nutrients, store, barcode, and a link to OpenfoodFacts' dedicated page) 
* then the user can ask for a substitute, see its details or save this one in a favourite list


## features

* get OpenFoodFacts database
* Search ingredients in personnal database, by category
* display some details about a particular product
* search for substitutes for a given product (find in the same category products with a better nutriscore) 
* save a list of favourite products in personnal database
* user interface with kivy
* database must be on a mysql database

## documentation

### dependencies: 
* Python 3.9
* Kivy[base]
* mysql-connector-python
* requests

and their dependencies. listed in requirements.txt files

### setup
* clone this repo (next, the folder where you cloned the repo will be named [pythonpath])

#### database
* install Mysql
    * windows:
        * Download mysql setup tool
        * setup at least the server
    * linux:
        * use integrated packet manager to install mariadb: apt, snap, flatpack, dnf, rpm...
    * macOS
        * find your own way to install mysql server
    
* configurer mysql
    * create user PurBeurre with password PurBeurre
    * create database PurBeurre
    * grant all privileges to PurBeure@% on PurBeurre 
    
* importe le MPD in database
    * execute "[pythonpath]/database/off.sql" within mysql command
    
#### Setup the app
* setup the app
    * [pythonpath]/settings.py
    * you can use custom mysql if configured mysql in another way
    * you can set the size of the data imported from Open Food Facts

#### Virtual environment and dependencies
* create and activate a virtual environment
    * python3 -m venv env
    * windows: env\Scripts\activate.bat ?
    * linux: source ./env/bin/activate

* install dependencies
    windows: python3 -m pip install -r requirementswin.txt
    linux: python3 -m pip install -r requirementsLinux.txt

#### Launch the app
* to launch the App, use "python3 [pythonpath]/Purbeurre.py"

