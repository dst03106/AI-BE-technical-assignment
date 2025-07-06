from django.core.management.base import BaseCommand

import example_datas.setup_company_data
import example_datas.setup_company_news_data
from core.infra.llm import PgVectorStore


class Command(BaseCommand):
    help = "데이터베이스 세팅 및 사전 데이터를 저장합니다."

    def handle(self, *_args, **_options):
        PgVectorStore().ensure_table_exists()
        example_datas.setup_company_data.main()
        example_datas.setup_company_news_data.main()
