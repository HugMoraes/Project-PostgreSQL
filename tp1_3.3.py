import os
from tabulate import tabulate

def execute_query():
    pass

def print_table(headers, matrix):
    """
    Print a table with given headers and matrix of values.

    :param headers: List of column headers.
    :param matrix: List of lists, where each inner list represents a row of values.
    """
    # Create the table
    table = tabulate(matrix, headers=headers, tablefmt='grid')
    
    # Print the table
    print(table)



if __name__ == '__main__':
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('(a) Dado um produto, listar os 5 comentários mais úteis e com maior avaliação e os 5 comentários mais úteis e com menor avaliação')
        print('(b) Dado um produto, listar os produtos similares com maiores vendas do que ele')
        print('(c) Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada')
        print('(d) Listar os 10 produtos líderes de venda em cada grupo de produtos')
        print('(e) Listar os 10 produtos com a maior média de avaliações úteis positivas por produto')
        print('(f) Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto')
        print('(g) Listar os 10 clientes que mais fizeram comentários por grupo de produto')
        print('\n(0) EXIT')

        op = input('\n\n - Select an option: ')

        if op == '0':
            break

        elif op == 'a':
            product = input(' - Please enter the product ASIN: ')
            print()

            print('The best comments:')
            # rows = execute_query()
            rows = [['1/1/1', '123', 2, 1, 1], ['2/2/2', '456', 2, 1, 1]]
            print_table(['Date', 'Customer', 'Rating', 'Votes', 'Helpful'], rows)
                
            print('\nThe worst comments:')
            # rows = execute_query()
            rows = [['1/1/1', '123', 2, 1, 1], ['2/2/2', '456', 2, 1, 1]]
            print_table(['Date', 'Customer', 'Rating', 'Votes', 'Helpful'], rows)
        
        elif op == 'b':
            product = input(' - Please enter the product ASIN: ')
            print()
            
            # rows = execute_query()
            rows = [['123', 'abc', 'qwe', 1], ['456', 'abc', 'qwe', 2]]
            print_table(['ASIN', 'Title', 'Group', 'Sales Rank'], rows)
            
        elif op == 'c':
            product = input(' - Please enter the product ASIN: ')
            print()
            
            # rows = execute_query()
            rows = [['1/1/1', 1], ['2/2/2', 2]]
            print_table(['Date', 'Average rating'], rows)
            
        elif op == 'd':
            # rows = execute_query()
            rows = [['123', 'abc', 'qwe', 1], ['456', 'abc', 'qwe', 2]]
            print_table(['ASIN', 'Title', 'Group', 'Sales Rank'], rows)
            
        elif op == 'e':
            # rows = execute_query()
            rows = [['123', 'abc', 'qwe', 1, 3], ['456', 'abc', 'qwe', 2, 3]]
            print_table(['ASIN', 'Title', 'Group', 'Sales Rank', 'Mean of positive reviews'], rows)
            
        elif op == 'f':
            # rows = execute_query()
            rows = [['abc', 3], ['qwe', 2]]
            print_table(['Category', 'Mean of positive reviews'], rows)
            
        elif op == 'g':
            # rows = execute_query()
            rows = [['abc', '123', 3], ['qwe', '456', 2]]
            print_table(['Group', 'Customer', 'Number of comments'], rows)
        
        else:
            print('Invalid input.')
        


        os.system('pause')