import PySimpleGUI as sg
import csv

def tambah_data(file_name, kode_barang, nama_barang, harga_satuan):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([kode_barang, nama_barang, harga_satuan])

def kurangi_data(file_name, target_kode_barang):
    with open(file_name, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    
    index_to_remove = None
    for i, row in enumerate(rows):
        if i > 0 and int(row[0]) == target_kode_barang:
            index_to_remove = i
            break

    
    if index_to_remove is not None:
        removed_row = rows.pop(index_to_remove)
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return removed_row
    else:
        return None

def main():
    sg.theme('Topanga')

    
    layout = [
        [sg.Text('Pilih aksi:'), sg.Radio('Tambah', 'RADIO1', key='tambah', default=True), sg.Radio('Hapus', 'RADIO1', key='hapus')],
        [sg.Text('Kode Barang:'), sg.InputText(key='kode_barang')],
        [sg.Text('Nama Barang:'), sg.InputText(key='nama_barang')],
        [sg.Text('Harga Satuan:'), sg.InputText(key='harga_satuan')],
        [sg.Button('Submit'), sg.Button('Exit')],
        [sg.Output(size=(60, 10))]
    ]

    window = sg.Window('Tambah dan Hapus barang', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Submit':
            if values['tambah']:
                kode_barang_input = int(values['kode_barang'])
                nama_barang_input = values['nama_barang']
                harga_satuan_input = int(values['harga_satuan'])

                tambah_data("databases.csv", kode_barang_input, nama_barang_input, harga_satuan_input)
                print("Data berhasil ditambahkan.")
            elif values['hapus']:
                kode_barang_yang_akan_dihapus = int(values['kode_barang'])
                data_yang_dihapus = kurangi_data("databases.csv", kode_barang_yang_akan_dihapus)

                if data_yang_dihapus:
                    print(f"Data dengan Kode Barang {kode_barang_yang_akan_dihapus} telah dihapus:")
                    print(data_yang_dihapus)
                else:
                    print(f"Tidak ada data dengan Kode Barang {kode_barang_yang_akan_dihapus}.")

    window.close()

def run():
    main()
