# store-backend

## Project setup
### Python3.8 was used for project setup

### Clone the project from github and cd to project folder
```
git clone
cd [project-folder-path]
```

### Create a venv of python using following command
```
python3.8 -m venv venv
```

### Update pip (if necessary)
```
pip install -U pip
```

### Install the required packages using following command
```
pip install -r requirements.txt
```

### Run the project using following command
```
uvicorn main:app --reload
```

### Open another terminal in the project folder and run following command to populate data
```
python populate_data.py
```


### Following is the brief description of APIs developed

#### POST /categories/  To create category with unique name
#### POST /products/  To create product
#### GET /products/  Search products by name
#### GET /sales-analysis-by-category/  Returns total sales, revenue, and profit of products sold in given category (Date range filter can also be applied to filter by date)
#### GET /sales-analysis-by-product/  Returns total sales, revenue, and profit of each product (Date range filter can also be applied to filter by date)
#### GET /inventory/  Show each product count with critical low flag
#### PATCH /update-inventory/  Update product count by passing list of objects with product id and updated count
#### GET /product-count-by-category/  Show no of products registered in each category

