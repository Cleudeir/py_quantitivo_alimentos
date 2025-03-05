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
    all_data.append(["Preparação","Cardápio Nº","Ingredientes","Fundamental 1-6 a 10 Anos", "Fundamental 2-11 a 15 Anos", "Médio-16 a 18 Anos","unidade"])
    cardapio_name = []
    preparacao = "ALMOÇO"

    for table in tables: 
          
        for row in table: 
                          
            if(row[0] == None or row[0] == ''):
                continue
            if(row[0].startswith(f"Cardápio")  and addData == False):
                cardapio_name.append(row[0])
                addData = True
                continue
            if(row[0].startswith(f"Ingredientes")):
                continue
            if(row[0].startswith(f"Informações nutricionais do Cardápio") or row[0].startswith(f"CHO (g)")):                
                addData = False
                count = count + 1
                continue
            if(addData == False):
                continue
            
            
            def extract_value_unit(text):
                if(text == None):
                    return "", ""
                pattern = r"(\d{1,3}[.,]?\d*)\s?(\D+)"
                match = re.search(pattern, text)
                if match:
                    value = match.group(1).replace(',', '.')  # Replace comma with dot for decimal consistency
                    unit = match.group(2).strip()
                    return float(value), unit
                return text, ""
            column0 = preparacao
            column1 = cardapio_name[count-1]
            column2 = row[0]
            column3, unit = extract_value_unit(row[1])
            column4, unit = extract_value_unit(row[2])
            column5, unit = extract_value_unit(row[3])  
             
            row = [column0, column1, column2, column3, column4,column5, unit]
            all_data.append(row)
    
    df = pd.DataFrame(all_data)
    df.to_excel(output_excel, index=False, header=False)
    print(f"Extracted tables saved to {output_excel}")

# Example usage
pdf_path = "02-Integral.pdf"
output_excel = "extracted_tables-Integral-02.xlsx"
extract_tables_from_pdf(pdf_path, output_excel)
