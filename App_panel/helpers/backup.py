import json
import uuid
import decimal
from datetime import date, datetime, time
from django.apps import apps
from django.db import models


class SQLGenerator:
    SUPPORTED_DB_TYPES = {"sqlite", "mysql", "postgresql", "postgres"}

    def __init__(self, db_type="sqlite"):
        db_type = (db_type or "sqlite").lower().strip()

        if db_type not in self.SUPPORTED_DB_TYPES:
            raise ValueError(
                f"Unsupported db_type: {db_type}. "
                f"Allowed values: sqlite, mysql, postgresql"
            )

        # normalize
        if db_type == "postgres":
            db_type = "postgresql"

        self.db_type = db_type

        if self.db_type == "mysql":
            self.quote = "`"
        elif self.db_type == "postgresql":
            self.quote = '"'
        else:
            self.quote = '"'

    # -----------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------
    def q(self, name):
        return f"{self.quote}{name}{self.quote}"

    def get_db_type(self):
        """
        Returns normalized database type:
        sqlite | mysql | postgresql
        """
        return self.db_type

    def get_header(self):
        return f"-- SQL export for {self.db_type}\n\n"

    # -----------------------------------------------------------
    # 1) Map Django model fields to DB-specific SQL column types
    # -----------------------------------------------------------
    def map_field_type(self, field):
        # Auto / primary key types
        if isinstance(field, models.BigAutoField):
            if self.db_type == "sqlite":
                return "INTEGER"
            elif self.db_type == "mysql":
                return "BIGINT AUTO_INCREMENT"
            return "BIGSERIAL"

        if isinstance(field, models.AutoField):
            if self.db_type == "sqlite":
                return "INTEGER"
            elif self.db_type == "mysql":
                return "INT AUTO_INCREMENT"
            return "SERIAL"

        # Relationship IDs
        if isinstance(field, (models.ForeignKey, models.OneToOneField)):
            target_field = field.target_field
            if isinstance(target_field, models.BigAutoField):
                return "BIGINT"
            elif isinstance(target_field, models.AutoField):
                return "INTEGER"
            return self.map_field_type(target_field)

        # Text-like
        if isinstance(field, (models.CharField, models.SlugField, models.EmailField, models.URLField)):
            return f"VARCHAR({field.max_length or 255})"

        if isinstance(field, models.TextField):
            return "TEXT"

        # Integers
        if isinstance(field, models.BigIntegerField):
            return "BIGINT"

        if isinstance(field, (models.IntegerField, models.PositiveIntegerField, models.PositiveSmallIntegerField)):
            return "INTEGER"

        if isinstance(field, models.SmallIntegerField):
            return "SMALLINT"

        # Boolean
        if isinstance(field, models.BooleanField):
            if self.db_type == "sqlite":
                return "INTEGER"
            return "BOOLEAN"

        # Decimal / float
        if isinstance(field, models.DecimalField):
            return f"DECIMAL({field.max_digits},{field.decimal_places})"

        if isinstance(field, models.FloatField):
            return "DOUBLE PRECISION" if self.db_type == "postgresql" else "FLOAT"

        # Date / time
        if isinstance(field, models.DateTimeField):
            return "TIMESTAMP"

        if isinstance(field, models.DateField):
            return "DATE"

        if isinstance(field, models.TimeField):
            return "TIME"

        if isinstance(field, models.DurationField):
            return "BIGINT" if self.db_type != "postgresql" else "INTERVAL"

        # JSON
        if isinstance(field, models.JSONField):
            if self.db_type == "postgresql":
                return "JSONB"
            elif self.db_type == "mysql":
                return "JSON"
            return "TEXT"

        # UUID
        if isinstance(field, models.UUIDField):
            if self.db_type == "postgresql":
                return "UUID"
            return "VARCHAR(36)"

        # Binary / file-ish
        if isinstance(field, models.BinaryField):
            if self.db_type == "postgresql":
                return "BYTEA"
            elif self.db_type == "mysql":
                return "LONGBLOB"
            return "BLOB"

        if isinstance(field, (models.FileField, models.ImageField)):
            return f"VARCHAR({getattr(field, 'max_length', 255) or 255})"

        return "TEXT"

    # -----------------------------------------------------------
    # 2) Build column definition
    # -----------------------------------------------------------
    def build_column_definition(self, field):
        col_name = self.q(field.column)
        col_type = self.map_field_type(field)

        parts = [col_name, col_type]

        # SQLite PK special handling
        if field.primary_key:
            if self.db_type == "sqlite":
                if isinstance(field, (models.AutoField, models.BigAutoField)):
                    return f"{col_name} INTEGER PRIMARY KEY AUTOINCREMENT"
                return f"{col_name} {col_type} PRIMARY KEY"
            else:
                if "AUTO_INCREMENT" not in col_type and "SERIAL" not in col_type:
                    parts.append("PRIMARY KEY")

        # Nullability
        if not field.null and not field.primary_key:
            parts.append("NOT NULL")

        # Unique
        if field.unique and not field.primary_key:
            parts.append("UNIQUE")

        # Default
        default_sql = self.get_default_sql(field)
        if default_sql is not None:
            parts.append(f"DEFAULT {default_sql}")

        return " ".join(parts)

    def get_default_sql(self, field):
        if not field.has_default():
            return None

        default = field.default

        # Skip callable defaults like timezone.now / uuid.uuid4
        if callable(default):
            return None

        return self.sql_literal(default)

    # -----------------------------------------------------------
    # 3) SQL literal serialization
    # -----------------------------------------------------------
    def sql_literal(self, value):
        if value is None:
            return "NULL"

        if isinstance(value, bool):
            if self.db_type == "postgresql":
                return "TRUE" if value else "FALSE"
            return "1" if value else "0"

        if isinstance(value, (int, float)):
            return str(value)

        if isinstance(value, decimal.Decimal):
            return str(value)

        if isinstance(value, uuid.UUID):
            return f"'{str(value)}'"

        if isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"

        if isinstance(value, date):
            return f"'{value.strftime('%Y-%m-%d')}'"

        if isinstance(value, time):
            return f"'{value.strftime('%H:%M:%S')}'"

        if isinstance(value, (dict, list)):
            return "'" + json.dumps(value, ensure_ascii=False).replace("'", "''") + "'"

        return "'" + str(value).replace("'", "''") + "'"

    # -----------------------------------------------------------
    # 4) Generate CREATE TABLE
    # -----------------------------------------------------------
    def generate_create_table(self, model, include_fk_constraints=False):
        table = model._meta.db_table
        fields = model._meta.local_fields

        cols_def = [self.build_column_definition(field) for field in fields]

        # Optional FK constraints
        if include_fk_constraints:
            for field in fields:
                if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                    ref_table = field.remote_field.model._meta.db_table
                    ref_column = field.target_field.column

                    constraint_name = f"{table}_{field.column}_fk"

                    cols_def.append(
                        f"CONSTRAINT {self.q(constraint_name)} "
                        f"FOREIGN KEY ({self.q(field.column)}) "
                        f"REFERENCES {self.q(ref_table)} ({self.q(ref_column)})"
                    )

        sql = (
            f"CREATE TABLE IF NOT EXISTS {self.q(table)} (\n    "
            + ",\n    ".join(cols_def)
            + "\n);\n"
        )
        return sql

    # -----------------------------------------------------------
    # 5) Generate INSERT statements
    # -----------------------------------------------------------
    def generate_insert(self, model, batch_size=500):
        table = model._meta.db_table
        fields = model._meta.local_fields

        qs = model.objects.all().values(*[f.attname for f in fields])

        rows = list(qs)
        if not rows:
            return ""

        colnames = ", ".join(self.q(f.column) for f in fields)

        sql_parts = []
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            values_sql = []

            for row in batch:
                vals = []
                for field in fields:
                    v = row.get(field.attname)
                    vals.append(self.sql_literal(v))

                values_sql.append("(" + ", ".join(vals) + ")")

            insert_sql = (
                f"INSERT INTO {self.q(table)} ({colnames}) VALUES\n    "
                + ",\n    ".join(values_sql)
                + ";\n"
            )
            sql_parts.append(insert_sql)

        return "\n".join(sql_parts)

    # -----------------------------------------------------------
    # 6) Generate full SQL for one model
    # -----------------------------------------------------------
    def generate_for_model(self, model, include_fk_constraints=False):
        sql = self.generate_create_table(model, include_fk_constraints=include_fk_constraints)
        sql += self.generate_insert(model)
        sql += "\n"
        return sql

    # -----------------------------------------------------------
    # 7) Generate SQL for model + auto-created M2M through tables
    # -----------------------------------------------------------
    def generate_for_model_with_m2m(self, model, include_fk_constraints=False):
        sql = self.generate_for_model(model, include_fk_constraints=include_fk_constraints)

        for m2m in model._meta.many_to_many:
            through = m2m.remote_field.through

            # skip custom through if you don't want duplicates elsewhere
            sql += self.generate_create_table(through, include_fk_constraints=include_fk_constraints)
            sql += self.generate_insert(through)
            sql += "\n"

        return sql

    # -----------------------------------------------------------
    # 8) Generate SQL for all project models
    # -----------------------------------------------------------
    def generate_full_database(self, include_fk_constraints=False, include_header=True):
        sql = self.get_header() if include_header else ""
        exported_tables = set()

        for model in apps.get_models():
            table = model._meta.db_table
            if table not in exported_tables:
                sql += self.generate_for_model(model, include_fk_constraints=include_fk_constraints)
                exported_tables.add(table)

            for m2m in model._meta.many_to_many:
                through = m2m.remote_field.through
                through_table = through._meta.db_table
                if through_table not in exported_tables:
                    sql += self.generate_create_table(
                        through,
                        include_fk_constraints=include_fk_constraints
                    )
                    sql += self.generate_insert(through)
                    sql += "\n"
                    exported_tables.add(through_table)

        return sql