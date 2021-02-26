class ContactInfo:
    insertOrg = \
    """
    INSERT INTO Organizations(%s)
    VALUES(%s);
    """
    getOrgs = \
    """
    SELECT name from Organizations
    WHERE name ~* %s;
    """
    insertContact = \
    """
    INSERT INTO Contacts(%s)
    VALUES(%s);
    """
    getContact = \
    """
    SELECT c.name,o.name,c.email,c.phone
    FROM Contacts c
    INNER JOIN Organizations o ON c.org=o.org_id
    WHERE c.name ~* %s,
    AND o.name ~* %s,
    AND c.email ~* %s,
    AND c.phone ~* %s;
    """

class DBAdmin:
    createTableCommands = (
    """
    CREATE TABLE Organizations (
        org_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        phone VARCHAR(20),
        email VARCHAR(100)
    )
    """,
    """
    CREATE TABLE Contacts (
        contact_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        phone VARCHAR(20),
        email VARCHAR(100),
        notes VARCHAR(255),
        org INTEGER NOT NULL,
        FOREIGN KEY (org)
            REFERENCES organizations (org_id)
    )
    """,
    """
    CREATE TABLE Communications (
        communication_id SERIAL PRIMARY KEY,
        contact Integer,
        dt timestamp,
        notes VARCHAR(255),
        FOREIGN KEY (contact)
            references Contacts (contact_id)
    )
    """,
    """
    CREATE TABLE Requests (
        request_id SERIAL PRIMARY KEY,
        org INTEGER,
        contact INTEGER,
        request_date timestamp,
        quantity INTEGER,
        quantityDesktops Integer,
        quantityLaptops Integer,
        quantityHotspots Integer,
        type VARCHAR(100),
        whoNeeds VARCHAR(255),
        addressed Boolean,
        willSupply Boolean,
        notes VARCHAR(255),
        FOREIGN KEY (contact)
            REFERENCES contacts (contact_id),
        FOREIGN KEY (org)
            REFERENCES organizations (org_id)
    )
    """,
    """
    CREATE TABLE Processing (
        order_id SERIAL PRIMARY KEY,
        request Integer,
        quantity INTEGER,
        quantityDesktops Integer,
        quantityLaptops Integer,
        quantityHotspots Integer,
        funder VARCHAR(100),
        FOREIGN KEY (request)
            REFERENCES Requests (request_id)
    )
    """,
    """
    CREATE TABLE Distributions (
        distribution_id SERIAL PRIMARY KEY,
        request Integer,
        quantityDistributed Integer,
        quantityDesktops Integer,
        quantityLaptops Integer,
        quantityHotspots Integer,
        complete Boolean,
        distroEventDate timestamp,
        funder VARCHAR(100),
        notes VARCHAR(255),
        FOREIGN KEY (request)
            REFERENCES Requests (request_id)
    )
    """
    )
    initializeDatabaseCommands=(
    """
    INSERT INTO Organizations(name)
    VALUES('pcsforpeople'),('pcs4ppl')
    """,
    """
    INSERT INTO Contacts(name,email)
    VALUES('K. Butler','kdemo@pcs4people.org'),('R. P.','rdemo@pcs4people.demo')
    """,
    )
