from sqlalchemy import text
from database import engine

def import_data():
    """Import all data into the party planning database"""
    commands = [
        # Customer data
        """
        INSERT INTO Customer (customer_id, name, phone_number, email) VALUES
        (352, 'Minyoung Lee', '434-123-4555', 'young@aol.com'),
        (497, 'Henry Cutright', '434-123-8777', 'cutwrong@gmail.com'),
        (101, 'Haley Fitch', '434-123-1222', 'fitchhaley@aol.com'),
        (683, 'Afreen Haq', '434-124-1233', 'afreen@yahoo.com'),
        (122, 'Linda Mu', '434-125-1323', 'mu.linda@email.com'),
        (761, 'Neal Langhorne', '434-126-1333', 'langhorneN@gmail.com'),
        (580, 'Kelly Gu', '434-127-1444', 'gukelly@outlook.com'),
        (800, 'Grant Sweeney', '434-128-1555', 'sweeney@outlook.com'),
        (777, 'Daniel Nedialkov', '434-129-2333', 'nedialkovdaniel@aol.com'),
        (780, 'Ian Douglas', '434-130-2555', 'douglass_business@gmail.com'),
        (294, 'Emmit James', '434-131-4567', 'emmitjames@email.com'),
        (874, 'Olivia Seto', '434-132-3444', 'olivia_email@gmail.com'),
        (336, 'Sophia Wang', '434-133-3588', 'wsophia456@aol.com'),
        (917, 'Allie Kim', '434-134-3888', 'kim.a123@gmail.com'),
        (299, 'Saarthak Gupta', '434-135-4888', 'SaarthakG@aol.com'),
        (583, 'Glory Gurrola', '434-136-9099', 'glory_g@outlook.com'),
        (548, 'Eva Terry', '434-137-8088', 'evaterryemail@outlook.com'),
        (260, 'Alex Suh', '434-138-8976', 'alex_s@gmail.com'),
        (479, 'Katilyn Song', '434-139-9333', 'song_k123@gmail.com'),
        (533, 'Hieu Vu', '434-140-3553', 'HieuVu678@outlook.com'),
        (576, 'Tyler Kim', '434-141-3773', 'kimTyler@aol.com'),
        (70, 'Nachiket Gusani', '434-142-9887', 'GusaniN@email.com'),
        (668, 'Lauren Marshall', '434-143-3777', 'MarshallBusiness@email.com'),
        (190, 'Rahul Andurkar', '434-144-2222', 'AndurkarR@gmail.com'),
        (448, 'Wright Quist', '434-145-8888', 'WrightQ@gmail.com'),
        (41, 'Peter Tessier', '434-146-6444', 'tessierbusiness@gmail.com'),
        (246, 'Farhan Khan', '434-147-4444', 'farhanaccount@aol.com'),
        (999, 'Jiayu Li', '434-148-7771', 'JiayuL@email.com'),
        (67, 'Tu-Yen Dang', '434-149-3334', 'Tu-Yen456@email.com'),
        (100, 'Vaughn Scott', '434-150-7755', 'scottv@email.com'),
        (96, 'Ethan Stokey', '434-151-5577', 'stokey_ethan@yahoo.com'),
        (232, 'Angela Hong', '434-152-4555', 'hongangela@email.com'),
        (6, 'Phi Lu', '434-153-5666', 'phi_lu123@yahoo.com'),
        (157, 'Betsy Altenburger', '434-154-6777', 'altenburger.betsy@gmail.com');
        """,

        # Venue data
        """
        INSERT INTO Venue (venue_id, name, location, cost, max_capacity, open_time, close_time) VALUES
        (319, 'Rainbow Room', 'Richmond', 800.00, 25, '12:00', '18:00'),
        (671, 'Blue Hall', 'Suffolk', 4500.00, 250, '09:00', '18:00'),
        (975, 'Kalimari Court', 'Richmond', 1100.00, 60, '11:00', '18:00'),
        (387, 'Oceanic Venue', 'Virginia Beach', 900.00, 75, '11:00', '19:00'),
        (811, 'The Ballroom', 'D.C.', 9000.00, 320, '10:00', '21:00'),
        (650, 'Paradise Venue', 'Virginia Beach', 6500.00, 300, '09:00', '21:00'),
        (916, 'Cloudtop Cabin', 'Spotsylvania', 750.00, 25, '12:00', '19:00'),
        (83, 'Fine Arts Hall', 'D.C.', 7000.00, 325, '09:00', '21:00'),
        (970, 'Luigi Center', 'Suffolk', 500.00, 30, '12:00', '18:00'),
        (278, 'Toad''s Party Room', 'Norfolk', 650.00, 55, '12:00', '19:00'),
        (913, 'Royal Room', 'Suffolk', 700.00, 40, '11:00', '19:00'),
        (607, 'Riverside Park Center', 'Richmond', 3400.00, 115, '11:00', '21:00'),
        (84, 'Sunset Wilds Club', 'Spotsylvania', 900.00, 75, '11:00', '23:00'),
        (473, 'Daisy Spot', 'D.C.', 800.00, 55, '11:00', '20:00'),
        (459, 'Sky Garden Loft', 'Norfolk', 4000.00, 200, '10:00', '21:00'),
        (706, 'Maple Ballroom', 'Caroline County', 1200.00, 150, '11:00', '22:00'),
        (752, 'Ribbon Road House', 'Spotsylvania', 900.00, 70, '11:00', '17:00'),
        (718, 'Boo''s House', 'Richmond', 2000.00, 175, '14:00', '23:00'),
        (762, 'Sunshine Spot', 'Virginia Beach', 3500.00, 250, '12:00', '21:00'),
        (145, 'Dolphin Shoals Spot', 'Virginia Beach', 4000.00, 225, '12:00', '20:00'),
        (899, 'Electrodome', 'Richmond', 15000.00, 500, '11:00', '23:00'),
        (925, 'Bone-Dry Club', 'Fairfax', 2000.00, 190, '14:00', '23:00'),
        (641, 'Sweet Sweet Spot', 'Farmville', 800.00, 175, '10:00', '18:00'),
        (39, 'Coconut Mall Court', 'Virginia Beach', 500.00, 70, '12:00', '19:00'),
        (808, 'Moonview Venue', 'Norfolk', 980.00, 55, '11:00', '20:00'),
        (550, 'Music Park Hall', 'Farmville', 700.00, 75, '12:00', '18:00'),
        (10, 'Koopa Cape Hall', 'Virginia Beach', 1500.00, 100, '11:00', '18:00'),
        (967, 'New York Minute', 'Farmville', 5000.00, 265, '10:00', '19:00'),
        (444, 'The Castle', 'Virginia Beach', 3600.00, 200, '10:00', '19:00'),
        (994, 'Tick Tock Clock', 'Suffolk', 500.00, 30, '12:00', '22:00'),
        (361, 'Peach Palace', 'Suffolk', 11500.00, 350, '11:00', '23:00');
        """,

        # Venue amenities
        """
        INSERT INTO Venue_amenities (venue_id, amenity) VALUES
        (387, 'Dressing Room'),
        (387, 'Kitchen'),
        (975, 'Projector/Screen'),
        (671, 'Kitchen'),
        (671, 'Dressing Room'),
        (650, 'Stage'),
        (278, 'Stage'),
        (641, 'Kitchen'),
        (361, 'Kitchen'),
        (361, 'Dressing Room'),
        (361, 'Stage'),
        (913, 'Dressing Room'),
        (607, 'Kitchen'),
        (607, 'Dressing Room'),
        (899, 'Stage'),
        (84, 'Stage'),
        (925, 'Stage'),
        (762, 'Kitchen'),
        (145, 'Kitchen'),
        (145, 'Dressing Room'),
        (550, 'Stage'),
        (994, 'Projector/Screen'),
        (444, 'Dressing Room'),
        (967, 'Kitchen'),
        (967, 'Dressing Room'),
        (459, 'Kitchen'),
        (459, 'Dressing Room'),
        (459, 'Stage'),
        (811, 'Kitchen'),
        (811, 'Dressing Room'),
        (970, 'Projector/Screen'),
        (706, 'Dressing Room'),
        (808, 'Kitchen');
        """,

        # Organizer data
        """
        INSERT INTO Organizer (organizer_id, name, email, phone_number, commission) VALUES
        (6000, 'Princess Peach', 'toadstool@royalty.com', '804-345-1200', 2000.00),
        (6070, 'Diddey Kong', 'annoyingmonkey@gmail.com', '804-346-1220', 500.00),
        (6140, 'Cranky Kong', 'strictkong@business.com', '804-347-1400', 1230.00),
        (6210, 'Captain Toad', 'CaptianToad@business.com', '804-348-1240', 305.00),
        (6280, 'Toadette', 'Toadette@outlook.com', '804-349-2300', 450.00),
        (6350, 'Tiny Kong', 'coolkong@email.com', '804-350-3880', 700.00),
        (6420, 'Funky Kong', 'funnface@gmail.com', '804-351-8990', 1000.00),
        (6490, 'Chunky Kong', 'lift4you@outlook.com', '804-352-345', 1200.00),
        (6560, 'Mario', 'ogplumber@outlook.com', '804-353-3333', 1600.00),
        (6630, 'Luigi', 'notmario@gmail.com', '804-354-3777', 1700.00),
        (6700, 'Wario', 'betterthanmario@gmail.com', '804-355-4555', 1000.00),
        (6770, 'Waluigi', 'upsidedownL@gmail.com', '804-356-4554', 1000.00),
        (6840, 'Bowser', 'partycrasher@evil.com', '804-357-6799', 5000.00),
        (6910, 'Donkey Kong', 'goodmonkey@gmail.com', '804-358-6700', 1300.00),
        (6980, 'Rosalina', 'galaxygirl@gmail.com', '804-359-3399', 2300.00),
        (7050, 'Princess Daisy', 'powerprincess@gmail.com', '804-360-3444', 1900.00),
        (7120, 'Pauline', 'mayorPauline@outlook.com', '804-361-3555', 900.00),
        (7190, 'Yoshi', 'lovesfruits@gmail.com', '804-362-3666', 600.00),
        (7260, 'King Boo', 'spookyboo@outlook.com', '804-363-3777', 1200.00),
        (7330, 'Cappy', 'hatbrother@outlook.com', '804-364-4555', 2300.00),
        (7400, 'Tiara', 'hatsister@outlook.com', '804-365-4666', 2500.00),
        (7470, 'Toadsworth', 'marioparty@gmail.com', '804-366-4777', 3000.00),
        (7540, 'Blue Yoshi', 'egghatcher@email.com', '804-367-9900', 800.00),
        (7610, 'Yellow Yoshi', 'flowerpower@gmail.com', '804-368-8877', 780.00),
        (7680, 'Koopa Kid', 'oldenoughtowork@email.com', '804-369-8666', 600.00),
        (7750, 'Red Yoshi', 'dinosaur@gmail.com', '804-370-6888', 900.00),
        (7820, 'Mii', 'mii_and_wii@business.com', '804-371-6777', 760.00),
        (7890, 'Looma', 'starpower@gmail.com', '804-372-5999', 450.00),
        (7960, 'Petey Piranha', 'crankypiranha@gmail.com', '804-373-5888', 600.00),
        (8030, 'Koopa Troopa', 'blueshell@outlook.com', '804-374-4888', 800.00),
        (8100, 'Assistant Boo', 'noflashlights@email.com', '804-375-3777', 900.00),
        (8170, 'Kamek', 'evilwitch@gmail.com', '804-376-3444', 760.00);
        """
    
        # Staff data
        """
        INSERT INTO Staff (employee_id, name, role, wage) VALUES
        (5000, 'Cheep Cheep', 'Cleaning', 12.00),
        (5060, 'Red Toad', 'Decorator', 20.00),
        (5090, 'Green Toad', 'Decorator', 20.00),
        (5140, 'Blue Toad', 'Decorator', 18.00),
        (5185, 'Purple Toad', 'Decorator', 19.00),
        (5230, 'Glasses Toad', 'IT', 20.00),
        (5275, 'Lakitu 1', 'Photography', 30.00),
        (5320, 'Lakitu 2', 'Photography', 50.00),
        (5365, 'Lochlady 1', 'Decorator', 30.00),
        (5410, 'Lochlady 2', 'Cleaner', 20.00),
        (5455, 'New Donker', 'IT', 12.00),
        (5500, 'Bonnetter', 'Photography', 20.00),
        (5545, 'Pink Bubblainer', 'Cleaner', 12.00),
        (5590, 'Blue Bubblainer', 'Cleaner', 12.00),
        (5635, 'Shiverian', 'Cleaning', 11.00),
        (5680, 'Shiverian', 'IT', 15.00),
        (5725, 'Wiggler', 'Decorator', 20.00),
        (5770, 'Bob-omb', 'Cleaner', 10.00),
        (5815, 'Pink Bob-omb', 'IT', 12.00),
        (5860, 'Shy Guy', 'Cleaner', 11.00),
        (5905, 'Blooper', 'Decorator', 14.00),
        (5950, 'Bullet Bill', 'Cleaner', 10.00),
        (5995, 'Pirhana Plant', 'IT', 12.00),
        (6040, 'Chain Chomp', 'IT', 13.00),
        (6085, 'Paratroopa', 'Photography', 20.00),
        (6130, 'Paragoomba', 'Photography', 18.00),
        (6175, 'Fly Guy', 'Photography', 22.00),
        (6220, 'Bully', 'Cleaner', 12.00),
        (6265, 'Boo', 'Cleaner', 14.00),
        (6310, 'Hammer Bro', 'IT', 16.00),
        (6355, 'Thwomp', 'Decorator', 12.00);
        """,

        # Caterer data
        """
        INSERT INTO Caterer (caterer_id, business_name, location, cuisine, phone_number, price_per_order, needs_kitchen) VALUES
        (99, 'Merry Mushroom', 'Richmond', 'Italian', '804-123-4561', 20.00, false),
        (100, 'Seafood Surfers', 'Richmond', 'Seafood', '804-234-5672', 34.00, true),
        (101, 'Tostarena Toasts', 'Norfolk', 'Tex-Mex', '757-123-4565', 23.00, true),
        (102, 'Luigi''s Ghost Chefs', 'Norfolk', 'Italian', '757-123-5555', 36.00, true),
        (103, 'Fire Flower Roasters', 'Farmville', 'Grilled', '434-233-1222', 40.00, false),
        (104, 'Merry Mushroom', 'Farmville', 'Italian', '434-322-2111', 22.00, false),
        (105, 'Delfino Delivery', 'Richmond', 'Italian', '804-321-1231', 18.00, false),
        (106, 'Gusy Garden Greens', 'Suffolk', 'Salads', '631-299-2199', 19.00, false),
        (107, 'Pianta Authentic Cuisine', 'Caroline County', 'Island', '804-120-1200', 30.00, false),
        (108, 'Sirena Seafood', 'Richmond', 'Seafood', '804-130-1300', 40.00, true),
        (109, 'Koopa Kooking', 'Richmond', 'Seafood', '804-140-1400', 18.00, false),
        (110, 'Royal Catering', 'Farmville', 'Plated Meal', '434-112-1112', 42.00, true),
        (111, 'Seafood Surfers', 'Suffolk', 'Seafood', '757-123-4441', 36.00, true),
        (112, 'Merry Mushroom', 'D.C', 'Italian', '771-700-1113', 25.00, false),
        (113, 'Galaxy Cooks', 'D.C', 'Plated Meal', '771-711-8222', 31.00, true),
        (114, 'Ricco Harbor Foods', 'D.C', 'Seafood', '771-611-1222', 44.00, false),
        (115, 'Koopa Kooking', 'Virginia Beach', 'Burgers', '757-822-1112', 16.00, false),
        (116, 'Cool Mountain Cuisine', 'Farmville', 'Salads', '434-133-1882', 17.00, false),
        (117, 'Penguin Catering', 'Farmville', 'Salads', '434-133-3444', 20.00, false),
        (118, 'Shiveria Delivery', 'D.C', 'Pastries', '771-008-1299', 13.00, false),
        (119, 'Fine Dining', 'Caroline County', 'Plated Meal', '804-150-1600', 38.00, true),
        (120, 'Fancy Creations', 'Richmond', 'Plated Meal', '804-160-1700', 44.00, true),
        (121, 'Volcano Cooking', 'D.C', 'Grilled', '771-211-7402', 32.00, false),
        (122, 'Tall Mountain Catering', 'Richmond', 'Vegetaria', '804-210-2111', 28.00, false),
        (123, 'Noki Bay Seafood', 'Virginia Beach', 'Seafood', '757-392-2484', 45.00, true),
        (124, 'Volbolo Chefs', 'Farmville', 'Soups', '434-299-1629', 24.00, true),
        (125, 'Merry Mushroom', 'Virginia Beach', 'Italia', '757-144-4411', 22.00, false),
        (126, 'Merry Mushroom', 'Fairfax', 'Italia', '703-665-4555', 26.00, false),
        (127, 'Fancy Creations', 'Fairfax', 'Plated Meal', '703-554-5678', 32.00, true),
        (128, 'Galaxy Cooks', 'Fairfax', 'Plated Meal', '703-555-3333', 28.00, true),
        (129, 'Fine Dining', 'D.C', 'Plated Meal', '771-133-1882', 50.00, true),
        (132, 'Volcano Cooking', 'Norfolk', 'Grilled', '757-003-2811', 30.00, false),
        (142, 'Royal Catering', 'Suffolk', 'Plated Meal', '757-101-1112', 38.00, true),
        (145, 'Shiveria Delivery', 'Suffolk', 'Pastries', '757-872-1209', 15.00, false),
        (147, 'Delfino Delivery', 'Spotsylvania', 'Italia', '540-344-2810', 18.00, false);
        """,

        # Performers data
        """
        INSERT INTO Performers (performer_id, cost, name, email, type) VALUES
        (2114, 250.00, 'Balloon Boo', 'booballons@email.com', 'Clown'),
        (2123, 900.00, 'Tostaerna Band', 'maracasandmore@gmail.com', 'Mariachi'),
        (2132, 300.00, 'Pauline', 'mayorPauline@outlook.com', 'Pop Singer'),
        (2141, 700.00, 'Birdo', 'pink_music@gmail.com', 'DJ'),
        (2150, 300.00, 'Cheep Cheep Show', 'cheepclowns@email.com', 'Clown'),
        (2159, 800.00, 'Lochlady Singers', 'waterperformers@gmail.com', 'Singers'),
        (2168, 900.00, 'Koopa Racers', 'koopabreakdance@gmail.com', 'Dancers'),
        (2177, 350.00, 'Stack of Goombas', 'goombastack@outlook.com', 'Jugglers'),
        (2186, 400.00, 'Boo Band', 'spooky_band@yahoo.com', 'Band'),
        (2195, 500.00, 'Steam Gardener', 'robotmusic@aol.com', 'DJ'),
        (2204, 600.00, 'Jazzy Jaxis', 'jazzyjaxi@gmail.com', 'Jazz Band'),
        (2213, 250.00, 'Piranha Plants', 'singingplants@yahoo.com', 'Band'),
        (2222, 550.00, 'Hotheads', 'flamingdancers@gmail.com', 'Dancers'),
        (2231, 500.00, 'Chill Bullies', 'coldpush@gmail.com', 'Band'),
        (2240, 900.00, 'Kameks', 'magiclights@email.com', 'Light Show'),
        (2249, 400.00, 'Talkatoos', 'talk2you@gmail.com', 'Singers'),
        (2258, 600.00, 'Thwomps', 'stompers@email.com', 'Dancers'),
        (2267, 1200.00, 'Koopa Paratroopers', 'flyingkoopas@aol.com', 'Acrobats'),
        (2276, 150.00, 'Lakitu Booth', 'photolakitus@outlook.com', 'Photo Booth'),
        (2285, 250.00, 'Chained Chompers', 'singingchomps@outlook.com', 'Cover Band'),
        (2294, 240.00, 'Hammer Bros', 'drumbros@gmail.com', 'Drums'),
        (2303, 400.00, 'Moe-Eye Magic', 'moeeyemagic@email.com', 'Magicians'),
        (2312, 1200.00, 'Shadow Mario', 'paintmagic@outlook.com', 'Portait Painting'),
        (2321, 2000.00, 'Frost Piranha', 'frostfower@email.com', 'Ice Sculpting'),
        (2330, 750.00, 'New Donkers', 'jazzbandnewdonk@email.com', 'Jazz Band'),
        (2339, 200.00, 'Sphynx', 'questionaire@buisness.com', 'Trivia'),
        (2348, 700.00, 'Dry Bones', 'dryboneband@gmail.com', 'Band'),
        (2357, 670.00, 'Spinies', 'spinydancers@gmail.com', 'Dancers'),
        (2366, 400.00, 'Mad Piano', 'bigboospiano@email.com', 'Musicians'),
        (2375, 360.00, 'Mr. Blizzard', 'chillysongs@yahoo.com', 'Singers'),
        (2384, 900.00, 'Kong Rappers', 'DK_rap@gmail.com', 'Band');
        """

        # Reservation data
        """
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
        """,

        # Party data
        """
        INSERT INTO Party (booking_id, party_id, type, description) VALUES
        (1001, 480, 'Graduation', 'Small graduation party for classmates'),
        (1005, 400, 'Wedding', 'Small sized wedding'),
        (1007, 410, 'Corporate', 'Product Launch party for new software'),
        (1011, 399, 'Birthday', 'Lunch Birthday Party'),
        (1013, 510, 'Graduation', 'Large graduation party for guest of honor'),
        (1009, 422, 'Quinceañera', 'Quinceañera for younger cousin'),
        (1015, 611, 'Holiday', 'Halloween Party for friends'),
        (1017, 615, 'Holiday', 'Late Night Halloween Party'),
        (1019, 618, 'Holiday', 'Large Masquerade Party'),
        (1021, 600, 'Birthday', 'Birthday Party for Twins'),
        (1023, 701, 'Birthday', 'Childre''s Birthday Party'),
        (1025, 715, 'Wedding', 'Medium sized wedding'),
        (1029, 733, 'Wedding', 'Large wedding with many services'),
        (1031, 755, 'Baby Shower', 'Small baby shower for expecting couple'),
        (1033, 590, 'Holiday', 'A christmas party for co-workers'),
        (1035, 812, 'Baby Shower', 'Afternoon get-together to celebrate baby on the way'),
        (1039, 500, 'Corporate', 'Board Meeting'),
        (1041, 544, 'Wedding', 'Large wedding with ocean theme'),
        (1043, 465, 'Birthday', 'Medium sized birthday party'),
        (1045, 901, 'Birthday', 'Kid''s birthday party'),
        (1047, 977, 'Misc', 'School Dance'),
        (1049, 920, 'Anniversary', 'Parent''s 30th anniversary celebration'),
        (1051, 800, 'Misc', 'Engagement Party'),
        (1055, 344, 'Birthday', 'Small sized birthday party'),
        (1057, 444, 'Holiday', 'Christmas Eve shopping pop-up market'),
        (1059, 555, 'Holiday', 'New Year''s Eve Celebration'),
        (1061, 230, 'Holiday', 'Thanksgiving lunch and get-together'),
        (1063, 250, 'Misc', 'Speed-dating event'),
        (1065, 720, 'Graduation', 'Combined graduation party for multiple students who were part of the same organization'),
        (1067, 200, 'Holiday', 'Holiday Party and Dinner, Fundraiser'),
        (1069, 210, 'Misc', 'Bachelorette Party');
        """,

        # Party_Decorations data
        """
        INSERT INTO Party_Decorations (booking_id, party_id, description) VALUES
        (1001, 480, 'Graduation Banner'),
        (1005, 400, 'Pastel Colored Flowers'),
        (1005, 400, 'Metallic Table Centerpieces'),
        (1009, 422, 'Pink Balloons'),
        (1013, 510, 'Paper Centerpieces'),
        (1019, 618, 'Disco Ball'),
        (1021, 600, 'Blue Balloons'),
        (1021, 600, 'Green Balloons'),
        (1021, 600, 'Birthday Banner'),
        (1023, 701, 'Assorted Balloons'),
        (1023, 701, 'Balloon Arch'),
        (1025, 715, 'Wedding Arch'),
        (1029, 733, 'White and Pink Flowers'),
        (1029, 733, 'Pearl-white balloons'),
        (1029, 733, 'Floral Centerpieces'),
        (1041, 544, 'Ocean-themed ornaments'),
        (1041, 544, 'blue tablecloth'),
        (1043, 465, 'Assorted Balloons'),
        (1045, 901, 'Colorful Backdrop'),
        (1045, 901, 'Assorted Balloons'),
        (1045, 901, 'Birthday Banner'),
        (1047, 977, 'Disco Ball'),
        (1047, 977, 'Iridescent Table Cloth'),
        (1051, 800, 'Confetti'),
        (1055, 344, 'Pink Tablecloth'),
        (1055, 344, 'Purple Streamers'),
        (1057, 444, 'Holiday Lights'),
        (1057, 444, 'Blow-Up Santa'),
        (1061, 230, 'Fake Fruit Bowl'),
        (1061, 230, 'Country Tablecloth'),
        (1065, 720, 'Graduation Backdrop'),
        (1069, 210, 'Pink Tablecloth'),
        (1069, 210, 'Red Balloons'),
        (1067, 200, 'Red Tablecloth');
        """,

        # Party_GuestOfHonor data
        """
        INSERT INTO Party_GuestOfHonor (booking_id, party_id, name) VALUES
        (1001, 480, 'Vaughn Scott'),
        (1001, 480, 'Wright Quist'),
        (1001, 480, 'Allie Kim'),
        (1005, 400, 'Mr. Kim'),
        (1005, 400, 'Ms. Kim'),
        (1009, 422, 'Maria Somebody'),
        (1013, 510, 'Peter Tessier'),
        (1021, 600, 'Tweedle-Dee'),
        (1021, 600, 'Tweedle-Dum'),
        (1023, 701, 'Little Mu'),
        (1025, 715, 'Mr. Douglas'),
        (1025, 715, 'Ms. Douglas'),
        (1029, 733, 'Mr. Gusani'),
        (1029, 733, 'Ms. Gusani'),
        (1041, 544, 'Mr. Lu'),
        (1041, 544, 'Ms. Lu'),
        (1043, 465, 'Best Friend'),
        (1045, 901, 'Lil Seto'),
        (1047, 977, 'Scholarship Recipient 1'),
        (1047, 977, 'Scholarship Recipient 2'),
        (1047, 977, 'Scholarship Recipient 3'),
        (1049, 920, 'Mr. Mu'),
        (1049, 920, 'Ms. Mu'),
        (1051, 800, 'Abey'),
        (1051, 800, 'Ethan'),
        (1055, 344, 'Haley Fitch'),
        (1065, 720, 'Ian Douglas'),
        (1065, 720, 'Henry Cutright'),
        (1065, 720, 'Param Patel'),
        (1065, 720, 'Maseel Shah'),
        (1065, 720, 'Grant Costello'),
        (1065, 720, 'Angela Chung');
        """,

        # Reservation_Staff data
        """
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
        """,

        # Reservation_Performers data
        """
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
        """
    ]

    with engine.connect() as conn:
        for command in commands:
            try:
                conn.execute(text(command))
                conn.commit()
                print(f"Successfully imported data: {command[:50]}...")
            except Exception as e:
                print(f"Error importing data: {command[:50]}...")
                print(f"Error message: {str(e)}")
                return False