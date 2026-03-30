import streamlit as st
import pandas as pd
import os

FILE = "data_pengeluaran_bmn.xlsx"

st.set_page_config(page_title="Pengeluaran BMN", layout="wide")

st.title("Aplikasi Pengeluaran Barang Persediaan")

menu = st.sidebar.selectbox("Menu", ["Input Data", "Lihat Data"])

# =========================
# AUTO NOMOR
# =========================
def generate_nomor(df):
    if len(df) == 0:
        return "TRX-001"
    last = df["Nomor"].iloc[-1]
    num = int(last.split("-")[1]) + 1
    return f"TRX-{num:03d}"

# =========================
# INPUT DATA
# =========================
if menu == "Input Data":
    st.header("Input Pengeluaran Barang")

    if os.path.exists(FILE):
        df = pd.read_excel(FILE)
    else:
        df = pd.DataFrame(columns=["Tanggal","Nomor","Nama Barang","Jumlah","Bidang","Keterangan"])

    nomor_otomatis = generate_nomor(df)

    col1, col2 = st.columns(2)

    with col1:
        tanggal = st.date_input("Tanggal")
        nomor = st.text_input("Nomor", nomor_otomatis)

    with col2:
        nama = st.text_input("Nama Barang")
        jumlah = st.number_input("Jumlah Keluar", min_value=1, step=1)

    bidang = st.text_input("Bidang / Ruang Tujuan")
    keterangan = st.text_area("Keterangan")

    if st.button("Simpan"):
        if nama == "" or bidang == "":
            st.warning("Data belum lengkap!")
        else:
            data_baru = pd.DataFrame([{
                "Tanggal": tanggal,
                "Nomor": nomor,
                "Nama Barang": nama,
                "Jumlah": jumlah,
                "Bidang": bidang,
                "Keterangan": keterangan
            }])

            df = pd.concat([df, data_baru], ignore_index=True)
            df.to_excel(FILE, index=False)

            st.success("Data pengeluaran berhasil disimpan!")

# =========================
# LIHAT DATA
# =========================
elif menu == "Lihat Data":
    st.header("Data Pengeluaran")

    if os.path.exists(FILE):
        df = pd.read_excel(FILE)

        st.dataframe(df, use_container_width=True)

        # =========================
        # FILTER (PENTING 🔥)
        # =========================
        st.subheader("Filter Data")

        cari = st.text_input("Cari Nama Barang / Bidang")

        if cari:
            df = df[df.apply(lambda row: cari.lower() in str(row).lower(), axis=1)]

        st.dataframe(df, use_container_width=True)

        # =========================
        # EDIT & HAPUS
        # =========================
        if len(df) > 0:
            pilih = st.selectbox("Pilih Data", df.index)

            data = df.loc[pilih]

            st.subheader("Edit Data")

            tanggal = st.date_input("Tanggal", pd.to_datetime(data["Tanggal"]))
            nomor = st.text_input("Nomor", data["Nomor"])
            nama = st.text_input("Nama Barang", data["Nama Barang"])
            jumlah = st.number_input("Jumlah", value=int(data["Jumlah"]))
            bidang = st.text_input("Bidang", data["Bidang"])
            keterangan = st.text_area("Keterangan", data["Keterangan"])

            col1, col2 = st.columns(2)

            # UPDATE
            with col1:
                if st.button("Update"):
                    df.loc[pilih] = [tanggal, nomor, nama, jumlah, bidang, keterangan]
                    df.to_excel(FILE, index=False)
                    st.success("Data berhasil diupdate!")

            # HAPUS
            with col2:
                if st.button("Hapus"):
                    df = df.drop(pilih).reset_index(drop=True)
                    df.to_excel(FILE, index=False)
                    st.success("Data berhasil dihapus!")

        # =========================
        # DOWNLOAD
        # =========================
        with open(FILE, "rb") as f:
            st.download_button("Download Excel", f, file_name="data_pengeluaran.xlsx")

    else:
        st.info("Belum ada data")