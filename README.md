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
* outside virtuel environment
    * docker 
    * docker-compose

* inside virtual environment
    * Python 3.9
    * Kivy[base]
    * mysql-connector-python
    * requests

and their dependencies, listed in requirements[OS].txt files

### setup
* clone this repo (next, the folder where you cloned the repo will be named [pythonpath])

#### database


```bash
# install database
docker-compose up

# create tables
docker exec -i oc-p5-purbeurre-db-1 mariadb --user="PurBeurre" --password="PurBeurre" --database="PurBeurre" --host="localhost" < database/PurBeurre.sql
```

to verify it worked, you can head do http://localhost:8080, and enter PurBeurre as username, PurBeurre as password, and PurBeurre as database, and You should see 3 empty tables named "categories" "food", and "favourites".

#### Setup the app
* setup the app
    * [pythonpath]/settings.py
    * you can set the size of the data imported from Open Food Facts

#### Virtual environment and dependencies
* create and activate a virtual environment
    * python3 -m venv env
    * windows: env\Scripts\activate
    * linux: source ./env/bin/activate

* install dependencies
    windows: python3 -m pip install -r requirementswin.txt
    linux: python3 -m pip install -r requirementsLinux.txt

#### Launch the app
* to launch the App, use `python3 [pythonpath]/OC_purbeurre.py`

