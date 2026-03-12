from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 使用本地 SQLite 数据库存放历史台账和预测结果
SQLALCHEMY_DATABASE_URL = "sqlite:///./galca.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 数据库获取依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
