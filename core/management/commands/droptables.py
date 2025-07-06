from django.core.management.base import BaseCommand

from core.infra.llm import PgVectorStore
from core.models import Company, CompanyNews, Document


class Command(BaseCommand):
    help = "Company, CompanyNews, Document 테이블을 삭제합니다"

    def handle(self, *_args, **_options):
        conn = PgVectorStore.get_db_connection()
        self.drop_table(conn, CompanyNews._meta.db_table)
        self.drop_table(conn, Company._meta.db_table)
        self.drop_table(conn, Document._meta.db_table)

    def drop_table(self, conn, table_name):
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table_name};")
            conn.commit()
