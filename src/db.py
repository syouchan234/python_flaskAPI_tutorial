from src import app
from src import db
from src import ma
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, desc

# DBの作成
class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(Integer, primary_key=True)  # 連番（主キー）
    product = db.Column(String(32))  # 受注した製品名
    date = db.Column(String(8))  # 受注日
    amount = db.Column(Integer)  # 受注した数量

# アプリケーションコンテキスト内でDBを作成
with app.app_context():
    db.create_all()

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

order_schema = OrderSchema(many=True)

# GET(全件参照)
@app.route('/order', methods=["GET"])
def getAll():
    data = Order.query.all()
    return jsonify(order_schema.dump(data))

#GET(1件参照)
@app.route('/order/<int:id>', methods=["GET"])
def get(id):
    data = Order.query.filter_by(id=id).all()
    return jsonify(order_schema.dump(data))

#POST(登録)
@app.route('/order', methods=["POST"])
def post():
    entry = Order()
    # jsonリクエストから値取得
    json = request.get_json()
    if type(json) == list:
        data = json[0]
    else:
        data = json
    entry.product = data["product"]
    entry.date = data["date"]
    entry.amount = data["amount"]
    db.session.add(entry)
    db.session.commit()
    db.session.close()

    latestdata= Order.query.order_by(desc(Order.id)).first()
    return redirect('/order/' + str(latestdata.id))

#PUT(更新)
@app.route('/order/<int:id>', methods=["PUT"])
def put(id):
    entry = Order.query.get(id)
    # jsonリクエストから値取得
    json = request.get_json()
    if type(json) == list:
        data = json[0]
    else:
        data = json
    entry.product = data["product"]
    entry.date = data["date"]
    entry.amount = data["amount"]
    db.session.merge(entry)
    db.session.commit()
    db.session.close()

    return redirect('/order/' + str(id))

#DELETE(削除)
@app.route('/order/<int:id>', methods=["DELETE"])
def delete(id):
    entry = Order.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    db.session.close()

    return '', 204