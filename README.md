# Cyber security base - Project 1

## Installing instructions

1. Open your terminal and clone the repository:
```bash
git clone https://github.com/huusolga/cyber-security-base-project-1
```
2. Move to the project’s directory:
```bash
cd csb-project1
```
3. Install PostgresSQL
If you’re using… 
- Linux: use [this installation script](https://github.com/hy-tsoha/local-pg)
- Windows: download the installation package from [Postgres website](https://www.postgresql.org/download/)
- Mac: use [Postgres.app](https://postgresapp.com/)
  
4. Create a new .env file
```bash
touch .env
```
Add this line to the file:
DATABASE_URL=address
where address is postgresql+psycopg2:// if Postgres was installed with Linux and otherwise postgresql:///user where “user” is the name of the database that shows up when opening the PostgreSQL interpreter.

5. Activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

6. Install the requirements:
```bash
pip install -r requirements.txt
```
7. Open an another terminal and start Postgres:
```bash
start-pg.sh
```
8. Define the database schema:
```bash
psql < schema.sql
```
9. Start the Todo App:
```bash
flask run
```
You'll find the Todo App by default at localhost:5000

## Essay 

