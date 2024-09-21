from src.controler import DatasetController, DatabaseController
from src.controler import ProductDAO, CategoryDAO, ProductCategoryDAO, SimilarProductDAO, ReviewDAO
from datetime import datetime

DATASET_PATH = './data/amazon-meta.txt'

def main():
    start_time = datetime.now()
    product_list, category_list, prod_category_list, similars_list, reviews_list = DatasetController.extract(DATASET_PATH)

    #Insere no banco de dados as instâncias
    DatabaseController.createDatabase()
    DatabaseController.createTables("database.sql")
    ProductDAO.insert_many(product_list)
    CategoryDAO.insert_many(category_list)
    ProductCategoryDAO.insert_many(prod_category_list)
    SimilarProductDAO.insert_many(similars_list)
    ReviewDAO.insert_many(reviews_list)

    #print(DatabaseController.getRows("SELECT * FROM Product")[:30])
    #print(f'Tempo execução = {datetime.now() - start_time}')

if __name__ == "__main__":
    main()
