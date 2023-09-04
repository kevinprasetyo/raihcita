from apps import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Snisub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    perusahaan = db.Column(db.Text, nullable=True)
    tanggal = db.Column(db.DateTime(timezone=True), default=func.now())
    nama = db.Column(db.Text, nullable=True)
    posisi = db.Column(db.Text, nullable=True)
    n1 = db.Column(db.Text, nullable=True)
    n2 = db.Column(db.Text, nullable=True)
    n3 = db.Column(db.Text, nullable=True)
    n4 = db.Column(db.Text, nullable=True)
    n5 = db.Column(db.Text, nullable=True)
    n6 = db.Column(db.Text, nullable=True)
    n7 = db.Column(db.Text, nullable=True)
    n8 = db.Column(db.Text, nullable=True)
    n9 = db.Column(db.Text, nullable=True)
    n10 = db.Column(db.Text, nullable=True)
    n11 = db.Column(db.Text, nullable=True)
    n12 = db.Column(db.Text, nullable=True)
    n13 = db.Column(db.Text, nullable=True)
    n14 = db.Column(db.Text, nullable=True)
    n15 = db.Column(db.Text, nullable=True)
    n16 = db.Column(db.Text, nullable=True)
    n17 = db.Column(db.Text, nullable=True)
    n18 = db.Column(db.Text, nullable=True)
    n19 = db.Column(db.Text, nullable=True)
    n20 = db.Column(db.Text, nullable=True)
    n21 = db.Column(db.Text, nullable=True)
    n22 = db.Column(db.Text, nullable=True)
    n23 = db.Column(db.Text, nullable=True)


class Janji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True)
    hp = db.Column(db.Text, nullable=True)
    tgl = db.Column(db.Text, nullable=True)
