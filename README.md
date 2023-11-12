# store-backend

## Project setup
### Python3.8 was used for project setup. SQLite is used as database. Same could be used for testing.

### Clone the project from github and cd to project folder
```
git clone git@github.com:abrar61/store_backend.git
cd [project-folder-path]
```

### Create docker image of backend app and mysql by following command
```
docker-compose build
```

### Run the containers by following command
```
docker-compose up -d
```

### To populate data, execute
```
pip install -r requirements.txt --no-deps
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

#### /docs to access API documentation
#### POST /categories/  To create category with unique name
#### POST /products/  To create product
#### GET /products/  Get products along with their sales (filter by name, category and date (all or none) is applicable). Date can be entered in formats 2023 or 2023-10 or 2023-10-03 to filter by year or month or date respectively
#### GET /sales/  Get sales (filter by name, category and date (all or none) is applicable). Date can be entered in formats 2023 or 2023-10 or 2023-10-03 to filter by year or month or date respectively
#### GET /sales-analysis-by-category/  Returns total sales, revenue, and profit of products sold in given category (Date range filter can also be applied to filter by date)
#### GET /sales-analysis-by-product/  Returns total sales, revenue, and profit of each product (Date range filter can also be applied to filter by date)
#### GET /inventory/  Show each product count with critical low flag
#### PATCH /update-inventory/  Update product count by passing list of objects with product id and updated count
#### GET /product-count-by-category/  Show no of products registered in each category

