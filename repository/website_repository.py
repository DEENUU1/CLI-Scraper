from sqlalchemy.orm import Session
from datetime import datetime
from ..models import Website
from ..schemas import WebsiteCreate


def get_website(db: Session, website_id: int):
    return db.query(Website).filter(Website.id == website_id).first()


def get_websites(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Website).offset(skip).limit(limit).all()


def create_website(db: Session, website: WebsiteCreate):
    db_website = Website(name=website.name, objects_numbers=website.objects_numbers, last_update=datetime.now())
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website


def update_website(db: Session, website_id: int, website: WebsiteCreate):
    db_website = db.query(Website).filter(Website.id == website_id).first()
    db_website.name = website.name
    db_website.objects_numbers = website.objects_numbers
    db_website.last_update = datetime.now()
    db.commit()
    db.refresh(db_website)
    return db_website


def delete_website(db: Session, website_id: int):
    db_website = db.query(Website).filter(Website.id == website_id).first()
    db.delete(db_website)
    db.commit()
    return db_website
