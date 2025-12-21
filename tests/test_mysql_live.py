# tests/test_mysql_live.py
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import unittest
from datetime import datetime, timezone
from core.mysql import MySQL


class TestMySQLLive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MySQL(
            host="mysql-35a80bf1-emadnama.e.aivencloud.com",
            user="avnadmin",
            password="AVNS_aVaQBUJA27G6uyBbJW_",
            database="test_db",
            port=23776,
            ssl_required=True,
        )
        cls.db.connect()

        cur = cls.db.connection.cursor()
        try:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cls.db.connection.commit()
        finally:
            cur.close()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_insert_select_update_real(self):
        unique_name = f"live_test_{datetime.now(timezone.utc).isoformat()}"
        new_id = self.db.insert("test_table", {"name": unique_name})
        self.assertIsNotNone(new_id)

        rows = self.db.select("test_table", {"id": new_id})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], unique_name)

        updated_name = unique_name + "_updated"
        affected = self.db.update("test_table", {"name": updated_name}, {"id": new_id})
        self.assertEqual(affected, 1)

        rows2 = self.db.select("test_table", {"id": new_id})
        self.assertEqual(len(rows2), 1)
        self.assertEqual(rows2[0]["name"], updated_name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
