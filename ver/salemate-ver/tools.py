"""Công cụ (tool) cho AI SalesMate — mảng thuốc thú y / vaccine (Nova Consumer).

Số liệu (liều lượng, giá, lịch sử đơn) luôn lấy từ dữ liệu có cấu trúc — KHÔNG để LLM bịa.
"""
import os
import json

from retrieval import Retriever, tokenize

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _load(name: str):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


VET_PRODUCTS = _load("vet_products.json")
DISEASES = _load("diseases.json")
DISTRIBUTORS = _load("distributors.json")
PRODUCTS = _load("products.json")
COMPETITORS = _load("competitors.json")
RETRIEVER = Retriever(os.path.join(DATA_DIR, "knowledge"))

PRODUCT_BY_MA = {p["ma_sp"]: p for p in VET_PRODUCTS}
FEED_PRODUCT_BY_MA = {p["ma_sp"]: p for p in PRODUCTS}


def _match(value: str, target: str) -> bool:
    if not value or not target:
        return False
    return " ".join(tokenize(value)) in " ".join(tokenize(target)) or \
        any(t in tokenize(target) for t in tokenize(value))


# ---------------------------------------------------------------------------
# 1) Tra cứu thuốc / vaccine (catalogue thú y có cấu trúc)
# ---------------------------------------------------------------------------
def tra_cuu_thuoc(vat_nuoi=None, loai=None, benh=None, tu_khoa=None, ma_sp=None):
    if ma_sp and ma_sp.upper() in PRODUCT_BY_MA:
        return {"ket_qua": [PRODUCT_BY_MA[ma_sp.upper()]]}
    results = []
    for p in VET_PRODUCTS:
        if vat_nuoi and vat_nuoi not in p["vat_nuoi"]:
            continue
        if loai and p["loai"] != loai:
            continue
        blob = f"{p['ten']} {p['cong_dung']} {p['chi_dinh']} {p.get('ghi_chu','')}"
        if benh and not _match(benh, blob):
            continue
        if tu_khoa and not _match(tu_khoa, blob):
            continue
        results.append(p)
    return {"ket_qua": results, "so_luong": len(results)}


# ---------------------------------------------------------------------------
# 2) Tra cứu tài liệu (RAG): an toàn sinh học, vaccine, chính sách, khuyến mãi
# ---------------------------------------------------------------------------
def tra_cuu_tai_lieu(cau_hoi, so_ket_qua=4):
    docs = RETRIEVER.search(cau_hoi, k=int(so_ket_qua or 4))
    return {
        "ket_qua": docs,
        "luu_y": "Chỉ dùng tri thức đã được R&D/thú y duyệt; trích dẫn 'nguon' khi trả lời.",
    }


# ---------------------------------------------------------------------------
# 3) Chẩn đoán bệnh + thông tin thị trường + escalation
# ---------------------------------------------------------------------------
def chan_doan_benh(trieu_chung, vat_nuoi="heo"):
    q = set(tokenize(trieu_chung))
    scored = []
    for d in DISEASES:
        if vat_nuoi and vat_nuoi not in d["vat_nuoi"]:
            continue
        matched = [s for s in d["trieu_chung"] if set(tokenize(s)) & q]
        if not matched:
            continue
        confidence = round(len(matched) / len(d["trieu_chung"]), 2)
        scored.append((confidence, len(matched), d, matched))

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)

    if not scored:
        return {
            "ket_luan": "Chưa khớp bệnh nào trong tri thức đã duyệt.",
            "can_chuyen_chuyen_gia": True,
            "ly_do_escalation": "Không đủ dữ kiện để chẩn đoán an toàn — đề nghị mô tả thêm hoặc mời thú y.",
        }

    confidence, _, best, matched = scored[0]
    escalate = (
        confidence < 0.4
        or best["muc_do"] in ("nang", "nguy_hiem")
        or best["can_chuyen_gia"]
        or not best["co_thuoc_dac_tri"]
    )
    sp = [PRODUCT_BY_MA[m] for m in best["san_pham_lien_quan"] if m in PRODUCT_BY_MA]

    return {
        "benh_kha_nang_nhat": {
            "ten_benh": best["ten_benh"],
            "ten_khoa_hoc": best["ten_khoa_hoc"],
            "tac_nhan": best["tac_nhan"],
            "do_tin_cay": confidence,
            "trieu_chung_khop": matched,
            "chan_doan": best["chan_doan"],
            "chan_doan_phan_biet": best.get("chan_doan_phan_biet"),
            "muc_do": best["muc_do"],
            "co_thuoc_dac_tri": best["co_thuoc_dac_tri"],
            "buoc_xu_ly": best["buoc_xu_ly"],
            "san_pham_de_xuat": [
                {"ma_sp": s["ma_sp"], "ten": s["ten"], "loai": s["loai"], "lieu_luong": s.get("lieu_luong")}
                for s in sp
            ],
            "thong_tin_thi_truong": best.get("thong_tin_thi_truong"),
        },
        "benh_khac_can_phan_biet": [
            {"ten_benh": s[2]["ten_benh"], "do_tin_cay": s[0]} for s in scored[1:3]
        ],
        "can_chuyen_chuyen_gia": escalate,
        "ly_do_escalation": (
            "Bệnh virus nguy hiểm / không có thuốc đặc trị / độ tin cậy thấp — cần thú y xác chẩn (PCR) và không tự kê đơn điều trị virus."
            if escalate else "Bệnh do vi khuẩn có thuốc đặc trị — có thể tư vấn sơ bộ kèm khuyến cáo."
        ),
        "khuyen_cao": "Đây là gợi ý sơ bộ, không thay thế chẩn đoán của bác sĩ thú y. Liều dùng theo chỉ định và tuân thủ thời gian ngừng thuốc.",
    }


# ---------------------------------------------------------------------------
# 4) Phân tích nhà phân phối + gợi ý đơn tiếp theo
# ---------------------------------------------------------------------------
def _find_distributor(ten_hoac_id):
    key = (ten_hoac_id or "").strip()
    for d in DISTRIBUTORS:
        if d["id"].lower() == key.lower():
            return d
    for d in DISTRIBUTORS:
        if _match(key, d["ten"]) or _match(d["ten"], key):
            return d
    return None


def phan_tich_nha_phan_phoi(nha_phan_phoi=None):
    if not nha_phan_phoi:
        return {
            "danh_sach": [{"id": d["id"], "ten": d["ten"], "khu_vuc": d["khu_vuc"]} for d in DISTRIBUTORS],
            "huong_dan": "Nêu tên hoặc mã nhà phân phối để phân tích chi tiết.",
        }
    d = _find_distributor(nha_phan_phoi)
    if not d:
        return {
            "loi": f"Không tìm thấy nhà phân phối '{nha_phan_phoi}'.",
            "goi_y": [x["ten"] for x in DISTRIBUTORS],
        }

    orders = d["lich_su_don"]
    tong_gia_tri = sum(o["gia_tri_vnd"] for o in orders)
    by_product = {}
    for o in orders:
        rec = by_product.setdefault(o["ma_sp"], {"ten_sp": o["ten_sp"], "so_luong": 0, "gia_tri": 0, "so_lan": 0})
        rec["so_luong"] += o["so_luong"]
        rec["gia_tri"] += o["gia_tri_vnd"]
        rec["so_lan"] += 1
    top = sorted(by_product.items(), key=lambda kv: kv[1]["gia_tri"], reverse=True)

    # Nhóm sản phẩm đã mua vs còn thiếu -> cơ hội bán thêm
    loai_da_mua = {PRODUCT_BY_MA[m]["loai"] for m in by_product if m in PRODUCT_BY_MA}
    co_hoi = []
    for p in VET_PRODUCTS:
        if p["loai"] not in loai_da_mua and p["ma_sp"] not in by_product:
            co_hoi.append({"ma_sp": p["ma_sp"], "ten": p["ten"], "loai": p["loai"], "ly_do": f"Chưa từng mua nhóm '{p['loai']}'."})
    # Ưu tiên vaccine ASF + sát trùng cho an toàn sinh học
    co_hoi.sort(key=lambda x: 0 if x["loai"] in ("vaccine", "sat_trung") else 1)

    thang_list = sorted({o["thang"] for o in orders})
    san_pham_chu_luc = top[0][1]["ten_sp"] if top else None

    return {
        "thong_tin": {
            "id": d["id"], "ten": d["ten"], "khu_vuc": d["khu_vuc"],
            "loai_hinh": d["loai_hinh"], "quy_mo": d["quy_mo"],
            "cong_no_vnd": d["cong_no_vnd"], "ghi_chu": d.get("ghi_chu"),
        },
        "tong_quan": {
            "tong_gia_tri_vnd": tong_gia_tri,
            "so_don": len(orders),
            "khoang_thoi_gian": f"{thang_list[0]} → {thang_list[-1]}" if thang_list else None,
            "san_pham_chu_luc": san_pham_chu_luc,
        },
        "san_pham_hay_mua": [
            {"ma_sp": ma, "ten_sp": v["ten_sp"], "tong_so_luong": v["so_luong"], "tong_gia_tri": v["gia_tri"], "so_lan_mua": v["so_lan"]}
            for ma, v in top
        ],
        "goi_y_don_tiep_theo": [
            {"ma_sp": ma, "ten_sp": v["ten_sp"], "so_luong_de_xuat": round(v["so_luong"] / max(1, v["so_lan"]))}
            for ma, v in top[:2]
        ],
        "co_hoi_ban_them": co_hoi[:3],
        "goi_y_cho_sales": "Chốt đơn lặp lại theo sản phẩm chủ lực + chu kỳ mua, đồng thời chào nhóm sản phẩm còn thiếu (ưu tiên vaccine ASF & sát trùng cho an toàn sinh học).",
    }


# ---------------------------------------------------------------------------
# 5) So sánh sản phẩm Anova với đối thủ (dữ liệu demo có cấu trúc)
# ---------------------------------------------------------------------------
def so_sanh_san_pham(vat_nuoi=None, giai_doan=None, ma_sp=None, doi_thu=None):
    def match_stage(query, target):
        if not query:
            return True
        q_tokens = tokenize(query)
        t_tokens = tokenize(target or "")
        return bool(q_tokens) and all(t in t_tokens for t in q_tokens)

    anova_matches = []
    if ma_sp and ma_sp.upper() in FEED_PRODUCT_BY_MA:
        anova_matches = [FEED_PRODUCT_BY_MA[ma_sp.upper()]]
    else:
        for p in PRODUCTS:
            if vat_nuoi and vat_nuoi not in p["vat_nuoi"]:
                continue
            if giai_doan and not match_stage(giai_doan, p.get("giai_doan")):
                continue
            if p["loai"] != "cam":
                continue
            anova_matches.append(p)

    competitor_matches = []
    for c in COMPETITORS:
        if vat_nuoi and vat_nuoi not in c["vat_nuoi"]:
            continue
        if giai_doan and not match_stage(giai_doan, c.get("giai_doan")):
            continue
        if doi_thu and not _match(doi_thu, c["hang"]):
            continue
        competitor_matches.append(c)

    def compact_anova(p):
        return {
            "ma_sp": p["ma_sp"],
            "ten": p["ten"],
            "vat_nuoi": p["vat_nuoi"],
            "giai_doan": p["giai_doan"],
            "dam_pct": p["dam_pct"],
            "xo_pct": p["xo_pct"],
            "nang_luong_kcal": p["nang_luong_kcal"],
            "canxi_pct": p["canxi_pct"],
            "fcr_tham_chieu": p["fcr_tham_chieu"],
            "gia_vnd_per_kg": p["gia_vnd_per_kg"],
            "quy_cach": p["quy_cach"],
            "huong_dan_dung": p["huong_dan_dung"],
            "ghi_chu": p["ghi_chu"],
        }

    def compact_competitor(c):
        return {
            "hang": c["hang"],
            "ten_sp": c["ten_sp"],
            "vat_nuoi": c["vat_nuoi"],
            "giai_doan": c["giai_doan"],
            "dam_pct": c["dam_pct"],
            "xo_pct": c["xo_pct"],
            "nang_luong_kcal": c["nang_luong_kcal"],
            "canxi_pct": c["canxi_pct"],
            "fcr_tham_chieu": c["fcr_tham_chieu"],
            "gia_vnd_per_kg": c["gia_vnd_per_kg"],
            "nguon": c["nguon"],
        }

    return {
        "anova": [compact_anova(p) for p in anova_matches],
        "doi_thu": [compact_competitor(c) for c in competitor_matches],
        "luu_y": "Dữ liệu đối thủ là DEMO/chưa kiểm chứng; chỉ dùng để minh họa cách so sánh khi demo.",
        "goi_y_cho_sales": "So sánh theo đạm, xơ, năng lượng, FCR tham chiếu và giá/kg; chốt bằng lợi điểm phù hợp giai đoạn nuôi thay vì chỉ nói rẻ hơn.",
    }


# ---------------------------------------------------------------------------
# Schema + điều phối
# ---------------------------------------------------------------------------
DISPATCH = {
    "tra_cuu_thuoc": tra_cuu_thuoc,
    "tra_cuu_tai_lieu": tra_cuu_tai_lieu,
    "chan_doan_benh": chan_doan_benh,
    "phan_tich_nha_phan_phoi": phan_tich_nha_phan_phoi,
    "so_sanh_san_pham": so_sanh_san_pham,
}


def dispatch(name: str, args: dict) -> dict:
    fn = DISPATCH.get(name)
    if fn is None:
        return {"loi": f"Không có công cụ tên {name}"}
    try:
        return fn(**(args or {}))
    except Exception as e:  # noqa: BLE001
        return {"loi": f"Lỗi khi chạy {name}: {e}"}


TOOL_SCHEMAS = [
    {
        "name": "chan_doan_benh",
        "description": "Chẩn đoán bệnh trên heo từ mô tả triệu chứng. Trả về bệnh khả năng nhất + độ tin cậy + tác nhân + bước xử lý + sản phẩm Nova Consumer phù hợp + thông tin thị trường + cờ cần-chuyển-chuyên-gia. Dùng khi người dùng mô tả tình trạng con vật.",
        "input_schema": {
            "type": "object",
            "properties": {
                "trieu_chung": {"type": "string", "description": "Mô tả triệu chứng/tình trạng con vật"},
                "vat_nuoi": {"type": "string", "description": "Mặc định 'heo'"},
            },
            "required": ["trieu_chung"],
        },
    },
    {
        "name": "tra_cuu_thuoc",
        "description": "Tra cứu thuốc thú y / vaccine của Nova Consumer (Anova Pharma, Navetco, Vetvaco, Anova Biotech): công dụng, chỉ định, LIỀU LƯỢNG, đường dùng, thời gian ngừng thuốc, giá. Dùng khi hỏi về sản phẩm hoặc cần thông tin chi tiết liều lượng.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vat_nuoi": {"type": "string"},
                "loai": {"type": "string", "description": "vaccine | khang_sinh | sat_trung | bo_tro | ho_tro"},
                "benh": {"type": "string", "description": "Tên bệnh cần tìm thuốc điều trị/phòng"},
                "tu_khoa": {"type": "string"},
                "ma_sp": {"type": "string", "description": "VD VX01, TP01"},
            },
        },
    },
    {
        "name": "phan_tich_nha_phan_phoi",
        "description": "Phân tích lịch sử mua/bán của nhà phân phối và gợi ý đơn hàng tiếp theo + sản phẩm nên chào bán. Bỏ trống tham số để liệt kê danh sách nhà phân phối.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nha_phan_phoi": {"type": "string", "description": "Tên hoặc mã nhà phân phối, VD 'Minh Phát' hoặc 'NPP001'"},
            },
        },
    },
    {
        "name": "tra_cuu_tai_lieu",
        "description": "Tra cứu tài liệu: an toàn sinh học/ASF, nguyên tắc dùng vaccine & kháng sinh, chính sách bán hàng, khuyến mãi (RAG).",
        "input_schema": {
            "type": "object",
            "properties": {
                "cau_hoi": {"type": "string"},
                "so_ket_qua": {"type": "integer"},
            },
            "required": ["cau_hoi"],
        },
    },
    {
        "name": "so_sanh_san_pham",
        "description": "So sánh sản phẩm cám Anova với sản phẩm đối thủ theo vật nuôi/giai đoạn/mã sản phẩm: đạm, xơ, năng lượng, canxi, FCR tham chiếu, giá/kg. Dùng khi người dùng hỏi so sánh Anova với CP, De Heus, GreenFeed, Cargill, Japfa.",
        "input_schema": {
            "type": "object",
            "properties": {
                "vat_nuoi": {"type": "string", "description": "heo hoặc gà"},
                "giai_doan": {"type": "string", "description": "VD heo thịt choai, gà thịt vỗ béo"},
                "ma_sp": {"type": "string", "description": "Mã sản phẩm Anova, VD A102"},
                "doi_thu": {"type": "string", "description": "Tên hãng đối thủ, VD CP, De Heus, GreenFeed"},
            },
        },
    },
]
