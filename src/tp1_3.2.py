import re
class Product:

    def _product_parser(self, product_info):
        result = {}

        id_match = re.search(r'Id:\s*(\d+)', product_info[0])
        product_id = id_match.group(1)

        asin_match = re.search(r'ASIN:\s*(\d+)', product_info[1])
        product_asin = asin_match.group(1)

        title_match = re.search(r'title:\s*(.*)', product_info[2])
        product_title = title_match.group(1)

        group_match = re.search(r'group:\s*(.*)', product_info[3])
        product_group = group_match.group(1)

        salesrank_match = re.search(r'salesrank:\s*(\d+)', input[4])
        product_salesrank = salesrank_match.group(1)

        total_review_match = re.search(r'reviews:\s*total:\s*(\d+)', product_info[9])
        total_review = total_review_match.group(1)

        review_download_match = re.search(r'downloaded:\s*(\d+)', product_info[9])
        review_download = review_download_match.group(1)

        avg_rating_match = re.search(r'avg rating:\s*(\d+)', product_info[9])
        avg_rating = avg_rating_match.group(1)

        produto = Product(product_id, product_asin, product_title, product_group, product_salesrank, total_review, review_download, avg_rating)
        
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
        
        return result

def input_file_reader(file_path:str):
    try:
        print("Opening input_file and transfering to memory...", end="")
        with open(file_path, "r", encoding="utf8") as file:
            input_text_lines = file.readlines()
        print(" Done!")
        
        print("Reading lines from input_file in memory...")
        
        iline = 0
        products = []

        while(iline < len(input_text_lines)):
            # IGNORE #
            percent = (iline / len(input_text_lines)) * 100
            bar = ('#' * int(percent // 2)).ljust(50)
            print(f'\r[{bar}] {percent:.2f}% | {iline}/{len(input_text_lines)} lines | {len(products)} products', end='')
            # IGNORE #

            # If found "Id:" in the line, it starts to read the product info block
            if "Id:" in input_text_lines[iline]:
                # If the in second line below contains "discontinued product" just jump to the next product info block and starts reading again
                if input_text_lines[iline + 2] == "  discontinued product\n":
                    iline += 4
                    continue

                # Else, found a valid product, search the end of this product info block
                else: 
                    # Jump to the minimmun product info block, without comments or categories
                    end_product_line = iline + 8 
                    # Search for the product block separation which is a line with only \n
                    while input_text_lines[end_product_line] != "\n": end_product_line += 1  
                    # Extract the product info block with the start line and end line
                    product_info = input_text_lines[iline:end_product_line]
                    
                    new_product = Product(product_info)
                    products.append(new_product)

                    iline = end_product_line + 1 # Jumping to the next line after the single "\n" which is an Id line

            # Else, found something that's not in a product info block so can be skipped
            else:
                iline += 1 
        # IGNORE #
        print(f'\r[{"#" * 50}] 100.00% | {iline}/{len(input_text_lines)} lines | {len(products)} products')
        # IGNORE #


        

    except Exception as e:
        print(e)

input_file_reader("data/amazon-meta.txt")
