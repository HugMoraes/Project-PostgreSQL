from DatabaseAccess import DatabaseController

DatabaseController.createDatabase()
DatabaseController.createTables("database.sql")
DatabaseController.executeQuery("INSERT INTO Product VALUES(1234567890, 12345, 'O Ultimo Computador', 'Livro', '27', '932', '10.4', '100')")
result = DatabaseController.getRows("SELECT * FROM Product")
print(result)

