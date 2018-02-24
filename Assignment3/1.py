import xlrd


def readData():
    gen1 = []
    gen2 = []
    gen3 = []
    gen4 = []
    workbook = xlrd.open_workbook('dataset.xlsx', on_demand=True)
    worksheet = workbook.sheet_by_index(0)
    first_row = []  # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append(worksheet.cell_value(0, col))
    # transform the workbook to a list of dictionaries
    data = []
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(worksheet.ncols):
            elm[first_row[col]] = worksheet.cell_value(row, col)
        data.append(elm)
    # print (data)

    ''' for each in data:
        if len(each['Name']) == 1 or len(each['Name']) == 2:
            gen1.append(each)
        elif len(each['Name']) == 3 or len(each['Name']) == 4:
            gen2.append(each)
        elif len(each['Name']) == 5 or len(each['Name']) == 6:
            gen3.append(each)
        elif len(each['Name']) == 7 or len(each['Name']) == 8:
            gen4.append(each)
    return gen1, gen2, gen3, gen4, data'''
    return data


def rel(name1, name2):
    relation = ""
    data = readData()

    if name1 in gen1:
        print("gen1")





relation = ""

# print(gen1)
name1 = input("Please enter one name: ")
name2 = input("Please enter the other name: ")
data = readData()
print(data)
#print(data[name1])
#rel(name1, name2)