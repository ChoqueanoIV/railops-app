import os

# O bootstrap dos testes não depende do .env nem de credenciais reais.
os.environ["DATABASE_URL"] = (
    "postgresql://railops_test:railops_test@localhost/railops_test"
)
os.environ["JWT_SECRET_KEY"] = "segredo-ficticio-exclusivo-para-testes"
os.environ["RAILOPS_ENV"] = "test"
