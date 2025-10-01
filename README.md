# Market Basket Analysis Web App

Ένα web εργαλείο για **ανάλυση συναλλαγών** με χρήση Apriori / FP-Growth αλγορίθμων και παραγωγή **association rules**.  
Παρέχει επίσης **οπτικοποιήσεις** (heatmaps, frequent itemsets, networks of rules, scatter plots).

---

## 🚀 Features
- Upload CSV με συναλλαγές (ή αυτόματη δημιουργία τυχαίου dataset).
- Εκτέλεση Apriori / FP-Growth.
- Εμφάνιση **frequent itemsets** & **association rules**.
- Δυναμικά **visualizations**:
  - Heatmap of items
  - Barplot frequent itemsets
  - Rules network graph
  - Scatter (support vs confidence, colored by lift)

---

## 🛠 Installation

1. Κάνε clone το repo:
   ```bash
   git clone <url>
   cd <repo>
2. Δημιούργησε virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
3. Εγκατέστησε dependencies
   ```bash
   pip install -r requirements.txt

## ▶️ Run the app
1. Τρέξε το backend
   ```bash
   cd backend
   py app.py
2. Άνοιξε το frontend
   Απλά ανοίγεις το αρχείο **frontend/static/home.html** σε οποιονδήποτε web browser

## 💭 Suggested use

1. Ανέβασε ένα αρχείο **.csv** ακολουθώντας αυστηρά της οδηγίες για το uploading
2. Μπες στο μενού **Preprocessing** για τον αυτόματο καθαρισμό και προεπεξεργασία του αρχείου
3. Έπειτα μπες στο μενού **Analysis** για την εκτέλεση του αλγορίθμου Apriori και την εξαγωγή των κανόνων (με βάση το επιλεγμένο confidence, lift & support)
4. Τέλος, δες οπτικοποιημένες αναλύσεις του αρχείου σου στο μενού **Visualise** (βλέπε παραπάνω)

## ‼️IMPORTANT NOTICE
ΤΟ PROJECT **ΔΕΝ ΕΙΝΑΙ ΣΤΗΝ ΤΕΛΙΚΗ ΤΟΥ ΜΟΡΦΗ**. ΔΕΝ ΣΥΝΙΣΤΑΤΑΙ ΑΚΟΜΑ ΤΟ DOWNLOAD.
