CREATE TABLE if NOT EXISTS words (
	id SERIAL PRIMARY KEY,
	english VARCHAR(80) UNIQUE NOT NULL,
	russian VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE if NOT EXISTS user (
	id SERIAL PRIMARY KEY,
	telegram_id BIGINT UNIQUE NOT NULL
);

CREATE TABLE if NOT EXISTS userword (
	id SERIAL PRIMARY KEY,
	word_id INTEGER NOT NULL REFERENCES words(id),
	telegram_id INTEGER NOT NULL REFERENCES users(id)
);

INSERT INTO words (english, russian) VALUES ('Red', 'Красный'),
            ('Blue', 'Синий'),
            ('Green', 'Зелёный'),
            ('Yellow', 'Жёлтый'),
            ('Apple', 'Яблоко'),
            ('Bus', 'Автобус'),
            ('Mouse', 'Мышь'),
            ('Orange', 'Апельсин'),
            ('Pencil', 'Карандаш'),
            ('Flower', 'Цветок'),
            ('City', 'Город'),
            ('Big', 'Большой'),
            ('Little', 'Маленький'),
            ('Girl', 'Девушка'),
            ('Boy', 'Мальчик'),
            ('Peace', 'Мир');
            