"""tables

Revision ID: 01b33a7fea42
Revises: 
Create Date: 2019-12-17 03:51:28.489540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01b33a7fea42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brokerage',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brokerageid', sa.Integer(), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('brokerage_sum', sa.String(length=20), nullable=True),
    sa.Column('operationoperation', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cash_apply',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cashid', sa.Integer(), nullable=True),
    sa.Column('cashphone', sa.String(length=11), nullable=True),
    sa.Column('cashmoney', sa.String(length=20), nullable=True),
    sa.Column('examine', sa.String(length=20), nullable=True),
    sa.Column('cash_date', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contents',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('globals',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cash_min', sa.String(length=20), nullable=True),
    sa.Column('task_num', sa.String(length=10), nullable=True),
    sa.Column('invite_money', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goods',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('goodsid', sa.Integer(), nullable=True),
    sa.Column('issuerphone', sa.String(length=11), nullable=False),
    sa.Column('g_title', sa.String(length=100), nullable=True),
    sa.Column('g_pic', sa.String(length=256), nullable=True),
    sa.Column('g_amount', sa.String(length=20), nullable=True),
    sa.Column('g_brokerage', sa.String(length=20), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('classid', sa.Integer(), nullable=False),
    sa.Column('issuerdate', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('issuerphone', 'classid')
    )
    op.create_table('goods_class',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.Column('classid', sa.Integer(), nullable=False),
    sa.Column('goodstype', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('classid')
    )
    op.create_table('goods_receive',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('goodsid', sa.Integer(), nullable=True),
    sa.Column('getphone', sa.String(length=11), nullable=True),
    sa.Column('getid', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settle',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bringid', sa.Integer(), nullable=True),
    sa.Column('bringclass', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('douyincode', sa.String(length=10), nullable=True),
    sa.Column('i_card', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('credit_code', sa.String(length=20), nullable=True),
    sa.Column('invitation', sa.String(length=10), nullable=True),
    sa.Column('positive_pic', sa.String(length=100), nullable=True),
    sa.Column('side_pic', sa.String(length=100), nullable=True),
    sa.Column('license', sa.String(length=100), nullable=True),
    sa.Column('examine', sa.String(length=20), nullable=True),
    sa.Column('sub_date', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('superuser',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token'),
    sa.UniqueConstraint('username')
    )
    op.create_table('users',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.Column('openid', sa.String(length=256), nullable=True),
    sa.Column('wxpic_url', sa.String(length=256), nullable=True),
    sa.Column('wxname', sa.String(length=80), nullable=True),
    sa.Column('wxnumber', sa.String(length=20), nullable=True),
    sa.Column('user_identity', sa.String(length=50), nullable=True),
    sa.Column('user_all_money', sa.String(length=20), nullable=True),
    sa.Column('user_y_money', sa.String(length=20), nullable=True),
    sa.Column('user_s_money', sa.String(length=20), nullable=True),
    sa.Column('user_icode', sa.String(length=10), nullable=True),
    sa.Column('user_all_friend', sa.String(length=10), nullable=True),
    sa.Column('up_phone', sa.String(length=11), nullable=True),
    sa.Column('alipay', sa.String(length=30), nullable=True),
    sa.Column('reg_time', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wheel',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adress_pic', sa.String(length=256), nullable=True),
    sa.Column('url_pic', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wheel')
    op.drop_table('users')
    op.drop_table('superuser')
    op.drop_table('settle')
    op.drop_table('goods_receive')
    op.drop_table('goods_class')
    op.drop_table('goods')
    op.drop_table('globals')
    op.drop_table('contents')
    op.drop_table('cash_apply')
    op.drop_table('brokerage')
    # ### end Alembic commands ###
