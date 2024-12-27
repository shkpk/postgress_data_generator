# postgress_data_generator
This script is used to generate large amount of data in postgres

# To Generate Data in the GB Range

You can scale up the number of rows, tables, and databases accordingly. Here's how you can achieve this:

## Target: 1 GB of Data

1. **Size per Row**: 16 bytes (as calculated earlier).

2. **Rows to Reach 1 GB**:
   - 1 GB = 1,073,741,824 bytes.
   - Rows needed = \( \frac{1,073,741,824}{16} = 67,108,864 \) rows.

3. **Distribute Rows Across Tables**:
   - If you keep 5 tables per database, you need:
     - \( \text{Rows per table} = \frac{67,108,864}{5} \approx 13,421,773 \text{ rows/table.} \)

4. **Distribute Across Databases**:
   - If you create multiple databases, reduce rows proportionally. For example:
     - \( 50 \text{ databases} \times 5 \text{ tables each} \times \frac{67,108,864}{50 \times 5} \approx 268,435 \text{ rows per table.} \)

## Key Adjustments:

- **Increased `ROWS_PER_TABLE`** to distribute rows evenly across tables and databases.
- **Controlled `DATABASE_COUNT` and `TABLES_PER_DATABASE`** for flexibility.
- **Change `DB_NAME_PREFIX` and `TABLE_NAME_PREFIX`** for change in databases name and table names to whatever you want.

## Scaling Further:

To generate larger datasets, simply:

1. Increase `DATABASE_COUNT` or `TABLES_PER_DATABASE`.
2. Increase `ROWS_PER_TABLE`.

### For example:

- For 10 GB, multiply the rows per table by 10.
- Adjust parameters to your storage capacity and performance requirements.

## Creating docker container of postgres 14 for testing

- Create data directory

```
rm -rf data
mkdir data
sudo chown -R 999:999 data
chmod -R 700 data
```

- Create `postgres.conf` file

```
cat > postgresql.conf <<END
listen_addresses = '*'
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
END
```

- Create `pg_hba.conf` file

```
cat > pg_hba.conf <<END
local   all             all                                     md5
host    all             all             0.0.0.0/0               md5
host replication replicator 0.0.0.0/0 md5
END
```

- Now run docker container

```
docker run -d \
  --name postgres14 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -e REPLICATOR_USER=replicator \
  -e REPLICATOR_PASSWORD=replicatorpassword \
  -p 5432:5432 \
  -v $(pwd)/postgresql.conf:/etc/postgresql/postgresql.conf \
  -v $(pwd)/pg_hba.conf:/etc/postgresql/pg_hba.conf \
  -v $(pwd)/data:/var/lib/postgresql/data \
  postgres:14 \
  -c config_file=/etc/postgresql/postgresql.conf \
  -c hba_file=/etc/postgresql/pg_hba.conf
```
