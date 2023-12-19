import PySimpleGUI as sg
import pandas as pd
from fpdf import FPDF
from datetime import datetime

sg.theme('Topanga')

data = pd.read_csv('databases.csv').to_dict(orient='records')

csv_FILE = 'databases.csv'
df = pd.read_csv(csv_FILE, sep=",")
print(df)

layout_l = [
    [sg.Text('Kode barang', size=(15, 1)), sg.InputText(key='Kode Barang')],
    [sg.Text('Jumlah', size=(15, 1)), sg.InputText(key='Jumlah')],
    [sg.Submit(), sg.Button('Clear'), sg.Button('Keluar')],
    [sg.Text('Hapus Barang', size=(15, 1)), sg.InputText(key='Hapus Barang'), sg.Button('Hapus')],
    [sg.Text('Total Harga', size=(15, 1)), sg.InputText(key='Total Harga', disabled=True)],
    [sg.Text('Uang', size=(15, 1)), sg.InputText(key='Uang')],
    [sg.Text('Kembalian', size=(15, 1)), sg.InputText(key='Kembalian', disabled=True)],
    [sg.Button('Hitung'), sg.Button('Cetak Struk')]
]

layout_r = [
    [sg.Multiline('Nama Barang \t\t Harga Satuan \t Jumlah \t\t Harga Total\n================================================\n', size=(55, 10), disabled=True, expand_x=True, key='-MULTILINE KEY-')]
]

layout = [
    [sg.Text("Cari Barang:"), sg.InputText(key='SEARCH', enable_events=True)],
    [sg.Column([[sg.Listbox(values=[], size=(65, 10), key='LISTBOX')]], key='LISTBOX_COLUMN')],
    [sg.Col(layout_l), sg.Col(layout_r)],
]

window = sg.Window('Sistem Kasir dan Pencarian Barang', layout)

def search_items(search_query):
    search_query = search_query.lower()
    return [f"{item['Kode Barang']} - {item['Nama Barang']} - {item['Harga Satuan']}" for item in data if search_query in item['Nama Barang'].lower()]
def hapus_barang(kode_barang_hapus, multiline_key):
    global sum
    lines = multiline_key.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith(f'{kode_barang_hapus} '):
            _, _, _, harga_total = line.rsplit('\t', 3)
            sum -= int(harga_total.strip())
            continue
        new_lines.append(line)
    return '\n'.join(new_lines)

def cetak_struk(data_struk, total_harga, uang, kembalian):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    file_name = now.strftime("Struk_%Y%m%d_%H%M%S.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Struk Pembelian", ln=True, align='C')

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=formatted_date, ln=True, align='C')

    start_x = 10
    start_y = 30
    pdf.set_xy(start_x, start_y)

    for line in data_struk.split('\n'):
        pdf.cell(0, 10, txt=line, ln=True)
        pdf.set_x(start_x)
    
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Total Harga: {total_harga}", ln=True)
    pdf.cell(0, 10, txt=f"Uang: {uang}", ln=True)
    pdf.cell(0, 10, txt=f"Kembalian: {kembalian}", ln=True)

    pdf.output(file_name)

def clear_input():
    for key in ['Kode Barang', 'Jumlah', 'Total Harga', 'Uang', 'Kembalian']:
        window[key].update('')
    window['-MULTILINE KEY-'].update('Nama Barang \t\t Harga Satuan \t Jumlah \t Harga Total\n================================================\n')
    global sum
    sum = 0

sum = 0

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Keluar':
        break

    if event == 'SEARCH':
        search_result = search_items(values['SEARCH'])
        window['LISTBOX'].update(search_result)

    if event == 'Clear':
        clear_input()

    if event == 'Hapus':
        kode_barang_hapus = values['Hapus Barang']
        if kode_barang_hapus:
            updated_text = hapus_barang(kode_barang_hapus, values['-MULTILINE KEY-'])
            window['-MULTILINE KEY-'].update(updated_text)
            window['Total Harga'].update(sum)
        else:
            sg.popup_error('Masukkan kode barang yang ingin dihapus!')

    if event == 'Submit':
        try:
            kode_barang = int(values['Kode Barang'])
            searcha = df[df["Kode Barang"] == kode_barang]
            if not searcha.empty:
                value1 = searcha.values
                kode, nama, harga = value1[0][0], value1[0][1], value1[0][2]
                jumlah = int(values['Jumlah'])
                total = harga * jumlah
                sum += total
                window['Total Harga'].update(sum)
                window['-MULTILINE KEY-'].print(f'{nama} \t\t {harga} \t\t {jumlah} \t {total}')
            else:
                sg.popup_error('Barang tidak ditemukan!')
        except ValueError:
            sg.popup_error('Masukkan angka yang valid!')

    if event == 'Hitung':
        try:
            uang = int(values['Uang'])
            if uang < sum:
                sg.popup_error('Uang tidak cukup!')
            else:
                kembalian = uang - sum
                window['Kembalian'].update(kembalian)
        except ValueError:
            sg.popup_error('Masukkan jumlah uang yang valid!')

    if event == 'Cetak Struk':
        if sum > 0 and 'Uang' in values and 'Kembalian' in values:
            cetak_struk(values['-MULTILINE KEY-'], sum, values['Uang'], kembalian)
        else:
            sg.popup_error('Data tidak lengkap!')

window.close()
