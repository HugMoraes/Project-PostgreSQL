from src.controler import DatasetController, DatabaseController

DATASET_PATH = './data/amazon-meta.txt'

def main():
    product_list, category_dict, prod_category_list, similars_list, reviews_list = DatasetController.extract(DATASET_PATH)

    #Insere no banco de dados as instâncias

if __name__ == "__main__":
    main()