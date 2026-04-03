from app.utils.db import DatabaseManager

class StockRepository:
    @staticmethod
    def get_stock_by_city_and_group(city, blood_group):
        query = """
        SELECT units_available FROM stock
        WHERE blood_group=?
        """
        return DatabaseManager.execute_query(query, (blood_group,), fetch_all=False)

    @staticmethod
    def get_all_stock():
        query = "SELECT 'System Wide' as city, blood_group, units_available FROM stock"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def update_stock_units(city, blood_group, units):
        """Medical Procurement: Increments stock for a phenotype."""
        # Using SQLite native UPSERT pattern for the mirror
        query = """
        INSERT INTO stock (blood_group, units_available)
        VALUES (?, ?)
        ON CONFLICT(blood_group) DO UPDATE SET units_available = units_available + excluded.units_available
        """
        return DatabaseManager.execute_modify(query, (blood_group, units))
