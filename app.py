import streamlit as st
import pandas as pd
import os
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Pengeluaran BMN", layout="wide")

# KECILKAN SIDEBAR
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            width: 180px !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Aplikasi Pengeluaran Barang Persediaan")

# =========================
# FILE
# =========================
FILE = "data_pengeluaran_bmn.xlsx"

# =========================
# MENU
# =========================
menu = st.sidebar.radio(
    "Menu",
    ["Input Data", "Lihat Data", "Edit Data"],
    label_visibility="collapsed"
)

# =========================
# MASTER BARANG
# =========================
data_master = {
    "Alat Tulis": [
        "Pilot Ball Liner Hitam","Spidol White Board Marker BG-12",
        "Pilot Ball Liner Hijau","Pilot Ball Liner Merah",
        "Pensil 2B Faber Castell (Kotak)","Stabilo Boss Art",
        "Snowman V-5","Snowman V-8 (Kotak)",
        "Pensil 2B (Kotak)","Tipex Kiriko",
        "Stip Pensil Steadler","Rautan Pensil"
    ],
    "Amplop": [
        "Amplop Cokelat Kecil-B (Bungkus)",
        "Amplop Cokelat Sedang-C (Bungkus)",
        "Amplop Cokelat Jumbo-E (Bungkus)",
        "Amplop Putih Besar (Kotak)",
        "Amplop Putih Kecil (Kotak)",
        "Amplop Besar KOP Kantor"
    ],
    "APAR": ["APAR 4L"],
    "Bahan Bakar": ["Dexlite"],
    "Box File": ["Box File Folio"],
    "Cutter": ["Cutter"],
    "Buku": ["Buku Tombow Mono Corection Tape","Buku Folio Kiky 100"],
    "Baterai": ["Baterai Kotak 9V","Baterai Kecil AA","Baterai Mini AAA"],
    "Clip": ["Binder 111 Clips (Kotak)","Binder 155 Clips (Kotak)","Binder Clips 200 (Kotak)"],
    "Lakban/Selotip": [
        "Lakban Bening (Roll)",
        "Lakban Hitam (Roll)",
        "Lakban Cokelat (Roll)",
        "Double Tap Side 48mm"
    ],
    "Lampu": [
        "Lampu Philips LED 8W","Lampu Philips LED 10W",
        "Lampu Philips LED 14.5W","Lampu Philips LED 12W"
    ],
    "Map": ["Map Batik","Map Biasa (Pak)","Map Business File"],
    "Lem": ["Lem Povinal","Pronto Glue Stick 15G"],
    "Materai": ["Materai 10000 2021"],
    "Masker": ["Masker Telinga (Box)","Masker Onemed (Kotak)","Masker DB"],
    "Staples": ["Staples Kecil-10 (Kotak)"],
    "Tinta": [
        "Tinta Stempel","Tinta Printer Canon DP40 Hitam (Kotak)",
        "Tinta Printer Canon DP41 Warna (Kotak)",
        "Tinta Printer Canon 790 Hitam","Tinta Printer Canon 790 Cyan",
        "Tinta Printer Canon 790 Magenta","Tinta Printer Canon 790 Yellow",
        "Tinta HP GT53 Hitam","Tinta HP GT52 Cyan",
        "Tinta HP GT52 Magenta","Tinta HP GT52 Yellow",
        "Tinta Printer Epson Hitam 003","Tinta Printer Epson Cyan 003",
        "Tinta Printer Epson Yellow 003","Tinta Printer Epson Magenta 003",
        "Canon 71 Cyan G2020","Canon 71 Yellow G2020",
        "Canon 71 Magenta G2020","Tinta Data Print HP Black",
        "Tinta Data HP Color"
    ],
    "Tissue": [
        "Tissue Jolly Napkin","Tissue Paseo Refill 250",
        "Tissue Jolly Napkin (240S)","Tissue Paseo Refill Smart 250",
        "Mitu Wetties Tissue"
    ]
}

# =========================
# NOMOR OTOMATIS
# =========================
def generate_nomor(df):
    if len(df) == 0:
        return "BTR-001"
    last = df["Nomor"].iloc[-1]
    try:
        num = int(str(last).split("-")[1]) + 1
    except:
        num = 1
    return f"BTR-{num:03d}"

# =========================
# INPUT DATA
# =========================
if menu == "Input Data":
    st.header("Input Pengeluaran Barang")

    if os.path.exists(FILE):
        df = pd.read_excel(FILE)
    else:
        df = pd.DataFrame(columns=[
            "Tanggal","Nomor","Kategori","Nama Barang","Jumlah","Bidang","Keterangan"
        ])

    nomor_otomatis = generate_nomor(df)

    col1, col2 = st.columns(2)

    with col1:
        tanggal = st.date_input("Tanggal")
        nomor = st.text_input("Nomor", nomor_otomatis)

    with col2:
        jumlah = st.number_input("Jumlah Keluar", min_value=1, step=1)

    kategori = st.selectbox("Pilih Kategori", list(data_master.keys()))
    nama_barang = st.selectbox("Pilih Barang", data_master[kategori])

    bidang = st.text_input("Bidang / Ruang Tujuan")
    keterangan = st.text_area("Keterangan")

    if st.button("Simpan"):
        if bidang == "":
            st.warning("Bidang harus diisi!")
        else:
            data_baru = pd.DataFrame([{
                "Tanggal": pd.to_datetime(tanggal),
                "Nomor": nomor,
                "Kategori": kategori,
                "Nama Barang": nama_barang,
                "Jumlah": int(jumlah),
                "Bidang": bidang,
                "Keterangan": keterangan
            }])

            df = pd.concat([df, data_baru], ignore_index=True)
            df.to_excel(FILE, index=False)

            st.success("Data berhasil disimpan!")

# =========================
# LIHAT DATA
# =========================
elif menu == "Lihat Data":
    st.header("Data Pengeluaran")

    if os.path.exists(FILE):
        df = pd.read_excel(FILE)
        df = df.sort_values(by="Tanggal", ascending=False)

        cari = st.text_input("Cari")

        if cari:
            df = df[df.apply(lambda row: cari.lower() in str(row).lower(), axis=1)]

        st.dataframe(df, use_container_width=True)

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
            label="Download Data Excel",
            data=buffer,
            file_name="data_pengeluaran_bmn.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.info("Belum ada data")

# =========================
# EDIT DATA
# =========================
elif menu == "Edit Data":
    st.header("Edit / Hapus Data")

    if os.path.exists(FILE):
        df = pd.read_excel(FILE)
        df = df.sort_values(by="Tanggal", ascending=False).reset_index(drop=True)

        if len(df) > 0:

            cari = st.text_input("Cari Data")

            if cari:
                df_filter = df[df.apply(lambda row: cari.lower() in str(row).lower(), axis=1)]
            else:
                df_filter = df

            st.dataframe(df_filter, use_container_width=True)

            if len(df_filter) > 0:
                pilih = st.selectbox("Pilih Data", df_filter.index)
                data = df.loc[pilih]

                tanggal = st.date_input("Tanggal", pd.to_datetime(data["Tanggal"]).date())
                nomor = st.text_input("Nomor", data["Nomor"])
                jumlah = st.number_input("Jumlah", value=int(data["Jumlah"]))

                kategori = st.selectbox(
                    "Kategori",
                    list(data_master.keys()),
                    index=list(data_master.keys()).index(data["Kategori"])
                )

                nama_barang = st.selectbox(
                    "Nama Barang",
                    data_master[kategori],
                    index=data_master[kategori].index(data["Nama Barang"])
                    if data["Nama Barang"] in data_master[kategori] else 0
                )

                bidang = st.text_input("Bidang", data["Bidang"])
                keterangan = st.text_area("Keterangan", data["Keterangan"])

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Update"):
                        df.loc[pilih, "Tanggal"] = pd.to_datetime(tanggal)
                        df.loc[pilih, "Nomor"] = nomor
                        df.loc[pilih, "Kategori"] = kategori
                        df.loc[pilih, "Nama Barang"] = nama_barang
                        df.loc[pilih, "Jumlah"] = int(jumlah)
                        df.loc[pilih, "Bidang"] = bidang
                        df.loc[pilih, "Keterangan"] = keterangan
                        df.to_excel(FILE, index=False)
                        st.success("Data berhasil diupdate!")

                with col2:
                    if st.button("Hapus"):
                        df = df.drop(pilih).reset_index(drop=True)
                        df.to_excel(FILE, index=False)
                        st.success("Data berhasil dihapus!")

            else:
                st.warning("Data tidak ditemukan")

            st.divider()
            st.warning("⚠️ Hapus semua data bersifat permanen!")

            if "confirm_delete_all" not in st.session_state:
                st.session_state.confirm_delete_all = False

            if not st.session_state.confirm_delete_all:
                if st.button("Hapus Semua Data"):
                    st.session_state.confirm_delete_all = True
            else:
                st.error("Yakin ingin menghapus SEMUA data?")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Ya, Hapus Semua"):
                        df = pd.DataFrame(columns=df.columns)
                        df.to_excel(FILE, index=False)
                        st.success("Semua data berhasil dihapus!")
                        st.session_state.confirm_delete_all = False

                with col2:
                    if st.button("Batal"):
                        st.session_state.confirm_delete_all = False

        else:
            st.info("Data kosong")

    else:
        st.info("Belum ada data")