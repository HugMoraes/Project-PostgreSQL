import re
class Comment:
    def __init__(self, date, customer, rating, votes, helpful):
        self.date = date  # date
        """
        Given the file about this homework, in the input file example we can see 
        that it stores the date with year, month and day. So we can use the date
        datatype which has resolution of 1 day, exacly what we need
        """

        self.customer = customer # varchar(14)
        """
        Given the file about this homework, in the input file example we can supose that customer or client id have
        14 characters maximum with uppercase letters and numbers, so we can use varchar(14)
        """

        self.rating = rating # smallint
        """
        Given the file about this homework, in the input file example we can supose that rating goes from 1 to 5. So
        we can use smallint (2 bytes) which goes from -32768 to +32767. Or we can use just a char which ocupies just 1 byte
        but can cause some trouble cause it will behave like a character not like an integer.
        """

        self.votes = votes # bigint
        """
        What's the limit of this variable? we can consider all customers voting in the same comment, so the maximmum
        votes we can have is all uppercase letters, 26 + 10 digits + 1 blanked space = 37. Using 14 characters we have...
        36^14 = 9.012.061.295.995.008.299.689, 22 digit number, and if we use bigint we can have just 19 digit number.
        but in reality is unlikely to have more than 9223372036854775807 votes in a single comment,
        depite we have 8 billion people on the planet they can have more than 1 account.
        So we gonna use bigint.
        """

        self.helpful = helpful # bigint
        """
        Bigint same reason as votes
        """

class Category:
    def __init__(self, name, id):
        self.name = name # bpchar
        """
        It's a text with any size just use bpchar
        """

        self.id = id # interger
        """
        category number probably won't pass 2147483647, so integer best fit
        """

class Product:
    def __init__(self, product_info:list[str]):
        return None # PlaceHolder
        asin, title, salesrank, similar, categories, comments = self._product_parser(product_info)

        """
        All datatypes are described in here reffering to the postgreSQL documentation about datatypes:
        https://www.postgresql.org/docs/current/datatype.html
        """

        self.asin = asin  # varchar(10)
        """
        Amazon Standard Identification Number (ASIN)
        A ten-digit alphanumeric code that identifies products on Amazon. Ref.: https://www.datafeedwatch.com/blog/amazon-asin-number-what-is-it-and-how-do-you-get-it
        So it is fixed to ten alphanumeric characters, we can use the character varying(n) or varchar(n), which is the same datatype
        """

        self.title = title # bpchar
        """
        For the title, we don't know the maximum size of this string,
        so we can have bpchar or text, but since text allows blanked spaces after the string we can use bpchar to trimm the blanked spaces.
        """

        self.salesrank = salesrank # bigint
        """
        Since ASIN have ten-digit alphanumeric code,
        we have 36 possible characters for each alphanumeric. 
        So, if we have 10 digits we can have at maximum 36^10 = 3.656.158.440.062.976 possible products,
        which is bigger than int (4 bytes) that can reach from -2147483648 to +2147483647, but
        the postgresql have the bigint (8 bytes) that can reach from -9223372036854775808 to +9223372036854775807

        """

        self.similar = similar # varchar(10)[]
        """
        In similiar we are storing a list of similar products by their ASIN, so we can use an array without limit of varchar(10)
        """

        self.categories = categories # n sei

        self.avg_rating = avg_rating # smallint
        """
        small number, we can use smallint
        """

        self.comments:list[Comment] = comments # n sei

    def _product_parser(self, product_info):
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

        """
        This function takes the product_info which is lines from the file and extracts all atributes needed

        Example:

        INPUT BELOW, WARNING: the \n in the text are in the string because its a raw string, so it need to be worked on:
        input=['Id:   1\n', 'ASIN: 0827229534\n', '  title: Patterns of Preaching: A Sermon Sampler\n', '  group: Book\n', '  salesrank: 396585\n', '  similar: 5  0804215715  156101074X  0687023955  0687074231  082721619X\n', '  categories: 2\n', '   |Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]\n', '   |Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Sermons[12370]\n', '  reviews: total: 2  downloaded: 2  avg rating: 5\n', '    2000-7-28  cutomer: A2JW67OY8U6HHK  rating: 5  votes:  10  helpful:   9\n', '    2003-12-14  cutomer: A2VE83MZF98ITY  rating: 5  votes:   6  helpful:   5\n']

        EXPECTED OUTPUT BELOW, WARNING: the output can vary because it's not determined how it should return, but we need these variables ready, and comment and category are objects as described above. Some categories are repeated so use the id, which is unique, to compared if the catefory have already been added:
        
        asin='0827229534'
        title='Patterns of Preaching: A Sermon Sampler'
        salesrank=396585
        similar=['0804215715', '156101074X', '0687023955', '0687074231', '082721619X']
        categories=[{'name':'Books', 'id':283155},
                    {'name':'Subjects', 'id':1000}, 
                    {'name':'Religion & Spirituality', 'id':22}, 
                    {'name':'Christianity', 'id':12290}, 
                    {'name':'Clergy', 'id':12360},
                    {'name':'Preaching', 'id':12368},
                    {'name':'Sermons', 'id':12370}]
        avg_rating=5
        comments=[{'date':date(2000, 7, 28), 'customer':'A2JW67OY8U6HHK', 'rating':5, 'votes':10, 'helpful':9}, 
                  {'date':date(2003, 12, 14), 'customer':'A2VE83MZF98ITY', 'rating':5, 'votes':6, 'helpful':5}]
        
        """

        print(result)
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

            if "Id:" in input_text_lines[iline]:
                # Found a product
                if input_text_lines[iline + 2] == "  discontinued product\n":
                    # Product discontinued, jump to the next product
                    iline += 4
                    
                else:
                    # Valid product, search the end of this product info
                    
                    end_product_line = iline + 8 # Jump to the minimmun product info, without comments or categories

                    while input_text_lines[end_product_line] != "\n": # Search for the product separation which is a line with only \n
                        end_product_line += 1 

                    product_info = input_text_lines[iline:end_product_line]
                    print("\n\n", product_info, "\n\n")
                    exit()
                    new_product = Product(product_info)
                    products.append(new_product)

                    iline = end_product_line + 1 # Jumping to the next line after the single "\n" which is an Id line

            else:
                iline += 1 # found something different
        # IGNORE #
        print(f'\r[{"#" * 50}] 100.00% | {iline}/{len(input_text_lines)} lines | {len(products)} products')
        # IGNORE #


        

    except Exception as e:
        print(e)

input_file_reader("amazon-meta.txt")