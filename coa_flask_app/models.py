"""
The models module is where sqlalchemy modesl are created.
"""

from coa_flask_app import db


class Item(db.Model):
    """
    The item class is to show off an item with its material and category.
    """
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(200))
    category = db.Column(db.String(200))
    item_name = db.Column(db.String(200))

    def __repr__(self):
        return f'<item {self.item_name}>'


class CoaSummaryView(db.Model):
    """
    The CoaSummaryView is meant to look over all the aspects of a record.
    """
    __tablename__ = 'coa_summary_view'
    record_id = db.Column(db.BigInteger, primary_key=True)
    quantity = db.Column(db.Float)
    team_captain = db.Column(db.String(200))
    updated_datetime = db.Column(db.TIMESTAMP)
    site_id = db.Column(db.BigInteger)
    site_name = db.Column(db.String(200))
    state = db.Column(db.String(200))
    county = db.Column(db.String(200))
    town = db.Column(db.String(200))
    street = db.Column(db.String(200))
    zipcode = db.Column(db.String(10))
    material = db.Column(db.String(200))
    category = db.Column(db.String(200))
    item_name = db.Column(db.String(200))
    item_id = db.Column(db.BigInteger)
    updated_by = db.Column(db.String(200))
    event_code = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    volunteer_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<COA_SUMMARY {self.record_id} {self.quantity} {self.team_captain}' \
            '{self.updated_datetime} {self.site_id} {self.site_name}' \
            '{self.state} {self.county} {self.town} {self.street}' \
            '{self.zipcode} {self.material} {self.category} {self.item_name}' \
            '{self.item_id} {self.updated_by} {self.event_code} {self.brand}' \
            '{self.volunteer_date}'
