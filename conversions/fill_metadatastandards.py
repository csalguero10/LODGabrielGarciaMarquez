import csv

# items metadata
data = [
    ["El general en su laberinto", "book", "Henry Ransom Center", "EAD"],
    ["Diatriba de amor contra un hombre sentado", "play", "Internet Archive", "MARC/XML"]
    ["La solitud de Latin America","sound", "Henry Ransom Center", "EAD"]
    ["Magic in service of truth", "article", "The New York Times", "N/A"]
    ["Gabo, la creación de Gabriel García Márquez","documentary", "IMDb", "Schema.org"]
    []
    []
    []
    []
    []
]

with open('metadatastandards.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # for Cata: tell me if the header should be changed
    writer.writerow(["Item Name", "Object Type", "Source", "Metadata Standard"])

    writer.writerows(data)

#a print function just in case
print("")

#TO DO when data is filled: run a new py script: python fill_metadatastandards.py to generate a table.csv with new data in it
