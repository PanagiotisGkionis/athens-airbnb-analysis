import matplotlib.pyplot as plt

# Δημιουργία του γραφήματος
plt.figure(figsize=(10, 6))

# Σχεδιάζουμε τις μπάρες (Τύπος Δωματίου vs Συνολικές Κριτικές)
plt.bar(room_analysis.index, room_analysis['Synolikes_Kritikes'], color='skyblue', edgecolor='black')

# Προσθήκη τίτλων και ετικετών
plt.title('Ζήτηση ανά Τύπο Δωματίου στην Αθήνα (Με βάση τις Κριτικές)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Τύπος Δωματίου (Room Type)', fontsize=12, labelpad=10)
plt.ylabel('Συνολικός Αριθμός Κριτικών', fontsize=12, labelpad=10)

# Βελτίωση της εμφάνισης των αριθμών στον Y άξονα
plt.ticklabel_format(style='plain', axis='y')

# Αυτόματη προσαρμογή για να μην κόβονται τα κείμενα
plt.tight_layout()

# Εμφάνιση του γραφήματος στην οθόνη
plt.show()
