import re
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
    all_data.append(["Cardápio Nº","Ingredientes","Fundamental 1 - 6 a 10 anos", "Fundamental 2 - 11 a 15 anos", "Médio", "EJA", "unidade"])
    cardapio_name = []

    for table in tables:       
        for row in table:            
            if(row[0].startswith(f"Cardápio {count}")  and addData == False):
                cardapio_name.append(row[0])
                addData = True
                continue
            if(row[0].startswith(f"Ingredientes")):
                continue
            if(row[0].startswith(f"Informações nutricionais do Cardápio {count}")):
                addData = False
                count = count + 1
                continue
            if(addData == False):
                continue
            
            def extract_value_unit(text):
                pattern = r"(\d{1,3}[.,]?\d*)\s?(\D+)"
                match = re.search(pattern, text)
                if match:
                    value = match.group(1).replace(',', '.')  # Replace comma with dot for decimal consistency
                    unit = match.group(2).strip()
                    return float(value), unit
                return text, ""

            column1 = cardapio_name[count-1]
            column2 = row[0]
            column3, unit = extract_value_unit(row[1])
            column4, unit = extract_value_unit(row[2])
            column5, unit = extract_value_unit(row[3])
            column6, unit = extract_value_unit(row[4])
            
            if( column3 == "" or column4 == "" or column5 == "" or column6 == ""):
                continue
            
            row = [column1, column2, column3, column4, column5, column6, unit]
            all_data.append(row)
    
    df = pd.DataFrame(all_data)
    df.to_excel(output_excel, index=False, header=False)
    print(f"Extracted tables saved to {output_excel}")

# Example usage
pdf_path = "Educacao-Basica.pdf"
output_excel = "extracted_tables.xlsx"
extract_tables_from_pdf(pdf_path, output_excel)
