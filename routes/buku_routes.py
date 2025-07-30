from flask import Blueprint,request,jsonify
from models import db
from models.buku import Buku
from utils.decoration import login_required
from schemas.buku_schema import BukuSchema
from utils.response import success_message, error_message

buku_bp = Blueprint('buku_bp', __name__)
buku_schema = BukuSchema()

@buku_bp.route('/buku', methods=['POST'])
@login_required
def tambah_buku():
    data = request.get_json()
    errors = buku_schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    buku = Buku(judul=data['judul'], penulis=data['penulis'], tahun=data['tahun'])
    db.session.add(buku)
    db.session.commit()
    return success_message(data=buku_schema.dump(buku), message="Data buku berhasil ditambahkan!!")

@buku_bp.route('/buku', methods=['GET'])
@login_required
def tampil_buku():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    judul_filter = request.args.get('judul', '', type=str)

    query = Buku.query
    if judul_filter:
        query = query.filter(Buku.judul.ilike(f"%{judul_filter}%"))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    buku_list = pagination.items

    if not buku_list:    
        return error_message(message="Data tidak ditemukan!!", status_code=404)

    result = {
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "per_page": pagination.per_page,
        "buku": BukuSchema(many=True).dump(buku_list)
    }

    return success_message(data=result, message="Daftar buku berhasil diambil")

@buku_bp.route('/buku/<int:id>', methods=['GET'])
@login_required
def cari_buku(id):
    b = Buku.query.get_or_404(id)
    return success_message(data=buku_schema.dump(b), message="Buku berhasil ditemukan!")

@buku_bp.route('/buku/<int:id>', methods=['PUT'])
@login_required
def edit_buku(id):
    data = request.get_json()
    b = Buku.query.get_or_404(id)
    b.judul = data.get("judul", b.judul)
    b.penulis = data.get("penulis", b.penulis)
    b.tahun = data.get("tahun", b.tahun)
    db.session.commit()
    return jsonify({"message": "Data buku diperbarui!!"})

@buku_bp.route('/buku/<int:id>', methods=['DELETE'])
@login_required
def hapus_buku(id):
    b = Buku.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return jsonify({"message": "Data buku sudah dihapus!!"})
