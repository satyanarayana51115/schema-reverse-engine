-- విక్రేత (అమ్మకందారుడు) యొక్క వివరాలను మరియు వారి GSTIN సమాచారాన్ని నిల్వ చేసే టేబుల్
CREATE TABLE IF NOT EXISTS sellers (
    seller_gstin VARCHAR(15) PRIMARY KEY,
    seller_name VARCHAR(100),
    address TEXT
);

-- కస్టమర్ల యొక్క వ్యక్తిగత మరియు సంప్రదింపు వివరాలను నిల్వ చేసే టేబుల్
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100),
    phone VARCHAR(15),
    address TEXT
);

-- ఉత్పత్తుల వివరాలు, వాటి HSN కోడ్‌లు మరియు ప్రామాణిక ధరలను నిల్వ చేసే టేబుల్
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    description VARCHAR(255),
    hsn_code VARCHAR(10),
    unit_price DECIMAL(10,2)
);

-- ఇన్‌వాయిస్ యొక్క ప్రధాన సమాచారం, తేదీ, పన్నులు మరియు మొత్తం బిల్లు వివరాలను నిల్వ చేసే టేబుల్
CREATE TABLE IF NOT EXISTS invoices (
    invoice_no VARCHAR(30) PRIMARY KEY,
    invoice_date DATE,
    seller_gstin VARCHAR(15),
    customer_id VARCHAR(20),
    subtotal DECIMAL(10,2),
    cgst_amount DECIMAL(10,2),
    sgst_amount DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_mode VARCHAR(50),
    FOREIGN KEY (seller_gstin) REFERENCES sellers(seller_gstin),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ప్రతి ఇన్‌వాయిస్‌లోని విడివిడి ఐటెమ్స్, వాటి పరిమాణం మరియు ధరల వివరాలను నిల్వ చేసే టేబుల్
CREATE TABLE IF NOT EXISTS invoice_items (
    invoice_item_id INTEGER PRIMARY KEY,
    invoice_no VARCHAR(30),
    product_id INTEGER,
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    FOREIGN KEY (invoice_no) REFERENCES invoices(invoice_no),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
