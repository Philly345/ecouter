from extensions import db  
from flask_login import UserMixin
import datetime
import uuid

# Association table for many-to-many relationship between Transcript and Tag
transcript_tags = db.Table('transcript_tags',
    db.Column('transcript_id', db.Integer, db.ForeignKey('transcript.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    generated_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    name_change_count = db.Column(db.Integer, default=0)
    password = db.Column(db.String(150))  # Only used for local signups
    provider = db.Column(db.String(50))  # 'local' or 'google'
    verified = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(300), default='default-avatar.png')
    country = db.Column(db.String(100))
    gender = db.Column(db.String(50))

    # ✅ Updated: Store birthdate as string (format: YYYY-MM-DD)
    age = db.Column(db.String(10))  # Stores birthdate as string like '2002-12-01'
    age_change_count = db.Column(db.Integer, default=0)

    transcripts = db.relationship('Transcript', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)
    tags = db.relationship('Tag', backref='user', lazy=True)


class Project(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transcripts = db.relationship('Transcript', backref='project', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id,
            'transcript_ids': [t.id for t in self.transcripts]
        }


class Tag(db.Model):
    __tablename__ = 'tag'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Tag {self.name}>"


class Transcript(db.Model):
    __tablename__ = 'transcript'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    text = db.Column(db.Text)
    summary = db.Column(db.Text)
    word_timings = db.Column(db.Text)
    status = db.Column(db.String(20), default='processing')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)

    tags = db.relationship('Tag', secondary=transcript_tags, backref='transcripts')

    def set_tags_from_string(self, tag_string):
        """Attach tags from a comma-separated string, creating any that don’t exist."""
        tag_names = [name.strip().lower() for name in tag_string.split(',') if name.strip()]
        self.tags = []
        for name in tag_names:
            existing_tag = Tag.query.filter_by(name=name, user_id=self.user_id).first()
            if not existing_tag:
                existing_tag = Tag(name=name, user_id=self.user_id)
                db.session.add(existing_tag)
            self.tags.append(existing_tag)
