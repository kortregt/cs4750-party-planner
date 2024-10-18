CREATE DATABASE PartyPlanningDB;
GO
USE PartyPlanningDB;
GO

-- TABLE CREATION --

-- Venue table --
CREATE TABLE Venue (
    venue_id INT PRIMARY KEY,
    name NVARCHAR(255),
    location NVARCHAR(255),
    cost DECIMAL(10, 2),
    max_capacity INT,
    open_time TIME,
    close_time TIME
);

-- Venue_amenities table --
CREATE TABLE Venue_amenities (
    venue_id INT,
    amenity NVARCHAR(255),
    CONSTRAINT PK_Venue_amenities PRIMARY KEY (venue_id, amenity),
    CONSTRAINT FK_Venue_amenities_Venue FOREIGN KEY (venue_id) REFERENCES Venue(venue_id),
    CONSTRAINT CHK_Venue_Amenities CHECK (amenity IN ('Dressing Room', 'Kitchen', 'Projector/Screen', 'Stage'))
);

-- Customer table --
CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    name NVARCHAR(255),
    phone_number NVARCHAR(12),
    email NVARCHAR(255)
);

-- Organizer table --
CREATE TABLE Organizer (
    organizer_id INT PRIMARY KEY,
    name NVARCHAR(255),
    email NVARCHAR(255),
    phone_number NVARCHAR(12),
    commission DECIMAL(10, 2)
);

-- Staff table --
CREATE TABLE Staff (
    employee_id INT PRIMARY KEY,
    name NVARCHAR(255),
    role NVARCHAR(255),
    wage DECIMAL(5, 2),
    CONSTRAINT CHK_Staff_Role CHECK (role IN ('Cleaning', 'Decorator', 'IT', 'Photography', 'Cleaner'))
);

-- Caterer table --
CREATE TABLE Caterer (
    caterer_id INT PRIMARY KEY,
    business_name NVARCHAR(255),
    location NVARCHAR(255),
    cuisine NVARCHAR(255),
    phone_number NVARCHAR(12),
    price_per_order DECIMAL(5, 2),
    needs_kitchen BIT
);

-- Reservation table --
CREATE TABLE Reservation (
    booking_id INT PRIMARY KEY,
    date DATE,
    number_of_guests INT,
    start_time TIME,
    end_time TIME,
    venue_id INT,
    organizer_id INT,
    caterer_id INT,
    customer_id INT,
    CONSTRAINT FK_Reservation_Venue FOREIGN KEY (venue_id) REFERENCES Venue(venue_id),
    CONSTRAINT FK_Reservation_Organizer FOREIGN KEY (organizer_id) REFERENCES Organizer(organizer_id),
    CONSTRAINT FK_Reservation_Caterer FOREIGN KEY (caterer_id) REFERENCES Caterer(caterer_id),
    CONSTRAINT FK_Reservation_Customer FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Party table --
CREATE TABLE Party (
    booking_id INT,
    party_id INT,
    type NVARCHAR(255),
    description NVARCHAR(MAX),
    CONSTRAINT PK_Party PRIMARY KEY (booking_id, party_id),
    CONSTRAINT FK_Party_Reservation FOREIGN KEY (booking_id) REFERENCES Reservation(booking_id),
    CONSTRAINT CHK_Party_Type CHECK (type IN ('Graduation', 'Wedding', 'Corporate', 'Birthday', 'Quinceañera', 'Holiday', 'Baby Shower', 'Misc', 'Anniversary'))
);

-- Party_Decorations table --
CREATE TABLE Party_Decorations (
    decoration_id INT IDENTITY(1,1) PRIMARY KEY,
    booking_id INT,
    party_id INT,
    description NVARCHAR(MAX),
    CONSTRAINT FK_Party_Decorations_Party FOREIGN KEY (booking_id, party_id) REFERENCES Party(booking_id, party_id)
);

-- Party_GuestOfHonor table --
CREATE TABLE Party_GuestOfHonor (
    guest_id INT IDENTITY(1,1) PRIMARY KEY,
    booking_id INT,
    party_id INT,
    name NVARCHAR(255),
    CONSTRAINT FK_Party_GuestOfHonor_Party FOREIGN KEY (booking_id, party_id) REFERENCES Party(booking_id, party_id)
);

-- Performers table --
CREATE TABLE Performers (
    performer_id INT PRIMARY KEY,
    cost DECIMAL(10, 2),
    name NVARCHAR(255),
    email NVARCHAR(255),
    type NVARCHAR(255)
);

-- Reservation_Staff junction table --
CREATE TABLE Reservation_Staff (
    booking_id INT,
    staff_id INT,
    CONSTRAINT PK_Reservation_Staff PRIMARY KEY (booking_id, staff_id),
    CONSTRAINT FK_Reservation_Staff_Reservation FOREIGN KEY (booking_id) REFERENCES Reservation(booking_id),
    CONSTRAINT FK_Reservation_Staff_Staff FOREIGN KEY (staff_id) REFERENCES Staff(employee_id)
);

-- Reservation_Performers junction table --
CREATE TABLE Reservation_Performers (
    booking_id INT,
    performer_id INT,
    CONSTRAINT PK_Reservation_Performers PRIMARY KEY (booking_id, performer_id),
    CONSTRAINT FK_Reservation_Performers_Reservation FOREIGN KEY (booking_id) REFERENCES Reservation(booking_id),
    CONSTRAINT FK_Reservation_Performers_Performers FOREIGN KEY (performer_id) REFERENCES Performers(performer_id)
);


-- DATA INSERTION -- 

-- INSERT statements for Customer table --
INSERT INTO Customer (customer_id, name, phone_number, email) VALUES
(352, N'Minyoung Lee', N'434-123-4555', N'young@aol.com'),
(497, N'Henry Cutright', N'434-123-8777', N'cutwrong@gmail.com'),
(101, N'Haley Fitch', N'434-123-1222', N'fitchhaley@aol.com'),
(683, N'Afreen Haq', N'434-124-1233', N'afreen@yahoo.com'),
(122, N'Linda Mu', N'434-125-1323', N'mu.linda@email.com'),
(761, N'Neal Langhorne', N'434-126-1333', N'langhorneN@gmail.com'),
(580, N'Kelly Gu', N'434-127-1444', N'gukelly@outlook.com'),
(800, N'Grant Sweeney', N'434-128-1555', N'sweeney@outlook.com'),
(777, N'Daniel Nedialkov', N'434-129-2333', N'nedialkovdaniel@aol.com'),
(780, N'Ian Douglas', N'434-130-2555', N'douglass_business@gmail.com'),
(294, N'Emmit James', N'434-131-4567', N'emmitjames@email.com'),
(874, N'Olivia Seto', N'434-132-3444', N'olivia_email@gmail.com'),
(336, N'Sophia Wang', N'434-133-3588', N'wsophia456@aol.com'),
(917, N'Allie Kim', N'434-134-3888', N'kim.a123@gmail.com'),
(299, N'Saarthak Gupta', N'434-135-4888', N'SaarthakG@aol.com'),
(583, N'Glory Gurrola', N'434-136-9099', N'glory_g@outlook.com'),
(548, N'Eva Terry', N'434-137-8088', N'evaterryemail@outlook.com'),
(260, N'Alex Suh', N'434-138-8976', N'alex_s@gmail.com'),
(479, N'Katilyn Song', N'434-139-9333', N'song_k123@gmail.com'),
(533, N'Hieu Vu', N'434-140-3553', N'HieuVu678@outlook.com'),
(576, N'Tyler Kim', N'434-141-3773', N'kimTyler@aol.com'),
(70, N'Nachiket Gusani', N'434-142-9887', N'GusaniN@email.com'),
(668, N'Lauren Marshall', N'434-143-3777', N'MarshallBusiness@email.com'),
(190, N'Rahul Andurkar', N'434-144-2222', N'AndurkarR@gmail.com'),
(448, N'Wright Quist', N'434-145-8888', N'WrightQ@gmail.com'),
(41, N'Peter Tessier', N'434-146-6444', N'tessierbusiness@gmail.com'),
(246, N'Farhan Khan', N'434-147-4444', N'farhanaccount@aol.com'),
(999, N'Jiayu Li', N'434-148-7771', N'JiayuL@email.com'),
(67, N'Tu-Yen Dang', N'434-149-3334', N'Tu-Yen456@email.com'),
(100, N'Vaughn Scott', N'434-150-7755', N'scottv@email.com'),
(96, N'Ethan Stokey', N'434-151-5577', N'stokey_ethan@yahoo.com'),
(232, N'Angela Hong', N'434-152-4555', N'hongangela@email.com'),
(6, N'Phi Lu', N'434-153-5666', N'phi_lu123@yahoo.com'),
(157, N'Betsy Altenburger', N'434-154-6777', N'altenburger.betsy@gmail.com');

-- INSERT statements for Venue table --
INSERT INTO Venue (venue_id, name, location, cost, max_capacity, open_time, close_time) VALUES
(319, N'Rainbow Room', N'Richmond', 800.00, 25, '12:00', '18:00'),
(671, N'Blue Hall', N'Suffolk', 4500.00, 250, '09:00', '18:00'),
(975, N'Kalimari Court', N'Richmond', 1100.00, 60, '11:00', '18:00'),
(387, N'Oceanic Venue', N'Virginia Beach', 900.00, 75, '11:00', '19:00'),
(811, N'The Ballroom', N'D.C.', 9000.00, 320, '10:00', '21:00'),
(650, N'Paradise Venue', N'Virginia Beach', 6500.00, 300, '09:00', '21:00'),
(916, N'Cloudtop Cabin', N'Spotsylvania', 750.00, 25, '12:00', '19:00'),
(83, N'Fine Arts Hall', N'D.C.', 7000.00, 325, '09:00', '21:00'),
(970, N'Luigi Center', N'Suffolk', 500.00, 30, '12:00', '18:00'),
(278, N'Toad''s Party Room', N'Norfolk', 650.00, 55, '12:00', '19:00'),
(913, N'Royal Room', N'Suffolk', 700.00, 40, '11:00', '19:00'),
(607, N'Riverside Park Center', N'Richmond', 3400.00, 115, '11:00', '21:00'),
(84, N'Sunset Wilds Club', N'Spotsylvania', 900.00, 75, '11:00', '23:00'),
(473, N'Daisy Spot', N'D.C.', 800.00, 55, '11:00', '20:00'),
(459, N'Sky Garden Loft', N'Norfolk', 4000.00, 200, '10:00', '21:00'),
(706, N'Maple Ballroom', N'Caroline County', 1200.00, 150, '11:00', '22:00'),
(752, N'Ribbon Road House', N'Spotsylvania', 900.00, 70, '11:00', '17:00'),
(718, N'Boo''s House', N'Richmond', 2000.00, 175, '14:00', '23:00'),
(762, N'Sunshine Spot', N'Virginia Beach', 3500.00, 250, '12:00', '21:00'),
(145, N'Dolphin Shoals Spot', N'Virginia Beach', 4000.00, 225, '12:00', '20:00'),
(899, N'Electrodome', N'Richmond', 15000.00, 500, '11:00', '23:00'),
(925, N'Bone-Dry Club', N'Fairfax', 2000.00, 190, '14:00', '23:00'),
(641, N'Sweet Sweet Spot', N'Farmville', 800.00, 175, '10:00', '18:00'),
(39, N'Coconut Mall Court', N'Virginia Beach', 500.00, 70, '12:00', '19:00'),
(808, N'Moonview Venue', N'Norfolk', 980.00, 55, '11:00', '20:00'),
(550, N'Music Park Hall', N'Farmville', 700.00, 75, '12:00', '18:00'),
(10, N'Koopa Cape Hall', N'Virginia Beach', 1500.00, 100, '11:00', '18:00'),
(967, N'The Castle', N'Virginia Beach', 3600.00, 200, '10:00', '19:00'),
(444, N'New York Minute', N'Farmville', 5000.00, 265, '10:00', '19:00'),
(994, N'Tick Tock Clock', N'Suffolk', 500.00, 30, '12:00', '22:00'),
(361, N'Peach Palace', N'Suffolk', 11500.00, 350, '11:00', '23:00');

-- INSERT statements for Venue_amenities table --
INSERT INTO Venue_amenities (venue_id, amenity) VALUES
(387, N'Dressing Room'),
(387, N'Kitchen'),
(975, N'Projector/Screen'),
(671, N'Kitchen'),
(671, N'Dressing Room'),
(650, N'Stage'),
(278, N'Stage'),
(641, N'Kitchen'),
(361, N'Kitchen'),
(361, N'Dressing Room'),
(361, N'Stage'),
(913, N'Dressing Room'),
(607, N'Kitchen'),
(607, N'Dressing Room'),
(899, N'Stage'),
(84, N'Stage'),
(925, N'Stage'),
(762, N'Kitchen'),
(145, N'Kitchen'),
(145, N'Dressing Room'),
(550, N'Stage'),
(994, N'Projector/Screen'),
(444, N'Dressing Room'),
(967, N'Kitchen'),
(967, N'Dressing Room'),
(459, N'Kitchen'),
(459, N'Dressing Room'),
(459, N'Stage'),
(811, N'Kitchen'),
(811, N'Dressing Room'),
(970, N'Projector/Screen'),
(706, N'Dressing Room'),
(808, N'Kitchen');

-- INSERT statements for Organizer table --
INSERT INTO Organizer (organizer_id, name, email, phone_number, commission) VALUES
(6000, N'Princess Peach', N'toadstool@royalty.com', N'804-345-1200', 2000.00),
(6070, N'Diddey Kong', N'annoyingmonkey@gmail.com', N'804-346-1220', 500.00),
(6140, N'Cranky Kong', N'strictkong@business.com', N'804-347-1400', 1230.00),
(6210, N'Captain Toad', N'CaptianToad@business.com', N'804-348-1240', 305.00),
(6280, N'Toadette', N'Toadette@outlook.com', N'804-349-2300', 450.00),
(6350, N'Tiny Kong', N'coolkong@email.com', N'804-350-3880', 700.00),
(6420, N'Funky Kong', N'funnface@gmail.com', N'804-351-8990', 1000.00),
(6490, N'Chunky Kong', N'lift4you@outlook.com', N'804-352-345', 1200.00),
(6560, N'Mario', N'ogplumber@outlook.com', N'804-353-3333', 1600.00),
(6630, N'Luigi', N'notmario@gmail.com', N'804-354-3777', 1700.00),
(6700, N'Wario', N'betterthanmario@gmail.com', N'804-355-4555', 1000.00),
(6770, N'Waluigi', N'upsidedownL@gmail.com', N'804-356-4554', 1000.00),
(6840, N'Bowser', N'partycrasher@evil.com', N'804-357-6799', 5000.00),
(6910, N'Donkey Kong', N'goodmonkey@gmail.com', N'804-358-6700', 1300.00),
(6980, N'Rosalina', N'galaxygirl@gmail.com', N'804-359-3399', 2300.00),
(7050, N'Princess Daisy', N'powerprincess@gmail.com', N'804-360-3444', 1900.00),
(7120, N'Pauline', N'mayorPauline@outlook.com', N'804-361-3555', 900.00),
(7190, N'Yoshi', N'lovesfruits@gmail.com', N'804-362-3666', 600.00),
(7260, N'King Boo', N'spookyboo@outlook.com', N'804-363-3777', 1200.00),
(7330, N'Cappy', N'hatbrother@outlook.com', N'804-364-4555', 2300.00),
(7400, N'Tiara', N'hatsister@outlook.com', N'804-365-4666', 2500.00),
(7470, N'Toadsworth', N'marioparty@gmail.com', N'804-366-4777', 3000.00),
(7540, N'Blue Yoshi', N'egghatcher@email.com', N'804-367-9900', 800.00),
(7610, N'Yellow Yoshi', N'flowerpower@gmail.com', N'804-368-8877', 780.00),
(7680, N'Koopa Kid', N'oldenoughtowork@email.com', N'804-369-8666', 600.00),
(7750, N'Red Yoshi', N'dinosaur@gmail.com', N'804-370-6888', 900.00),
(7820, N'Mii', N'mii_and_wii@business.com', N'804-371-6777', 760.00),
(7890, N'Looma', N'starpower@gmail.com', N'804-372-5999', 450.00),
(7960, N'Petey Piranha', N'crankypiranha@gmail.com', N'804-373-5888', 600.00),
(8030, N'Koopa Troopa', N'blueshell@outlook.com', N'804-374-4888', 800.00),
(8100, N'Assistant Boo', N'noflashlights@email.com', N'804-375-3777', 900.00),
(8170, N'Kamek', N'evilwitch@gmail.com', N'804-376-3444', 760.00);

-- INSERT statements for Staff table --
INSERT INTO Staff (employee_id, name, role, wage) VALUES
(5000, N'Cheep Cheep', N'Cleaning', 12.00),
(5060, N'Red Toad', N'Decorator', 20.00),
(5090, N'Green Toad', N'Decorator', 20.00),
(5140, N'Blue Toad', N'Decorator', 18.00),
(5185, N'Purple Toad', N'Decorator', 19.00),
(5230, N'Glasses Toad', N'IT', 20.00),
(5275, N'Lakitu 1', N'Photography', 30.00),
(5320, N'Lakitu 2', N'Photography', 50.00),
(5365, N'Lochlady 1', N'Decorator', 30.00),
(5410, N'Lochlady 2', N'Cleaner', 20.00),
(5455, N'New Donker', N'IT', 12.00),
(5500, N'Bonnetter', N'Photography', 20.00),
(5545, N'Pink Bubblainer', N'Cleaner', 12.00),
(5590, N'Blue Bubblainer', N'Cleaner', 12.00),
(5635, N'Shiverian', N'Cleaning', 11.00),
(5680, N'Shiverian', N'IT', 15.00),
(5725, N'Wiggler', N'Decorator', 20.00),
(5770, N'Bob-omb', N'Cleaner', 10.00),
(5815, N'Pink Bob-omb', N'IT', 12.00),
(5860, N'Shy Guy', N'Cleaner', 11.00),
(5905, N'Blooper', N'Decorator', 14.00),
(5950, N'Bullet Bill', N'Cleaner', 10.00),
(5995, N'Pirhana Plant', N'IT', 12.00),
(6040, N'Chain Chomp', N'IT', 13.00),
(6085, N'Paratroopa', N'Photography', 20.00),
(6130, N'Paragoomba', N'Photography', 18.00),
(6175, N'Fly Guy', N'Photography', 22.00),
(6220, N'Bully', N'Cleaner', 12.00),
(6265, N'Boo', N'Cleaner', 14.00),
(6310, N'Hammer Bro', N'IT', 16.00),
(6355, N'Thwomp', N'Decorator', 12.00);

-- INSERT statements for Caterer table --
INSERT INTO Caterer (caterer_id, business_name, location, cuisine, phone_number, price_per_order, needs_kitchen) VALUES
(99, N'Merry Mushroom', N'Richmond', N'Italian', N'804-123-4561', 20.00, 0),
(100, N'Seafood Surfers', N'Richmond', N'Seafood', N'804-234-5672', 34.00, 1),
(101, N'Tostarena Toasts', N'Norfolk', N'Tex-Mex', N'757-123-4565', 23.00, 1),
(102, N'Luigi''s Ghost Chefs', N'Norfolk', N'Italian', N'757-123-5555', 36.00, 1),
(103, N'Fire Flower Roasters', N'Farmville', N'Grilled', N'434-233-1222', 40.00, 0),
(104, N'Merry Mushroom', N'Farmville', N'Italian', N'434-322-2111', 22.00, 0),
(105, N'Delfino Delivery', N'Richmond', N'Italian', N'804-321-1231', 18.00, 0),
(106, N'Gusy Garden Greens', N'Suffolk', N'Salads', N'631-299-2199', 19.00, 0),
(107, N'Pianta Authentic Cuisine', N'Caroline County', N'Island', N'804-120-1200', 30.00, 0),
(108, N'Sirena Seafood', N'Richmond', N'Seafood', N'804-130-1300', 40.00, 1),
(109, N'Koopa Kooking', N'Richmond', N'Seafood', N'804-140-1400', 18.00, 0),
(110, N'Royal Catering', N'Farmville', N'Plated Meal', N'434-112-1112', 42.00, 1),
(111, N'Seafood Surfers', N'Suffolk', N'Seafood', N'757-123-4441', 36.00, 1),
(112, N'Merry Mushroom', N'D.C', N'Italian', N'771-700-1113', 25.00, 0),
(113, N'Galaxy Cooks', N'D.C', N'Plated Meal', N'771-711-8222', 31.00, 1),
(114, N'Ricco Harbor Foods', N'D.C', N'Seafood', N'771-611-1222', 44.00, 0),
(115, N'Koopa Kooking', N'Virginia Beach', N'Burgers', N'757-822-1112', 16.00, 0),
(116, N'Cool Mountain Cuisine', N'Farmville', N'Salads', N'434-133-1882', 17.00, 0),
(117, N'Penguin Catering', N'Farmville', N'Salads', N'434-133-3444', 20.00, 0),
(118, N'Shiveria Delivery', N'D.C', N'Pastries', N'771-008-1299', 13.00, 0),
(119, N'Fine Dining', N'Caroline County', N'Plated Meal', N'804-150-1600', 38.00, 1),
(120, N'Fancy Creations', N'Richmond', N'Plated Meal', N'804-160-1700', 44.00, 1),
(121, N'Volcano Cooking', N'D.C', N'Grilled', N'771-211-7402', 32.00, 0),
(122, N'Tall Mountain Catering', N'Richmond', N'Vegetarian', N'804-210-2111', 28.00, 0),
(123, N'Noki Bay Seafood', N'Virginia Beach', N'Seafood', N'757-392-2484', 45.00, 1),
(124, N'Volbolo Chefs', N'Farmville', N'Soups', N'434-299-1629', 24.00, 1),
(125, N'Merry Mushroom', N'Virginia Beach', N'Italian', N'757-144-4411', 22.00, 0),
(126, N'Merry Mushroom', N'Fairfax', N'Italian', N'703-665-4555', 26.00, 0),
(127, N'Fancy Creations', N'Fairfax', N'Plated Meal', N'703-554-5678', 32.00, 1),
(128, N'Galaxy Cooks', N'Fairfax', N'Plated Meal', N'703-555-3333', 28.00, 1),
(129, N'Fine Dining', N'D.C', N'Plated Meal', N'771-133-1882', 50.00, 1),
(132, N'Volcano Cooking', N'Norfolk', N'Grilled', N'757-003-2811', 30.00, 0),
(142, N'Royal Catering', N'Suffolk', N'Plated Meal', N'757-101-1112', 38.00, 1),
(145, N'Shiveria Delivery', N'Suffolk', N'Pastries', N'757-872-1209', 15.00, 0),
(147, N'Delfino Delivery', N'Spotsylvania', N'Italian', N'540-344-2810', 18.00, 0);

-- INSERT statements for Performers table --
INSERT INTO Performers (performer_id, cost, name, email, type) VALUES
(2114, 250.00, N'Balloon Boo', N'booballons@email.com', N'Clown'),
(2123, 900.00, N'Tostaerna Band', N'maracasandmore@gmail.com', N'Mariachi'),
(2132, 300.00, N'Pauline', N'mayorPauline@outlook.com', N'Pop Singer'),
(2141, 700.00, N'Birdo', N'pink_music@gmail.com', N'DJ'),
(2150, 300.00, N'Cheep Cheep Show', N'cheepclowns@email.com', N'Clown'),
(2159, 800.00, N'Lochlady Singers', N'waterperformers@gmail.com', N'Singers'),
(2168, 900.00, N'Koopa Racers', N'koopabreakdance@gmail.com', N'Dancers'),
(2177, 350.00, N'Stack of Goombas', N'goombastack@outlook.com', N'Jugglers'),
(2186, 400.00, N'Boo Band', N'spooky_band@yahoo.com', N'Band'),
(2195, 500.00, N'Steam Gardener', N'robotmusic@aol.com', N'DJ'),
(2204, 600.00, N'Jazzy Jaxis', N'jazzyjaxi@gmail.com', N'Jazz Band'),
(2213, 250.00, N'Piranha Plants', N'singingplants@yahoo.com', N'Band'),
(2222, 550.00, N'Hotheads', N'flamingdancers@gmail.com', N'Dancers'),
(2231, 500.00, N'Chill Bullies', N'coldpush@gmail.com', N'Band'),
(2240, 900.00, N'Kameks', N'magiclights@email.com', N'Light Show'),
(2249, 400.00, N'Talkatoos', N'talk2you@gmail.com', N'Singers'),
(2258, 600.00, N'Thwomps', N'stompers@email.com', N'Dancers'),
(2267, 1200.00, N'Koopa Paratroopers', N'flyingkoopas@aol.com', N'Acrobats'),
(2276, 150.00, N'Lakitu Booth', N'photolakitus@outlook.com', N'Photo Booth'),
(2285, 250.00, N'Chained Chompers', N'singingchomps@outlook.com', N'Cover Band'),
(2294, 240.00, N'Hammer Bros', N'drumbros@gmail.com', N'Drums'),
(2303, 400.00, N'Moe-Eye Magic', N'moeeyemagic@email.com', N'Magicians'),
(2312, 1200.00, N'Shadow Mario', N'paintmagic@outlook.com', N'Portait Painting'),
(2321, 2000.00, N'Frost Piranha', N'frostfower@email.com', N'Ice Sculpting'),
(2330, 750.00, N'New Donkers', N'jazzbandnewdonk@email.com', N'Jazz Band'),
(2339, 200.00, N'Sphynx', N'questionaire@buisness.com', N'Trivia'),
(2348, 700.00, N'Dry Bones', N'dryboneband@gmail.com', N'Band'),
(2357, 670.00, N'Spinies', N'spinydancers@gmail.com', N'Dancers'),
(2366, 400.00, N'Mad Piano', N'bigboospiano@email.com', N'Musicians'),
(2375, 360.00, N'Mr. Blizzard', N'chillysongs@yahoo.com', N'Singers'),
(2384, 900.00, N'Kong Rappers', N'DK_rap@gmail.com', N'Band');


-- INSERT statements for Reservation table --
INSERT INTO Reservation (booking_id, date, number_of_guests, start_time, end_time, venue_id, organizer_id, caterer_id, customer_id) VALUES
(1001, '2025-05-20', 20, '13:00', '17:00', 319, 7190, 105, 448),
(1003, '2024-10-21', 440, '16:00', '21:00', 899, 6980, NULL, 683),
(1005, '2025-04-21', 50, '14:00', '18:00', 387, 6560, 123, 576),
(1007, '2024-11-23', 25, '14:00', '17:00', 970, 6210, 106, 299),
(1009, '2024-11-23', 38, '15:00', '18:00', 913, 7400, 145, 101),
(1011, '2025-01-13', 45, '12:00', '15:00', 473, 6350, 118, 533),
(1013, '2025-05-20', 55, '14:00', '17:00', 975, 8100, 99, 41),
(1015, '2024-10-31', 40, '16:00', '19:00', 808, 7330, 101, 777),
(1017, '2024-10-31', 100, '19:00', '23:00', 718, 8100, 122, 479),
(1019, '2024-10-31', 290, '18:00', '21:00', 811, 6840, 121, 352),
(1021, '2025-03-12', 40, '13:00', '17:00', 550, 6700, 104, 294),
(1023, '2024-11-09', 45, '13:00', '17:00', 278, 6210, NULL, 122),
(1025, '2024-10-20', 100, '12:00', '16:00', 706, 7050, 107, 780),
(1027, '2024-10-21', 310, '11:00', '15:00', 83, 6910, NULL, 583),
(1029, '2025-06-24', 200, '14:00', '17:00', 361, 6000, 111, 70),
(1031, '2024-10-29', 40, '12:00', '14:00', 975, 7890, 105, 800),
(1033, '2024-12-08', 30, '16:00', '20:00', 994, 7750, NULL, 299),
(1035, '2024-12-11', 20, '13:00', '16:00', 916, 7960, NULL, 999),
(1037, '2024-12-15', 150, '17:00', '20:00', 925, 7190, 126, 479),
(1039, '2025-06-01', 57, '13:00', '16:00', 975, 7120, 99, 299),
(1041, '2025-07-16', 190, '12:00', '18:00', 967, 7680, 123, 6),
(1043, '2024-12-19', 60, '12:00', '15:00', 641, 7610, 124, 157),
(1045, '2025-03-04', 55, '13:00', '16:00', 473, 6210, 112, 874),
(1047, '2025-04-21', 98, '12:00', '17:00', 10, 7470, 115, 336),
(1049, '2025-08-13', 68, '13:00', '16:00', 550, 6910, 103, 122),
(1051, '2024-08-09', 65, '12:00', '17:00', 752, 6770, NULL, 548),
(1053, '2024-05-30', 150, '11:00', '22:00', 706, 8100, 107, 260),
(1055, '2025-01-31', 25, '11:00', '18:00', 473, 7260, 114, 101),
(1057, '2024-12-24', 70, '12:00', '16:00', 39, 7260, NULL, 576),
(1059, '2024-12-31', 500, '17:00', '23:00', 899, 6840, 109, 497),
(1061, '2024-11-20', 50, '11:00', '16:00', 808, 7470, 102, 497),
(1063, '2024-02-14', 16, '12:00', '15:00', 916, 6840, 147, 190),
(1065, '2025-05-25', 140, '14:00', '18:00', 459, 6630, 132, 780),
(1067, '2024-12-12', 110, '14:00', '19:00', 607, 7120, 120, 533),
(1069, '2025-06-20', 90, '14:00', '20:00', 459, 6000, 101, 6);

-- INSERT statements for Party table --
INSERT INTO Party (booking_id, party_id, type, description) VALUES
(1001, 480, N'Graduation', N'Small graduation party for classmates'),
(1005, 400, N'Wedding', N'Small sized wedding'),
(1007, 410, N'Corporate', N'Product Launch party for new software'),
(1011, 399, N'Birthday', N'Lunch Birthday Party'),
(1013, 510, N'Graduation', N'Large graduation party for guest of honor'),
(1009, 422, N'Quinceañera', N'Quinceañera for younger cousin'),
(1015, 611, N'Holiday', N'Halloween Party for friends'),
(1017, 615, N'Holiday', N'Late Night Halloween Party'),
(1019, 618, N'Holiday', N'Large Masquerade Party'),
(1021, 600, N'Birthday', N'Birthday Party for Twins'),
(1023, 701, N'Birthday', N'Children''s Birthday Party'),
(1025, 715, N'Wedding', N'Medium sized wedding'),
(1029, 733, N'Wedding', N'Large wedding with many services'),
(1031, 755, N'Baby Shower', N'Small baby shower for expecting couple'),
(1033, 590, N'Holiday', N'A christmas party for co-workers'),
(1035, 812, N'Baby Shower', N'Afternoon get-together to celebrate baby on the way'),
(1039, 500, N'Corporate', N'Board Meeting'),
(1041, 544, N'Wedding', N'Large wedding with ocean theme'),
(1043, 465, N'Birthday', N'Medium sized birthday party'),
(1045, 901, N'Birthday', N'Kid''s birthday party'),
(1047, 977, N'Misc', N'School Dance'),
(1049, 920, N'Anniversary', N'Parent''s 30th anniversary celebration'),
(1051, 800, N'Misc', N'Engagement Party'),
(1055, 344, N'Birthday', N'Small sized birthday party'),
(1057, 444, N'Holiday', N'Christmas Eve shopping pop-up market'),
(1059, 555, N'Holiday', N'New Year''s Eve Celebration'),
(1061, 230, N'Holiday', N'Thanksgiving lunch and get-together'),
(1063, 250, N'Misc', N'Speed-dating event'),
(1065, 720, N'Graduation', N'Combined graduation party for multiple students who were part of the same organization'),
(1067, 200, N'Holiday', N'Holiday Party and Dinner, Fundraiser'),
(1069, 210, N'Misc', N'Bachelorette Party');

-- INSERT statements for Party_Decorations table --
INSERT INTO Party_Decorations (booking_id, party_id, description) VALUES
(1001, 480, N'Graduation Banner'),
(1005, 400, N'Pastel Colored Flowers'),
(1005, 400, N'Metallic Table Centerpieces'),
(1009, 422, N'Pink Balloons'),
(1013, 510, N'Paper Centerpieces'),
(1019, 618, N'Disco Ball'),
(1021, 600, N'Blue Balloons'),
(1021, 600, N'Green Balloons'),
(1021, 600, N'Birthday Banner'),
(1023, 701, N'Assorted Balloons'),
(1023, 701, N'Balloon Arch'),
(1025, 715, N'Wedding Arch'),
(1029, 733, N'White and Pink Flowers'),
(1029, 733, N'Pearl-white balloons'),
(1029, 733, N'Floral Centerpieces'),
(1041, 544, N'Ocean-themed ornaments'),
(1041, 544, N'blue tablecloth'),
(1043, 465, N'Assorted Balloons'),
(1045, 901, N'Colorful Backdrop'),
(1045, 901, N'Assorted Balloons'),
(1045, 901, N'Birthday Banner'),
(1047, 977, N'Disco Ball'),
(1047, 977, N'Iridescent Table Cloth'),
(1051, 800, N'Confetti'),
(1055, 344, N'Pink Tablecloth'),
(1055, 344, N'Purple Streamers'),
(1057, 444, N'Holiday Lights'),
(1057, 444, N'Blow-Up Santa'),
(1061, 230, N'Fake Fruit Bowl'),
(1061, 230, N'Country Tablecloth'),
(1065, 720, N'Graduation Backdrop'),
(1069, 210, N'Pink Tablecloth'),
(1069, 210, N'Red Balloons'),
(1067, 200, N'Red Tablecloth');

-- INSERT statements for Party_GuestOfHonor table --
INSERT INTO Party_GuestOfHonor (booking_id, party_id, name) VALUES
(1001, 480, N'Vaughn Scott'),
(1001, 480, N'Wright Quist'),
(1001, 480, N'Allie Kim'),
(1005, 400, N'Mr. Kim'),
(1005, 400, N'Ms. Kim'),
(1009, 422, N'Maria Somebody'),
(1013, 510, N'Peter Tessier'),
(1021, 600, N'Tweedle-Dee'),
(1021, 600, N'Tweedle-Dum'),
(1023, 701, N'Little Mu'),
(1025, 715, N'Mr. Douglas'),
(1025, 715, N'Ms. Douglas'),
(1029, 733, N'Mr. Gusani'),
(1029, 733, N'Ms. Gusani'),
(1041, 544, N'Mr. Lu'),
(1041, 544, N'Ms. Lu'),
(1043, 465, N'Best Friend'),
(1045, 901, N'Lil Seto'),
(1047, 977, N'Scholarship Recipient 1'),
(1047, 977, N'Scholarship Recipient 2'),
(1047, 977, N'Scholarship Recipient 3'),
(1049, 920, N'Mr. Mu'),
(1049, 920, N'Ms. Mu'),
(1051, 800, N'Abey'),
(1051, 800, N'Ethan'),
(1055, 344, N'Haley Fitch'),
(1065, 720, N'Ian Douglas'),
(1065, 720, N'Henry Cutright'),
(1065, 720, N'Param Patel'),
(1065, 720, N'Maseel Shah'),
(1065, 720, N'Grant Costello'),
(1065, 720, N'Angela Chung');

-- INSERT statements for Reservation_Staff table --
INSERT INTO Reservation_Staff (booking_id, staff_id) VALUES
(1003, 5815),
(1003, 6310),
(1003, 6040),
(1003, 5770),
(1005, 5365),
(1005, 5410),
(1013, 5905),
(1013, 6040),
(1019, 5455),
(1019, 5635),
(1017, 6265),
(1023, 5060),
(1029, 5320),
(1029, 5950),
(1029, 5365),
(1041, 5905),
(1041, 5590),
(1051, 6175),
(1051, 6220),
(1057, 5060),
(1057, 6220),
(1057, 5860),
(1059, 5815),
(1059, 6355),
(1059, 5725),
(1059, 5590),
(1059, 5060),
(1063, 6040),
(1069, 5275),
(1069, 5545),
(1069, 6040),
(1067, 5680),
(1067, 5950),
(1067, 5770);

-- INSERT statements for Reservation_Performers table --
INSERT INTO Reservation_Performers (booking_id, performer_id) VALUES
(1003, 2141),
(1003, 2186),
(1003, 2195),
(1003, 2231),
(1003, 2357),
(1003, 2348),
(1003, 2276),
(1003, 2132),
(1003, 2240),
(1003, 2222),
(1005, 2159),
(1019, 2195),
(1019, 2285),
(1029, 2159),
(1029, 2240),
(1041, 2321),
(1045, 2114),
(1047, 2195),
(1055, 2339),
(1063, 2204),
(1063, 2276),
(1045, 2177),
(1069, 2267),
(1069, 2222),
(1069, 2132),
(1069, 2357),
(1067, 2321),
(1067, 2339),
(1067, 2276),
(1061, 2276);


--TEN QUERIES BELOW ABOUT USEFUL DATA--

--Find all performers that have not yet been hired--
Select DISTINCT [name] AS [Performers Not Hired Yet], [type] AS [type] FROM Performers P 
WHERE P.performer_id NOT IN (
    SELECT Hired.performer_id   
    FROM Reservation_Performers Hired
);

--Find all Party Organizers who have been hired at least 3 times--
Select O.name, COUNT(O.organizer_id) AS TimesHired FROM 
Reservation R INNER JOIN Organizer O ON R.organizer_id = O.organizer_id GROUP BY O.organizer_id, O.name HAVING COUNT(O.organizer_id) > 2 ORDER BY TimesHired DESC;

--Find the reserved venues listed by popularity--
Select V.name, V.[location], COUNT(V.venue_id) AS TimesReserved FROM 
Venue V INNER JOIN Reservation R ON V.venue_id = R.venue_id GROUP BY V.venue_id, [location], V.name ORDER BY TimesReserved DESC;

--Find which city has the highest average cost of a venue--
Select V.[location], CONVERT(numeric(10,2), AVG(V.cost)) AS AverageCostOfAVenue FROM Venue V GROUP BY V.[location] ORDER BY AverageCostOfAVenue DESC;

--Find which city has the lowest cost of a small venue (meaning less than 100 people capacity)--
Select V.[location], CONVERT(numeric(10,2), AVG(V.cost)) AS AverageCostOfSmallVenue FROM Venue V WHERE V.max_capacity < 100 GROUP BY V.[location] ORDER BY AverageCostOfSmallVenue ASC;

--Find the average duration of wedding parties--
Select AVG(DATEPART(hour, R.end_time) - DATEPART(hour, R.start_time)) AS [Average Duration of Wedding Party (in hours)] FROM Party P JOIN Reservation R ON P.booking_id = R.booking_id WHERE P.[type] = 'Wedding';

--Find the average number of guests per party types--
Select P.type, AVG(number_of_guests) AS [Average Number of Guests] FROM Party P JOIN Reservation R ON P.booking_id = R.booking_id GROUP BY P.type;

--List the information of the performers who have performed at the electrodome--
SELECT [name] AS [Performer Name], [type], cost, email 
FROM Reservation_Performers P2 
INNER JOIN Performers P1 ON P2.performer_id = P1.performer_id 
WHERE P2.booking_id IN
(SELECT R.booking_id FROM Venue V INNER JOIN Reservation R ON V.venue_id = R.venue_id WHERE V.[name] = 'Electrodome');

--List the number of caterers who do not require a kitchen per city--
SELECT C.location, COUNT(C.business_name) FROM Caterer C WHERE C.needs_kitchen = 0 GROUP BY location;

--Find all holiday parties in december that mention christmas in the description and list their venues and dates--
SELECT R.date, R.name, P.type, P.description FROM Party P INNER JOIN (
    SELECT booking_id, V.name, R1.[date] FROM Reservation R1 INNER JOIN Venue V ON R1.venue_id = V.venue_id where DATEPART(month, R1.date) = 12
    ) R 
ON P.booking_id = R.booking_id WHERE P.type = 'Holiday' AND P.[description] LIKE  '%christmas%';
