import re
from src.model import Product, Category, ProductCategory, SimilarProduct, Review

class DatasetController:

    @staticmethod
    def extract(dataset_path:str):

        product_list = []
        category_list = []
        prod_category_list = []
        similars_list = []
        reviews_list = []

        with open(dataset_path, "r", encoding="utf8") as file:
            # Jump the 3 header lines 
            for i in range(3):
                _ = file.readline()
            
            # List that contains each line of information of a product information block
            product_block_lines = []

            for line in file:
                # If the line has only a '\n' it means that is the end of a product info block
                if line == '\n':    
                    # Extract objects from the product info block and store
                    #print(product_block_lines)

                    product_obj, categories_objs, products_category_objs, similars_objs, reviews_objs = DatasetController._extract_objs(product_block_lines)

                    product_list.append(product_obj)
                    category_list.extend(categories_objs)
                    prod_category_list.extend(products_category_objs)
                    similars_list.extend(similars_objs)
                    reviews_list.extend(reviews_objs)

                    # After extracting reset the product block
                    product_block_lines = []
                    continue

                # If the current line is not the end of a block, add the line to the product block
                product_block_lines.append(line)

        return product_list, category_list, prod_category_list, similars_list, reviews_list

    def _extract_objs(block):
        # If the product is descontinued it will have only 3 lines

        categories_list = []
        products_category_list = []
        similars_list = []
        reviews_list = []

        product = Product(int(block[0][3:].strip()), block[1][5:].strip())

        if len(block) == 3:
            return (product, [None], [None], [None], [None])

        print(block)

        product.title = block[2][8:].strip()
        product.product_group = block[3][8:].strip()
        product.salesrank = int(block[4][12:].strip())

        similars_info = block[11:].split()

        product.to_str()

        

        exit() # in development, below is old code

        result = {}
        
        result["asin"] = product_info[1][6:].strip()
        result["title"] = product_info[2][9:].strip()
        result["salesrank"] = product_info[4][13:].strip()

        elements = re.findall(r'\b\d+\b|\b\w{10}\b', product_info[5])
        if(elements[0] != 0):
            result["similar"] = elements[1:]
        else:
            result["similar"] = []
        
        number_categories = product_info[6][14:].strip()
        categories = []
        for i in range(int(number_categories)):
            pattern = r'(\w[\w\s&]+)\[(\d+)\]'
            matches = re.findall(pattern, product_info[7+i])
            for items in matches:
                categories.append({"name":items[0],"id":int(items[1])})

        result["categories"] = categories

        pattern = r'avg rating:\s*(\d+)'
        review_download_avgrating_index = 6 + number_categories + 1
        match = re.search(pattern, product_info[review_download_avgrating_index])
        result["avg_rating"] = int(match.group(1))

        comments = []

        for customer_feedback in product_info[review_download_avgrating_index+1:]:
            cst_fdbk = {}
            pattern = r'(\d{4})-(\d{1,2})-(\d{1,2})\s+cutomer:\s+(\w+)\s+rating:\s+(\d+)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)'
            match = re.search(pattern, customer_feedback)
            year, month, day = map(str, match.groups()[:3])  # Extract and convert date parts
            customer = match.group(4)  # Customer ID
            rating = int(match.group(5))  # Rating
            votes = int(match.group(6))  # Number of votes
            helpful = int(match.group(7))  # Helpfulness
            cst_fdbk["date"] = year + "-" + month + "-" + day
            cst_fdbk["customer"] = customer
            cst_fdbk["rating"] = rating
            cst_fdbk["votes"] = votes
            cst_fdbk["helpful"] = helpful
            comments.append(cst_fdbk)

        result["comments"] = comments
        
        return (None, [None], [None], [None], [None])
        
                
class DatabaseController:
    def insert_one():
        pass
    def insert_batch():
        pass

class ProductDAO(DatabaseController):
    pass
class CategoryDAO(DatabaseController):
    pass
class ProductCategoryDAO(DatabaseController):
    pass
class SimilarProductDAO(DatabaseController):
    pass
class ReviewDAO(DatabaseController):
    pass


     

DatasetController.extract("./data/amazon-meta.txt")
        