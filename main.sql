-- update ITEM_COLLECT
DROP TABLE IF EXISTS ITEM_COLLECT;
CREATE TABLE ITEM_COLLECT (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    PREFIX VARCHAR(20) NOT NULL,
    ITEM_NAME VARCHAR(20) NOT NULL
);