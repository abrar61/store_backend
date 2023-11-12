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

### To populate data, execute following command
```
docker exec -it store_backend-backend-app-1 python populate_data.py
```



### Following is the brief description of APIs developed

#### /docs to access API documentation
#### POST /v1/products/ Create Product
#### GET /v1/products/id/{product_id}/ Search Product By Id
#### GET /v1/products/name/{name}/ Get Products By Name
#### GET /v1/products/category/{category}/ Search Products By Category
#### GET /v1/products/inventory/ Get Inventory
#### PATCH /v1/products/update-inventory/ Update Inventory

#### POST /v1/sales/ Sell Product
#### GET /v1/sales/ Get Sales
#### GET /v1/sales/analysis-by-category/ Get Sales Analysis By Category
#### GET /v1/sales/analysis-by-product/ Get Sales Analysis By Product

#### POST /v1/categories/ Create Category
#### GET /v1/categories/search-by-name/ Search Category By Name


