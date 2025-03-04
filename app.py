import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path, output_excel):
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                tables.append(table)
    
    # Convert extracted tables to DataFrame and clean up
    all_data = []
    addData = False
    count = 1
    # add header
    all_data.append(["Cardápio Nº","Ingredientes","Fundamental 1 - 6 a 10 anos", "Fundamental 2 - 11 a 15 anos", "Médio", "EJA"])
    for table in tables:
        for row in table:
            if(row[0].startswith(f"Cardápio {count}")  and addData == False):
                addData = True
            if(row[0].startswith(f"Ingredientes")):
                continue
            if(row[0].startswith(f"Informações nutricionais do Cardápio {count}")):
                addData = False
                count = count + 1
                continue  
            if(addData == False):
                continue
            print(row)
            all_data.append(row)
    
    df = pd.DataFrame(all_data)
    df.to_excel(output_excel, index=False, header=False)
    print(f"Extracted tables saved to {output_excel}")

# Example usage
pdf_path = "Educacao-Basica.pdf"
output_excel = "extracted_tables.xlsx"
extract_tables_from_pdf(pdf_path, output_excel)
