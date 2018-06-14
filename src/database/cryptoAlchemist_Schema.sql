--Time in Milliseconds
CREATE TABLE IF NOT EXISTS history
(
    insert_time     bigint,
    exchange_name   varchar(50),
    currency_name   varchar(50),
    price           real,
    "size"          real,
    bid             real,
    ask             real,
    volume          real
);

CREATE TABLE IF NOT EXISTS buy_history
(
    insert_time     bigint,
    exchange_name   varchar(50),
    currency_name   varchar(50),
    buy_price       real
);

CREATE TABLE IF NOT EXISTS order_book_summary
(
    insert_time     bigint,
    exchange_name   varchar(50),
    currency_name   varchar(50),
    bid1_price      real,
    bid2_price      real,
    bid3_price      real,
    bid4_price      real,
    bid5_price      real,
    ask1_price      real,
    ask2_price      real,
    ask3_price      real,
    ask4_price      real,
    ask5_price      real,
    bid1_size      real,
    bid2_size      real,
    bid3_size      real,
    bid4_size      real,
    bid5_size      real,
    ask1_size      real,
    ask2_size      real,
    ask3_size      real,
    ask4_size      real,
    ask5_size      real,
    bid1_num_orders      real,
    bid2_num_orders      real,
    bid3_num_orders      real,
    bid4_num_orders      real,
    bid5_num_orders      real,
    ask1_num_orders      real,
    ask2_num_orders      real,
    ask3_num_orders      real,
    ask4_num_orders      real,
    ask5_num_orders      real
);
