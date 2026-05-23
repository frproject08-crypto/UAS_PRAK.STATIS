# UAS PRAKTIKUM STATISTIKA DAN PROBABILITAS
# data_uas_phton_xlxs Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

# Folder output grafik
OUTPUT_DIR = r"C:\\Users\\Lenovo\\Documents\\UAS PRAK STATISTIKA\\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
warnings.filterwarnings('ignore')

# Pengaturan tampilan
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
pd.set_option('display.float_format', '{:,.2f}'.format)
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'

#TAHAP 1: PERSIAPAN DATA

print("=" * 60)
print("TAHAP 1: PERSIAPAN DATA")
print("=" * 60)

# 1. Baca dataset
data = pd.read_excel("data_uas_phyton.xlsx")

# 2. Tampilkan 6 data pertama
print("\n--- 6 Data Pertama ---")
print(data.head(6).to_string())

# 3. Tampilkan 6 data terakhir
print("\n--- 6 Data Terakhir ---")
print(data.tail(6).to_string())

# 4. Tampilkan struktur data
print("\n--- Struktur Data (Info) ---")
data.info()

# 5. Tampilkan ringkasan statistik awal
print("\n--- Ringkasan Statistik Awal ---")
print(data.describe(include='all').to_string())

# 6. Tampilkan jumlah baris dan kolom
print(f"\n--- Jumlah Baris dan Kolom ---")
print(f"Jumlah Baris  : {data.shape[0]}")
print(f"Jumlah Kolom  : {data.shape[1]}")


# TAHAP 2: ANALISIS STATISTIK DESKRIPTIF DASAR

print("\n" + "=" * 60)
print("TAHAP 2: ANALISIS STATISTIK DESKRIPTIF DASAR")
print("=" * 60)

# 1. Rata-rata penjualan
rata_rata_sales = data['Sales'].mean()
print(f"\n1. Rata-rata Penjualan (Sales) : {rata_rata_sales:,.2f}")

# 2. Statistik Sales
print("\n2. Statistik Penjualan (Sales):")
print(f"   a. Minimum          : {data['Sales'].min():,.2f}")
print(f"   b. Maksimum         : {data['Sales'].max():,.2f}")
print(f"   c. Median           : {data['Sales'].median():,.2f}")
print(f"   d. Standar Deviasi  : {data['Sales'].std():,.2f}")
print(f"   e. Kuartil Pertama  : {data['Sales'].quantile(0.25):,.2f}")
print(f"   f. Kuartil Ketiga   : {data['Sales'].quantile(0.75):,.2f}")

# 3. Top 10 Order ID dengan penjualan terbesar
print("\n3. Top 10 Order ID dengan Penjualan Terbesar:")
top10_terbesar = data[['Order ID', 'Sales']].sort_values('Sales', ascending=False).head(10).reset_index(drop=True)
top10_terbesar.index += 1
print(top10_terbesar.to_string())

# 4. Top 10 Order ID dengan penjualan terkecil
print("\n4. Top 10 Order ID dengan Penjualan Terkecil:")
top10_terkecil = data[['Order ID', 'Sales']].sort_values('Sales', ascending=True).head(10).reset_index(drop=True)
top10_terkecil.index += 1
print(top10_terkecil.to_string())

# 5. Jumlah transaksi berdasarkan kategori
print("\n5. Jumlah Transaksi:")
for col in ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category', 'Order Priority']:
    print(f"\n   Berdasarkan {col}:")
    result = data[col].value_counts().reset_index()
    result.columns = [col, 'Jumlah Transaksi']
    print(result.to_string(index=False))

# 6. Total penjualan berdasarkan kategori
print("\n6. Total Penjualan:")
for col in ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category', 'Order Priority']:
    print(f"\n   Berdasarkan {col}:")
    result = data.groupby(col)['Sales'].sum().sort_values(ascending=False).reset_index()
    result.columns = [col, 'Total Penjualan']
    result['Total Penjualan'] = result['Total Penjualan'].map('{:,.2f}'.format)
    print(result.to_string(index=False))

# 7. Total, rata-rata, min, max untuk Quantity, Discount, Profit, Shipping Cost
print("\n7. Statistik Quantity, Discount, Profit, Shipping Cost:")
cols_stat = ['Quantity', 'Discount', 'Profit', 'Shipping Cost']
stat_df = data[cols_stat].agg(['sum', 'mean', 'min', 'max'])
stat_df.index = ['Total', 'Rata-rata', 'Minimum', 'Maksimum']
print(stat_df.to_string())

# 8. Interpretasi
print("""
8. Interpretasi Statistik Deskriptif:
   - Rata-rata penjualan cukup tinggi, namun nilai standar deviasi yang besar
     menunjukkan variasi penjualan antar transaksi sangat lebar.
   - Penjualan minimum sangat kecil sementara maksimum sangat besar,
     mengindikasikan adanya transaksi bernilai sangat tinggi (outlier).
   - Standard Class mendominasi jumlah transaksi berdasarkan Ship Mode.
   - Segmen Consumer memiliki jumlah transaksi paling banyak.
   - Kategori Office Supplies memiliki transaksi terbanyak, namun
     Technology cenderung menyumbang nilai penjualan yang lebih besar per transaksi.
""")


# TAHAP 3: ANALISIS PENJUALAN BERDASARKAN LOKASI

print("=" * 60)
print("TAHAP 3: ANALISIS PENJUALAN BERDASARKAN LOKASI")
print("=" * 60)

# 1. Top 5 kota dengan total penjualan terbesar
print("\n1. Top 5 Kota dengan Total Penjualan Terbesar:")
top5_city = data.groupby('City')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
top5_city.columns = ['City', 'Total Penjualan']
print(top5_city.to_string(index=False))

#2. Visualisasi top 5 kota
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=top5_city, x='City', y='Total Penjualan', palette='Blues_d', ax=ax)
ax.set_title('Top 5 Kota dengan Total Penjualan Terbesar')
ax.set_xlabel('Kota')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10000,
            f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_top5_kota.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_top5_kota.png")

# 3. Top 5 state/provinsi
print("\n3. Top 5 State/Provinsi dengan Total Penjualan Terbesar:")
top5_state = data.groupby('State')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
top5_state.columns = ['State', 'Total Penjualan']
print(top5_state.to_string(index=False))

# 4. Visualisasi top 5 state
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=top5_state, x='State', y='Total Penjualan', palette='Greens_d', ax=ax)
ax.set_title('Top 5 State/Provinsi dengan Total Penjualan Terbesar')
ax.set_xlabel('State/Provinsi')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10000,
            f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_top5_state.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_top5_state.png")

# 5. Top 5 region
print("\n5. Top 5 Region dengan Total Penjualan Terbesar:")
top5_region = data.groupby('Region')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
top5_region.columns = ['Region', 'Total Penjualan']
print(top5_region.to_string(index=False))

# 6. Visualisasi total penjualan per region
all_region_sales = data.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(11, 5))
sns.barplot(data=all_region_sales, x='Region', y='Sales', palette='Set2', ax=ax)
ax.set_title('Total Penjualan Berdasarkan Region')
ax.set_xlabel('Region')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_penjualan_region.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_penjualan_region.png")

# 7. Total profit per region
print("\n7. Total Profit Berdasarkan Region:")
profit_region = data.groupby('Region')['Profit'].sum().sort_values(ascending=False).reset_index()
profit_region.columns = ['Region', 'Total Profit']
print(profit_region.to_string(index=False))

# 8. Visualisasi total profit per region
fig, ax = plt.subplots(figsize=(11, 5))
colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in profit_region['Total Profit']]
bars = ax.bar(profit_region['Region'], profit_region['Total Profit'], color=colors, edgecolor='white')
ax.set_title('Total Profit Berdasarkan Region')
ax.set_xlabel('Region')
ax.set_ylabel('Total Profit')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
            f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=7)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_profit_region.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_profit_region.png")

# 9. Interpretasi
print("""
9. Interpretasi Analisis Lokasi:
   - Beberapa kota besar mendominasi total penjualan, menunjukkan konsentrasi
     pasar di pusat-pusat urban.
   - Region dengan penjualan tertinggi tidak selalu memiliki profit tertinggi,
     hal ini bisa dipengaruhi oleh tingginya diskon atau biaya pengiriman.
   - Perlu strategi khusus untuk region dengan profit rendah atau negatif
     agar efisiensi bisnis meningkat.
""")


# TAHAP 4: ANALISIS PENJUALAN BERDASARKAN PRODUK

print("=" * 60)
print("TAHAP 4: ANALISIS PENJUALAN BERDASARKAN PRODUK")
print("=" * 60)

# 1. Total penjualan per Category
print("\n1. Total Penjualan Berdasarkan Category:")
sales_cat = data.groupby('Category')['Sales'].sum().sort_values(ascending=False).reset_index()
print(sales_cat.to_string(index=False))

# 2. Visualisasi total penjualan per Category
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(data=sales_cat, x='Category', y='Sales', palette='Set1', ax=ax)
ax.set_title('Total Penjualan Berdasarkan Category')
ax.set_xlabel('Category')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
            f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_penjualan_category.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_penjualan_category.png")

# 3. Top 5 Sub-Category
print("\n3. Top 5 Sub-Category dengan Total Penjualan Terbesar:")
top5_subcat = data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(5).reset_index()
print(top5_subcat.to_string(index=False))

# 4. Visualisasi top 5 Sub-Category
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=top5_subcat, x='Sub-Category', y='Sales', palette='Oranges_d', ax=ax)
ax.set_title('Top 5 Sub-Category dengan Total Penjualan Terbesar')
ax.set_xlabel('Sub-Category')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20000,
            f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_top5_subcat.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_top5_subcat.png")

# 5. Rata-rata penjualan per Category
print("\n5. Rata-rata Penjualan Berdasarkan Category:")
print(data.groupby('Category')['Sales'].mean().reset_index().rename(
    columns={'Sales': 'Rata-rata Penjualan'}).to_string(index=False))

# 6. Rata-rata penjualan per Sub-Category
print("\n6. Rata-rata Penjualan Berdasarkan Sub-Category:")
print(data.groupby('Sub-Category')['Sales'].mean().sort_values(ascending=False).reset_index().rename(
    columns={'Sales': 'Rata-rata Penjualan'}).to_string(index=False))

# 7. Total Quantity per Category
print("\n7. Total Quantity Berdasarkan Category:")
print(data.groupby('Category')['Quantity'].sum().reset_index().to_string(index=False))

# 8. Total Quantity per Sub-Category
print("\n8. Total Quantity Berdasarkan Sub-Category:")
print(data.groupby('Sub-Category')['Quantity'].sum().sort_values(ascending=False).reset_index().to_string(index=False))

# 9. Total Profit per Category
print("\n9. Total Profit Berdasarkan Category:")
print(data.groupby('Category')['Profit'].sum().sort_values(ascending=False).reset_index().to_string(index=False))

# 10. Total Profit per Sub-Category
print("\n10. Total Profit Berdasarkan Sub-Category:")
print(data.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=False).reset_index().to_string(index=False))

# 11. Interpretasi
print("""
11. Interpretasi Analisis Produk:
    - Technology adalah kategori dengan total penjualan tertinggi, diikuti
      Furniture dan Office Supplies.
    - Sub-Category dengan penjualan terbesar mencerminkan produk-produk dengan
      harga satuan tinggi seperti Copiers dan Chairs.
    - Meskipun Office Supplies memiliki jumlah transaksi terbanyak, nilai
      penjualannya lebih rendah karena harga per unit yang kecil.
    - Beberapa Sub-Category memiliki profit negatif yang perlu dievaluasi
      terkait kebijakan diskon atau penetapan harga.
""")


#TAHAP 5: VISUALISASI PENJUALAN BERDASARKAN VARIABEL KATEGORI

print("=" * 60)
print("TAHAP 5: VISUALISASI PENJUALAN BERDASARKAN VARIABEL KATEGORI")
print("=" * 60)

# Helper function untuk bar chart sederhana
def bar_chart(data_series, title, xlabel, ylabel, color_palette='Set2', filename=None, rotation=0):
    df = data_series.sort_values(ascending=False).reset_index()
    df.columns = [xlabel, ylabel]
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df, x=xlabel, y=ylabel, palette=color_palette, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    plt.xticks(rotation=rotation, ha='right' if rotation else 'center')
    for bar in ax.patches:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
                f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    if filename:
        plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
        print(f"   >> Grafik disimpan: {filename}")
    plt.show()

# 1. Total penjualan berdasarkan Ship Mode
print("\n1. Visualisasi Total Penjualan berdasarkan Ship Mode")
bar_chart(data.groupby('Ship Mode')['Sales'].sum(),
          'Total Penjualan Berdasarkan Ship Mode', 'Ship Mode', 'Total Penjualan',
          'Blues_d', 'grafik_sales_shipmode.png')

# 2. Total penjualan berdasarkan Segment
print("\n2. Visualisasi Total Penjualan berdasarkan Segment")
bar_chart(data.groupby('Segment')['Sales'].sum(),
          'Total Penjualan Berdasarkan Segment', 'Segment', 'Total Penjualan',
          'Set1', 'grafik_sales_segment.png')

# 3. Total penjualan berdasarkan Region
print("\n3. Visualisasi Total Penjualan berdasarkan Region")
bar_chart(data.groupby('Region')['Sales'].sum(),
          'Total Penjualan Berdasarkan Region', 'Region', 'Total Penjualan',
          'Set2', 'grafik_sales_region.png', rotation=45)

# 4. Total penjualan berdasarkan Category
print("\n4. Visualisasi Total Penjualan berdasarkan Category")
bar_chart(data.groupby('Category')['Sales'].sum(),
          'Total Penjualan Berdasarkan Category', 'Category', 'Total Penjualan',
          'Paired', 'grafik_sales_category.png')

# 5. Total penjualan berdasarkan Order Priority
print("\n5. Visualisasi Total Penjualan berdasarkan Order Priority")
bar_chart(data.groupby('Order Priority')['Sales'].sum(),
          'Total Penjualan Berdasarkan Order Priority', 'Order Priority', 'Total Penjualan',
          'Accent', 'grafik_sales_orderpriority.png')

# 6. Kombinasi Region dan Category (heatmap)
print("\n6. Visualisasi Total Penjualan berdasarkan Kombinasi Region dan Category")
pivot_rc = data.pivot_table(values='Sales', index='Region', columns='Category', aggfunc='sum')
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(pivot_rc, annot=True, fmt=',.0f', cmap='YlOrRd', linewidths=0.5, ax=ax)
ax.set_title('Total Penjualan: Region vs Category')
ax.set_xlabel('Category')
ax.set_ylabel('Region')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_heatmap_region_category.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_heatmap_region_category.png")

# 7. Kombinasi Ship Mode dan Category (grouped bar)
print("\n7. Visualisasi Total Penjualan berdasarkan Kombinasi Ship Mode dan Category")
pivot_sc = data.groupby(['Ship Mode', 'Category'])['Sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=pivot_sc, x='Ship Mode', y='Sales', hue='Category', palette='Set1', ax=ax)
ax.set_title('Total Penjualan: Ship Mode vs Category')
ax.set_xlabel('Ship Mode')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.legend(title='Category', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_shipmode_category.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_shipmode_category.png")

# 8. Kombinasi Segment dan Category (grouped bar)
print("\n8. Visualisasi Total Penjualan berdasarkan Kombinasi Segment dan Category")
pivot_seg = data.groupby(['Segment', 'Category'])['Sales'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=pivot_seg, x='Segment', y='Sales', hue='Category', palette='Set2', ax=ax)
ax.set_title('Total Penjualan: Segment vs Category')
ax.set_xlabel('Segment')
ax.set_ylabel('Total Penjualan')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.legend(title='Category', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_segment_category.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_segment_category.png")

# 9. Total profit berdasarkan Order Priority
print("\n9. Visualisasi Total Profit berdasarkan Order Priority")
profit_op = data.groupby('Order Priority')['Profit'].sum().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#e74c3c' if x < 0 else '#3498db' for x in profit_op['Profit']]
bars = ax.bar(profit_op['Order Priority'], profit_op['Profit'], color=colors, edgecolor='white', width=0.5)
ax.set_title('Total Profit Berdasarkan Order Priority')
ax.set_xlabel('Order Priority')
ax.set_ylabel('Total Profit')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
            f"{bar.get_height():,.0f}", ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'grafik_profit_orderpriority.png'), dpi=150)
plt.show()
print("   >> Grafik disimpan: grafik_profit_orderpriority.png")

# 10. Interpretasi
print("""
10. Interpretasi Visualisasi Tahap 5:
    1. Ship Mode   : Standard Class mendominasi total penjualan, menunjukkan
                     preferensi pelanggan pada metode pengiriman standar.
    2. Segment     : Consumer menyumbang penjualan tertinggi, diikuti Corporate
                     dan Home Office.
    3. Region      : Beberapa region seperti Central dan West (jika data US)
                     atau APAC (global) memimpin penjualan.
    4. Category    : Technology unggul dalam total penjualan dibanding dua
                     kategori lainnya.
    5. Order Priority: Medium priority mendominasi penjualan, mengindikasikan
                     sebagian besar pesanan bersifat rutin.
    6. Region x Category: Heatmap menunjukkan kombinasi region dan kategori
                     mana yang paling produktif secara penjualan.
    7. Ship Mode x Category: Technology cenderung dikirim dengan berbagai
                     metode pengiriman, sementara Office Supplies lebih
                     banyak menggunakan Standard Class.
    8. Segment x Category: Segment Consumer dan Corporate aktif di semua
                     kategori, sementara Home Office lebih terfokus.
    9. Profit x Order Priority: Critical dan High priority cenderung
                     menghasilkan profit lebih tinggi per transaksi.
""")

print("\n" + "=" * 60)
print("ANALISIS SELESAI - Semua grafik telah disimpan.")
print("=" * 60)