from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from app import db
from app.models import user


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    calib_data = db.Column(JSON)
    throw_data = db.Column(JSON)
    start_ts = db.Column(db.BigInteger)
    end_ts = db.Column(db.BigInteger)
    calib_start_ts = db.Column(db.BigInteger)
    calib_end_ts = db.Column(db.BigInteger)
    velocity = db.Column(db.Float)
    angle = db.Column(db.Float)
    def __repr__(self):
        return self.id
    
    def get_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "calib_data": self.calib_data,
            "throw_data": self.throw_data,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "calib_start_ts": self.calib_start_ts,
            "calib_end_ts": self.calib_end_ts,
            "velocity": self.velocity,
            "angle": self.angle,
            "created_at": self.created_at.isoformat()
        }

    def get_meta(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "velocity": self.velocity,
            "angle": self.angle,
            "created_at": self.created_at.isoformat()
        }


def get():
    measurements = Measurement.query.order_by(Measurement.created_at.desc()).all()
    return [measurement.get_json() for measurement in measurements]


def find(id):
    res = Measurement.query.filter_by(id=id).first()
    if res:
        return res.get_json()
    return None


def create(
    user_id,
    title,
    calib_data,
    throw_data,
    start_ts,
    end_ts,
    calib_start_ts,
    calib_end_ts,
    velocity,
    angle
):
    meas = Measurement(
        user_id=user_id, 
        title=title,
        calib_data=calib_data,
        throw_data=throw_data,
        start_ts=start_ts,
        end_ts=end_ts,
        calib_start_ts=calib_start_ts,
        calib_end_ts=calib_end_ts,
        velocity=velocity,
        angle=angle
    )
    try:
        db.session.add(meas)
        db.session.commit()
        return meas.get_meta()
    except:
        return None


def find_metas(user_id):
    measurements = Measurement.query.filter_by(user_id=user_id).all()
    return [res.get_meta() for res in measurements]