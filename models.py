from datetime import datetime
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conditions = relationship('PatientCondition', back_populates='patient', cascade='all, delete-orphan')
    sessions = relationship('TherapySession', back_populates='patient', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PatientCondition(db.Model):
    __tablename__ = 'patient_conditions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    condition_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20))
    diagnosis_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='conditions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'condition_type': self.condition_type,
            'severity': self.severity,
            'diagnosis_date': self.diagnosis_date.isoformat() if self.diagnosis_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TherapySession(db.Model):
    __tablename__ = 'therapy_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    session_date = db.Column(db.DateTime, nullable=False)
    session_type = db.Column(db.String(50), nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='sessions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'session_date': self.session_date.isoformat(),
            'session_type': self.session_type,
            'duration_minutes': self.duration_minutes,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }