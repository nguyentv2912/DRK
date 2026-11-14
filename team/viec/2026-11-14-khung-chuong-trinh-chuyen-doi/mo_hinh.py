# -*- coding: utf-8 -*-
"""
Mo hinh tai chinh "Dau Tu Binh An" tren Skool - 24 thang (phien ban 2).
Ma viec: 2026-11-14-khung-chuong-trinh-chuyen-doi
Nguon: brief.md muc "Hien trang chu du an". Khong dung ban-nhap-cu/.

Chay:  python3 mo_hinh.py   -> ghi tai-chinh.json va tai-chinh.md cung thu muc.
Moi so trong tai-chinh.md deu do script nay tinh.
Don vi noi bo: VND. Hien thi: trieu dong (tr), gia ghi kem USD.
"""
import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TR = 1_000_000  # 1 trieu dong

# =====================================================================
# 1. THAM SO DAU VAO  (sua o day; moi muc co nguon / ly do)
# =====================================================================
P = {
    # --- Gia (chu du an chot, KHONG doi) ---
    "gia_co_ban_usd": 100.0,        # USD/thang, thue bao Skool
    "gia_chuyen_sau_usd": 1000.0,   # USD, gia dinh: thanh toan MOT LAN
    "gia_ebook_vnd": 1_000_000,     # VND, ban kem khoa hoc

    # --- Ty gia & phi ---
    "ty_gia": 26_000,               # VND/USD - gia dinh (vung 25.000-26.500), cho Lan cap nhat ty gia ngay
    # Skool: gia dinh cong khai pho bien - CHO LAN XAC MINH
    # Nguon: nghien-cuu.md (trich doan help.skool.com Payments FAQ, tin cay Trung binh)
    "skool_hobby_phi_thang_usd": 9.0, "skool_hobby_phi_gd": 0.10, "skool_hobby_phi_co_dinh_usd": 0.30,
    "skool_pro_phi_thang_usd": 99.0, "skool_pro_phi_gd": 0.029, "skool_pro_phi_co_dinh_usd": 0.30,
    "skool_pro_phi_gd_lon": 0.039, "skool_nguong_gd_lon_usd": 900.0,  # giao dich > 900 USD: 3,9% + 0,30
    "phi_chuyen_ve_vn": 0.02,       # gia dinh 2% (rut USD qua trung gian/ngan hang + chenh lech quy doi)
    "phi_cong_tt_ebook": 0.01,      # gia dinh 1% (ebook ban bang chuyen khoan/VietQR/cong noi dia)
    # Thue: ca nhan/ho kinh doanh online, dich vu: 5% GTGT + 2% TNCN tren doanh thu = 7%.
    # Gia dinh than trong: ap tu dong dau tien (chua tru nguong mien thue doanh thu thap) - can ke toan xac nhan.
    "thue_tren_doanh_thu": 0.07,
    # nghien-cuu.md: nguong khong chiu thue ho KD 500 tr/nam (Luat TNCN 2025), bao chi neu ND 141/2026 nang len 1 ty (chua doi chieu).
    "ap_nguong_mien_thue": False,     # mac dinh KHONG ap (than trong); True = chi tinh thue phan doanh thu nam vuot nguong
    "nguong_mien_thue_nam": 1_000_000_000,

    # --- Chi phi co dinh hang thang (VND) ---
    "cp_cong_cu_ai": 1_600_000,     # gia dinh ~60 USD: 2 goi AI chat + Canva/CapCut Pro
    "cp_khac_thang": 500_000,       # gia dinh: ten mien, email, Zoom/Meet, luu tru
    "cp_quang_cao_thang": 0,        # mac dinh 0 - dau pheu la video tu nhien
    # Chu du an tu quay, doi AI, van phong, ha tang co san -> 0 (theo brief)

    # --- Von ban dau (VND) ---
    "dt_ebook_thiet_ke": 8_000_000,     # gia dinh: dan trang + bia ebook
    "dt_ebook_bien_tap": 5_000_000,     # gia dinh: bien tap/hieu dinh
    "dt_ebook_isbn": 15_000_000,        # BAT BUOC: ebook ban ra la xuat ban pham dien tu, phai qua NXB (nghien-cuu.md, Luat Xuat ban Dieu 45-46); chi phi lien ket xuat ban = gia dinh
    "dt_tu_van_phap_ly": 10_000_000,    # gia dinh: luat su ra soat dieu khoan, noi dung tai chinh/crypto
    "dt_thiet_bi_quay": 5_000_000,      # gia dinh: mic, den bo sung (co the = 0 neu da co)
    "dt_trang_ban_hang": 3_000_000,     # gia dinh: bo nhan dien Skool, anh bia, trang gioi thieu
    "quy_du_phong_thang": 3,            # quy du phong = 3 thang chi phi co dinh + 3 thang luong CSKH ban thoi gian

    # --- Lich ra mat ---
    "thang_mo_co_ban": 2,       # thang 1 xay cong dong mien phi, thang 2 mo khoa 100 USD
    "thang_mo_chuyen_sau": 3,   # can co noi dung + bai giang dau tien
    "thang_mo_ebook": 3,        # ebook xong sau ~2 thang

    # --- Pheu (gia dinh, xem ly do trong tai-chinh.md) ---
    "nguoi_theo_doi_dau": 0,          # mac dinh 0: kenh dang xay lai (KENH.md) - CHO SO THAT, nhap vao day roi chay lai
    "theo_doi_moi_thang_dau": 2_000,  # gia dinh: nguoi theo doi moi thang 1
    "tang_theo_doi_thang": 0.05,      # gia dinh: nguoi theo doi moi tang 5%/thang (ramp-up)
    "ty_le_vao_skool_moi": 0.05,      # % nguoi theo doi MOI vao Skool mien phi (Skool khong co tieng Viet, phai tao tai khoan -> co rao can)
    "ty_le_vao_skool_ton": 0.05,      # % nguoi theo doi SAN CO vao Skool, rai deu 3 thang dau
    "free_roi_thang": 0.05,           # % thanh vien mien phi roi / ngung hoat dong moi thang
    "cd_free_sang_tra_phi_thang_dau": 0.03,  # % thanh vien mien phi MOI mua 100 USD ngay thang dau
    "cd_free_sang_tra_phi_ton": 0.003,       # % kho mien phi con lai mua moi thang
    "huy_thang": 0.09,                # nghien-cuu.md: churn cong dong tra phi 4-9%/thang (TB 5,8%); lay can tren vi gia 100 USD cao so voi thu nhap VN
    "nang_cap_chuyen_sau_thang": 0.015,  # % hoc vien 100 USD dang hoat dong mua goi 1.000 USD moi thang
    "ebook_kem_co_ban": 0.25,         # % hoc vien 100 USD moi mua ebook
    "ebook_kem_chuyen_sau": 0.40,     # % nguoi mua chuyen sau mua ebook (neu chua co)
    "ebook_tu_free_thang": 0.002,     # % kho mien phi mua ebook moi thang

    # --- Cau truc goi chuyen sau (cho anh chot) ---
    "chuyen_sau_gom_co_ban": False,   # False: goi 1.000 USD la goi BO SUNG, van can thue bao 100 USD
    "chuyen_sau_tra_gop_ky": 1,       # 1 = tra mot lan; 4 = chia 4 ky hang thang
    "tra_gop_bo_ngang": 0.10,         # % nguoi tra gop dung sau ky 1 (chi ap khi > 1 ky)
    # Ghi nhan & quy du phong goi 10 nam
    "cs_ghi_nhan_ngay": 0.20,         # 20% ghi nhan ngay (onboarding, tai lieu), 80% phan bo 120 thang
    "cs_so_thang_phuc_vu": 120,
    "cs_trich_quy": 0.30,             # trich 30% tien thuc nhan goi chuyen sau vao quy phuc vu dai han

    # --- Thue nguoi (chi khi dat nguong; luong thi truong gia dinh, TP.HCM/HN 2026) ---
    "he_so_bhxh": 1.215,              # chi phi nguoi su dung lao dong ~21,5% tren luong nhan vien chinh thuc
    "nhan_su": [
        # ten, luong VND/thang, chinh_thuc?, dieu kien (xem ham can_thue)
        {"ma": "cskh_bt", "ten": "Tro giang/CSKH cong dong (ban thoi gian)", "luong": 6_000_000, "chinh_thuc": False},
        {"ma": "cskh_ft", "ten": "Tro giang/CSKH cong dong (toan thoi gian, thay ban thoi gian)", "luong": 10_000_000, "chinh_thuc": True},
        {"ma": "chot_don", "ten": "Tu van/chot don goi chuyen sau (luong cung + 5% hoa hong)", "luong": 7_000_000, "chinh_thuc": True},
        {"ma": "dung_video", "ten": "Dung video/tro ly noi dung", "luong": 9_000_000, "chinh_thuc": True},
        {"ma": "cskh_ft2", "ten": "CSKH cong dong thu 2", "luong": 10_000_000, "chinh_thuc": True},
        {"ma": "ke_toan", "ten": "Ke toan dich vu (thue ngoai)", "luong": 2_500_000, "chinh_thuc": False},
    ],
    "hoa_hong_chot_don": 0.05,
    "tran_chi_nhan_su": 0.25,          # tong chi nhan su khong vuot 25% doanh thu thang truoc

    "chiet_khau_nam": 0.12,            # gia dinh: chi phi co hoi von 12%/nam
    "so_thang": 24,
}

# Nguong thue nguoi (dua tren so lieu THANG TRUOC)
NGUONG = {
    "cskh_bt": "hoc vien tra phi >= 60",
    "cskh_ft": "hoc vien tra phi >= 200",
    "cskh_ft2": "hoc vien tra phi >= 500",
    "chot_don": "doanh thu thang >= 150 tr va kho mien phi >= 2.000",
    "dung_video": "doanh thu thang >= 200 tr",
    "ke_toan": "doanh thu thang >= 40 tr",
}


def can_thue(ma, hv, dt, free):
    return {
        "cskh_bt": 60 <= hv < 200,
        "cskh_ft": hv >= 200,
        "cskh_ft2": hv >= 500,
        "chot_don": dt >= 150 * TR and free >= 2000,
        "dung_video": dt >= 200 * TR,
        "ke_toan": dt >= 40 * TR,
    }[ma]


def nhan_su_theo(p, hv, dt, free, dt_cs):
    """Tra ve (chi phi nhan su, danh sach ma). Ap tran % doanh thu theo thu tu uu tien."""
    tong, ds = 0.0, []
    for ns in p["nhan_su"]:
        if not can_thue(ns["ma"], hv, dt, free):
            continue
        cp = ns["luong"] * (p["he_so_bhxh"] if ns["chinh_thuc"] else 1.0)
        if ns["ma"] == "chot_don":
            cp += p["hoa_hong_chot_don"] * dt_cs
        if tong + cp <= p["tran_chi_nhan_su"] * dt:
            tong += cp
            ds.append(ns["ma"])
    return tong, ds


def phi_skool(p, n_gd, gross_usd, gross_lon_usd=0.0):
    """Chon goi re hon moi thang. gross_lon_usd = phan doanh thu tu giao dich > 900 USD (Pro: 3,9%).
    Tra ve (phi USD, ten goi)."""
    hobby = (p["skool_hobby_phi_thang_usd"] + p["skool_hobby_phi_gd"] * gross_usd
             + p["skool_hobby_phi_co_dinh_usd"] * n_gd)
    pro = (p["skool_pro_phi_thang_usd"] + p["skool_pro_phi_gd"] * (gross_usd - gross_lon_usd)
           + p["skool_pro_phi_gd_lon"] * gross_lon_usd + p["skool_pro_phi_co_dinh_usd"] * n_gd)
    return (hobby, "Hobby") if hobby <= pro else (pro, "Pro")


# =====================================================================
# 2. MO PHONG THEO THANG
# =====================================================================
def von_ban_dau(p):
    cp_cd = p["cp_cong_cu_ai"] + p["cp_khac_thang"] + p["cp_quang_cao_thang"] \
        + p["skool_pro_phi_thang_usd"] * p["ty_gia"]
    du_phong = p["quy_du_phong_thang"] * (cp_cd + p["nhan_su"][0]["luong"])
    hm = {
        "Thiet ke, dan trang ebook": p["dt_ebook_thiet_ke"],
        "Bien tap ebook": p["dt_ebook_bien_tap"],
        "Lien ket xuat ban qua NXB": p["dt_ebook_isbn"],
        "Tu van phap ly (dieu khoan, noi dung tai chinh/crypto)": p["dt_tu_van_phap_ly"],
        "Thiet bi quay bo sung (mic, den)": p["dt_thiet_bi_quay"],
        "Nhan dien Skool, trang gioi thieu": p["dt_trang_ban_hang"],
        "Quy du phong van hanh (3 thang chi phi co dinh + CSKH)": du_phong,
    }
    return hm, sum(hm.values())


def mo_phong(p):
    fx = p["ty_gia"]
    T = p["so_thang"]
    _, von = von_ban_dau(p)
    theo_doi = p["nguoi_theo_doi_dau"]
    free = 0.0
    hv = 0.0           # hoc vien 100 USD dang hoat dong
    hv_da_nc = 0.0     # trong do: da mua goi chuyen sau (moi nguoi chi mua 1 lan)
    cs_tong = 0.0      # luy ke hoc vien chuyen sau
    tra_gop_dang = []  # danh sach [so_nguoi, ky_con_lai]
    hoan_lai_chua_gn = 0.0  # doanh thu chua ghi nhan (VND)
    quy_cs = 0.0
    prev_hv, prev_dt, prev_free = 0.0, 0.0, 0.0
    luy_ke = -von
    rows = []
    for t in range(1, T + 1):
        moi_theo_doi = p["theo_doi_moi_thang_dau"] * (1 + p["tang_theo_doi_thang"]) ** (t - 1)
        theo_doi_dau_ky = theo_doi
        theo_doi += moi_theo_doi
        free_moi = moi_theo_doi * p["ty_le_vao_skool_moi"]
        if t <= 3:
            free_moi += p["nguoi_theo_doi_dau"] * p["ty_le_vao_skool_ton"] / 3
        free = free * (1 - p["free_roi_thang"])

        hv_moi = 0.0
        if t >= p["thang_mo_co_ban"]:
            hv_moi = free_moi * p["cd_free_sang_tra_phi_thang_dau"] + free * p["cd_free_sang_tra_phi_ton"]
        free = free + free_moi - hv_moi
        hv_huy = hv * p["huy_thang"]

        cs_moi = 0.0
        if t >= p["thang_mo_chuyen_sau"]:
            cs_moi = (hv - hv_da_nc) * p["nang_cap_chuyen_sau_thang"]
        hv_da_nc = hv_da_nc * (1 - p["huy_thang"])
        hv = hv - hv_huy + hv_moi
        if p["chuyen_sau_gom_co_ban"]:
            hv -= cs_moi  # nguoi nang cap ngung tra 100 USD
        else:
            hv_da_nc += cs_moi
        cs_tong += cs_moi

        # --- Doanh thu USD qua Skool ---
        n_cb = hv  # so lan thu phi co ban thang nay
        dt_cb_usd = n_cb * p["gia_co_ban_usd"]
        k = p["chuyen_sau_tra_gop_ky"]
        if k <= 1:
            dt_cs_usd = cs_moi * p["gia_chuyen_sau_usd"]
            n_cs_gd = cs_moi
        else:
            ky = p["gia_chuyen_sau_usd"] / k
            moi_list = []
            dt_cs_usd, n_cs_gd = cs_moi * ky, cs_moi
            for nhom in tra_gop_dang:
                nhom[0] *= (1 - p["tra_gop_bo_ngang"]) if nhom[1] == k - 1 else 1.0
                dt_cs_usd += nhom[0] * ky
                n_cs_gd += nhom[0]
                nhom[1] -= 1
            tra_gop_dang = [n for n in tra_gop_dang if n[1] > 0]
            if k > 1 and cs_moi > 0:
                tra_gop_dang.append([cs_moi, k - 1])
        gross_usd = dt_cb_usd + dt_cs_usd
        ky_usd = p["gia_chuyen_sau_usd"] / max(k, 1)
        lon = dt_cs_usd if ky_usd > p["skool_nguong_gd_lon_usd"] else 0.0
        skool_usd, goi = phi_skool(p, n_cb + n_cs_gd, gross_usd, lon)

        # --- Ebook (ban VND ngoai Skool) ---
        eb = 0.0
        if t >= p["thang_mo_ebook"]:
            eb = (hv_moi * p["ebook_kem_co_ban"] + cs_moi * p["ebook_kem_chuyen_sau"]
                  + free * p["ebook_tu_free_thang"])
        dt_eb = eb * p["gia_ebook_vnd"]

        dt_cb = dt_cb_usd * fx
        dt_cs = dt_cs_usd * fx
        dt = dt_cb + dt_cs + dt_eb

        # --- Chi phi ---
        cp_skool = skool_usd * fx
        cp_chuyen = (gross_usd - skool_usd) * fx * p["phi_chuyen_ve_vn"]
        cp_tt_eb = dt_eb * p["phi_cong_tt_ebook"]
        if (t - 1) % 12 == 0:
            dt_nam_luy_ke = 0.0
        if p["ap_nguong_mien_thue"]:
            vuot = max(0.0, dt_nam_luy_ke + dt - p["nguong_mien_thue_nam"]) - max(0.0, dt_nam_luy_ke - p["nguong_mien_thue_nam"])
            thue = vuot * p["thue_tren_doanh_thu"]
        else:
            thue = dt * p["thue_tren_doanh_thu"]
        dt_nam_luy_ke += dt
        cp_co_dinh = p["cp_cong_cu_ai"] + p["cp_khac_thang"] + p["cp_quang_cao_thang"]
        cp_ns, ds_ns = nhan_su_theo(p, prev_hv, prev_dt, prev_free, dt_cs)
        tong_cp = cp_skool + cp_chuyen + cp_tt_eb + thue + cp_co_dinh + cp_ns
        lai = dt - tong_cp

        # --- Goi 10 nam: ghi nhan & quy ---
        ti_le_thuc = 1 - (cp_skool + cp_chuyen) / max(gross_usd * fx, 1)
        cs_thuc = dt_cs * ti_le_thuc * (1 - p["thue_tren_doanh_thu"])
        trich = cs_thuc * p["cs_trich_quy"]
        quy_cs += trich
        hoan_lai_chua_gn += dt_cs * (1 - p["cs_ghi_nhan_ngay"])
        phan_bo = 0.0
        # phan bo tuyen tinh doanh thu chua ghi nhan (xap xi theo luy ke nguoi mua)
        phan_bo = cs_tong * p["gia_chuyen_sau_usd"] * fx * (1 - p["cs_ghi_nhan_ngay"]) / p["cs_so_thang_phuc_vu"] \
            if k <= 1 else 0.0
        phan_bo = min(phan_bo, hoan_lai_chua_gn)
        hoan_lai_chua_gn -= phan_bo
        dt_ghi_nhan = dt_cb + dt_eb + dt_cs * p["cs_ghi_nhan_ngay"] + phan_bo

        tien_ranh = lai - trich
        luy_ke += lai
        rows.append({
            "thang": t, "theo_doi": theo_doi, "free": free, "hv_moi": hv_moi, "hv_huy": hv_huy,
            "hv": hv, "cs_moi": cs_moi, "cs_tong": cs_tong, "ebook": eb,
            "dt_co_ban": dt_cb, "dt_chuyen_sau": dt_cs, "dt_ebook": dt_eb, "doanh_thu": dt,
            "cp_skool": cp_skool, "goi_skool": goi, "cp_chuyen_tien": cp_chuyen + cp_tt_eb,
            "thue": thue, "cp_co_dinh": cp_co_dinh, "cp_nhan_su": cp_ns, "nhan_su": ds_ns,
            "tong_chi_phi": tong_cp, "lai": lai, "trich_quy_cs": trich, "tien_ranh": tien_ranh,
            "luy_ke": luy_ke, "quy_cs": quy_cs, "dt_chua_ghi_nhan": hoan_lai_chua_gn,
            "dt_ghi_nhan": dt_ghi_nhan,
        })
        prev_hv, prev_dt, prev_free = hv, dt, free
    return rows


def npv_irr(p, rows):
    _, von = von_ban_dau(p)
    cf = [-von] + [r["lai"] for r in rows]
    r_m = (1 + p["chiet_khau_nam"]) ** (1 / 12) - 1
    npv = sum(c / (1 + r_m) ** i for i, c in enumerate(cf))

    def f(r):
        return sum(c / (1 + r) ** i for i, c in enumerate(cf))
    lo, hi = -0.99, 10.0
    irr = None
    if f(lo) * f(hi) < 0:
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
        irr_m = (lo + hi) / 2
        irr = {"thang": irr_m, "nam": (1 + irr_m) ** 12 - 1}
    hoan_von = next((r["thang"] for r in rows if r["luy_ke"] >= 0), None)
    return npv, irr, hoan_von


# =====================================================================
# 3. TRANG THAI ON DINH: can bao nhieu hoc vien de hoa von / dat thu nhap
# =====================================================================
def on_dinh(p, n, co_upsell=True):
    """Lai thang (VND) khi co n hoc vien 100 USD on dinh (so moi = so huy)."""
    fx = p["ty_gia"]
    moi = n * p["huy_thang"]
    u, c = p["nang_cap_chuyen_sau_thang"], p["huy_thang"]
    cs = n * u * c / (c + u) if co_upsell else 0.0  # chi nguoi chua nang cap moi mua
    eb = (moi * p["ebook_kem_co_ban"] + cs * p["ebook_kem_chuyen_sau"]) if co_upsell else 0.0
    gross = n * p["gia_co_ban_usd"] + cs * p["gia_chuyen_sau_usd"]
    lon = cs * p["gia_chuyen_sau_usd"] if p["gia_chuyen_sau_usd"] > p["skool_nguong_gd_lon_usd"] else 0.0
    sk, _ = phi_skool(p, n + cs, gross, lon)
    dt_eb = eb * p["gia_ebook_vnd"]
    dt = gross * fx + dt_eb
    free_gia_dinh = 10_000  # gia dinh: kho mien phi du lon de can nguoi chot don
    ns, _ = nhan_su_theo(p, n, dt, free_gia_dinh, cs * p["gia_chuyen_sau_usd"] * fx)
    cp = (sk * fx + (gross - sk) * fx * p["phi_chuyen_ve_vn"] + dt_eb * p["phi_cong_tt_ebook"]
          + dt * p["thue_tren_doanh_thu"] + p["cp_cong_cu_ai"] + p["cp_khac_thang"]
          + p["cp_quang_cao_thang"] + ns)
    return dt - cp, dt


def hv_can(p, muc_tieu, co_upsell=True):
    for n in range(0, 5001):
        if on_dinh(p, n, co_upsell)[0] >= muc_tieu:
            return n
    return None


def dong_gop_1hv(p):
    """Dong gop/thang cua 1 hoc vien 100 USD, chua tinh upsell (goi Pro, khong tinh phi thang)."""
    fx = p["ty_gia"]
    g = p["gia_co_ban_usd"]
    out = {}
    for goi in ("Hobby", "Pro"):
        if goi == "Hobby":
            sk = p["skool_hobby_phi_gd"] * g + p["skool_hobby_phi_co_dinh_usd"]
        else:
            sk = p["skool_pro_phi_gd"] * g + p["skool_pro_phi_co_dinh_usd"]
        net = (g - sk) * (1 - p["phi_chuyen_ve_vn"]) * fx - g * fx * p["thue_tren_doanh_thu"]
        out[goi] = net
    return out


def ltv_usd(p, gom, u=None):
    """Gia tri tron doi (USD) cua 1 hoc vien 100 USD moi."""
    c = p["huy_thang"]
    u = p["nang_cap_chuyen_sau_thang"] if u is None else u
    if gom:   # thoat khoi thue bao khi huy HOAC nang cap
        thang = 1 / (c + u)
    else:     # van tra 100 USD sau khi nang cap
        thang = 1 / c
    return thang * p["gia_co_ban_usd"] + u / (c + u) * p["gia_chuyen_sau_usd"], thang


# =====================================================================
# 4. KICH BAN & DO NHAY
# =====================================================================
KICH_BAN = {
    # "Khong dang lam": truy cap thap + chuyen doi thap + huy cao -> dung de dat nguong dung/doi cach ban
    "khong_dang_lam": {"theo_doi_moi_thang_dau": 500, "tang_theo_doi_thang": 0.0, "ty_le_vao_skool_moi": 0.02,
                       "cd_free_sang_tra_phi_thang_dau": 0.01, "cd_free_sang_tra_phi_ton": 0.001,
                       "huy_thang": 0.20, "nang_cap_chuyen_sau_thang": 0.005, "ebook_kem_co_ban": 0.10},
    "than_trong": {"theo_doi_moi_thang_dau": 1_000, "tang_theo_doi_thang": 0.03, "ty_le_vao_skool_moi": 0.025,
                   "cd_free_sang_tra_phi_thang_dau": 0.02, "cd_free_sang_tra_phi_ton": 0.002,
                   "huy_thang": 0.15, "nang_cap_chuyen_sau_thang": 0.008, "ebook_kem_co_ban": 0.15},
    "co_so": {},
    "lac_quan": {"theo_doi_moi_thang_dau": 3_500, "tang_theo_doi_thang": 0.06, "ty_le_vao_skool_moi": 0.08,
                 "cd_free_sang_tra_phi_thang_dau": 0.045, "cd_free_sang_tra_phi_ton": 0.004,
                 "huy_thang": 0.06, "nang_cap_chuyen_sau_thang": 0.025, "ebook_kem_co_ban": 0.35},
}
NHAN_KB = {
    "theo_doi_moi_thang_dau": "Người theo dõi mới tháng 1", "tang_theo_doi_thang": "Tốc độ tăng người theo dõi mới/tháng",
    "ty_le_vao_skool_moi": "Theo dõi mới → Skool miễn phí", "cd_free_sang_tra_phi_thang_dau": "Miễn phí mới → 100 USD (tháng đầu)",
    "cd_free_sang_tra_phi_ton": "Kho miễn phí → 100 USD (mỗi tháng)", "huy_thang": "Tỷ lệ huỷ/tháng",
    "nang_cap_chuyen_sau_thang": "Nâng cấp 1.000 USD/tháng", "ebook_kem_co_ban": "Mua kèm ebook (HV 100 USD mới)",
}
TEN_KB_VN = {"khong_dang_lam": "Không đáng làm", "than_trong": "Thận trọng", "co_so": "Cơ sở (tham vọng)", "lac_quan": "Lạc quan"}
HDR = " | ".join(TEN_KB_VN[k] for k in KICH_BAN)
SEP = "---:|" * len(KICH_BAN)
TEN_KB = {"khong_dang_lam": "Khong dang lam", "than_trong": "Than trong", "co_so": "Co so", "lac_quan": "Lac quan"}

BIEN_NHAY = {
    "huy_thang": "Ty le huy thang",
    "cd_free_sang_tra_phi_thang_dau": "Chuyen doi free -> 100 USD (thang dau)",
    "cd_free_sang_tra_phi_ton": "Chuyen doi kho free -> 100 USD (hang thang)",
    "theo_doi_moi_thang_dau": "Nguoi theo doi moi/thang",
    "ty_le_vao_skool_moi": "Ty le vao Skool mien phi",
    "nang_cap_chuyen_sau_thang": "Ty le nang cap goi 1.000 USD",
}


def voi(p, **kw):
    q = copy.deepcopy(p)
    q.update(kw)
    return q


def tom_tat(p):
    rows = mo_phong(p)
    npv, irr, hv_ = npv_irr(p, rows)
    nam = []
    for y in (1, 2):
        rr = rows[(y - 1) * 12: y * 12]
        nam.append({
            "nam": y,
            "doanh_thu": sum(r["doanh_thu"] for r in rr),
            "dt_co_ban": sum(r["dt_co_ban"] for r in rr),
            "dt_chuyen_sau": sum(r["dt_chuyen_sau"] for r in rr),
            "dt_ebook": sum(r["dt_ebook"] for r in rr),
            "chi_phi": sum(r["tong_chi_phi"] for r in rr),
            "thue": sum(r["thue"] for r in rr),
            "cp_nhan_su": sum(r["cp_nhan_su"] for r in rr),
            "lai": sum(r["lai"] for r in rr),
            "trich_quy_cs": sum(r["trich_quy_cs"] for r in rr),
            "hv_cuoi_nam": rr[-1]["hv"],
            "cs_luy_ke": rr[-1]["cs_tong"],
        })
    thang_lai = next((r["thang"] for r in rows if r["lai"] > 0), None)
    return {"rows": rows, "npv": npv, "irr": irr, "hoan_von_thang": hv_, "nam": nam,
            "thang_dau_co_lai": thang_lai, "lai_t24": rows[-1]["lai"], "luy_ke_24": rows[-1]["luy_ke"],
            "hv_t24": rows[-1]["hv"], "dt_t24": rows[-1]["doanh_thu"]}


# =====================================================================
# 5. XUAT KET QUA
# =====================================================================
def m(x, d=1):
    """trieu dong, dau phay thap phan kieu VN"""
    s = f"{x / TR:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def so(x, d=0):
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x, d=1):
    return so(x * 100, d) + "%"


def main():
    p = P
    fx = p["ty_gia"]
    hm, von = von_ban_dau(p)
    kq = {k: tom_tat(voi(p, **v)) for k, v in KICH_BAN.items()}
    base = kq["co_so"]

    # Kich ban phu cho goi chuyen sau
    phu = {
        "Tra gop 4 ky x 250 USD (10% bo ngang sau ky 1)": tom_tat(voi(p, chuyen_sau_tra_gop_ky=4)),
        "Goi 1.000 USD GOM luon thue bao co ban (nguoi nang cap ngung tra 100 USD)":
            tom_tat(voi(p, chuyen_sau_gom_co_ban=True)),
        "Goi GOM co ban va nguoi dung chuyen sang hang loat (nang cap 8%/thang)":
            tom_tat(voi(p, chuyen_sau_gom_co_ban=True, nang_cap_chuyen_sau_thang=0.08)),
    }

    dai_han = {"co_so": tom_tat(voi(p, so_thang=60))}
    for k, kw in [(list(phu)[0], {"chuyen_sau_tra_gop_ky": 4}), (list(phu)[1], {"chuyen_sau_gom_co_ban": True}),
                  (list(phu)[2], {"chuyen_sau_gom_co_ban": True, "nang_cap_chuyen_sau_thang": 0.08})]:
        dai_han[k] = tom_tat(voi(p, so_thang=60, **kw))

    def phuc_vu(k, r):
        gom = k != "co_so" and "GOM" in k
        return r["hv_t24"] + (r["rows"][-1]["cs_tong"] if gom else 0)
    ltv = {"bo_sung": ltv_usd(p, False), "gom_1_5": ltv_usd(p, True), "gom_8": ltv_usd(p, True, 0.08)}

    # Do nhay +-20%
    nhay = []
    for k, ten in BIEN_NHAY.items():
        lo = tom_tat(voi(p, **{k: p[k] * 0.8}))
        hi = tom_tat(voi(p, **{k: p[k] * 1.2}))
        nhay.append({"bien": k, "ten": ten, "gia_tri": p[k],
                     "lai_t24_-20": lo["lai_t24"], "lai_t24_+20": hi["lai_t24"],
                     "luy_ke_-20": lo["luy_ke_24"], "luy_ke_+20": hi["luy_ke_24"]})
    vao_skool = {v: tom_tat(voi(p, ty_le_vao_skool_moi=v)) for v in (0.02, 0.04, 0.08)}
    thue_2 = {kb: tom_tat(voi(p, thue_tren_doanh_thu=0.02, **KICH_BAN[kb]))["luy_ke_24"] for kb in KICH_BAN}
    thue_nguong = {kb: tom_tat(voi(p, ap_nguong_mien_thue=True, **KICH_BAN[kb]))["luy_ke_24"] for kb in KICH_BAN}
    fx_lo = tom_tat(voi(p, ty_gia=fx * 0.95))
    fx_hi = tom_tat(voi(p, ty_gia=fx * 1.05))

    # Luoi huy x chuyen doi
    huy_ds = [0.04, 0.06, 0.09, 0.12, 0.15, 0.20]
    cd_he = [0.5, 0.75, 1.0, 1.25, 1.5]
    luoi = []
    for h in huy_ds:
        hang = []
        for c in cd_he:
            r = tom_tat(voi(p, huy_thang=h,
                            cd_free_sang_tra_phi_thang_dau=p["cd_free_sang_tra_phi_thang_dau"] * c,
                            cd_free_sang_tra_phi_ton=p["cd_free_sang_tra_phi_ton"] * c))
            hang.append({"hv_t24": r["hv_t24"], "lai_t24": r["lai_t24"]})
        luoi.append(hang)

    # Hoa von / moc thu nhap (on dinh)
    moc = [0, 50 * TR, 100 * TR, 200 * TR]
    can = {kb: {str(int(mt / TR)): hv_can(voi(p, **KICH_BAN[kb]), mt) for mt in moc} for kb in KICH_BAN}
    can_khong_upsell = {str(int(mt / TR)): hv_can(p, mt, co_upsell=False) for mt in moc}
    dg = dong_gop_1hv(p)
    # nguong doi goi Skool Hobby -> Pro
    nguong_pro_usd = (p["skool_pro_phi_thang_usd"] - p["skool_hobby_phi_thang_usd"]) / \
        (p["skool_hobby_phi_gd"] - p["skool_pro_phi_gd"])  # phi 0,30 USD nhu nhau o 2 goi

    # Moc thue nguoi trong kich ban co so
    moc_thue = {}
    for kb, r in kq.items():
        d = {}
        for row in r["rows"]:
            for ma in row["nhan_su"]:
                d.setdefault(ma, row["thang"])
        moc_thue[kb] = d

    # Nguong dung / doi cach ban: "duong toi thieu dang lam" = duong (nen co so, chi ha ty le vao Skool)
    # cho lai thang 24 vua dat MUC_DANG_LAM. Doc so thang 3 va 6 cua duong do lam nguong.
    MUC_DANG_LAM = 50 * TR
    lo_, hi_ = 0.001, p["ty_le_vao_skool_moi"]
    for _ in range(40):
        mid = (lo_ + hi_) / 2
        if tom_tat(voi(p, ty_le_vao_skool_moi=mid))["lai_t24"] >= MUC_DANG_LAM:
            hi_ = mid
        else:
            lo_ = mid
    duong_tt = tom_tat(voi(p, ty_le_vao_skool_moi=hi_))["rows"]
    nguong_dung = {
        "muc_lai_t24_toi_thieu_tr": MUC_DANG_LAM / TR, "ty_le_vao_skool_tuong_ung": hi_,
        "thang_3": {"free_toi_thieu": round(duong_tt[2]["free"]), "hv_toi_thieu": round(duong_tt[2]["hv"])},
        "thang_6": {"free_toi_thieu": round(duong_tt[5]["free"]), "hv_toi_thieu": round(duong_tt[5]["hv"]),
                    "lai_toi_thieu_tr": round(duong_tt[5]["lai"] / TR, 1)},
        # ty le: diem giua than trong va co so
        "cd_toi_thieu": (KICH_BAN["than_trong"]["cd_free_sang_tra_phi_thang_dau"] + p["cd_free_sang_tra_phi_thang_dau"]) / 2,
        "huy_toi_da": (KICH_BAN["than_trong"]["huy_thang"] + p["huy_thang"]) / 2,
    }

    def qua_nguong(kb, t):
        q, r = voi(p, **KICH_BAN[kb]), kq[kb]["rows"][t - 1]
        n = nguong_dung[f"thang_{t}"]
        ok = r["free"] >= n["free_toi_thieu"] and r["hv"] >= n["hv_toi_thieu"] \
            and q["cd_free_sang_tra_phi_thang_dau"] >= nguong_dung["cd_toi_thieu"]
        if t == 6:
            ok = ok and q["huy_thang"] <= nguong_dung["huy_toi_da"] and r["lai"] >= n["lai_toi_thieu_tr"] * TR
        return ok
    nguong_dung["ket_qua"] = {kb: {"thang_3": qua_nguong(kb, 3), "thang_6": qua_nguong(kb, 6)} for kb in KICH_BAN}

    # ---------------- JSON ----------------
    def gon(r):
        return {k: (v if not isinstance(v, float) else round(v, 2)) for k, v in r.items()}
    out = {
        "don_vi": "VND", "ty_gia": fx,
        "gia": {"co_ban_usd_thang": p["gia_co_ban_usd"], "co_ban_vnd": p["gia_co_ban_usd"] * fx,
                "chuyen_sau_usd": p["gia_chuyen_sau_usd"], "chuyen_sau_vnd": p["gia_chuyen_sau_usd"] * fx,
                "ebook_vnd": p["gia_ebook_vnd"]},
        "von_ban_dau": {"hang_muc": hm, "tong": von},
        "dong_gop_1_hv_thang": dg,
        "nguong_doi_skool_pro_usd_thang": nguong_pro_usd,
        "hv_can_on_dinh": can, "hv_can_khong_upsell_co_so": can_khong_upsell,
        "kich_ban": {kb: {"npv": r["npv"], "irr": r["irr"], "hoan_von_thang": r["hoan_von_thang"],
                          "thang_dau_co_lai": r["thang_dau_co_lai"], "nam": r["nam"],
                          "lai_t24": r["lai_t24"], "luy_ke_24": r["luy_ke_24"], "hv_t24": r["hv_t24"],
                          "moc_thue": moc_thue[kb],
                          "thang": [gon(x) for x in r["rows"]]} for kb, r in kq.items()},
        "kich_ban_phu_chuyen_sau": {k: {"luy_ke_24": r["luy_ke_24"], "lai_t24": r["lai_t24"],
                                        "hv_t24": r["hv_t24"], "nam": r["nam"],
                                        "dt_chua_ghi_nhan_t24": r["rows"][-1]["dt_chua_ghi_nhan"],
                                        "lai_t60": dai_han[k]["lai_t24"], "hv_t60": dai_han[k]["hv_t24"]}
                                    for k, r in phu.items()},
        "ltv_usd_thang_o_lai": ltv,
        "co_so_60_thang": {"lai_t60": dai_han["co_so"]["lai_t24"], "hv_t60": dai_han["co_so"]["hv_t24"]},
        "do_nhay": nhay,
        "luy_ke_24_neu_ap_nguong_mien_thue_1ty": thue_nguong,
        "luy_ke_24_neu_thue_2pct": thue_2,
        "do_nhay_vao_skool": {str(v): {"hv_t24": r["hv_t24"], "lai_t24": r["lai_t24"], "luy_ke_24": r["luy_ke_24"]}
                              for v, r in vao_skool.items()},
        "nguong_dung": nguong_dung,
        "do_nhay_ty_gia_5pct": {"-5": fx_lo["luy_ke_24"], "+5": fx_hi["luy_ke_24"]},
        "luoi_huy_chuyen_doi": {"huy": huy_ds, "he_so_chuyen_doi": cd_he, "gia_tri": luoi},
    }
    with open(os.path.join(HERE, "tai-chinh.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    # ---------------- MARKDOWN ----------------
    L = []
    a = L.append
    usd = lambda x: f"{so(x)} USD"
    gcb, gcs = p["gia_co_ban_usd"], p["gia_chuyen_sau_usd"]
    r24 = base["rows"][-1]
    pt, pl = kq["than_trong"], kq["lac_quan"]
    a("# Mô hình tài chính — Đầu Tư Bình An trên Skool (phiên bản 2, 24 tháng)\n")
    a(f"Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng – Tài chính · "
      f"Mọi con số do `mo_hinh.py` tính (chạy lại: `python3 mo_hinh.py`). Đơn vị: **triệu đồng (tr)**, "
      f"tỷ giá giả định {so(fx)} đ/USD.\n")
    a("## 5 kết luận chính\n")
    a(f"1. **Vốn ban đầu rất thấp: {m(von)} tr**, trong đó {m(hm['Quy du phong van hanh (3 thang chi phi co dinh + CSKH)'])} tr là quỹ dự phòng (tiền vẫn nằm trong tài khoản). "
      f"Chi phí cố định khi chưa thuê ai chỉ ~{m(p['cp_cong_cu_ai'] + p['cp_khac_thang'])} tr/tháng + phí Skool.")
    a(f"2. **Hoà vốn hằng tháng: {can_khong_upsell['0']} học viên trả 100 USD nếu chỉ có khoá cơ bản** (chưa thuê người; công của anh không tính vào chi phí). "
      f"Mỗi học viên 100 USD/tháng (≈{m(gcb * fx, 2)} tr) để lại ≈{m(dg['Pro'], 2)} tr sau phí Skool Pro, phí chuyển tiền, thuế "
      f"(gói Hobby: {m(dg['Hobby'], 2)} tr). Rủi ro không nằm ở chi phí mà ở **có kéo được người trả 100 USD/tháng và giữ họ hay không**.")
    a(f"3. **Mốc thu nhập (lãi sau thuế, phí, lương nhân viên) — kịch bản cơ sở:** 50 tr/tháng cần ~{can['co_so']['50']} học viên, "
      f"100 tr cần ~{can['co_so']['100']}, 200 tr cần ~{can['co_so']['200']} học viên 100 USD đang hoạt động (đã tính bán kèm gói 1.000 USD và ebook). "
      f"Nếu không bán được gói chuyên sâu/ebook: {can_khong_upsell['50']} / {can_khong_upsell['100']} / {can_khong_upsell['200']} học viên.")
    pk = kq["khong_dang_lam"]
    a(f"4. **Kịch bản cơ sở là kịch bản tham vọng:** tháng 24 có ~{so(base['hv_t24'])} học viên 100 USD, doanh thu {m(base['dt_t24'])} tr/tháng, lãi {m(base['lai_t24'])} tr/tháng; "
      f"lãi luỹ kế 24 tháng (sau khi trừ vốn) {m(base['luy_ke_24'])} tr; hoàn vốn tháng {base['hoan_von_thang']}. "
      f"Thận trọng: ~{so(pt['hv_t24'])} học viên, lãi tháng 24 {m(pt['lai_t24'])} tr, hoàn vốn tháng {pt['hoan_von_thang']}. "
      f"Lạc quan: ~{so(pl['hv_t24'])} học viên, lãi tháng 24 {m(pl['lai_t24'])} tr. "
      f"**Không đáng làm** (ít người xem, chuyển đổi thấp, huỷ cao): chỉ ~{so(pk['hv_t24'])} học viên, lãi tháng 24 {m(pk['lai_t24'])} tr — không đủ trả công anh; ngưỡng dừng/đổi cách bán ở tháng 3 và 6 xem mục 5b. **Biến quyết định là tỷ lệ huỷ và tỷ lệ chuyển đổi**, không phải chi phí. "
      f"Lưu ý: kịch bản cơ sở cần kênh đạt ~{so(base['rows'][-1]['theo_doi'])} người theo dõi và ~{so(base['rows'][-1]['free'])} thành viên Skool miễn phí vào tháng 24 — đây là giả định, chưa có số thật của kênh.")
    k3n = list(phu)[2]
    k3 = phu[k3n]
    a(f"5. **Gói 1.000 USD \"đồng hành 10 năm\" mang tiền về sớm nhưng tạo nghĩa vụ dài hạn:** 1.000 USD/120 tháng ≈ {so(gcs / 120, 1)} USD/tháng, rẻ hơn 12 lần gói cơ bản. "
      f"Kịch bản cơ sở: cuối tháng 24 có {m(r24['dt_chua_ghi_nhan'])} tr doanh thu \"chưa phục vụ\" (rủi ro hoàn tiền nếu dừng). "
      f"Nếu gói này bao gồm luôn khoá cơ bản và học viên chuyển sang hàng loạt (8%/tháng), tiền mặt 24 tháng trông đẹp hơn ({m(k3['luy_ke_24'])} so với {m(base['luy_ke_24'])} tr) "
      f"nhưng người trả 100 USD tháng 24 còn ~{so(k3['hv_t24'])} (thay vì {so(base['hv_t24'])}), doanh thu chưa phục vụ lên {m(k3['rows'][-1]['dt_chua_ghi_nhan'])} tr, "
      f"và đến tháng 60 phải phục vụ ~{so(phuc_vu(k3n, dai_han[k3n]))} người so với {so(phuc_vu('co_so', dai_han['co_so']))}. "
      f"Đề xuất: gói 1.000 USD là **gói bổ sung**, yêu cầu duy trì thuê bao 100 USD; ghi nhận doanh thu phân bổ và trích {pct(p['cs_trich_quy'], 0)} tiền thu vào quỹ phục vụ dài hạn (chờ anh chốt).\n")

    a("## 1. Giá (anh chốt) và giả định\n")
    a("| Sản phẩm | Giá | Quy đổi | Ghi chú |\n|---|---|---|---|")
    a(f"| Khoá cơ bản (Con đường + Công thức đầu tư) | {usd(gcb)}/tháng | {m(gcb * fx, 2)} tr/tháng | Thuê bao Skool |")
    a(f"| Khoá chuyên sâu \"đồng hành 10 năm\" | {usd(gcs)} | {m(gcs * fx, 1)} tr | **Giả định: trả một lần**, là gói bổ sung (vẫn cần thuê bao 100 USD) — chờ anh |")
    a(f"| Ebook | {m(p['gia_ebook_vnd'], 1)} tr (≈{so(p['gia_ebook_vnd'] / fx, 0)} USD) | — | Bản số, bán VND ngoài Skool (chuyển khoản/VietQR) — giả định |\n")

    a("| Giả định | Giá trị | Nguồn / lý do |\n|---|---|---|")
    G = [
        ("Tỷ giá", f"{so(fx)} đ/USD", "Giả định trong vùng 25.000–26.500; chờ Lan cập nhật tỷ giá ngày"),
        ("Skool Hobby", f"{so(p['skool_hobby_phi_thang_usd'])} USD/tháng + {pct(p['skool_hobby_phi_gd'], 0)} + {so(p['skool_hobby_phi_co_dinh_usd'], 2)} USD/giao dịch", "nghien-cuu.md (tin cậy Trung bình, trích đoạn tìm kiếm — cần mở skool.com/pricing xác nhận)"),
        ("Skool Pro", f"{so(p['skool_pro_phi_thang_usd'])} USD/tháng + {pct(p['skool_pro_phi_gd'])} + {so(p['skool_pro_phi_co_dinh_usd'], 2)} USD/giao dịch; giao dịch > {so(p['skool_nguong_gd_lon_usd'])} USD: {pct(p['skool_pro_phi_gd_lon'])} + {so(p['skool_pro_phi_co_dinh_usd'], 2)} USD (áp cho khoá 1.000 USD)", "nghien-cuu.md (Trung bình, trích đoạn help.skool.com Payments FAQ). Mô hình tự chọn gói rẻ hơn mỗi tháng"),
        ("Phí nhận tiền về VN", pct(p["phi_chuyen_ve_vn"]), "Giả định. nghien-cuu.md: payout qua Stripe Express do Skool tạo, VN có trong danh sách, về VND thứ Tư hằng tuần — chưa kiểm thử; phí quy đổi chưa rõ nên đặt 2%"),
        ("Phí thu ebook", pct(p["phi_cong_tt_ebook"]), "Giả định. Skool không bán file lẻ (nghien-cuu.md) → ebook bán VND qua chuyển khoản/cổng nội địa, hoặc gói thành khoá trả một lần trên Skool"),
        ("Thuế", pct(p["thue_tren_doanh_thu"]) + " doanh thu", "Giả định: hộ/cá nhân kinh doanh dịch vụ 5% GTGT + 2% TNCN, tính từ đồng đầu tiên (thận trọng). Skool là \"merchant of record\" tự xử lý VAT ở vùng áp dụng (nghien-cuu.md) → phần 5% GTGT có thể trùng; độ nhạy 2% vs 7% ở mục 6. nghien-cuu.md: ngưỡng không chịu thuế 500 tr/năm, báo chí nói NĐ 141/2026 nâng lên 1 tỷ — chưa đối chiếu; thuế khi bán qua nền tảng nước ngoài các nguồn mâu thuẫn. Hỏi cơ quan thuế"),
        ("Công cụ AI, phần mềm", f"{m(p['cp_cong_cu_ai'])} tr/tháng", "Giả định ~60 USD: 2 gói AI + Canva/CapCut Pro"),
        ("Chi phí khác", f"{m(p['cp_khac_thang'])} tr/tháng", "Giả định: tên miền, email, họp online"),
        ("Quảng cáo", f"{m(p['cp_quang_cao_thang'])} tr/tháng", "Mặc định 0 — đầu phễu là video tự nhiên (brief)"),
        ("Nhân công chủ dự án, đội AI, văn phòng", "0", "Brief: anh tự quay, đội AI có sẵn, hạ tầng có sẵn. Lãi trong mô hình = thu nhập của anh, chưa trừ công anh"),
        ("Lịch ra mắt", f"Tháng 1 cộng đồng miễn phí; tháng {p['thang_mo_co_ban']} mở 100 USD; tháng {p['thang_mo_chuyen_sau']} mở 1.000 USD và ebook", "Giả định"),
        ("Người theo dõi hiện có", so(p["nguoi_theo_doi_dau"]), "Mặc định 0 — **chờ số thật**: kênh đang xây lại (KENH.md). Nhập số thật vào `nguoi_theo_doi_dau` rồi chạy lại"),
        ("Người theo dõi mới", f"{so(p['theo_doi_moi_thang_dau'])}/tháng, tăng {pct(p['tang_theo_doi_thang'], 0)}/tháng", "Giả định: 1 video ngắn/ngày, tăng dần nhờ đều đặn (ramp-up)"),
        ("Theo dõi mới → Skool miễn phí", pct(p["ty_le_vao_skool_moi"], 1), "Giả định. Có rào cản: Skool không có giao diện tiếng Việt, phải tạo tài khoản, video ngắn khó gắn link (nghien-cuu.md). Thận trọng 2,5%, không đáng làm 2%; độ nhạy 2%/4%/8% ở mục 6"),
        ("Theo dõi sẵn có → Skool miễn phí", pct(p["ty_le_vao_skool_ton"], 0) + " (rải 3 tháng đầu)", "Giả định: lượt kêu gọi ra mắt"),
        ("Thành viên miễn phí rời/ngủ", pct(p["free_roi_thang"], 0) + "/tháng", "Giả định"),
        ("Miễn phí mới → 100 USD (tháng đầu)", pct(p["cd_free_sang_tra_phi_thang_dau"], 0), "Giả định, nằm trong vùng tham khảo 2–5% (nghien-cuu.md, số SaaS); 100 USD/tháng (≈2,6 tr) cao so với thu nhập 25–40 tuổi ở VN nên lấy phía thấp"),
        ("Kho miễn phí → 100 USD (mỗi tháng)", pct(p["cd_free_sang_tra_phi_ton"]), "Giả định: chuyển đổi chậm nhờ nội dung + buổi live"),
        ("Tỷ lệ huỷ 100 USD", pct(p["huy_thang"], 0) + "/tháng", "nghien-cuu.md: cộng đồng trả phí 4–9%/tháng (TB ~5,8%; Circle: 10% là trung bình, ≥15% cần xử lý). Lấy cận trên vì giá cao với thu nhập VN và crypto biến động. Thời gian ở lại TB ≈ " + so(1 / p["huy_thang"], 1) + " tháng"),
        ("Nâng cấp 1.000 USD", pct(p["nang_cap_chuyen_sau_thang"]) + " học viên 100 USD/tháng", "Giả định: ~1 trong 67 học viên/tháng; vé lớn cần tư vấn"),
        ("Mua kèm ebook", f"{pct(p['ebook_kem_co_ban'], 0)} học viên 100 USD mới; {pct(p['ebook_kem_chuyen_sau'], 0)} người mua 1.000 USD; {pct(p['ebook_tu_free_thang'])} kho miễn phí/tháng", "Giả định"),
        ("Chiết khấu", pct(p["chiet_khau_nam"], 0) + "/năm", "Giả định chi phí cơ hội vốn"),
    ]
    for g in G:
        a(f"| {g[0]} | {g[1]} | {g[2]} |")
    a("")

    a("## 2. Vốn ban đầu\n")
    a("| Hạng mục | Triệu đồng | Ghi chú |\n|---|---:|---|")
    ghi = {"Lien ket xuat ban qua NXB": "Ebook bán ra là xuất bản phẩm điện tử, cá nhân không tự xuất bản được (nghien-cuu.md). Số tiền là giả định — chờ báo giá NXB",
           "Thiet bi quay bo sung (mic, den)": "= 0 nếu anh đã đủ thiết bị"}
    VN = {"Thiet ke, dan trang ebook": "Thiết kế, dàn trang ebook", "Bien tap ebook": "Biên tập ebook",
          "Lien ket xuat ban qua NXB": "Liên kết xuất bản qua nhà xuất bản (bắt buộc)",
          "Tu van phap ly (dieu khoan, noi dung tai chinh/crypto)": "Tư vấn pháp lý (điều khoản, nội dung tài chính/crypto)",
          "Thiet bi quay bo sung (mic, den)": "Thiết bị quay bổ sung (mic, đèn)",
          "Nhan dien Skool, trang gioi thieu": "Nhận diện Skool, trang giới thiệu",
          "Quy du phong van hanh (3 thang chi phi co dinh + CSKH)": "Quỹ dự phòng vận hành (3 tháng chi phí cố định + 1 CSKH bán thời gian)"}
    for k, v in hm.items():
        a(f"| {VN[k]} | {m(v)} | {ghi.get(k, 'Giả định')} |")
    a(f"| **Tổng** | **{m(von)}** | |\n")

    a("## 3. Kết quả kịch bản cơ sở theo năm\n")
    a("| Chỉ tiêu (tr) | Năm 1 | Năm 2 |\n|---|---:|---:|")
    y1, y2 = base["nam"]
    for key, ten in [("dt_co_ban", "Doanh thu khoá 100 USD"), ("dt_chuyen_sau", "Doanh thu khoá 1.000 USD (tiền thu)"),
                     ("dt_ebook", "Doanh thu ebook"), ("doanh_thu", "**Tổng doanh thu**"), ("thue", "Thuế"),
                     ("cp_nhan_su", "Lương nhân viên thuê thêm"), ("chi_phi", "Tổng chi phí (gồm thuế, phí Skool, chuyển tiền)"),
                     ("lai", "**Lãi (tiền mặt)**"), ("trich_quy_cs", "Trích quỹ phục vụ gói 10 năm")]:
        a(f"| {ten} | {m(y1[key])} | {m(y2[key])} |")
    a(f"| Biên lãi | {pct(y1['lai'] / y1['doanh_thu'])} | {pct(y2['lai'] / y2['doanh_thu'])} |")
    a(f"| Học viên 100 USD cuối năm | {so(y1['hv_cuoi_nam'])} | {so(y2['hv_cuoi_nam'])} |")
    a(f"| Học viên 1.000 USD luỹ kế | {so(y1['cs_luy_ke'])} | {so(y2['cs_luy_ke'])} |\n")

    a("### Theo tháng (kịch bản cơ sở)\n")
    a("| Tháng | Skool free | HV 100 USD | Mua 1.000 USD | Ebook | Doanh thu | Chi phí | Lãi | Luỹ kế (sau vốn) | Gói Skool | Nhân sự |\n|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for r in base["rows"]:
        a(f"| {r['thang']} | {so(r['free'])} | {so(r['hv'])} | {so(r['cs_moi'], 1)} | {so(r['ebook'], 1)} | {m(r['doanh_thu'])} | "
          f"{m(r['tong_chi_phi'])} | {m(r['lai'])} | {m(r['luy_ke'])} | {r['goi_skool']} | {', '.join(r['nhan_su']) or '—'} |")
    a("\n(Số học viên lẻ là trung bình kỳ vọng của mô hình, làm tròn khi hiển thị.)\n")

    a("## 4. Hoà vốn, hoàn vốn, NPV/IRR\n")
    a(f"| Chỉ tiêu | {HDR} |\n|---|{SEP}")
    a("| HV 100 USD cần để hoà vốn tháng | " + " | ".join(str(can[k]["0"]) for k in KICH_BAN) + " |")
    a("| Tháng đầu tiên có lãi | " + " | ".join(str(kq[k]["thang_dau_co_lai"]) for k in KICH_BAN) + " |")
    a("| Tháng hoàn vốn (luỹ kế ≥ 0) | " + " | ".join(str(kq[k]["hoan_von_thang"] or "chưa hoàn vốn") for k in KICH_BAN) + " |")
    a("| NPV 24 tháng @12%/năm (tr) | " + " | ".join(m(kq[k]["npv"]) for k in KICH_BAN) + " |")
    a("| IRR (năm) | " + " | ".join((pct(kq[k]["irr"]["nam"], 0) if kq[k]["irr"] else "n/a") for k in KICH_BAN) + " |")
    a("\nIRR rất cao vì vốn ban đầu rất nhỏ — chỉ số này không có ý nghĩa so sánh; nên nhìn số học viên và lãi tháng.\n")
    a(f"Đóng góp mỗi học viên 100 USD/tháng: gói Pro {m(dg['Pro'], 2)} tr, gói Hobby {m(dg['Hobby'], 2)} tr. "
      f"Chuyển Skool Hobby → Pro khi doanh thu qua Skool vượt ~{so(nguong_pro_usd)} USD/tháng (≈{so(nguong_pro_usd / gcb)} học viên).\n")

    a("### Số học viên 100 USD cần cho các mốc thu nhập (trạng thái ổn định, đã trừ lương người thuê theo ngưỡng)\n")
    a(f"| Lãi mục tiêu/tháng | {HDR} | Cơ sở, chỉ có khoá cơ bản |\n|---|{SEP}---:|")
    for mt in ("0", "50", "100", "200"):
        nhan = "Hoà vốn" if mt == "0" else f"{mt} tr"
        a(f"| {nhan} | " + " | ".join(str(can[k][mt]) for k in KICH_BAN) + f" | {can_khong_upsell[mt]} |")
    a("\nKhác biệt giữa các kịch bản ở đây do tỷ lệ huỷ (ảnh hưởng số người mua ebook) và tỷ lệ nâng cấp 1.000 USD.\n")

    a("## 5. Bốn kịch bản (24 tháng)\n")
    a("Kịch bản cơ sở là **kịch bản tham vọng** (giả định kênh tăng đều 24 tháng, chưa có số thật). Kế hoạch nên bám thận trọng; \"không đáng làm\" dùng để đặt ngưỡng dừng ở mục 5b.\n")
    a(f"| Biến | {HDR} |\n|---|{SEP}")
    for k in ["theo_doi_moi_thang_dau", "tang_theo_doi_thang", "ty_le_vao_skool_moi", "cd_free_sang_tra_phi_thang_dau",
              "cd_free_sang_tra_phi_ton", "huy_thang", "nang_cap_chuyen_sau_thang", "ebook_kem_co_ban"]:
        vals = [voi(p, **KICH_BAN[kb])[k] for kb in KICH_BAN]
        f = (lambda v: so(v)) if k == "theo_doi_moi_thang_dau" else (lambda v: pct(v))
        a(f"| {NHAN_KB[k]} | " + " | ".join(f(v) for v in vals) + " |")
    a("| Người theo dõi tháng 24 | " + " | ".join(so(kq[k]["rows"][-1]["theo_doi"]) for k in KICH_BAN) + " |")
    a("| Thành viên Skool miễn phí tháng 24 | " + " | ".join(so(kq[k]["rows"][-1]["free"]) for k in KICH_BAN) + " |")
    a("| **HV 100 USD tháng 24** | " + " | ".join(so(kq[k]["hv_t24"]) for k in KICH_BAN) + " |")
    a("| **Doanh thu tháng 24 (tr)** | " + " | ".join(m(kq[k]["dt_t24"]) for k in KICH_BAN) + " |")
    a("| **Lãi tháng 24 (tr)** | " + " | ".join(m(kq[k]["lai_t24"]) for k in KICH_BAN) + " |")
    a("| Doanh thu năm 1 / năm 2 (tr) | " + " | ".join(f"{m(kq[k]['nam'][0]['doanh_thu'])} / {m(kq[k]['nam'][1]['doanh_thu'])}" for k in KICH_BAN) + " |")
    a("| Lãi năm 1 / năm 2 (tr) | " + " | ".join(f"{m(kq[k]['nam'][0]['lai'])} / {m(kq[k]['nam'][1]['lai'])}" for k in KICH_BAN) + " |")
    a("| **Lãi luỹ kế 24 tháng sau vốn (tr)** | " + " | ".join(m(kq[k]["luy_ke_24"]) for k in KICH_BAN) + " |\n")

    a("### Kịch bản phụ gói 1.000 USD (trên nền cơ sở)\n")
    a("| Phương án | HV 100 USD tháng 24 | Lãi tháng 24 (tr) | Lãi luỹ kế 24 tháng (tr) | Doanh thu chưa ghi nhận T24 (tr) | HV 100 USD tháng 60 | Người phải phục vụ T60 | Lãi tháng 60 (tr) |\n|---|---:|---:|---:|---:|---:|---:|---:|")
    a(f"| Cơ sở: trả 1 lần, gói bổ sung | {so(base['hv_t24'])} | {m(base['lai_t24'])} | {m(base['luy_ke_24'])} | {m(r24['dt_chua_ghi_nhan'])} | "
      f"{so(dai_han['co_so']['hv_t24'])} | {so(phuc_vu('co_so', dai_han['co_so']))} | {m(dai_han['co_so']['lai_t24'])} |")
    for k, r in phu.items():
        k_vn = k.replace("Tra gop 4 ky x 250 USD (10% bo ngang sau ky 1)", "Trả góp 4 kỳ × 250 USD (10% bỏ ngang sau kỳ 1)") \
                .replace("Goi 1.000 USD GOM luon thue bao co ban (nguoi nang cap ngung tra 100 USD)",
                         "Gói 1.000 USD GỒM luôn khoá cơ bản (người nâng cấp ngừng trả 100 USD)") \
                .replace("Goi GOM co ban va nguoi dung chuyen sang hang loat (nang cap 8%/thang)",
                         "Gói GỒM khoá cơ bản và học viên chuyển sang hàng loạt (nâng cấp 8%/tháng)")
        dcg = m(r["rows"][-1]["dt_chua_ghi_nhan"]) if "Tra gop" not in k else "—"
        a(f"| {k_vn} | {so(r['hv_t24'])} | {m(r['lai_t24'])} | {m(r['luy_ke_24'])} | {dcg} | "
          f"{so(dai_han[k]['hv_t24'])} | {so(phuc_vu(k, dai_han[k]))} | {m(dai_han[k]['lai_t24'])} |")
    a("\nCột tháng 60 chạy cùng giả định phễu đến năm thứ 5 (người theo dõi tiếp tục tăng) — chỉ để so sánh cấu trúc gói, không phải dự báo. \"Người phải phục vụ\" với phương án GỒM = HV 100 USD + toàn bộ người đã mua gói 10 năm (giả định họ ở lại, mức trần).\n")
    a(f"Giá trị trọn đời 1 học viên 100 USD mới (USD): gói bổ sung {so(ltv['bo_sung'][0])} (ở lại TB {so(ltv['bo_sung'][1], 1)} tháng); "
      f"gói GỒM, nâng cấp 1,5%/tháng {so(ltv['gom_1_5'][0])}; gói GỒM, nâng cấp 8%/tháng {so(ltv['gom_8'][0])} — chênh lệch nhỏ về tiền, "
      f"khác biệt nằm ở **số người phải phục vụ không thu phí hằng tháng trong 10 năm**.\n")

    a("### 5b. Ngưỡng dừng / đổi cách bán (đo bằng số thật)\n")
    a(f"Ngưỡng = mức tháng 3 và tháng 6 của **đường tối thiểu đáng làm**: giữ giả định cơ sở, chỉ hạ tỷ lệ vào Skool xuống {pct(nguong_dung['ty_le_vao_skool_tuong_ung'])} "
      f"để lãi tháng 24 vừa đạt {so(nguong_dung['muc_lai_t24_toi_thieu_tr'])} tr (mức giả định đủ bù công anh). "
      f"Vì số lượng tháng 3 còn nhỏ, phải xét kèm **tỷ lệ**: chuyển đổi miễn phí mới → 100 USD ≥ {pct(nguong_dung['cd_toi_thieu'])} và tỷ lệ huỷ ≤ {pct(nguong_dung['huy_toi_da'], 1)}/tháng "
      "(điểm giữa thận trọng và cơ sở).\n")
    a(f"| Chỉ số | Tháng | {HDR} |\n|---|---:|{SEP}")
    for t in (3, 6):
        a(f"| Thành viên Skool miễn phí | {t} | " + " | ".join(so(kq[k]["rows"][t - 1]["free"]) for k in KICH_BAN) + " |")
        a(f"| HV 100 USD đang trả | {t} | " + " | ".join(so(kq[k]["rows"][t - 1]["hv"], 1) for k in KICH_BAN) + " |")
        a(f"| Lãi tháng (tr) | {t} | " + " | ".join(m(kq[k]["rows"][t - 1]["lai"]) for k in KICH_BAN) + " |")
    for t in (3, 6):
        a(f"| **Qua ngưỡng?** | {t} | " + " | ".join("Đạt" if nguong_dung["ket_qua"][k][f"thang_{t}"] else "Không" for k in KICH_BAN) + " |")
    n3, n6 = nguong_dung["thang_3"], nguong_dung["thang_6"]
    a("")
    a(f"- **Mốc tháng 3 — đổi cách bán** nếu Skool miễn phí < {so(n3['free_toi_thieu'])} người **hoặc** < {n3['hv_toi_thieu']} học viên trả 100 USD **hoặc** chuyển đổi < {pct(nguong_dung['cd_toi_thieu'])}: "
      "thêm thu VND (chuyển khoản/QR rồi mời vào Skool), hướng dẫn vào Skool bằng tiếng Việt, buổi live miễn phí để chốt, cân nhắc gói năm. Giá anh chốt giữ nguyên trừ khi anh quyết khác.")
    a(f"- **Mốc tháng 6 — dừng mở rộng / xem lại mô hình** nếu < {so(n6['free_toi_thieu'])} thành viên miễn phí, < {n6['hv_toi_thieu']} học viên trả phí, **hoặc** tỷ lệ huỷ thực > {pct(nguong_dung['huy_toi_da'], 1)}/tháng, "
      f"**hoặc** lãi < {so(n6['lai_toi_thieu_tr'], 1)} tr/tháng: không thuê người, không chi quảng cáo; trình anh phương án đổi giá/định dạng (gói năm, khoá trả một lần) trước khi làm tiếp.")
    a("- Kết quả: kịch bản **thận trọng không qua ngưỡng** (chuyển đổi và huỷ kém) dù số thành viên tháng 3 có thể đủ — nếu số thật giống thận trọng thì đổi cách bán ngay ở tháng 3, chưa mở rộng.")
    a("- Ở mức \"không đáng làm\", tiền không mất nhiều (vốn nhỏ) nhưng **thời gian của anh** là chi phí chính bị mất.\n")
    a("## 6. Độ nhạy ±20% (kịch bản cơ sở)\n")
    a(f"Gốc: lãi tháng 24 = {m(base['lai_t24'])} tr; lãi luỹ kế 24 tháng = {m(base['luy_ke_24'])} tr.\n")
    a("| Biến | Giá trị gốc | Lãi T24 khi −20% | Lãi T24 khi +20% | Luỹ kế 24T khi −20% | Luỹ kế 24T khi +20% |\n|---|---:|---:|---:|---:|---:|")
    VNB = {"huy_thang": "Tỷ lệ huỷ/tháng", "cd_free_sang_tra_phi_thang_dau": "Chuyển đổi miễn phí mới → 100 USD",
           "cd_free_sang_tra_phi_ton": "Chuyển đổi kho miễn phí → 100 USD", "theo_doi_moi_thang_dau": "Người theo dõi mới/tháng",
           "ty_le_vao_skool_moi": "Tỷ lệ vào Skool miễn phí", "nang_cap_chuyen_sau_thang": "Tỷ lệ nâng cấp 1.000 USD"}
    for n in sorted(nhay, key=lambda x: -abs(x["luy_ke_+20"] - x["luy_ke_-20"])):
        gv = so(n["gia_tri"]) if n["bien"] == "theo_doi_moi_thang_dau" else pct(n["gia_tri"])
        a(f"| {VNB[n['bien']]} | {gv} | {m(n['lai_t24_-20'])} | {m(n['lai_t24_+20'])} | {m(n['luy_ke_-20'])} | {m(n['luy_ke_+20'])} |")
    a(f"\nTỷ giá ±5%: lãi luỹ kế 24 tháng {m(fx_lo['luy_ke_24'])} tr (−5%) / {m(fx_hi['luy_ke_24'])} tr (+5%).\n")
    a("Nếu được áp ngưỡng không chịu thuế 1 tỷ đ/năm (chỉ tính thuế phần vượt — cách tính giả định, chờ cơ quan thuế): lãi luỹ kế 24 tháng " +
      " / ".join(f"{TEN_KB_VN[k]} {m(thue_nguong[k])} tr (+{m(thue_nguong[k] - kq[k]['luy_ke_24'])})" for k in KICH_BAN) + ".\n")
    a("**Tỷ lệ theo dõi mới → Skool miễn phí (nền cơ sở):**\n")
    a("| Tỷ lệ vào Skool | HV 100 USD tháng 24 | Lãi tháng 24 (tr) | Lãi luỹ kế 24 tháng (tr) |\n|---:|---:|---:|---:|")
    for v, r in vao_skool.items():
        a(f"| {pct(v, 0)} | {so(r['hv_t24'])} | {m(r['lai_t24'])} | {m(r['luy_ke_24'])} |")
    a("")
    a("**Thuế 2% (chỉ TNCN, nếu VAT đã do Skool thu) vs 7%** — lãi luỹ kế 24 tháng (tr):\n")
    a(f"| Thuế | {HDR} |\n|---|{SEP}")
    a("| 7% (mặc định) | " + " | ".join(m(kq[k]["luy_ke_24"]) for k in KICH_BAN) + " |")
    a("| 2% | " + " | ".join(m(thue_2[k]) for k in KICH_BAN) + " |")
    a("\nCả hai cách chưa được cơ quan thuế xác nhận; mô hình giữ 7% cho thận trọng.\n")
    a("### Lưới tỷ lệ huỷ × chuyển đổi — học viên 100 USD và lãi tháng 24 (tr)\n")
    a("Hệ số chuyển đổi nhân cả hai tỷ lệ chuyển đổi miễn phí → 100 USD của kịch bản cơ sở.\n")
    a("| Huỷ/tháng \\ Chuyển đổi | " + " | ".join(f"×{so(c, 2)} ({pct(p['cd_free_sang_tra_phi_thang_dau'] * c)})" for c in cd_he) + " |")
    a("|---|" + "---:|" * len(cd_he))
    for h, hang in zip(huy_ds, luoi):
        a(f"| {pct(h, 0)} | " + " | ".join(f"{so(x['hv_t24'])} HV / {m(x['lai_t24'])}" for x in hang) + " |")
    a("")

    a("## 7. Khi nào mới thuê người\n")
    a(f"Quy tắc: chỉ thuê khi số liệu **tháng trước** chạm ngưỡng, và tổng lương không vượt {pct(p['tran_chi_nhan_su'], 0)} doanh thu tháng trước. "
      f"Nhân viên chính thức tính thêm {pct(p['he_so_bhxh'] - 1)} chi phí bảo hiểm phía người sử dụng lao động. Lương là **giả định mặt bằng thị trường 2026**, chờ xác minh.\n")
    a(f"| Vị trí | Lương giả định (tr/tháng) | Ngưỡng thuê | Tháng thuê — {HDR} |\n|---|---:|---|{SEP}")
    NG_VN = {"cskh_bt": "≥ 60 học viên trả phí (thay bằng bản toàn thời gian khi ≥ 200)", "cskh_ft": "≥ 200 học viên trả phí",
             "cskh_ft2": "≥ 500 học viên trả phí", "chot_don": "Doanh thu ≥ 150 tr/tháng và ≥ 2.000 thành viên miễn phí",
             "dung_video": "Doanh thu ≥ 200 tr/tháng (giải phóng thời gian anh)", "ke_toan": "Doanh thu ≥ 40 tr/tháng"}
    TEN_VN = {"cskh_bt": "Trợ giảng/CSKH cộng đồng (bán thời gian)", "cskh_ft": "Trợ giảng/CSKH cộng đồng (toàn thời gian)",
              "chot_don": "Tư vấn/chốt đơn gói 1.000 USD (lương cứng + 5% hoa hồng)", "dung_video": "Dựng video/trợ lý nội dung",
              "cskh_ft2": "CSKH cộng đồng thứ 2", "ke_toan": "Kế toán dịch vụ (thuê ngoài)"}
    for ns in p["nhan_su"]:
        ma = ns["ma"]
        a(f"| {TEN_VN[ma]} | {m(ns['luong'])} | {NG_VN[ma]} | " +
          " | ".join(str(moc_thue[kb].get(ma, "không")) for kb in KICH_BAN) + " |")
    a("\n\"không\" = trong 24 tháng chưa chạm ngưỡng, anh và đội AI tự làm. Không thuê trước doanh thu.\n")

    a("## 8. Gói \"đồng hành 10 năm\" thu một lần — rủi ro dòng tiền và cách xử lý\n")
    a(f"- **Nghĩa vụ dài hạn:** thu {usd(gcs)} một lần nhưng phải phục vụ 120 tháng. Doanh thu thực chất ≈ {so(gcs / 120, 1)} USD/tháng/người. "
      "Nếu tiêu hết tiền thu ngay, các năm sau sẽ phục vụ không công; nếu dừng chương trình có thể phát sinh yêu cầu hoàn tiền phần chưa phục vụ.")
    a(f"- **Đề xuất ghi nhận:** ghi nhận ngay {pct(p['cs_ghi_nhan_ngay'], 0)} (onboarding, tài liệu), phần {pct(1 - p['cs_ghi_nhan_ngay'], 0)} phân bổ đều 120 tháng. "
      f"Kịch bản cơ sở: cuối tháng 24 còn **{m(r24['dt_chua_ghi_nhan'])} tr doanh thu chưa ghi nhận** (nghĩa vụ phải phục vụ).")
    a(f"- **Quỹ phục vụ dài hạn:** trích {pct(p['cs_trich_quy'], 0)} tiền thực nhận (sau phí, thuế) mỗi lần bán gói 1.000 USD vào tài khoản riêng; "
      f"cơ sở tháng 24 quỹ đạt **{m(r24['quy_cs'])} tr**. Lãi \"tiêu được\" = lãi tiền mặt − trích quỹ.")
    a("- **Điều khoản cần chốt (chờ anh + luật sư):** gói 1.000 USD có bao gồm khoá 100 USD không (mô hình giả định KHÔNG); \"đồng hành\" gồm gì cụ thể "
      "(số buổi live/năm, hỏi đáp), điều kiện chấm dứt/hoàn tiền, xử lý khi Skool đổi chính sách. Không cam kết lợi nhuận, không gọi kèo, không giữ tiền/ví hộ.")
    a("- **Thay thế an toàn hơn để anh cân nhắc:** gói 1.000 USD cho 12 tháng gia hạn được, hoặc trả góp — xem kịch bản phụ ở mục 5.\n")

    a("## 9. Nhận định\n")
    a(f"- Về chi phí, dự án gần như không thể lỗ nặng: vốn {m(von)} tr, hoà vốn từ {can_khong_upsell['0']} học viên nếu chỉ có khoá cơ bản. Kịch bản cơ sở là tham vọng; nên lập kế hoạch theo thận trọng và kiểm tra ngưỡng ở tháng 3, tháng 6 (mục 5b). Rủi ro thật là **doanh thu bằng 0** nếu không ai trả 100 USD/tháng.")
    a(f"- 100 USD/tháng (≈{m(gcb * fx, 1)} tr) là giá cao với người 25–40 tuổi ở VN; tỷ lệ huỷ quyết định quy mô: huỷ {pct(huy_ds[0], 0)} vs {pct(huy_ds[-1], 0)} làm số học viên tháng 24 chênh "
      f"{so(luoi[0][2]['hv_t24'])} vs {so(luoi[-1][2]['hv_t24'])}. Cần đo tỷ lệ huỷ thật ngay 2–3 tháng đầu.")
    a("- Số người theo dõi và tỷ lệ chuyển đổi là giả định — thay bằng số thật của kênh trong tháng 1 rồi chạy lại `mo_hinh.py`.")
    a("- Chưa xác minh (nghien-cuu.md mới ở mức tin cậy Trung bình/Thấp): phí Skool, payout Stripe Express về VN (phải thử 1 giao dịch thật), thuế khi bán qua nền tảng nước ngoài, chi phí liên kết xuất bản ebook. Khách trả USD còn chịu thêm ~1–4% phí đổi ngoại tệ phía thẻ — làm giá thực tế với khách cao hơn 100 USD, có thể kéo chuyển đổi xuống.")
    a("- Không cần dựng bộ máy: theo quy tắc ngưỡng, người đầu tiên (CSKH bán thời gian) chỉ thuê khi có ~60 học viên trả phí.\n")

    with open(os.path.join(HERE, "tai-chinh.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"Von ban dau: {m(von)} tr")
    for kb, r in kq.items():
        print(kb, "HV t24", so(r["hv_t24"]), "DT t24", m(r["dt_t24"]), "Lai t24", m(r["lai_t24"]),
              "Luy ke", m(r["luy_ke_24"]), "Hoan von", r["hoan_von_thang"], "lai dau", r["thang_dau_co_lai"],
              "Nam", [(m(y['doanh_thu']), m(y['lai'])) for y in r["nam"]], "thue", moc_thue[kb])
    print("HV can", can, "khong upsell", can_khong_upsell, "dong gop", {k: m(v, 2) for k, v in dg.items()})
    for k, r in phu.items():
        print(k, m(r["luy_ke_24"]), so(r["hv_t24"]))


if __name__ == "__main__":
    main()
