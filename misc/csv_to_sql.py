import csv


with open('vendas_roupas.csv', 'r', encoding='utf-8') as file_csv:
    with open('vendas_roupas.sql', 'w', encoding='utf-8') as file_sql:
        csv_reader = csv.reader(file_csv, delimiter=',')
        for count, row in enumerate(csv_reader):
            if count > 0:
                value = f'INSERT INTO vendas_venda (onde_comprou, genero, tipo_roupa, cor, tamanho, preco, estacao, mes) VALUES ("{row[0]}", "{row[1]}", "{row[2]}", "{row[3]}", "{row[4]}", {row[5]}, "{row[6]}", "{row[7]}");\n'
                file_sql.write(value)
