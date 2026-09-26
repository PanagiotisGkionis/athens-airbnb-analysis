import pandas as pd

import matplotlib.pyplot as plt

import sqlite3

# 1. Φόρτωση των δεδομένων
df = pd.read_csv('listings.csv', low_memory=False)

# 2. Επιλογή των στηλών που υπάρχουν στο μικρό listings.csv
columns_to_keep = [
    'id', 'name', 'neighbourhood', 'latitude', 'longitude',
    'room_type', 'price', 'number_of_reviews'
]
df = df[columns_to_keep]

# 3. Καθαρισμός της στήλης 'price'
# Γεμίζουμε τυχόν κενά με 0 και μετατρέπουμε σε float
df['price'] = df['price'].fillna(0).astype(float)

# 4. Έλεγχος και Επιβεβαίωση
print("Τα δεδομένα καθαρίστηκαν επιτυχώς!")
print("\nΟι πρώτες 5 γραμμές του dataset:")
print(df.head())

# 5. Πρώτη Ανάλυση: Μέση τιμή ανά γειτονιά
print("\nΟι 10 πιο ακριβές γειτονιές κατά μέσο όρο:")
top_neighbourhoods = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)
print(top_neighbourhoods.head(10))

# 6. Ανάλυση δημοφιλίας ανά τύπο δωματίου (room_type)
print("\n=== ΑΝΑΛΥΣΗ ΔΗΜΟΦΙΛΙΑΣ ΑΝΑ ΤΥΠΟ ΔΩΜΑΤΙΟΥ ===")

# Ομαδοποίηση και υπολογισμός πλήθους ακινήτων και συνολικών κριτικών
room_analysis = df.groupby('room_type').agg(
    Arithmos_Akiniton=('id', 'count'),
    Synolikes_Kritikes=('number_of_reviews', 'sum'),
    Mesi_Timi=('price', 'mean')
).sort_values(ascending=False, by='Synolikes_Kritikes')

# Εμφάνιση των αποτελεσμάτων
print(room_analysis)

df.to_csv('athens_airbnb_clean.csv', index=False)
print("\nΤο καθαρό αρχείο 'athens_airbnb_clean.csv' αποθηκεύτηκε!")

# 1. Δημιουργία σύνδεσης με μια εικονική βάση δεδομένων στη μνήμη (RAM)
conn = sqlite3.connect(':memory:')

# 2. Μεταφορά του DataFrame της Pandas σε πίνακα SQL με το όνομα 'listings'
df.to_sql('listings', conn, index=False, if_exists='replace')

# 3. Συνάρτηση για να τρέχουμε εύκολα τα SQL queries και να βλέπουμε τα αποτελέσματα
def run_query(query):
    return pd.read_sql_query(query, conn)

query_1 = """
SELECT neighbourhood, 
       COUNT(id) AS total_properties, 
       AVG(price) AS average_price
FROM listings
GROUP BY neighbourhood
HAVING total_properties >= 50
ORDER BY average_price ASC
LIMIT 5;
"""
print("\n=== TOP 5 ΟΙΚΟΝΟΜΙΚΕΣ ΓΕΙΤΟΝΙΕΣ (Με >= 50 ακίνητα) ===")
print(run_query(query_1))


query_2 = """
SELECT id, name, neighbourhood, room_type, price, number_of_reviews,
       (price * number_of_reviews) AS estimated_revenue
FROM listings
WHERE number_of_reviews > 0
ORDER BY estimated_revenue DESC
LIMIT 5;
"""
print("\n=== TOP 5 ΑΚΙΝΗΤΑ ΜΕ ΤΑ ΥΨΗΛΟΤΕΡΑ ΕΚΤΙΜΩΜΕΝΑ ΕΣΟΔΑ ===")
print(run_query(query_2))

query_3 = """
SELECT neighbourhood,
       COUNT(id) AS total_listings,
       SUM(CASE WHEN room_type = 'Entire home/apt' THEN 1 ELSE 0 END) * 100.0 / COUNT(id) AS pct_entire_homes
FROM listings
GROUP BY neighbourhood
HAVING total_listings > 20
ORDER BY pct_entire_homes DESC
LIMIT 5;
"""
print("\n=== TOP 5 ΓΕΙΤΟΝΙΕΣ ΜΕ ΤΟ ΥΨΗΛΟΤΕΡΟ % ΟΛΟΚΛΗΡΩΝ ΔΙΑΜΕΡΙΣΜΑΤΩΝ ===")
print(run_query(query_3))



