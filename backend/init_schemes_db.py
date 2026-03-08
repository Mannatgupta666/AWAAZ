"""
Initialize SQLite database with government schemes
"""
import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'schemes.db')

# Create database directory if it doesn't exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create schemes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target_occupation TEXT,
    max_income REAL,
    gender TEXT,
    min_age INTEGER,
    max_age INTEGER,
    category TEXT,
    benefit TEXT,
    description TEXT,
    application_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Clear existing data
cursor.execute('DELETE FROM schemes')

# Insert schemes
schemes = [
    (
        'PM Kisan',
        'farmer',
        2.0,
        'any',
        18,
        999,
        'any',
        'Rs 6000 per year direct to bank account',
        'Financial support to farmers for agricultural activities',
        'https://pmkisan.gov.in/'
    ),
    (
        'Ayushman Bharat',
        'any',
        5.0,
        'any',
        0,
        999,
        'any',
        'Free health insurance up to Rs 5 lakh',
        'Health insurance scheme for economically vulnerable families',
        'https://pmjay.gov.in/'
    ),
    (
        'Post Matric Scholarship (SC/ST)',
        'student',
        2.5,
        'any',
        16,
        30,
        'SC,ST',
        'Scholarship for higher education',
        'Financial assistance for SC/ST students pursuing higher education',
        'https://scholarships.gov.in/'
    ),
    (
        'National Scholarship Portal (OBC)',
        'student',
        3.0,
        'any',
        16,
        30,
        'OBC',
        'Merit-based scholarship for OBC students',
        'Scholarship for OBC students based on merit and family income',
        'https://scholarships.gov.in/'
    ),
    (
        'Pradhan Mantri Matru Vandana Yojana',
        'any',
        5.0,
        'female',
        18,
        45,
        'any',
        'Rs 5000 for pregnant and lactating mothers',
        'Cash incentive for pregnant and lactating mothers',
        'https://wcd.nic.in/schemes/pradhan-mantri-matru-vandana-yojana'
    ),
    (
        'Beti Bachao Beti Padhao',
        'student',
        5.0,
        'female',
        0,
        21,
        'any',
        'Financial support for girl child education',
        'Scheme to promote education and welfare of girl children',
        'https://wcd.nic.in/schemes/beti-bachao-beti-padhao-scheme'
    )
]

cursor.executemany('''
    INSERT INTO schemes (name, target_occupation, max_income, gender, min_age, max_age, category, benefit, description, application_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', schemes)

conn.commit()

# Verify data
cursor.execute('SELECT COUNT(*) FROM schemes')
count = cursor.fetchone()[0]

print(f"✅ Database initialized successfully!")
print(f"✅ Created schemes table")
print(f"✅ Inserted {count} schemes")
print(f"✅ Database location: {DB_PATH}")

# Display schemes
cursor.execute('SELECT id, name, target_occupation, benefit FROM schemes')
print("\n📋 Schemes in database:")
for row in cursor.fetchall():
    print(f"  {row[0]}. {row[1]} ({row[2]}) - {row[3]}")

conn.close()
