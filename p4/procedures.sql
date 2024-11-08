-- Procedure 1: Main procedure for adding a reservation --
CREATE PROCEDURE dbo.AddReservation
    @VenueID INT,
    @Date DATE,
    @StartTime TIME,
    @EndTime TIME,
    @NumberOfGuests INT,
    @CatererID INT = NULL,
    @OrganizerID INT,
    @CustomerID INT,
    -- Optional party parameters --
    @AddParty BIT = 0,
    @PartyType NVARCHAR(255) = NULL,
    @PartyDescription NVARCHAR(MAX) = NULL
AS
BEGIN
    -- Check if venue exists --
    IF NOT EXISTS (SELECT 1 FROM Venue WHERE venue_id = @VenueID)
        THROW 50001, 'Invalid venue ID.', 1;

    -- Check venue operating hours --
    IF dbo.IsWithinVenueHours(@VenueID, @StartTime, @EndTime) = 0
        THROW 50002, 'Reservation time is outside venue operating hours.', 1;

    -- Check for scheduling conflicts --
    IF EXISTS (SELECT 1 FROM dbo.ListOverlappingReservations(@VenueID, @Date, @StartTime, @EndTime))
        THROW 50003, 'This time slot conflicts with an existing reservation.', 1;

    -- If caterer is provided, check compatibility --
    IF @CatererID IS NOT NULL AND 
        NOT EXISTS (SELECT 1 FROM dbo.ListCaterersNearThisVenue(@VenueID) WHERE caterer_id = @CatererID)
        THROW 50004, 'Selected caterer is not compatible with this venue.', 1;

    -- Check venue capacity --
    DECLARE @MaxCapacity INT
    SELECT @MaxCapacity = max_capacity FROM Venue WHERE venue_id = @VenueID
    IF @NumberOfGuests > @MaxCapacity
        THROW 50005, 'Number of guests exceeds venue capacity.', 1;

    -- Generate new booking_id --
    DECLARE @BookingID INT
    SELECT @BookingID = ISNULL(MAX(booking_id), 1000) + 1 FROM Reservation

    -- Insert reservation --
    INSERT INTO Reservation (
        booking_id, date, number_of_guests, start_time, end_time,
        venue_id, organizer_id, caterer_id, customer_id
    )
    VALUES (
        @BookingID, @Date, @NumberOfGuests, @StartTime, @EndTime,
        @VenueID, @OrganizerID, @CatererID, @CustomerID
    )

    -- If party details provided, add party --
    IF @AddParty = 1 AND @PartyType IS NOT NULL
    BEGIN
        -- Generate party_id --
        DECLARE @PartyID INT
        SELECT @PartyID = ISNULL(MAX(party_id), 0) + 1 
        FROM Party 
        WHERE booking_id = @BookingID

        INSERT INTO Party (booking_id, party_id, type, description)
        VALUES (@BookingID, @PartyID, @PartyType, @PartyDescription)
    END

    -- Return the booking_id and party_id (if applicable) --
    SELECT @BookingID AS booking_id, 
            CASE WHEN @AddParty = 1 THEN @PartyID ELSE NULL END AS party_id
END;
GO

--Procedure 2: Insert party decorations using booking_id
CREATE PROCEDURE AddDecorToParty
    @BookingID INT,
    @PartyDecorDescription NVARCHAR(MAX)
AS
BEGIN
    DECLARE @PartyID INT;

    SELECT @PartyID = party_id FROM Party WHERE booking_id = @BookingID;

    IF NOT EXISTS (SELECT booking_id FROM Reservation WHERE booking_id = @BookingID)
    BEGIN
        RAISERROR('This booking does not exist', 11, 2);
        RETURN;
    END
    ELSE IF @PartyID IS NULL 
    BEGIN
        RAISERROR('This venue does not have existing party', 11, 1);
        RETURN;
    END

    INSERT INTO Party_Decorations(booking_id, party_id, [description]) VALUES (@BookingID, @PartyID, @PartyDecorDescription);
END;

--Procedure 3: Add Party to existing Reservation
IF EXISTS (SELECT * FROM sys.procedures WHERE name = 'AddPartyToReservation')
    DROP PROCEDURE dbo.AddPartyToReservation
GO

CREATE PROCEDURE dbo.AddPartyToReservation
    @BookingID INT,
    @PartyType NVARCHAR(255),
    @PartyDescription NVARCHAR(MAX) = NULL,
    @GuestOfHonorName NVARCHAR(255) = NULL
AS
BEGIN
    -- Check if reservation exists
    IF NOT EXISTS (SELECT 1 FROM Reservation WHERE booking_id = @BookingID)
        THROW 50001, 'This booking does not exist.', 1;

    -- Check if party already exists for this reservation
    IF EXISTS (SELECT 1 FROM Party WHERE booking_id = @BookingID)
        THROW 50002, 'A party already exists for this reservation.', 1;

    -- Validate party type
    IF NOT EXISTS (
        SELECT 1 WHERE @PartyType IN (
            'Graduation', 'Wedding', 'Corporate', 'Birthday', 
            'Quinceañera', 'Holiday', 'Baby Shower', 'Misc', 
            'Anniversary'
        )
    )
        THROW 50003, 'Invalid party type. Please check allowed party types.', 1;

    -- Generate party_id
    DECLARE @PartyID INT;
    SELECT @PartyID = ISNULL(MAX(party_id), 0) + 1 
    FROM Party 
    WHERE booking_id = @BookingID;

    -- Insert party record
    INSERT INTO Party (booking_id, party_id, type, description)
    VALUES (@BookingID, @PartyID, @PartyType, @PartyDescription);

    -- Add guest of honor if provided
    IF @GuestOfHonorName IS NOT NULL
    BEGIN
        INSERT INTO Party_GuestOfHonor (booking_id, party_id, name)
        VALUES (@BookingID, @PartyID, @GuestOfHonorName);
    END

    -- Return the created party details
    SELECT 
        p.booking_id,
        p.party_id,
        p.type,
        p.description AS party_description,
        pgh.name AS guest_of_honor
    FROM Party p
    LEFT JOIN Party_GuestOfHonor pgh 
        ON p.booking_id = pgh.booking_id 
        AND p.party_id = pgh.party_id
    WHERE p.booking_id = @BookingID 
    AND p.party_id = @PartyID;
END;
GO