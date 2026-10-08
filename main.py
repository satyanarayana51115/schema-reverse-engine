import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from schema_models import InferredDatabaseSchema

# 1. ఎన్విరాన్‌మెంట్ వేరియబుల్స్ లోడ్ చేయడం
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY కనుగొనబడలేదు! దయచేసి .env ఫైల్‌ని సరిచూసుకోండి.")

# 2. Gemini క్లయింట్ ప్రారంభించడం
client = genai.Client(api_key=api_key)

# 3. టెస్టింగ్ కోసం ఒక శాంపిల్ ఇన్‌వాయిస్ టెక్స్ట్
sample_invoice = """
=============================================================
TAX INVOICE / CASH BILL
INVOICE NO: INV-2026-0894
DATE: 2026-10-08

SELLER DETAILS:
TechRetail Solutions Pvt Ltd
Plot 45, Hitec City, Hyderabad, TG - 500081
GSTIN: 36AAAAA0000A1Z5

BILL TO (CUSTOMER):
Customer ID: CUST-7741
Name: Satyanarayana Raj
Phone: +91 9876543210
Address: Madhapur, Hyderabad, TG - 500086

LINE ITEMS:
-------------------------------------------------------------
S.No | Description              | HSN Code | Qty | Unit Price | Total
-------------------------------------------------------------
1    | 2D Barcode Scanner USB   | 84719000 | 2   | 3,500.00   | 7,000.00
2    | Thermal Label Paper Roll | 48211000 | 5   | 250.00     | 1,250.00
3    | Inverter PCB Board (DA97)| 85371000 | 1   | 4,200.00   | 4,200.00
-------------------------------------------------------------
Subtotal: Rs. 12,450.00
CGST (9%): Rs. 1,120.50
SGST (9%): Rs. 1,120.50
TOTAL AMOUNT: Rs. 14,691.00
PAYMENT MODE: UPI / Online
=============================================================
"""

def generate_ddl_sql(schema: InferredDatabaseSchema) -> str:
    """ఊహించిన స్కీమా ఆధారంగా ఆటోమేటిక్ SQL CREATE TABLE స్టేట్‌మెంట్లను తయారు చేస్తుంది."""
    sql_statements = []
    
    for table in schema.tables:
        lines = [f"-- {table.description}", f"CREATE TABLE IF NOT EXISTS {table.table_name} ("]
        col_defs = []
        fk_defs = []
        
        for col in table.columns:
            pk_str = " PRIMARY KEY" if col.is_primary_key else ""
            col_defs.append(f"    {col.name} {col.data_type}{pk_str}")
            
            if col.is_foreign_key and col.references_table and col.references_column:
                fk_defs.append(
                    f"    FOREIGN KEY ({col.name}) REFERENCES {col.references_table}({col.references_column})"
                )
        
        all_table_lines = col_defs + fk_defs
        lines.append(",\n".join(all_table_lines))
        lines.append(");\n")
        sql_statements.append("\n".join(lines))
        
    return "\n".join(sql_statements)

def infer_schema_from_document(invoice_text: str):
    print(" ఇన్‌వాయిస్ విశ్లేషణ ప్రారంభమైంది...")
    
    prompt = f"""
    You are an expert Principal Database Architect.
    Analyze this flat invoice document and reverse-engineer the normalized Relational Database Schema (3rd Normal Form).
    
    Instructions:
    1. Separate flat repeating entities into proper normalized tables (e.g., customers, sellers/merchants, invoices, invoice_items, products).
    2. Correctly identify primary keys, data types, and foreign keys connecting parent-child entities.
    3. Produce a clean Mermaid.js ER diagram syntax (erDiagram).
    
    Document Content:
    {invoice_text}
    """
    
    # Gemini మోడల్‌ని Structured Output తో కాల్ చేయడం
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InferredDatabaseSchema,
            temperature=0.1
        )
    )
    
    schema: InferredDatabaseSchema = response.parsed
    return schema

if __name__ == "__main__":
    # స్కీమా రన్ చేయడం
    schema = infer_schema_from_document(sample_invoice)
    
    print("\n✅ స్కీమా రివర్స్ ఇంజనీరింగ్ విజయవంతమైంది!\n")
    print(f"కనుగొన్న టేబుల్స్ సంఖ్య: {len(schema.tables)}")
    for t in schema.tables:
        print(f" - {t.table_name}: ({len(t.columns)} కాలమ్స్)")
        
    # SQL DDL జనరేట్ చేసి ఫైల్‌లో రాయడం
    sql_ddl = generate_ddl_sql(schema)
    with open("schema.sql", "w", encoding="utf-8") as f:
        f.write(sql_ddl)
    print("\n💾 SQL DDL కోడ్ 'schema.sql' ఫైల్‌లో సేవ్ చేయబడింది.")

    # Mermaid డయాగ్రమ్‌ను సేవ్ చేయడం
    with open("diagram.mmd", "w", encoding="utf-8") as f:
        f.write(schema.mermaid_er_diagram)
    print("📊 Mermaid ERD కోడ్ 'diagram.mmd' ఫైల్‌లో సేవ్ చేయబడింది.")