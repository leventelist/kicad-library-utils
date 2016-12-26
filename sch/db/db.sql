BEGIN TRANSACTION;
CREATE TABLE supplier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    homepage TEXT,
    address TEXT,
    country TEXT,
    city TEXT,
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    portable TEXT,
    fax TEXT
);
CREATE TABLE stock (
    dev_id integer NOT NULL,
    quantity integer DEFAULT 0,
    warn integer DEFAULT 0
);
CREATE TABLE source (
    sup_id integer NOT NULL,
    dev_id integer NOT NULL,
    uprice real DEFAULT 0,
    ppu integer DEFAULT 1,
    ordering_code TEXT,
    comment TEXT
);
CREATE TABLE device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category integer,
    technology TEXT,
    value TEXT,
    value2 TEXT,
    value3 TEXT,
    type TEXT,
    description TEXT,
    documentation TEXT,
    comment TEXT
);
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent integer,
    name TEXT,
    comment TEXT
);
CREATE TABLE "cad_tools" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT,
	`comment`	TEXT
);
INSERT INTO `cad_tools` VALUES (1,'gEDA','good old gEDA');
INSERT INTO `cad_tools` VALUES (2,'KiCad','Brave new KiCad');
CREATE TABLE "cad_data" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`dev_id`	integer NOT NULL,
	`is_default`	integer DEFAULT 1,
	`cad_tool`	INTEGER DEFAULT 2,
	`symbol`	TEXT,
	`pinmap`	TEXT,
	`footprint`	TEXT,
	`mech_model`	TEXT,
	`comment`	TEXT
);
COMMIT;
