from sqlalchemy import text
from database import engine

def test_schema_creation():
    """Test creating a single simple table"""
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255)
                )
            """))
            conn.commit()
            print("Successfully created test table")
            
            result = conn.execute(text("SELECT * FROM test_table"))
            print("Successfully queried test table")
            
            conn.execute(text("DROP TABLE test_table"))
            conn.commit()
            print("Successfully cleaned up test table")
            
    except Exception as e:
        print("Test failed!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_schema_creation()