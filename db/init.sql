.open data.sqlite

-- --------------------------------------------------------

--
-- Table structure for table `boards`
--

DROP TABLE IF EXISTS boards;
CREATE TABLE boards (name VARCHAR(10) PRIMARY KEY,
						desc VARCHAR(24)
					);

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
   id INTEGER,
   board INTEGER,
   thread INT(11) DEFAULT NULL,
   subject VARCHAR(100) DEFAULT NULL,
   email VARCHAR(30) DEFAULT NULL,
   name VARCHAR(35) DEFAULT NULL,
   trip VARCHAR(15) DEFAULT NULL,
   capcode VARCHAR(50) DEFAULT NULL,
   body text,
   time VARCHAR(30),
   num_files INT(11) DEFAULT 0, -- Used for integrity checks, NOT redundant
   --`filehash` text CHARACTER SET ascii
   PRIMARY KEY (id, board)
);

-- --------------------------------------------------------

--
-- Table structure for table `files`
--
 
DROP TABLE IF EXISTS files;
CREATE TABLE files (
   id INTEGER PRIMARY KEY,
   name TEXT,
   post INTEGER NOT NULL,
   board INTEGER NOT NULL,
   path text
);
