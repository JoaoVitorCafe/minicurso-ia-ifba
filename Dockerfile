# Use a imagem base do PostgreSQL
FROM pgvector/pgvector:pg16

# Defina variáveis de ambiente para o PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=DB_IFBA
ENV PORT=5433

# Comando para iniciar o PostgreSQL quando o contêiner for iniciado
CMD ["postgres"]