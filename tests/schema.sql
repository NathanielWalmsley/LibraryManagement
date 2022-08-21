/* ======================= TABLES ========================*/

CREATE TABLE library_branch (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(100) UNIQUE NOT NULL,
    address VARCHAR(200) UNIQUE NOT NULL
);

CREATE TABLE borrower (
    card_number INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    phone VARCHAR(50) NOT NULL
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title VARCHAR(100) NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    FOREIGN KEY (publisher)
        REFERENCES tbl_publisher(publisher) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (title, publisher)
);

CREATE TABLE author (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE book_author_link(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    book_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) 
        REFERENCES book(id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (author_id)
        REFERENCES author(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    book_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    FOREIGN KEY (book_id)
        REFERENCES book(id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (branch_id)
        REFERENCES library_branch(id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE (book_id, branch_id)
);

CREATE TABLE loan (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    book_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    card_number INTEGER NOT NULL,
    date_out VARCHAR(50) NOT NULL,
    date_due VARCHAR(50) NOT NULL,
    FOREIGN KEY (book_id)
        REFERENCES book(id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (branch_id)
        REFERENCES branch(id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (card_number)
        REFERENCES borrower(card_number) 
        ON UPDATE CASCADE ON DELETE CASCADE
);

/*==================== POPULATING TABLES ======================*/

INSERT INTO library_branch
    (name, address)
    VALUES
    ('Sharpstown','32 Corner Road, New York, NY 10012'),
    ('Central','491 3rd Street, New York, NY 10014'),
    ('Saline','40 State Street, Saline, MI 48176'),
    ('Ann Arbor','101 South University, Ann Arbor, MI 48104')
;

INSERT INTO borrower
    (name, address, phone)
    VALUES
    ('Joe Smith','1321 4th Street, New York, NY 10014','212-312-1234'),
    ('Jane Smith','1321 4th Street, New York, NY 10014','212-931-4124'),
    ('Tom Li','981 Main Street, Ann Arbor, MI 48104','734-902-7455'),
    ('Angela Thompson','2212 Green Avenue, Ann Arbor, MI 48104','313-591-2122'),
    ('Harry Emnace','121 Park Drive, Ann Arbor, MI 48104','412-512-5522'),
    ('Tom Haverford','23 75th Street, New York, NY 10014','212-631-3418'),
    ('Haley Jackson','231 52nd Avenue New York, NY 10014','212-419-9935'),
    ('Michael Horford','653 Glen Avenue, Ann Arbor, MI 48104','734-998-1513')
;

INSERT INTO book
    (title, publisher)
    VALUES 
    ('The Name of the Wind', 'DAW Books'),
    ('It', 'Viking'),
    ('The Green Mile', 'Signet Books'),
    ('Dune', 'Chilton Books'),
    ('The Hobbit', 'George Allen & Unwin'),
    ('Eragon', 'Alfred A. Knopf'),
    ('The Wise Mans Fear', 'DAW Books'),
    ('Harry Potter and the Philosophers Stone', 'Bloomsbury'),
    ('Hard Boiled Wonderland and The End of the World', 'Shinchosa'),
    ('The Giving Tree', 'Harper and Row'),
    ('The Hitchhikers Guide to the Galaxy', 'Pan Books'),
    ('Brave New World', 'Chalto & Windus'),
    ('The Princess Bride', 'Harcourt Brace Jovanovich'),
    ('Fight Club', 'W.W. Norton'),
    ('Holes', 'Scholastic'),
    ('Harry Potter and the Chamber of Secrets', 'Bloomsbury'),
    ('Harry Potter and the Prisoner of Azkaban', 'Bloomsbury'),
    ('The Fellowship of the Ring', 'George Allen & Unwin'),
    ('A Game of Thrones', 'Bantam'),
    ('The Lost Tribe', 'Picador USA')
;

INSERT INTO author
    (name)
    VALUES
    'Patrick Rothfuss',
    'Stephen King',
    'Frank Herbert',
    'J.R.R. Tolkien',
    'Christopher Paolini',
    'J.K. Rowling',
    'Haruki Murakami',
    'Shel Silverstein',
    'Douglas Adams',
    'Aldous Huxley',
    'William Goldman',
    'Chuck Palahniuk',
    'Louis Sachar',
    'George R.R. Martin',
    'Mark Lee'
;

INSERT INTO book_author_link
    (book_id, author_id)
    VALUES
    (1, 1),
    (2, 2),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 5),
    (7, 1),
    (8, 6),
    (9, 7),
    (10, 8),
    (11, 9),
    (12, 10),
    (13, 11),
    (14, 12),
    (15, 13),
    (16, 6),
    (17, 6),
    (18, 4),
    (19, 14),
    (20, 15)
;

INSERT INTO inventory
    (book_id, branch_id, stock)
    VALUES
    (
(1, 1, 5),
(2, 1, 5),
(3, 1, 5),
(4, 1, 5),
(5, 1, 5),
(6, 1, 5),
(7, 1, 5),
(8, 1, 5),
(9, 1, 5),
(10, 1, 5),
(11, 1, 5),
(12, 1, 5),
(13, 1, 5),
(14, 1, 5),
(15, 1, 5),
(16, 1, 5),
(17, 1, 5),
(18, 1, 5),
(19, 1, 5),
(20, 1, 5),
(1, 2, 5),
(2, 2, 5),
(3, 2, 5),
(4, 2, 5),
(5, 2, 5),
(6, 2, 5),
(7, 2, 5),
(8, 2, 5),
(9, 2, 5),
(10, 2, 5),
(11, 2, 5),
(12, 2, 5),
(13, 2, 5),
(14, 2, 5),
(15, 2, 5),
(16, 2, 5),
(17, 2, 5),
(18, 2, 5),
(19, 2, 5),
(20, 2, 5),
(1, 3, 5),
(2, 3, 5),
(3, 3, 5),
(4, 3, 5),
(5, 3, 5),
(6, 3, 5),
(7, 3, 5),
(8, 3, 5),
(9, 3, 5),
(10, 3, 5),
(11, 3, 5),
(12, 3, 5),
(13, 3, 5),
(14, 3, 5),
(15, 3, 5),
(16, 3, 5),
(17, 3, 5),
(18, 3, 5),
(19, 3, 5),
(20, 3, 5),
(1, 4, 5),
(2, 4, 5),
(3, 4, 5),
(4, 4, 5),
(5, 4, 5),
(6, 4, 5),
(7, 4, 5),
(8, 4, 5),
(9, 4, 5),
(10, 4, 5),
(11, 4, 5),
(12, 4, 5),
(13, 4, 5),
(14, 4, 5),
(15, 4, 5),
(16, 4, 5),
(17, 4, 5),
(18, 4, 5),
(19, 4, 5),
(20, 4, 5)
;

INSERT INTO loan
    (book_id, branch_id, card_number, date_out, date_due)
    VALUES
    (1, 1, 1, '1/1/18', '2/2/18'),
    (2, 1, 1, '1/1/18', '2/2/18'),
    (3, 1, 1, '1/1/18', '2/2/18'),
    (4, 1, 1, '1/1/18', '2/2/18'),
    (5, 1, 2, '1/3/18', '2/3/18'),
    (6, 1, 2, '1/3/18', '2/3/18'),
    (7, 1, 2, '1/3/18', '2/3/18'),
    (8, 1, 2, '1/3/18', '2/3/18'),
    (9, 1, 2, '1/3/18', '2/3/18'),
    (11, 1, 2, '1/3/18', '2/3/18'),
    (12, 2, 5, '12/12/17', '1/12/18'),
    (10, 2, 5, '12/12/17', '1/12/18'),
    (20, 2, 5, '2/3/18', '3/3/18'),
    (18, 2, 5, '1/5/18', '2/5/18'),
    (19, 2, 5, '1/5/18', '2/5/18'),
    (19, 2, 1, '1/3/18', '2/3/18'),
    (11, 2, 6, '1/7/18', '2/7/18'),
    (1, 2, 6, '1/7/18', '2/7/18'),
    (2, 2, 1, '1/7/18', '2/7/18'),
    (3, 2, 1, '1/7/18', '2/7/18'),
    (5, 2, 5, '12/12/17', '1/12/18'),
    (4, 3, 3, '1/9/18', '2/9/18'),
    (7, 3, 2, '1/3/18', '2/3/18'),
    (17, 3, 2, '1/3/18', '2/3/18'),
    (16, 3, 4, '1/3/18', '2/3/18'),
    (15, 3, 4, '1/3/18', '2/3/18'),
    (14, 3, 4, '1/3/18', '2/3/18'),
    (13, 3, 7, '1/3/18', '2/3/18'),
    (13, 3, 2, '1/3/18', '2/3/18'),
    (19, 3, 2, '12/12/17', '1/12/18'),
    (20, 4, 3, '1/3/18', '2/3/18'),
    (1, 4, 2, '1/12/18', '2/12/18'),
    (3, 4, 7, '1/3/18', '2/3/18'),
    (18, 4, 7, '1/3/18', '2/3/18'),
    (12, 4, 2, '1/4/18', '2/4/18'),
    (11, 4, 3, '1/15/18', '2/15/18'),
    (9, 4, 3, '1/15/18', '2/15/18'),
    (7, 4, 7, '1/1/18', '2/2/18'),
    (4, 4, 3, '1/1/18', '2/2/18'),
    (1, 4, 3, '2/2/17', '3/2/18'),
    (20, 4, 3, '1/3/18', '2/3/18'),
    (1, 4, 2, '1/12/18', '2/12/18'),
    (3, 4, 7, '1/13/18', '2/13/18'),
    (18, 4, 7, '1/13/18', '2/13/18'),
    (12, 4, 2, '1/14/18', '2/14/18'),
    (11, 4, 3, '1/14/18', '2/14/18'),
    (9, 4, 3, '1/15/18', '2/15/18'),
    (7, 4, 7, '1/19/18', '2/19/18'),
    (4, 4, 3, '1/19/18', '2/19/18'),
    (1, 4, 3, '1/22/18', '2/22/18')
;