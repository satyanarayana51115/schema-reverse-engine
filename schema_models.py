from typing import List, Optional
from pydantic import BaseModel, Field

class ColumnDefinition(BaseModel):
    name: str = Field(description="కాలమ్ పేరు, ఉదా: customer_id, invoice_date, unit_price")
    data_type: str = Field(description="SQL డేటా టైప్, ఉదా: INTEGER, TEXT, DECIMAL(10,2), DATE")
    is_primary_key: bool = Field(default=False, description="ఇది ప్రైమరీ కీ అయితే True")
    is_foreign_key: bool = Field(default=False, description="ఇది వేరే టేబుల్‌కు లింక్ అయ్యే ఫారిన్ కీ అయితే True")
    references_table: Optional[str] = Field(default=None, description="ఫారిన్ కీ అయితే ఏ టేబుల్‌ని రిఫర్ చేస్తుంది, ఉదా: customers")
    references_column: Optional[str] = Field(default=None, description="ఫారిన్ కీ ఏ కాలమ్‌ని రిఫర్ చేస్తుంది, ఉదా: customer_id")

class TableDefinition(BaseModel):
    table_name: str = Field(description="టేబుల్ పేరు (ప్లూరల్ రూపంలో), ఉదా: customers, invoices, invoice_items")
    description: str = Field(description="ఈ టేబుల్ దేని కోసం ఉపయోగపడుతుంది")
    columns: List[ColumnDefinition] = Field(description="ఈ టేబుల్‌లో ఉండే కాలమ్స్ లిస్ట్")

class InferredDatabaseSchema(BaseModel):
    database_name: str = Field(default="invoice_system", description="డేటాబేస్ పేరు")
    tables: List[TableDefinition] = Field(description="ఇన్‌వాయిస్ నుండి ఊహించిన నార్మలైజ్డ్ టేబుల్స్ (3NF)")
    mermaid_er_diagram: str = Field(description="ఈ టేబుల్స్ రిలేషన్స్‌ను చూపే Mermaid.js ER డయాగ్రమ్ కోడ్")