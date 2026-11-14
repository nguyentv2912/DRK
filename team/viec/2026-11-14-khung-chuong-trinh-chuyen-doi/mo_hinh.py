# -*- coding: utf-8 -*-
"""
Mô hình tài chính — Chương trình chuyển đổi khách hàng (giáo dục + đồng hành
quản lý tài chính & đầu tư crypto an toàn) và kế hoạch tài chính phòng ban vận hành.

Mã việc: 2026-11-14-khung-chuong-trinh-chuyen-doi · Người lập: Hùng (Tài chính)
Đơn vị tiền: triệu đồng (trđ) trừ khi ghi khác. Mô hình theo tháng, 48 tháng
(báo cáo 24 tháng; tháng 25–48 giữ quy mô giai đoạn 3, lead tự nhiên giữ mức T24, để đo hoàn vốn/NPV).

Nguyên tắc: KHÔNG nhận uỷ thác, KHÔNG giữ tiền/tài sản số của khách, KHÔNG cam kết
lợi nhuận. Doanh thu chỉ từ học phí, phí thành viên và hoa hồng giới thiệu hợp pháp.

Chạy:  python3 mo_hinh.py          -> in bảng + ghi tai-chinh.json
"""
import copy
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
THANG = 48          # tầm mô hình (NPV/IRR/hoàn vốn tính trên 48 tháng, không giá trị cuối kỳ)
BAO_CAO = 24        # tầm báo cáo

# ---------------------------------------------------------------------------
# 1. GIẢ ĐỊNH (nguồn: NC = nghien-cuu.md của Lan, độ tin cậy tối đa Trung bình;
#    GD = giả định của Hùng; BR = brief.md)
# ---------------------------------------------------------------------------
GD = {
    # --- Thang sản phẩm (giá đã gồm thuế, trđ) ---
    "gia_nen_tang": 0.99,      # NC: khoá video TCCN 899k (niêm yết 1,2tr); "vài trăm nghìn–vài triệu"
    "gia_dong_hanh": 12.0,     # GD: chương trình đồng hành 3 tháng; thị trường không công bố giá
    "gia_thanh_vien": 3.6,     # GD: thành viên năm (~300k/tháng); NC: VIP quốc tế 30–200 USD/tháng
    "ty_le_gia_han_tv": 0.50,  # GD: tỷ lệ gia hạn thành viên sau 12 tháng

    # --- Phễu (tỷ lệ chuyển đổi, GD — chưa có dữ liệu thực) ---
    "ty_le_tiep_can_dk": 0.02,     # GD: người tiếp cận -> đăng ký hội thảo/lead (chỉ để hiển thị quy mô tiếp cận)
    "ty_le_dk_tham_du": 0.40,      # GD: đăng ký -> tham dự hội thảo miễn phí (online + offline tại VP)
    "ty_le_tham_du_nen_tang": 0.12,  # GD: tham dự -> mua khoá nền tảng
    "ty_le_tham_du_tu_van": 0.08,  # GD: tham dự -> đặt lịch tư vấn 1:1 miễn phí
    "ty_le_tu_van_dong_hanh": 0.25,  # GD: tư vấn 1:1 -> mua đồng hành (cùng tháng)
    "ty_le_nen_tang_dong_hanh": 0.20,  # GD: học viên nền tảng -> mua đồng hành (trễ 1 tháng)
    "ty_le_dong_hanh_thanh_vien": 0.40,  # GD: học xong đồng hành -> thành viên năm (trễ 3 tháng)
    "ty_le_nen_tang_thanh_vien": 0.05,   # GD: học viên nền tảng -> thành viên năm (cùng tháng)
    "he_so_ramp_cd": {1: 0.0, 2: 0.6, 3: 0.7, 4: 0.8, 5: 0.85, 6: 0.9},  # GD: niềm tin thương hiệu tăng dần; T7+ = 1.0
    "ty_le_hoan_tien": 0.05,   # GD: % doanh thu đồng hành hoàn lại (chính sách hoàn tiền = tín hiệu uy tín)

    # --- Thu hút lead ---
    "cpl": 0.06,               # GD: 60.000 đ/lead (quảng cáo giáo dục tài chính, KHÔNG quảng cáo crypto — NC 2.7)
    "ngan_sach_qc": {"Khởi động": 30, "Tăng trưởng": 60, "Mở rộng": 100},  # GD: trđ/tháng theo giai đoạn (T1 = 10, tháng chuẩn bị)
    "lead_tu_nhien_dau": 50,   # GD: lead tự nhiên tháng 2 (nội dung organic, giới thiệu)
    "lead_tu_nhien_cuoi": 900, # GD: lead tự nhiên tháng 24 (tăng tuyến tính), giữ nguyên sau đó

    # --- Doanh thu phụ ngân hàng (referral hợp pháp) ---
    "ty_le_mo_tk": 0.30,       # GD: % khách đồng hành mở tài khoản NH/CK qua link giới thiệu
    "hh_mo_tk": 0.068,         # NC: VPBank NEO ~64.000–72.000 đ/tài khoản (Ecomobi)
    "ty_le_mua_ccq": 0.15,     # GD: % khách đồng hành mua chứng chỉ quỹ qua kênh đối tác
    "gia_tri_ccq_tb": 50.0,    # GD: giá trị mua CCQ bình quân/khách (trđ)
    "hh_ccq": 0.004,           # NC: TCBS iWealth Partner 0,4% giá trị CCQ (cá nhân được duyệt)
    "tai_tro_nh_thang": 0.0,   # GD: tài trợ sự kiện từ NH (cơ sở = 0, chưa có văn bản)

    # --- Chi phí biến đổi ---
    "phi_thanh_toan": 0.02,    # GD: cổng thanh toán/ngân hàng % doanh thu
    "hoc_lieu_dong_hanh": 0.30,  # GD: tài liệu, công cụ, buổi offline / khách đồng hành
    "hoc_lieu_nen_tang": 0.05,   # GD: chi phí phục vụ / học viên nền tảng
    "hh_sales_dong_hanh": 0.08,  # GD: hoa hồng tư vấn viên trên DT đồng hành
    "hh_sales_khac": 0.05,       # GD: hoa hồng trên DT nền tảng + thành viên
    "hh_truong_nhom": 0.015,     # GD: hoa hồng vượt cấp trưởng nhóm trên toàn DT bán
    "chi_phi_hoi_thao": 4.0,     # GD: trđ/buổi offline tại VP (nước, in ấn, quà, quay)

    # --- Nhân sự ---
    "ty_le_bh_dn": 0.215,      # GD (cần kế toán xác nhận): BHXH 17,5% + BHYT 3% + BHTN 1% trên lương đóng BH
                               # Chưa tính kinh phí công đoàn 2% nếu có.
    "chi_phi_tuyen_dao_tao": 8.0,  # GD: trđ/người mới (đăng tin, phỏng vấn, 2 tuần đào tạo nội dung & tuân thủ)
    "nghi_viec_nam": 0.30,     # GD: tỷ lệ nghỉ việc/năm -> chi phí tuyển thay thế
    "may_tinh_moi_nguoi": 12.0,  # GD: thiết bị cho mỗi người mới (capex)
    "hv_toi_da_moi_coach": 40,   # GD: 1 coach + 1 trợ giảng phụ trách tối đa 40 học viên đồng hành đang học
                                 # (học nhóm 8–10 người/lớp + 1 buổi 1:1/tháng). Vượt -> tự thêm cặp coach+TG.

    # --- Thuế, tài chính ---
    "thue_tndn": 0.20,         # GD: thuế TNDN 20%, chuyển lỗ luỹ kế
    "chiet_khau_nam": 0.15,    # GD: suất chiết khấu năm cho NPV
}

# Giai đoạn: (tháng bắt đầu, tháng kết thúc)
GIAI_DOAN = {
    "Khởi động": (1, 6),
    "Tăng trưởng": (7, 15),
    "Mở rộng": (16, THANG),
}

# Vị trí: (bộ phận, lương cứng trđ/tháng, nguồn)
VI_TRI = {
    "Quản lý vận hành":        ("Quản lý", 25.0, "NC v2: trưởng phòng vận hành 13–30, mốc ~21,7 (TB); tin logistics HCM 40 (Thấp)"),
    "Coach tài chính":         ("Thực thi", 20.0, "NC v2: giảng viên HCM TB 21,9 (15–30) (TB); huấn luyện viên HCM TB 19,0 (10–30) (Thấp)"),
    "Trợ giảng":               ("Thực thi", 11.0, "NC: trợ giảng HCM TB 10,9; HN 13,4"),
    "Trưởng nhóm bán hàng":    ("Bán hàng", 20.0, "NC: TP KD B2C 20–40 (Thấp)"),
    "Tư vấn viên":             ("Bán hàng", 9.0, "NC: SVFC 7–20, AIA lương hỗ trợ 8–24, Chubb 12–30 (gồm hoa hồng)"),
    "Chăm sóc khách hàng":     ("CSKH", 9.0, "NC: CSKH HCM 8–10"),
    "Content creator":         ("Nội dung", 13.0, "NC: content TikTok HCM 12–15 (Thấp)"),
    "Video editor":            ("Nội dung", 12.0, "NC: video editor HCM TB ~12"),
    "Chuyên viên quảng cáo":   ("Nội dung", 15.0, "GD"),
    "Kế toán – hành chính":    ("Quản lý", 10.0, "GD"),
}

# Số người theo giai đoạn
NHAN_SU = {
    "Khởi động":   {"Quản lý vận hành": 1, "Coach tài chính": 1, "Trợ giảng": 1, "Trưởng nhóm bán hàng": 0,
                    "Tư vấn viên": 2, "Chăm sóc khách hàng": 1, "Content creator": 1, "Video editor": 1,
                    "Chuyên viên quảng cáo": 0, "Kế toán – hành chính": 0},
    "Tăng trưởng": {"Quản lý vận hành": 1, "Coach tài chính": 2, "Trợ giảng": 2, "Trưởng nhóm bán hàng": 1,
                    "Tư vấn viên": 4, "Chăm sóc khách hàng": 2, "Content creator": 2, "Video editor": 1,
                    "Chuyên viên quảng cáo": 1, "Kế toán – hành chính": 1},
    "Mở rộng":     {"Quản lý vận hành": 1, "Coach tài chính": 4, "Trợ giảng": 3, "Trưởng nhóm bán hàng": 1,
                    "Tư vấn viên": 6, "Chăm sóc khách hàng": 3, "Content creator": 2, "Video editor": 2,
                    "Chuyên viên quảng cáo": 1, "Kế toán – hành chính": 1},
}

# Chi phí cố định khác theo giai đoạn (trđ/tháng). Mặt bằng = 0 (văn phòng có sẵn — BR)
CP_CO_DINH_KHAC = {
    "Khởi động":   {"Điện nước phân bổ tăng thêm": 3, "Phần mềm (CRM, LMS, Zoom, thiết kế)": 8,
                    "Pháp lý định kỳ (luật sư rà nội dung, hợp đồng)": 5, "Khác/văn phòng phẩm": 2},
    "Tăng trưởng": {"Điện nước phân bổ tăng thêm": 5, "Phần mềm (CRM, LMS, Zoom, thiết kế)": 12,
                    "Pháp lý định kỳ (luật sư rà nội dung, hợp đồng)": 5, "Khác/văn phòng phẩm": 3},
    "Mở rộng":     {"Điện nước phân bổ tăng thêm": 8, "Phần mềm (CRM, LMS, Zoom, thiết kế)": 18,
                    "Pháp lý định kỳ (luật sư rà nội dung, hợp đồng)": 6, "Khác/văn phòng phẩm": 4},
}
SO_HOI_THAO_OFFLINE = {"Khởi động": 4, "Tăng trưởng": 8, "Mở rộng": 12}   # GD: buổi/tháng (từ T2)

# Vốn đầu tư ban đầu (tháng 0), trđ
VON_BAN_DAU = {
    "Thiết bị quay dựng (máy quay, mic, đèn, phông)": 80,
    "Thiết bị cho đội khởi động (8 người x 12)": None,   # tính theo nhân sự
    "Pháp lý khởi tạo (ngành nghề, hợp đồng mẫu, rà soát tuân thủ)": 30,
    "Nhận diện, website, LMS, phễu đăng ký": 40,
    "Sản xuất nội dung nền tảng (bài giảng khoá nền tảng)": 30,
    "Cải tạo nhỏ không gian hội thảo trong VP có sẵn": 20,
}

# Kịch bản
KICH_BAN = {
    "Thận trọng": {"he_so_cd": 0.70, "he_so_cpl": 1.30, "he_so_gia_dh": 0.85, "he_so_lead_tn": 0.70,
                   "ty_le_hoan_tien": 0.08, "tai_tro_nh_thang": 0.0},
    "Cơ sở":      {"he_so_cd": 1.00, "he_so_cpl": 1.00, "he_so_gia_dh": 1.00, "he_so_lead_tn": 1.00,
                   "ty_le_hoan_tien": 0.05, "tai_tro_nh_thang": 0.0},
    "Lạc quan":   {"he_so_cd": 1.25, "he_so_cpl": 0.85, "he_so_gia_dh": 1.10, "he_so_lead_tn": 1.30,
                   "ty_le_hoan_tien": 0.04, "tai_tro_nh_thang": 10.0},
}


# ---------------------------------------------------------------------------
# 2. HÀM TÍNH
# ---------------------------------------------------------------------------
# Phương án đề xuất: lùi mốc tuyển (chỉ mở giai đoạn khi phễu đã chứng minh) — GD
GIAI_DOAN_LUI = {
    "Khởi động": (1, 9),
    "Tăng trưởng": (10, 18),
    "Mở rộng": (19, THANG),
}
GD_HIEN = GIAI_DOAN


def giai_doan(t):
    for ten, (a, b) in GD_HIEN.items():
        if a <= t <= b:
            return ten
    return "Mở rộng"


def bac_thang(d, t):
    """Giá trị theo mốc tháng (dict {thang_bat_dau: gia_tri})."""
    v = 0
    for k in sorted(d):
        if t >= k:
            v = d[k]
    return v


def chi_phi_nhan_su(gd_ten, p, he_so_luong_sales=1.0):
    """Lương cứng + BH doanh nghiệp theo giai đoạn (chưa gồm hoa hồng)."""
    tong = 0.0
    for vt, n in NHAN_SU[gd_ten].items():
        luong = VI_TRI[vt][1]
        if vt == "Tư vấn viên":
            luong *= he_so_luong_sales
        tong += n * luong * (1 + p["ty_le_bh_dn"])
    return tong


def so_nguoi(gd_ten):
    return sum(NHAN_SU[gd_ten].values())


def chay(p_override=None, kb="Cơ sở", he_so_cd=None, he_so_gia_dh=None, he_so_luong_sales=1.0,
         he_so_cpl=None, he_so_ngan_sach=1.0, he_so_lead_tn=None):
    p = copy.deepcopy(GD)
    k = KICH_BAN[kb]
    p["ty_le_hoan_tien"] = k["ty_le_hoan_tien"]
    p["tai_tro_nh_thang"] = k["tai_tro_nh_thang"]
    if p_override:
        p.update(p_override)
    hcd = k["he_so_cd"] * (he_so_cd if he_so_cd else 1.0)
    hgia = k["he_so_gia_dh"] * (he_so_gia_dh if he_so_gia_dh else 1.0)
    hcpl = k["he_so_cpl"] * (he_so_cpl if he_so_cpl else 1.0)
    hltn = k["he_so_lead_tn"] * (he_so_lead_tn if he_so_lead_tn else 1.0)
    gia_dh = p["gia_dong_hanh"] * hgia
    cpl = p["cpl"] * hcpl

    # Vốn ban đầu
    von = {}
    for ten, v in VON_BAN_DAU.items():
        if v is None:
            v = so_nguoi("Khởi động") * p["may_tinh_moi_nguoi"]
        von[ten] = v
    von_ban_dau = sum(von.values())

    rows = []
    nen_tang_hist = [0.0] * (THANG + 2)
    dh_hist = [0.0] * (THANG + 2)
    tv_hist = [0.0] * (THANG + 2)
    lo_luy_ke = 0.0
    thue_tich = 0.0
    them_truoc = 0
    for t in range(1, THANG + 1):
        gd_ten = giai_doan(t)
        ramp = p["he_so_ramp_cd"].get(t, 1.0)
        c = hcd * ramp
        # T1 = tháng chuẩn bị: 10 trđ quảng cáo là chi phí thử nghiệm (test mẫu quảng cáo/CPL),
        # lead T1 KHÔNG tạo khách và không chuyển sang T2 (thận trọng).
        ngan_sach = (10 if t == 1 else p["ngan_sach_qc"][gd_ten]) * he_so_ngan_sach
        lead_qc = ngan_sach / cpl
        if t == 1:
            lead_tn = 0.0
        else:
            tt = min(t, BAO_CAO)
            lead_tn = (p["lead_tu_nhien_dau"] + (p["lead_tu_nhien_cuoi"] - p["lead_tu_nhien_dau"])
                       * (tt - 2) / (BAO_CAO - 2)) * hltn
        lead = lead_qc + lead_tn
        tiep_can = lead / p["ty_le_tiep_can_dk"]
        # Tỷ lệ tham dự giữ nguyên; các bước mua nhân hệ số chuyển đổi c (gồm ramp-up)
        tham_du = lead * p["ty_le_dk_tham_du"] if t >= 2 else 0.0
        nen_tang = tham_du * p["ty_le_tham_du_nen_tang"] * c
        tu_van = tham_du * p["ty_le_tham_du_tu_van"] * c
        dh_truc_tiep = tu_van * p["ty_le_tu_van_dong_hanh"]
        dh_tu_nen_tang = nen_tang_hist[t - 1] * p["ty_le_nen_tang_dong_hanh"] * (hcd if t > 1 else 0)
        dong_hanh = dh_truc_tiep + dh_tu_nen_tang
        tv_moi = (nen_tang * p["ty_le_nen_tang_thanh_vien"]
                  + (dh_hist[t - 3] if t > 3 else 0) * p["ty_le_dong_hanh_thanh_vien"] * hcd)
        tv_gia_han = (tv_hist[t - 12] if t > 12 else 0) * p["ty_le_gia_han_tv"]
        thanh_vien = tv_moi + tv_gia_han
        nen_tang_hist[t] = nen_tang
        dh_hist[t] = dong_hanh
        tv_hist[t] = thanh_vien

        dt_nen_tang = nen_tang * p["gia_nen_tang"]
        dt_dong_hanh_gross = dong_hanh * gia_dh
        hoan_tien = dt_dong_hanh_gross * p["ty_le_hoan_tien"]
        dt_dong_hanh = dt_dong_hanh_gross - hoan_tien
        dt_thanh_vien = thanh_vien * p["gia_thanh_vien"]
        dt_ngan_hang = (dong_hanh * (p["ty_le_mo_tk"] * p["hh_mo_tk"]
                                     + p["ty_le_mua_ccq"] * p["gia_tri_ccq_tb"] * p["hh_ccq"])
                        + (p["tai_tro_nh_thang"] if gd_ten != "Khởi động" else 0))
        dt_ban = dt_nen_tang + dt_dong_hanh + dt_thanh_vien
        doanh_thu = dt_ban + dt_ngan_hang

        # Biến đổi
        cp_tt = p["phi_thanh_toan"] * dt_ban
        cp_hoc_lieu = dong_hanh * p["hoc_lieu_dong_hanh"] + nen_tang * p["hoc_lieu_nen_tang"]
        hh = (p["hh_sales_dong_hanh"] * dt_dong_hanh + p["hh_sales_khac"] * (dt_nen_tang + dt_thanh_vien))
        if NHAN_SU[gd_ten]["Trưởng nhóm bán hàng"] > 0:
            hh += p["hh_truong_nhom"] * dt_ban
        cp_hoi_thao = SO_HOI_THAO_OFFLINE[gd_ten] * p["chi_phi_hoi_thao"] if t >= 2 else 0
        cp_qc = ngan_sach
        cp_bien_doi = cp_tt + cp_hoc_lieu + hh

        # Cố định
        cp_ns = chi_phi_nhan_su(gd_ten, p, he_so_luong_sales)
        cp_khac = sum(CP_CO_DINH_KHAC[gd_ten].values())
        # Tuyển dụng: đầu giai đoạn cho người mới + thay thế nghỉ việc hằng tháng
        moi = 0
        capex = 0.0
        if t == 1:
            moi = so_nguoi("Khởi động")
        elif t == GD_HIEN[gd_ten][0]:
            truoc = giai_doan(t - 1)
            moi = max(0, so_nguoi(gd_ten) - so_nguoi(truoc))
            capex = moi * p["may_tinh_moi_nguoi"]
        cp_tuyen = (moi + so_nguoi(gd_ten) * p["nghi_viec_nam"] / 12) * p["chi_phi_tuyen_dao_tao"]

        # Bổ sung cặp coach + trợ giảng khi vượt công suất
        dang_hoc = dh_hist[t] + dh_hist[t - 1] + (dh_hist[t - 2] if t >= 2 else 0)
        can = math.ceil(dang_hoc / p["hv_toi_da_moi_coach"] - 1e-9) if dang_hoc > 0 else 0
        them = max(0, can - NHAN_SU[gd_ten]["Coach tài chính"])
        cp_them = them * (VI_TRI["Coach tài chính"][1] + VI_TRI["Trợ giảng"][1]) * (1 + p["ty_le_bh_dn"])
        moi_them = max(0, them - them_truoc) * 2
        cp_tuyen += moi_them * p["chi_phi_tuyen_dao_tao"]
        capex += moi_them * p["may_tinh_moi_nguoi"]
        them_truoc = them
        cp_ns += cp_them

        cp_co_dinh = cp_ns + cp_khac + cp_tuyen
        ebitda = doanh_thu - cp_bien_doi - cp_qc - cp_hoi_thao - cp_co_dinh

        # Thuế TNDN: tính trên lợi nhuận luỹ kế dương (chuyển lỗ), trả theo tháng cho đơn giản
        lo_luy_ke += ebitda
        thue = 0.0
        if lo_luy_ke > 0:
            co_so = lo_luy_ke - thue_tich / p["thue_tndn"]
            if co_so > 0:
                thue = co_so * p["thue_tndn"]
                thue_tich += thue
        dong_tien = ebitda - thue - capex

        rows.append(dict(
            thang=t, giai_doan=gd_ten, tiep_can=tiep_can, lead=lead, lead_qc=lead_qc, lead_tn=lead_tn,
            tham_du=tham_du, tu_van=tu_van, nen_tang=nen_tang, dong_hanh=dong_hanh, thanh_vien=thanh_vien,
            dt_nen_tang=dt_nen_tang, dt_dong_hanh=dt_dong_hanh, dt_thanh_vien=dt_thanh_vien,
            dt_ngan_hang=dt_ngan_hang, doanh_thu=doanh_thu, hoan_tien=hoan_tien,
            cp_qc=cp_qc, cp_hoi_thao=cp_hoi_thao, cp_bien_doi=cp_bien_doi, hoa_hong=hh,
            cp_nhan_su=cp_ns, cp_khac=cp_khac, cp_tuyen=cp_tuyen, cp_co_dinh=cp_co_dinh,
            ebitda=ebitda, thue=thue, capex=capex, dong_tien=dong_tien,
            so_nguoi=so_nguoi(gd_ten) + 2 * them, coach_them=them,
            hv_dong_hanh_dang_hoc=dang_hoc,
        ))

    # Luỹ kế (tháng 0 = vốn ban đầu)
    luy_ke = -von_ban_dau
    for r in rows:
        luy_ke += r["dong_tien"]
        r["luy_ke"] = luy_ke
    day = min([-von_ban_dau] + [r["luy_ke"] for r in rows])
    thang_day = 0 if day == -von_ban_dau else min(rows, key=lambda r: r["luy_ke"])["thang"]

    # Hoà vốn vận hành: tháng đầu tiên EBITDA >= 0 và duy trì tới hết tầm báo cáo
    hoa_von_vh = None
    for r in rows:
        if r["ebitda"] >= 0 and all(x["ebitda"] >= 0 for x in rows if r["thang"] <= x["thang"] <= BAO_CAO):
            hoa_von_vh = r["thang"]
            break
    hoan_von = next((r["thang"] for r in rows if r["luy_ke"] >= 0 and r["thang"] > thang_day), None)

    # Quỹ dự phòng = 2 tháng chi phí cố định tại tháng đáy (tối thiểu giai đoạn 1)
    gd_day = giai_doan(max(1, thang_day))
    cp_cd_day = chi_phi_nhan_su(gd_day, p, he_so_luong_sales) + sum(CP_CO_DINH_KHAC[gd_day].values())
    du_phong = 2 * cp_cd_day
    von_luu_dong = -day - von_ban_dau  # phần lỗ vận hành phải bù trước khi hoà vốn
    tong_von = -day + du_phong

    # NPV / IRR (48 tháng, không giá trị cuối kỳ)
    r_m = (1 + p["chiet_khau_nam"]) ** (1 / 12) - 1
    dong = [-von_ban_dau] + [r["dong_tien"] for r in rows]
    npv = sum(cf / (1 + r_m) ** i for i, cf in enumerate(dong))
    irr_m = irr(dong)
    irr_nam = (1 + irr_m) ** 12 - 1 if irr_m is not None else None

    return dict(p=p, rows=rows, von=von, von_ban_dau=von_ban_dau, day=day, thang_day=thang_day,
                du_phong=du_phong, von_luu_dong=von_luu_dong, tong_von=tong_von, hoa_von_vh=hoa_von_vh,
                hoan_von=hoan_von, npv=npv, irr_nam=irr_nam, gia_dh=gia_dh, cpl=cpl,
                luy_ke_24=rows[BAO_CAO - 1]["luy_ke"])


def irr(dong):
    def f(r):
        return sum(cf / (1 + r) ** i for i, cf in enumerate(dong))
    lo, hi = -0.99, 1.0
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def don_vi_kinh_te(kq):
    """Đóng góp biên trên 1 khách đồng hành (gồm khách nền tảng, thành viên đi kèm theo tỷ lệ phễu
    và chi phí quảng cáo để có khách đó) -> hoà vốn phòng ban theo số khách/tháng."""
    p = kq["p"]
    # Trên 1.000 lead ở trạng thái ổn định (hệ số chuyển đổi = 1, kịch bản đang chạy)
    hcd = KICH_BAN_HIEN.get("he_so_cd", 1.0)
    tham_du = 1000 * p["ty_le_dk_tham_du"]
    nt = tham_du * p["ty_le_tham_du_nen_tang"] * hcd
    dh = tham_du * p["ty_le_tham_du_tu_van"] * hcd * p["ty_le_tu_van_dong_hanh"] + nt * p["ty_le_nen_tang_dong_hanh"] * hcd
    tv = nt * p["ty_le_nen_tang_thanh_vien"] + dh * p["ty_le_dong_hanh_thanh_vien"] * hcd
    dt_nt = nt * p["gia_nen_tang"]
    dt_dh = dh * kq["gia_dh"] * (1 - p["ty_le_hoan_tien"])
    dt_tv = tv * p["gia_thanh_vien"]
    dt_nh = dh * (p["ty_le_mo_tk"] * p["hh_mo_tk"] + p["ty_le_mua_ccq"] * p["gia_tri_ccq_tb"] * p["hh_ccq"])
    dt_ban = dt_nt + dt_dh + dt_tv
    bien = (p["phi_thanh_toan"] * dt_ban + dh * p["hoc_lieu_dong_hanh"] + nt * p["hoc_lieu_nen_tang"]
            + p["hh_sales_dong_hanh"] * dt_dh + p["hh_sales_khac"] * (dt_nt + dt_tv) + p["hh_truong_nhom"] * dt_ban)
    qc = 1000 * kq["cpl"]
    dong_gop_1000 = dt_ban + dt_nh - bien - qc
    return dict(lead=1000, tham_du=tham_du, nen_tang=nt, dong_hanh=dh, thanh_vien=tv,
                doanh_thu=dt_ban + dt_nh, bien_doi=bien, quang_cao=qc, dong_gop=dong_gop_1000,
                dong_gop_moi_dh=dong_gop_1000 / dh, dt_moi_dh=(dt_ban + dt_nh) / dh,
                ty_le_bien_dong_gop=(dt_ban + dt_nh - bien) / (dt_ban + dt_nh),
                cac_dong_hanh=qc / dh)


KICH_BAN_HIEN = {}


def hoa_von_phong_ban(kq):
    global KICH_BAN_HIEN
    ue = don_vi_kinh_te(kq)
    p = kq["p"]
    out = {}
    for gd_ten in GIAI_DOAN:
        cd = (chi_phi_nhan_su(gd_ten, p) + sum(CP_CO_DINH_KHAC[gd_ten].values())
              + so_nguoi(gd_ten) * p["nghi_viec_nam"] / 12 * p["chi_phi_tuyen_dao_tao"]
              + SO_HOI_THAO_OFFLINE[gd_ten] * p["chi_phi_hoi_thao"])
        kh = cd / ue["dong_gop_moi_dh"]
        out[gd_ten] = dict(
            so_nguoi=so_nguoi(gd_ten),
            chi_phi_co_dinh=cd,
            khach_dong_hanh_hoa_von=kh,
            khach_nen_tang_di_kem=kh * ue["nen_tang"] / ue["dong_hanh"],
            lead_can=kh * 1000 / ue["dong_hanh"],
            doanh_so_can=kh * ue["dt_moi_dh"],
        )
    return ue, out


# ---------------------------------------------------------------------------
# 3. CHẠY & IN
# ---------------------------------------------------------------------------
def f0(x):
    return f"{x:,.0f}".replace(",", ".")


def f1(x):
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tom_tat(kq):
    return dict(tong_von=kq["tong_von"], von_ban_dau=kq["von_ban_dau"], von_luu_dong=kq["von_luu_dong"],
                du_phong=kq["du_phong"], day=kq["day"], thang_day=kq["thang_day"],
                hoa_von_vh=kq["hoa_von_vh"], hoan_von=kq["hoan_von"], npv=kq["npv"], irr_nam=kq["irr_nam"],
                luy_ke_24=kq["luy_ke_24"],
                doi_toi_da=max(r["so_nguoi"] for r in kq["rows"][:BAO_CAO]),
                dt_nam3=sum(r["doanh_thu"] for r in kq["rows"][24:36]),
                ebitda_nam3=sum(r["ebitda"] for r in kq["rows"][24:36]),
                luy_ke_36=kq["rows"][35]["luy_ke"], luy_ke_48=kq["rows"][47]["luy_ke"],
                dt_nam1=sum(r["doanh_thu"] for r in kq["rows"][:12]),
                dt_nam2=sum(r["doanh_thu"] for r in kq["rows"][12:24]),
                ebitda_nam1=sum(r["ebitda"] for r in kq["rows"][:12]),
                ebitda_nam2=sum(r["ebitda"] for r in kq["rows"][12:24]))


def main():
    global KICH_BAN_HIEN
    ket_qua = {}
    for kb in KICH_BAN:
        KICH_BAN_HIEN = KICH_BAN[kb]
        kq = chay(kb=kb)
        ue, hv = hoa_von_phong_ban(kq)
        ket_qua[kb] = (kq, ue, hv)
    KICH_BAN_HIEN = KICH_BAN["Cơ sở"]
    cs, ue, hv = ket_qua["Cơ sở"]

    # Phương án đề xuất: lùi mốc tuyển 3 tháng (cùng giả định phễu cơ sở)
    global GD_HIEN
    GD_HIEN = GIAI_DOAN_LUI
    pa_lui = {kb: chay(kb=kb) for kb in KICH_BAN}
    GD_HIEN = GIAI_DOAN

    print("=== VỐN BAN ĐẦU (trđ) ===")
    for k, v in cs["von"].items():
        print(f"  {k}: {f0(v)}")
    print(f"  Cộng: {f0(cs['von_ban_dau'])}")
    print(f"  Lỗ vận hành phải bù trước hoà vốn (vốn lưu động): {f0(cs['von_luu_dong'])}")
    print(f"  Quỹ dự phòng (2 tháng CP cố định): {f0(cs['du_phong'])}")
    print(f"  TỔNG VỐN CẦN CHUẨN BỊ: {f0(cs['tong_von'])}")

    print("\n=== THEO THÁNG — CƠ SỞ (trđ) ===")
    print("T  GĐ           Lead  ThamDu NenTang DongHanh TV    DoanhThu  QC   HoaHong NhanSu  EBITDA  LuyKe  Coach-load")
    for r in cs["rows"][:BAO_CAO]:
        print(f"{r['thang']:>2} {r['giai_doan']:<11} {r['lead']:>6.0f} {r['tham_du']:>6.0f} {r['nen_tang']:>6.1f} "
              f"{r['dong_hanh']:>7.1f} {r['thanh_vien']:>5.1f} {r['doanh_thu']:>9.1f} {r['cp_qc']:>5.0f} "
              f"{r['hoa_hong']:>6.1f} {r['cp_nhan_su']:>7.1f} {r['ebitda']:>7.1f} {r['luy_ke']:>7.0f} "
              f"{r['hv_dong_hanh_dang_hoc'] / (NHAN_SU[r['giai_doan']]['Coach tài chính'] + r['coach_them']):>5.0f} {r['so_nguoi']:>3}")

    print("\n=== THEO NĂM — CƠ SỞ ===")
    for i, nam in enumerate(["Năm 1", "Năm 2", "Năm 3"]):
        rr = cs["rows"][i * 12:(i + 1) * 12]
        dt = sum(r["doanh_thu"] for r in rr)
        eb = sum(r["ebitda"] for r in rr)
        print(f"{nam}: DT {f0(dt)} | QC {f0(sum(r['cp_qc'] for r in rr))} | Nhân sự {f0(sum(r['cp_nhan_su'] for r in rr))}"
              f" | EBITDA {f0(eb)} ({eb / dt * 100:.0f}%) | Dòng tiền {f0(sum(r['dong_tien'] for r in rr))}")

    print("\n=== BẢNG THEO NĂM CHI TIẾT — CƠ SỞ (trđ) ===")
    dong = [("Lead", "lead"), ("Người tiếp cận", "tiep_can"), ("Khách nền tảng", "nen_tang"),
            ("Khách đồng hành", "dong_hanh"), ("Thành viên", "thanh_vien"),
            ("DT nền tảng", "dt_nen_tang"), ("DT đồng hành (sau hoàn tiền)", "dt_dong_hanh"),
            ("DT thành viên", "dt_thanh_vien"), ("DT ngân hàng", "dt_ngan_hang"), ("Tổng doanh thu", "doanh_thu"),
            ("Quảng cáo", "cp_qc"), ("Hội thảo offline", "cp_hoi_thao"), ("CP biến đổi (gồm hoa hồng)", "cp_bien_doi"),
            ("Lương cứng + BH", "cp_nhan_su"), ("CP cố định khác", "cp_khac"), ("Tuyển dụng", "cp_tuyen"),
            ("EBITDA", "ebitda"), ("Thuế TNDN", "thue"), ("Thiết bị (capex)", "capex"), ("Dòng tiền", "dong_tien")]
    print(f"{'':<30}" + "".join(f"{'Năm ' + str(i + 1):>12}" for i in range(4)))
    for ten, k in dong:
        print(f"{ten:<30}" + "".join(f"{f0(sum(r[k] for r in cs['rows'][i * 12:(i + 1) * 12])):>12}" for i in range(4)))
    print(f"{'Luỹ kế cuối năm (gồm vốn 296)':<30}" + "".join(f"{f0(cs['rows'][i * 12 + 11]['luy_ke']):>12}" for i in range(4)))

    print("\n=== THEO NĂM — 3 KỊCH BẢN (trđ) ===")
    for kb, (kq, _, _) in ket_qua.items():
        for ten, k in [("Doanh thu", "doanh_thu"), ("EBITDA", "ebitda"), ("Dòng tiền", "dong_tien")]:
            print(f"  {kb:<11} {ten:<10}" + "".join(f"{f0(sum(r[k] for r in kq['rows'][i * 12:(i + 1) * 12])):>10}" for i in range(4)))
        print(f"  {kb:<11} {'Luỹ kế T6':<10}{f0(kq['rows'][5]['luy_ke']):>10}")

    print("\n=== KINH TẾ ĐƠN VỊ (trên 1.000 lead, cơ sở) ===")
    for k, v in ue.items():
        print(f"  {k}: {v:,.2f}")
    print("\n=== HOÀ VỐN PHÒNG BAN (cơ sở) ===")
    for g, d in hv.items():
        print(f"  {g}: {d['so_nguoi']} người, CP cố định {f1(d['chi_phi_co_dinh'])} trđ/th -> "
              f"{d['khach_dong_hanh_hoa_von']:.1f} khách đồng hành/th (+{d['khach_nen_tang_di_kem']:.0f} nền tảng), "
              f"{d['lead_can']:.0f} lead/th, doanh số {f1(d['doanh_so_can'])} trđ/th")

    print("\n=== 3 KỊCH BẢN ===")
    for kb, (kq, u, h) in ket_qua.items():
        s = tom_tat(kq)
        print(f"  {kb}: Tổng vốn {f0(s['tong_von'])} | Đáy {f0(s['day'])} (T{s['thang_day']}) | HV vận hành T{s['hoa_von_vh']}"
              f" | Hoàn vốn T{s['hoan_von']} | Luỹ kế T24 {f0(s['luy_ke_24'])} | NPV48 {f0(s['npv'])} | "
              f"IRR {('%.0f%%' % (s['irr_nam'] * 100)) if s['irr_nam'] is not None else 'n/a'} | "
              f"Đội tối đa {s['doi_toi_da']} người")

    print("\n=== PHƯƠNG ÁN ĐỀ XUẤT: LÙI MỐC TUYỂN (Tăng trưởng T10, Mở rộng T19) ===")
    for kb, kq in pa_lui.items():
        s_ = tom_tat(kq)
        print(f"  {kb}: Tổng vốn {f0(s_['tong_von'])} | Đáy {f0(s_['day'])} (T{s_['thang_day']}) | HV vận hành T{s_['hoa_von_vh']}"
              f" | Hoàn vốn T{s_['hoan_von']} | Luỹ kế T24 {f0(s_['luy_ke_24'])} | NPV48 {f0(s_['npv'])} | "
              f"IRR {('%.0f%%' % (s_['irr_nam'] * 100)) if s_['irr_nam'] is not None else 'n/a'}")

    # Độ nhạy ±20% (kịch bản cơ sở)
    bien = {
        "Tỷ lệ chuyển đổi (toàn phễu)": "he_so_cd",
        "Giá gói đồng hành": "he_so_gia_dh",
        "Lương cứng tư vấn viên": "he_so_luong_sales",
        "Chi phí quảng cáo / lead (CPL)": "he_so_cpl",
        "Ngân sách quảng cáo (giữ CPL)": "he_so_ngan_sach",
        "Lead tự nhiên (nội dung organic)": "he_so_lead_tn",
    }
    do_nhay = []
    print("\n=== ĐỘ NHẠY ±20% (cơ sở) ===")
    for ten, arg in bien.items():
        for h in (0.8, 1.2):
            kq = chay(kb="Cơ sở", **{arg: h})
            do_nhay.append(dict(bien=ten, he_so=h, npv=kq["npv"], luy_ke_24=kq["luy_ke_24"],
                                tong_von=kq["tong_von"], hoan_von=kq["hoan_von"], hoa_von_vh=kq["hoa_von_vh"]))
            print(f"  {ten} x{h}: NPV {f0(kq['npv'])} | Luỹ kế T24 {f0(kq['luy_ke_24'])} | Tổng vốn {f0(kq['tong_von'])}"
                  f" | HV vận hành T{kq['hoa_von_vh']} | Hoàn vốn T{kq['hoan_von']}")

    # Ngưỡng: mỗi biến (đơn lẻ) phải đổi bao nhiêu để hoàn vốn trong 24 tháng (luỹ kế T24 >= 0)
    nguong = {}
    print("\n=== NGƯỠNG ĐỂ HOÀN VỐN TRONG 24 THÁNG (đổi từng biến, giữ biến khác ở cơ sở) ===")
    for ten, arg in [("Tỷ lệ chuyển đổi (toàn phễu)", "he_so_cd"), ("Giá gói đồng hành", "he_so_gia_dh"),
                     ("Chi phí quảng cáo / lead (CPL)", "he_so_cpl")]:
        lo, hi = (1.0, 2.0) if arg != "he_so_cpl" else (0.3, 1.0)
        for _ in range(40):
            mid = (lo + hi) / 2
            ok = chay(kb="Cơ sở", **{arg: mid})["luy_ke_24"] >= 0
            if arg == "he_so_cpl":
                lo, hi = (mid, hi) if ok else (lo, mid)
            else:
                lo, hi = (lo, mid) if ok else (mid, hi)
        h = hi if arg != "he_so_cpl" else lo
        nguong[ten] = round(h, 3)
        print(f"  {ten}: hệ số {h:.2f} ({(h - 1) * 100:+.0f}%)")

    # Kiểm tra hợp lý
    print("\n=== KIỂM TRA ===")
    for r in cs["rows"]:
        tai = r["hv_dong_hanh_dang_hoc"] / (NHAN_SU[r["giai_doan"]]["Coach tài chính"] + r["coach_them"])
        if tai > 40:
            print(f"  CẢNH BÁO T{r['thang']}: {tai:.0f} học viên đồng hành/coach (>40)")
        lead_sale = r["lead"] / NHAN_SU[r["giai_doan"]]["Tư vấn viên"]
        if lead_sale > 600:
            print(f"  CẢNH BÁO T{r['thang']}: {lead_sale:.0f} lead/tư vấn viên (>600)")
    thu_nhap_sale = []
    for r in cs["rows"][:BAO_CAO]:
        g = r["giai_doan"]
        hh_tv = r["hoa_hong"] - (GD["hh_truong_nhom"] * (r["dt_nen_tang"] + r["dt_dong_hanh"] + r["dt_thanh_vien"])
                                 if NHAN_SU[g]["Trưởng nhóm bán hàng"] else 0)
        thu_nhap_sale.append(VI_TRI["Tư vấn viên"][1] + hh_tv / NHAN_SU[g]["Tư vấn viên"])
    print(f"  Thu nhập TB tư vấn viên (cứng+HH) T6/T12/T24: {f1(thu_nhap_sale[5])} / {f1(thu_nhap_sale[11])} / {f1(thu_nhap_sale[23])} trđ")

    # Bảng nhân sự
    bang_ns = []
    for g in GIAI_DOAN:
        a, b = GIAI_DOAN[g]
        for vt, n in NHAN_SU[g].items():
            if n:
                bang_ns.append(dict(giai_doan=g, thang=f"T{a}–T{min(b, BAO_CAO) if g != 'Mở rộng' else str(BAO_CAO) + '+'}",
                                    bo_phan=VI_TRI[vt][0], vi_tri=vt, so_nguoi=n, luong_cung=VI_TRI[vt][1],
                                    chi_phi_thang_gom_bh=round(n * VI_TRI[vt][1] * (1 + GD["ty_le_bh_dn"]), 2),
                                    nguon_luong=VI_TRI[vt][2]))
    ns_bo_phan = {}
    for g in GIAI_DOAN:
        d = {}
        for vt, n in NHAN_SU[g].items():
            d[VI_TRI[vt][0]] = d.get(VI_TRI[vt][0], 0) + n
        ns_bo_phan[g] = d

    out = dict(
        ma_viec="2026-11-14-khung-chuong-trinh-chuyen-doi",
        don_vi="triệu đồng",
        ghi_chu="Mọi số thị trường từ nghien-cuu.md có độ tin cậy tối đa Trung bình (chưa mở được trang gốc); "
                "tỷ lệ phễu, giá đồng hành/thành viên, lương quản lý là giả định.",
        tong_von_can_chuan_bi=round(cs["tong_von"], 1),
        von_ban_dau=round(cs["von_ban_dau"], 1),
        von_ban_dau_chi_tiet={k: v for k, v in cs["von"].items()},
        von_luu_dong_bu_lo=round(cs["von_luu_dong"], 1),
        quy_du_phong=round(cs["du_phong"], 1),
        day_dong_tien=dict(gia_tri=round(cs["day"], 1), thang=cs["thang_day"]),
        hoa_von_van_hanh_thang=cs["hoa_von_vh"],
        hoan_von_thang=cs["hoan_von"],
        npv_48_thang=round(cs["npv"], 1),
        irr_nam=round(cs["irr_nam"], 4) if cs["irr_nam"] is not None else None,
        thang_ten=[f"T{r['thang']}" for r in cs["rows"][:BAO_CAO]],
        dong_tien_luy_ke_co_so_24t=[round(r["luy_ke"], 1) for r in cs["rows"][:BAO_CAO]],
        dong_tien_thang_co_so_24t=[round(r["dong_tien"], 1) for r in cs["rows"][:BAO_CAO]],
        doanh_thu_thang_co_so_24t=[round(r["doanh_thu"], 1) for r in cs["rows"][:BAO_CAO]],
        chi_phi_thang_co_so_24t=[round(r["doanh_thu"] - r["ebitda"], 1) for r in cs["rows"][:BAO_CAO]],
        so_nguoi_thang_24t=[r["so_nguoi"] for r in cs["rows"][:BAO_CAO]],
        luy_ke_theo_kich_ban_24t={kb: [round(r["luy_ke"], 1) for r in kq["rows"][:BAO_CAO]]
                                  for kb, (kq, _, _) in ket_qua.items()},
        phieu_thang_co_so_24t=[dict(thang=r["thang"], tiep_can=round(r["tiep_can"]), lead=round(r["lead"]),
                                     tham_du=round(r["tham_du"]), nen_tang=round(r["nen_tang"], 1),
                                     dong_hanh=round(r["dong_hanh"], 1), thanh_vien=round(r["thanh_vien"], 1))
                                for r in cs["rows"][:BAO_CAO]],
        nhan_su_theo_giai_doan=bang_ns,
        nhan_su_theo_bo_phan=ns_bo_phan,
        hoa_von_phong_ban={g: {k: round(v, 1) if isinstance(v, float) else v for k, v in d.items()}
                           for g, d in hv.items()},
        kinh_te_don_vi_1000_lead={k: round(v, 3) for k, v in ue.items()},
        kich_ban={kb: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in tom_tat(kq).items()}
                  for kb, (kq, _, _) in ket_qua.items()},
        phuong_an_lui_moc_tuyen=dict(
            mo_ta="Giữ đội Khởi động tới T9, Tăng trưởng T10–T18, Mở rộng từ T19",
            kich_ban={kb: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in tom_tat(kq).items()}
                      for kb, kq in pa_lui.items()},
            luy_ke_co_so_24t=[round(r["luy_ke"], 1) for r in pa_lui["Cơ sở"]["rows"][:BAO_CAO]],
        ),
        nguong_hoan_von_24t=nguong,
        do_nhay=[{k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()} for d in do_nhay],
        thang_san_pham=[
            dict(tang="Miễn phí", ten="Nội dung + hội thảo miễn phí tại VP/online", gia=0),
            dict(tang="Nhập môn", ten="Khoá nền tảng Quản lý tài chính & crypto an toàn", gia=GD["gia_nen_tang"]),
            dict(tang="Cốt lõi", ten="Chương trình đồng hành 3 tháng", gia=GD["gia_dong_hanh"]),
            dict(tang="Gắn bó", ten="Thành viên năm (cộng đồng)", gia=GD["gia_thanh_vien"]),
        ],
    )
    with open(os.path.join(HERE, "tai-chinh.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("\nĐã ghi tai-chinh.json")


if __name__ == "__main__":
    main()
