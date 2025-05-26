import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
data = pd.read_csv('task2/data.csv')
total_sales = data['Sales'].sum()
plt.figure(figsize=(7, 5))
colors = plt.cm.Paired.colors  #
sales_by_category = data.groupby('Category')['Sales'].sum()
bars = plt.bar(sales_by_category.index, sales_by_category.values, color=colors[:len(sales_by_category)])
plt.title('Sales by Category', fontsize=16, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height * 1.01,
             f'${height:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('sales_by_category.png')
plt.close()
class PDF(FPDF):
    def header(self):
        self.set_fill_color(70, 130, 180)  
        self.rect(0, 0, self.w, 25, 'F')  
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'Automated Sales Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 12)
        self.cell(0, 8, 'Monthly Performance Overview', 0, 1, 'C')
        self.ln(2)
        self.set_text_color(0, 0, 0)  #
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(70, 130, 180) 
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(3)
        self.set_text_color(0, 0, 0)
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, body)
        self.ln()
    def add_image(self, image_path):
        self.image(image_path, x=(self.w - 160) / 2, y=self.get_y(), w=160)
        self.ln(95)
pdf = PDF()
pdf.add_page()
pdf.chapter_title('Introduction')
pdf.chapter_body(f'This report provides an insightful overview of the sales data.\n\n'
                  f'Total Sales: ${total_sales:,.2f}')
pdf.chapter_title('Sales Analysis')
pdf.chapter_body('The following chart illustrates the sales distribution across different categories for this period.')
pdf.add_image('sales_by_category.png')
pdf.output('sales_report1.pdf')
print("Enhanced report generated successfully!")
