import sqlite3

# 1. Δημιουργία σύνδεσης με μια εικονική βάση δεδομένων στη μνήμη (RAM)
conn = sqlite3.connect(':memory:')

# 2. Μεταφορά του DataFrame της Pandas σε πίνακα SQL με το όνομα 'listings'
df.to_sql('listings', conn, index=False, if_exists='replace')

# 3. Συνάρτηση για να τρέχουμε εύκολα τα SQL queries και να βλέπουμε τα αποτελέσματα
def run_query(query):
    return pd.read_sql_query(query, conn)
