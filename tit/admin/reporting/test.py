from fpdf import FPDF
WIDTH = 210
HEIGHT = 297

pdf = FPDF('P', 'mm', 'A4')
pdf.add_font('BebasNeue', '', 'BebasNeue-Regular.ttf', uni=True)
pdf.add_page()
pdf.image("tit/tmp/Letterhead.png", 0, 0, WIDTH)
pdf.set_fill_color(255,255,255)
pdf.rect(5, 50, 100, 50, 'D')
pdf.set_draw_color(255,255,255)
pdf.rect(4, 65, 100, 50, 'DF')
pdf.rect(30, 49, 100, 50, 'DF')

pdf.set_font('BebasNeue', '', 48)
pdf.cell(WIDTH-50, 10, "Threads In Time")
pdf.set_font('BebasNeue', '', 12)
pdf.cell(0, 0, "Date: 2022/01/24")
pdf.ln(20)
pdf.set_font('BebasNeue', '', 32)
pdf.cell(0, 0, "Report")

pdf.image("tit/tmp/image.png", 10, 50, WIDTH/2-20)
pdf.image("tit/tmp/image.png", WIDTH/2+10, 50, WIDTH/2-20)

pdf.output(f'tit\\static\\files\\reports\\test.pdf', 'F')
# pdf.output(f'{app.config["STATIC_PATH"]}files\\reports\\{output}')

print('SUCCESS')