table_names_to_sql = {
    'hello_name_views': '''
    create table if not exists hello_name_views (
        minute_view_id integer primary key autoincrement,
        ip_address     varchar(15) not null,
        name           varchar(32),
        views          integer not null,
        dt_received    timestamp not null
    )
    ''',
    'hello_world_views': '''
    create table if not exists hello_world_views (
        minute_view_id  integer primary key autoincrement,
        ip_address      varchar(15) not null,
        views           integer not null,
        dt_received     timestamp not null
    )
    '''
}
