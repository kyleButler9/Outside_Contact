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
    INSERT INTO Contacts(org,%s)
    VALUES(%s);
    """
    updateContact = \
    """
    UPDATE Contacts
    %s
    WHERE contact_id=%s;
    """
    getContact = \
    """
    SELECT c.name,o.name,c.email,c.phone,c.notes,c.contact_id
    FROM Contacts c
    INNER JOIN Organizations o ON c.org=o.org_id
    """
    getContactID = \
    """
    SELECT c.name,o.name,c.email,c.phone,c.notes
    FROM Contacts c
    INNER JOIN Organizations o ON c.org=o.org_id
    """
class Comms:
    insertCommsLog=\
    """
    INSERT INTO Communications(contact,dt,notes)
    VALUES(%s,%s,%s);
    """
    getMostRecentLog=\
    """
    SELECT dt,notes
    FROM Communications
    WHERE contact = %s
    ORDER BY dt desc
    LIMIT 1;
    """
    getNextLog=\
    """
    SELECT dt,notes
    FROM Communications
    WHERE contact = %s
    AND dt < %s
    ORDER BY dt desc
    LIMIT 1;
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
    INSERT INTO Contacts(name,email,org)
    VALUES('K. Butler','kbutler@pcs4people.org',
            (SELECT org_id from Organizations
                WHERE name = 'pcsforpeople')),
        ('R. P.','rp@pcs4people.org',
            (SELECT org_id from Organizations
                WHERE name = 'pcsforpeople'))
    """,
    )
    dropTablesCommands =(
    """
    DROP TABLE Distributions;
    """,
    """
    DROP TABLE Processing;
    """,
    """
    DROP TABLE Requests;
    """,
    """
    DROP TABLE Communications;
    """,
    """
    DROP TABLE Contacts;
    """,
    """
    DROP TABLE Organizations;
    """,
    )
