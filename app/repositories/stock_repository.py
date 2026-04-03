from app.utils.db import DatabaseManager

class StockRepository:
    @staticmethod
    def get_stock_by_city_and_group(city, blood_group):
        query = """
        SELECT units_available FROM blood_stock
        WHERE city=%s AND blood_group=%s
        """
        return DatabaseManager.execute_query(query, (city, blood_group), fetch_all=False)

    @staticmethod
    def get_all_stock():
        query = "SELECT city, blood_group, units_available FROM blood_stock"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def update_stock_units(city, blood_group, units):
        """Medical Procurement: Increments stock for a phenotype."""
        query = """
        INSERT INTO blood_stock (city, blood_group, units_available)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE units_available = units_available + VALUES(units_available)
        """
        return DatabaseManager.execute_modify(query, (city, blood_group, units))
