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

class DBAdmin:
    createTableCommands = (
    """
    CREATE TABLE Organizations (
        org_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255),
        phone VARCHAR(20)
        email VARCHAR(100),
    )
    """,
    """
    CREATE TABLE Contacts (
        contact_id SERIAL PRIMARY KEY
        name VARCHAR(255),
        phone VARCHAR(20),
        email VARCHAR(20),
        notes VARCHAR(255),
        org INTEGER,
        FOREIGN KEY (org)
            REFERENCES organizations (org_id)
    )
    """,
    """
    CREATE TABLE Communications (
        communication_id SERIAL PRIMARY KEY,
        contact Integer,
        dt datetime,
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
        request_date datetime,
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
        Grant VARCHAR(100),
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
        distroEventDate datetime,
        Grant VARCHAR(100),
        notes VARCHAR(255),
        FOREIGN KEY (request)
            REFERENCES Requests (request_id)
    )
    """
    )
