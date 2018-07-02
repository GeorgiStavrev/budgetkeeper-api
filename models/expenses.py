import sqlalchemy as sa

metadata = sa.MetaData()
expenses = sa.Table(
    'expenses',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String),
    sa.Column('sum', sa.REAL),
    sa.Column('date', sa.DateTime)
)