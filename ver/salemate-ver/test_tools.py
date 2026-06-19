"""Kiểm thử logic các tool thú y — chạy được KHÔNG cần API key.

    python test_tools.py
"""
import json

import tools as T


def show(title, result):
    print("\n" + "=" * 70)
    print(title)
    print("-" * 70)
    print(json.dumps(result, ensure_ascii=False, indent=2)[:1600])


def main():
    # 1) Tra cứu thuốc / vaccine
    r = T.tra_cuu_thuoc(benh="dịch tả lợn châu Phi")
    assert r["so_luong"] >= 1, "Phải tìm thấy vaccine ASF"
    assert any(p["ma_sp"] == "VX01" for p in r["ket_qua"]), "Phải có NAVET-ASFVAC"
    show("1) tra_cuu_thuoc(benh='dịch tả lợn châu Phi')", r)

    # 2) RAG tài liệu
    r = T.tra_cuu_tai_lieu("an toàn sinh học phòng ASF")
    assert len(r["ket_qua"]) >= 1 and any("an-toan" in d["nguon"] for d in r["ket_qua"])
    show("2) tra_cuu_tai_lieu(an toàn sinh học ASF)", r)

    # 3a) Chẩn đoán ASF -> escalation, không thuốc đặc trị
    r = T.chan_doan_benh("heo sốt cao da tai bụng đỏ tím chết nhanh nằm chồng đống", vat_nuoi="heo")
    b = r["benh_kha_nang_nhat"]
    assert "châu Phi" in b["ten_benh"], "Phải nhận diện ASF"
    assert b["co_thuoc_dac_tri"] is False and r["can_chuyen_chuyen_gia"] is True
    assert b.get("thong_tin_thi_truong"), "Phải có thông tin thị trường"
    show("3a) chan_doan_benh(ASF) — escalation + market info", r)

    # 3b) Chẩn đoán bệnh vi khuẩn -> có thuốc đặc trị
    r = T.chan_doan_benh("heo con tiêu chảy phân trắng bỏ ăn mất nước", vat_nuoi="heo")
    b = r["benh_kha_nang_nhat"]
    assert b["co_thuoc_dac_tri"] is True, "Tiêu chảy E.coli có thuốc đặc trị"
    assert len(b["san_pham_de_xuat"]) >= 1
    show("3b) chan_doan_benh(tiêu chảy E.coli) — có thuốc + liều", r)

    # 4a) Liệt kê nhà phân phối
    r = T.phan_tich_nha_phan_phoi()
    assert len(r["danh_sach"]) >= 1
    show("4a) phan_tich_nha_phan_phoi() — danh sách NPP", r)

    # 4b) Phân tích 1 NPP -> gợi ý đơn + bán thêm
    r = T.phan_tich_nha_phan_phoi("Minh Phát")
    assert r["thong_tin"]["id"] == "NPP001"
    assert len(r["san_pham_hay_mua"]) >= 1
    assert len(r["goi_y_don_tiep_theo"]) >= 1
    assert len(r["co_hoi_ban_them"]) >= 1, "Phải có cơ hội bán thêm (vd sát trùng/vaccine)"
    show("4b) phan_tich_nha_phan_phoi('Minh Phát') — gợi ý đơn + bán thêm", r)

    print("\n" + "=" * 70)
    print("✅ TẤT CẢ TOOL THÚ Y HOẠT ĐỘNG ĐÚNG (không cần API key).")
    print("=" * 70)


if __name__ == "__main__":
    main()
