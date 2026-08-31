"""
Real rosters for remaining 16 Serie A clubs and 6 Ligue 1 clubs.
"""

REMAINING_REAL_CLUBS = {
    # --- SERIE A ---
    "Atalanta": [
        ("Marco Carnesecchi", "GK", 24, 2700), ("Rui Patricio", "GK", 36, 900), ("Isak Hien", "CB", 25, 2600),
        ("Berat Djimsiti", "CB", 31, 2700), ("Sead Kolasinac", "CB", 31, 2400), ("Odilon Kossounou", "CB", 23, 2100),
        ("Ben Godfrey", "CB", 26, 1400), ("Raoul Bellanova", "FB", 24, 2600), ("Matteo Ruggeri", "FB", 22, 2500),
        ("Davide Zappacosta", "FB", 32, 2000), ("Marco Palestra", "FB", 19, 1100), ("Marten de Roon", "CM", 33, 2800),
        ("Ederson", "CM", 25, 2800), ("Mario Pasalic", "CM", 29, 2300), ("Lazar Samardzic", "CM", 22, 2200),
        ("Marco Brescianini", "CM", 24, 1900), ("Charles De Ketelaere", "W", 23, 2600), ("Ademola Lookman", "W", 27, 2700),
        ("Nicolo Zaniolo", "W", 25, 1700), ("Mateo Retegui", "ST", 25, 2700), ("Gianluca Scamacca", "ST", 25, 1800)
    ],
    "AS Roma": [
        ("Mile Svilar", "GK", 25, 2800), ("Mathew Ryan", "GK", 32, 900), ("Gianluca Mancini", "CB", 28, 2700),
        ("Evan Ndicka", "CB", 25, 2700), ("Mats Hummels", "CB", 36, 1500), ("Mario Hermoso", "CB", 29, 2000),
        ("Zeki Celik", "FB", 27, 2400), ("Angelino", "FB", 27, 2600), ("Saud Abdulhamid", "FB", 25, 1400),
        ("Samuel Dahl", "FB", 21, 1100), ("Bryan Cristante", "CM", 29, 2600), ("Manu Kone", "CM", 23, 2600),
        ("Leandro Paredes", "CM", 30, 2100), ("Lorenzo Pellegrini", "CM", 28, 2500), ("Enzo Le Fee", "CM", 24, 2000),
        ("Tommaso Baldanzi", "CM", 21, 1800), ("Paulo Dybala", "W", 31, 2400), ("Stephan El Shaarawy", "W", 32, 2100),
        ("Matias Soule", "W", 21, 2400), ("Alexis Saelemaekers", "W", 25, 1900), ("Artem Dovbyk", "ST", 27, 2700),
        ("Eldor Shomurodov", "ST", 29, 1300)
    ],
    "Lazio": [
        ("Ivan Provedel", "GK", 30, 2700), ("Christos Mandas", "GK", 23, 1100), ("Alessio Romagnoli", "CB", 29, 2700),
        ("Mario Gila", "CB", 24, 2600), ("Samuel Gigot", "CB", 31, 1500), ("Patric", "CB", 31, 1600),
        ("Manuel Lazzari", "FB", 31, 2300), ("Nuno Tavares", "FB", 24, 2600), ("Adam Marusic", "FB", 32, 2200),
        ("Luca Pellegrini", "FB", 25, 1400), ("Nicolo Rovella", "CM", 23, 2700), ("Matteo Guendouzi", "CM", 25, 2800),
        ("Matias Vecino", "CM", 33, 2000), ("Fisayo Dele-Bashiru", "CM", 23, 1800), ("Gaetano Castrovilli", "CM", 27, 1400),
        ("Mattia Zaccagni", "W", 29, 2700), ("Gustav Isaksen", "W", 23, 2200), ("Loum Tchaouna", "W", 21, 1800),
        ("Pedro", "W", 37, 1600), ("Valentin Castellanos", "ST", 26, 2700), ("Boulaye Dia", "ST", 28, 2500),
        ("Tijjani Noslin", "ST", 25, 2000)
    ],
    "Fiorentina": [
        ("David de Gea", "GK", 34, 2700), ("Pietro Terracciano", "GK", 34, 1100), ("Lucas Martinez Quarta", "CB", 28, 2300),
        ("Marin Pongracic", "CB", 27, 2100), ("Luca Ranieri", "CB", 25, 2600), ("Pietro Comuzzo", "CB", 19, 2200),
        ("Dodo", "FB", 26, 2700), ("Robin Gosens", "FB", 30, 2600), ("Michael Kayode", "FB", 20, 1800),
        ("Cristiano Biraghi", "FB", 32, 1900), ("Fabiano Parisi", "FB", 24, 1500), ("Yacine Adli", "CM", 24, 2400),
        ("Edoardo Bove", "CM", 22, 2500), ("Danilo Cataldi", "CM", 30, 2300), ("Rolando Mandragora", "CM", 27, 2100),
        ("Amir Richardson", "CM", 22, 1600), ("Albert Gudmundsson", "W", 27, 2500), ("Andrea Colpani", "W", 25, 2400),
        ("Jonathan Ikone", "W", 26, 1700), ("Riccardo Sottil", "W", 25, 1700), ("Moise Kean", "ST", 24, 2700),
        ("Lucas Beltran", "ST", 23, 2100), ("Christian Kouame", "ST", 27, 1600)
    ],
    "Bologna": [
        ("Lukasz Skorupski", "GK", 33, 2500), ("Federico Ravaglia", "GK", 25, 1200), ("Sam Beukema", "CB", 26, 2700),
        ("Jhon Lucumi", "CB", 26, 2600), ("Martin Erlic", "CB", 26, 1700), ("Nicolo Casale", "CB", 26, 1600),
        ("Stefan Posch", "FB", 27, 2600), ("Charalampos Lykogiannis", "FB", 31, 2100), ("Juan Miranda", "FB", 24, 2300),
        ("Emil Holm", "FB", 24, 1700), ("Remo Freuler", "CM", 32, 2800), ("Michel Aebischer", "CM", 28, 2300),
        ("Nikola Moro", "CM", 26, 2000), ("Giovanni Fabbian", "CM", 21, 2400), ("Tommaso Pobega", "CM", 25, 1900),
        ("Lewis Ferguson", "CM", 25, 1800), ("Riccardo Orsolini", "W", 27, 2600), ("Dan Ndoye", "W", 24, 2600),
        ("Jesper Karlsson", "W", 26, 1400), ("Samuel Iling-Junior", "W", 21, 1600), ("Santiago Castro", "ST", 20, 2500),
        ("Thijs Dallinga", "ST", 24, 2200), ("Jens Odgaard", "ST", 25, 1900)
    ],
    "Torino": [
        ("Vanja Milinkovic-Savic", "GK", 27, 2800), ("Saul Coco", "CB", 25, 2700), ("Guillermo Maripan", "CB", 30, 2400),
        ("Sebastian Walukiewicz", "CB", 24, 2200), ("Adrien Tameze", "CB", 30, 1800), ("Marcus Pedersen", "FB", 24, 2200),
        ("Borna Sosa", "FB", 26, 2300), ("Mergim Vojvoda", "FB", 29, 2300), ("Valentino Lazaro", "FB", 28, 2600),
        ("Samuele Ricci", "CM", 23, 2800), ("Ivan Ilic", "CM", 23, 2400), ("Karol Linetty", "CM", 29, 2300),
        ("Gvidas Gineitis", "CM", 20, 1500), ("Cesare Casadei", "CM", 21, 1400), ("Nikola Vlasic", "W", 27, 2400),
        ("Yann Karamoh", "W", 26, 1400), ("Ali Dembele", "W", 20, 1100), ("Duvan Zapata", "ST", 33, 2200),
        ("Che Adams", "ST", 28, 2500), ("Antonio Sanabria", "ST", 28, 2300)
    ],
    "Genoa": [
        ("Pierluigi Gollini", "GK", 29, 2300), ("Nicola Leali", "GK", 31, 1300), ("Johan Vasquez", "CB", 26, 2700),
        ("Mattia Bani", "CB", 31, 2400), ("Koni De Winter", "CB", 22, 2300), ("Alessandro Vogliacco", "CB", 26, 2100),
        ("Alan Matturro", "CB", 20, 1300), ("Stefano Sabelli", "FB", 31, 2400), ("Aaron Martin", "FB", 27, 2500),
        ("Alessandro Zanoli", "FB", 24, 1800), ("Brooke Norton-Cuffy", "FB", 20, 1500), ("Morten Frendrup", "CM", 23, 2800),
        ("Milan Badelj", "CM", 35, 2300), ("Morten Thorsby", "CM", 28, 2400), ("Fabio Miretti", "CM", 21, 2300),
        ("Ruslan Malinovskyi", "CM", 31, 1600), ("Junior Messias", "W", 33, 1700), ("Vitinha", "W", 24, 2100),
        ("Gaston Pereiro", "W", 29, 1200), ("Andrea Pinamonti", "ST", 25, 2700), ("Mario Balotelli", "ST", 34, 1200),
        ("Caleb Ekuban", "ST", 30, 1600), ("David Ankeye", "ST", 22, 1100)
    ],
    "Como": [
        ("Emil Audero", "GK", 27, 2200), ("Pepe Reina", "GK", 42, 1100), ("Alberto Dossena", "CB", 26, 2600),
        ("Marc-Oliver Kempf", "CB", 29, 2500), ("Edoardo Goldaniga", "CB", 31, 1800), ("Felipe Jack", "CB", 18, 900),
        ("Ignace Van der Brempt", "FB", 22, 2300), ("Alberto Moreno", "FB", 32, 2400), ("Alessio Iovine", "FB", 33, 1500),
        ("Marco Sala", "FB", 25, 1400), ("Maximo Perrone", "CM", 21, 2600), ("Sergi Roberto", "CM", 32, 2300),
        ("Yannik Engelhardt", "CM", 23, 2000), ("Lucas Da Cunha", "CM", 23, 2200), ("Daniele Baselli", "CM", 32, 1200),
        ("Nico Paz", "CM", 20, 2700), ("Gabriel Strefezza", "W", 27, 2600), ("Alieu Fadera", "W", 23, 2400),
        ("Simone Verdi", "W", 32, 1400), ("Patrick Cutrone", "ST", 26, 2700), ("Andrea Belotti", "ST", 31, 2100),
        ("Alberto Cerri", "ST", 28, 1200), ("Alessandro Gabrielloni", "ST", 30, 1100)
    ],
    "Parma": [
        ("Zion Suzuki", "GK", 22, 2800), ("Leandro Chichizola", "GK", 34, 900), ("Botond Balogh", "CB", 22, 2600),
        ("Alessandro Circati", "CB", 21, 2000), ("Yordan Osorio", "CB", 30, 1800), ("Lautaro Valenti", "CB", 25, 1600),
        ("Woyo Coulibaly", "FB", 25, 2500), ("Emanuele Valeri", "FB", 26, 2600), ("Enrico Delprato", "FB", 25, 2700),
        ("Gianluca Di Chiara", "FB", 31, 1400), ("Adrian Bernabe", "CM", 23, 2700), ("Nahuel Estevez", "CM", 29, 2100),
        ("Simon Sohm", "CM", 23, 2600), ("Hernani", "CM", 30, 2400), ("Mandela Keita", "CM", 22, 2200),
        ("Antoine Hainaut", "CM", 22, 1500), ("Dennis Man", "W", 26, 2700), ("Valentin Mihaila", "W", 24, 2500),
        ("Matteo Cancellieri", "W", 22, 2300), ("Pontus Almqvist", "W", 25, 2100), ("Ange-Yoan Bonny", "ST", 21, 2700),
        ("Mateusz Kowalski", "ST", 19, 1200), ("Gabriel Charpentier", "ST", 25, 1400)
    ],
    "Udinese": [
        ("Maduka Okoye", "GK", 25, 2800), ("Daniele Padelli", "GK", 39, 900), ("Jaka Bijol", "CB", 25, 2800),
        ("Christian Kabasele", "CB", 33, 2100), ("Thomas Kristensen", "CB", 22, 2200), ("Lautaro Giannetti", "CB", 31, 2300),
        ("Isaak Toure", "CB", 21, 1800), ("Kingsley Ehizibue", "FB", 29, 2600), ("Hassane Kamara", "FB", 30, 2500),
        ("Jordan Zemura", "FB", 25, 2200), ("Rui Modesto", "FB", 25, 1400), ("Jesper Karlstrom", "CM", 29, 2700),
        ("Sandi Lovric", "CM", 26, 2600), ("Martin Payero", "CM", 26, 2300), ("Oier Zarraga", "CM", 25, 1900),
        ("Arthur Atta", "CM", 21, 1500), ("Jurgen Ekkelenkamp", "CM", 24, 2100), ("Florian Thauvin", "W", 31, 2700),
        ("Iker Bravo", "W", 19, 1600), ("Lorenzo Lucca", "ST", 24, 2700), ("Keinan Davis", "ST", 26, 2100),
        ("Gerard Deulofeu", "ST", 30, 1100), ("Damian Pizarro", "ST", 19, 1200)
    ],
    "Monza": [
        ("Stefano Turati", "GK", 23, 2600), ("Semuel Pizzignacco", "GK", 23, 1100), ("Pablo Mari", "CB", 31, 2700),
        ("Armando Izzo", "CB", 32, 2600), ("Andrea Carboni", "CB", 23, 2400), ("Luca Caldirola", "CB", 33, 1700),
        ("Pedro Pereira", "FB", 26, 2600), ("Georgios Kyriakopoulos", "FB", 28, 2700), ("Samuele Birindelli", "FB", 25, 1800),
        ("Matteo Pessina", "CM", 27, 2800), ("Warren Bondo", "CM", 21, 2600), ("Alessandro Bianco", "CM", 22, 2200),
        ("Roberto Gagliardini", "CM", 30, 2000), ("Stefano Sensi", "CM", 29, 1400), ("Daniel Maldini", "W", 23, 2700),
        ("Gianluca Caprari", "W", 31, 2100), ("Patrick Ciurria", "W", 29, 1800), ("Dany Mota", "ST", 26, 2600),
        ("Milan Djuric", "ST", 34, 2500), ("Mirko Maric", "ST", 29, 1300), ("Omari Forson", "W", 20, 1200)
    ],
    "Hellas Verona": [
        ("Lorenzo Montipo", "GK", 28, 2800), ("Simone Perilli", "GK", 29, 900), ("Diego Coppola", "CB", 21, 2700),
        ("Pawel Dawidowicz", "CB", 29, 2500), ("Giangiacomo Magnani", "CB", 29, 2600), ("Flavius Daniliuc", "CB", 23, 1900),
        ("Daniele Ghilardi", "CB", 21, 1500), ("Jackson Tchatchoua", "FB", 23, 2700), ("Domagoj Bradaric", "FB", 24, 2500),
        ("Martin Frese", "FB", 26, 1700), ("Davide Faraoni", "FB", 33, 1400), ("Ondrej Duda", "CM", 30, 2700),
        ("Suat Serdar", "CM", 27, 2500), ("Reda Belahyane", "CM", 20, 2600), ("Dani Silva", "CM", 24, 2000),
        ("Tomas Suslov", "W", 22, 2600), ("Darko Lazovic", "W", 34, 2500), ("Abdou Harroui", "W", 26, 1800),
        ("Dailon Livramento", "W", 23, 1900), ("Casper Tengstedt", "ST", 24, 2600), ("Daniel Mosquera", "ST", 25, 2300),
        ("Amin Sarr", "ST", 23, 1600), ("Faride Alidou", "W", 23, 1400)
    ],
    "Cagliari": [
        ("Simone Scuffet", "GK", 28, 2600), ("Alen Sherri", "GK", 26, 1100), ("Yerry Mina", "CB", 30, 2500),
        ("Sebastiano Luperto", "CB", 28, 2700), ("Mateusz Wieteska", "CB", 27, 1800), ("Jose Luis Palomino", "CB", 35, 1400),
        ("Gabriele Zappa", "FB", 25, 2700), ("Tommaso Augello", "FB", 30, 2600), ("Paulo Azzi", "FB", 30, 1900),
        ("Adam Obert", "FB", 22, 1700), ("Razvan Marin", "CM", 28, 2700), ("Michel Adopo", "CM", 24, 2500),
        ("Antoine Makoumbou", "CM", 26, 2400), ("Matteo Prati", "CM", 20, 2200), ("Alessandro Deiola", "CM", 29, 2100),
        ("Gianluca Gaetano", "CM", 24, 2400), ("Nicolas Viola", "CM", 35, 1800), ("Zito Luvumbo", "W", 22, 2600),
        ("Mattia Felici", "W", 23, 1600), ("Roberto Piccoli", "ST", 23, 2700), ("Gianluca Lapadula", "ST", 34, 1800),
        ("Leonardo Pavoletti", "ST", 36, 1300), ("Kingstone Mutandwa", "ST", 21, 1000)
    ],
    "Empoli": [
        ("Devis Vasquez", "GK", 26, 2700), ("Federico Brancolini", "GK", 23, 900), ("Ardian Ismajli", "CB", 28, 2800),
        ("Mattia Viti", "CB", 22, 2700), ("Saba Goglichidze", "CB", 20, 2400), ("Luca Marianucci", "CB", 20, 1300),
        ("Emmanuel Gyasi", "FB", 31, 2700), ("Giuseppe Pezzella", "FB", 27, 2600), ("Junior Sambia", "FB", 28, 1600),
        ("Liberato Cacace", "FB", 24, 1900), ("Liam Henderson", "CM", 28, 2600), ("Alberto Grassi", "CM", 29, 2500),
        ("Youssef Maleh", "CM", 26, 2400), ("Tino Anjorin", "CM", 23, 2300), ("Jacopo Fazzini", "CM", 21, 2400),
        ("Nicolas Haas", "CM", 28, 1700), ("Szymon Zurkowski", "CM", 27, 1500), ("Ola Solbakken", "W", 26, 2100),
        ("Emmanuel Ekong", "W", 22, 1400), ("Sebastiano Esposito", "ST", 22, 2600), ("Lorenzo Colombo", "ST", 22, 2700),
        ("Pietro Pellegri", "ST", 23, 1900)
    ],
    "Venezia": [
        ("Jesse Joronen", "GK", 31, 2100), ("Filip Stankovic", "GK", 22, 1600), ("Jay Idzes", "CB", 24, 2700),
        ("Michael Svoboda", "CB", 26, 2600), ("Marin Sverko", "CB", 26, 2300), ("Giorgio Altare", "CB", 26, 1700),
        ("Antonio Candela", "FB", 24, 2600), ("Ridgeciano Haps", "FB", 31, 2400), ("Francesco Zampano", "FB", 31, 2500),
        ("Franco Carboni", "FB", 21, 1400), ("Gianluca Busio", "CM", 22, 2700), ("Hans Nicolussi Caviglia", "CM", 24, 2600),
        ("Alfred Duncan", "CM", 31, 2400), ("Mikael Ellertsson", "CM", 22, 2500), ("Domen Crnigoj", "CM", 29, 1700),
        ("Mato Jajalo", "CM", 36, 1200), ("Gaetano Oristanio", "W", 22, 2600), ("John Yeboah", "W", 24, 2100),
        ("Bjarki Bjarkason", "W", 24, 1500), ("Joel Pohjanpalo", "ST", 30, 2700), ("Christian Gytkjaer", "ST", 34, 1800),
        ("Antonio Raimondo", "ST", 20, 1600)
    ],
    "Lecce": [
        ("Wladimiro Falcone", "GK", 29, 2800), ("Christian Fruchtl", "GK", 24, 900), ("Federico Baschirotto", "CB", 28, 2800),
        ("Kialonda Gaspar", "CB", 27, 2700), ("Gaby Jean", "CB", 24, 1600), ("Kevin Bonifazi", "CB", 28, 1400),
        ("Frederic Guilbert", "FB", 30, 2600), ("Antonino Gallo", "FB", 24, 2700), ("Andy Pelmard", "FB", 24, 1700),
        ("Patrick Dorgu", "FB", 20, 2700), ("Ylber Ramadani", "CM", 28, 2800), ("Lassana Coulibaly", "CM", 28, 2600),
        ("Balthazar Pierret", "CM", 24, 2100), ("Mohamed Kaba", "CM", 23, 1900), ("Hamza Rafia", "CM", 25, 2300),
        ("Medon Berisha", "CM", 21, 1700), ("Tete Morente", "W", 28, 2400), ("Lameck Banda", "W", 23, 2200),
        ("Remi Oudin", "W", 28, 2100), ("Santiago Pierotti", "W", 23, 1800), ("Nikola Krstovic", "ST", 24, 2800),
        ("Ante Rebic", "ST", 31, 2000), ("Rareș Burnete", "ST", 20, 1200)
    ],

    # --- LIGUE 1 ---
    "Strasbourg": [
        ("Djordje Petrovic", "GK", 25, 2700), ("Karl-Johan Johnsson", "GK", 34, 1000), ("Saidou Sow", "CB", 22, 2500),
        ("Mamadou Sarr", "CB", 19, 2300), ("Abakar Sylla", "CB", 22, 2100), ("Guela Doue", "FB", 22, 2600),
        ("Diego Moreira", "FB", 20, 2500), ("Marvin Senaya", "FB", 23, 1900), ("Eduard Sobol", "FB", 29, 1300),
        ("Andrey Santos", "CM", 20, 2700), ("Ismael Doukoure", "CM", 21, 2600), ("Habib Diarra", "CM", 20, 2700),
        ("Pape Diong", "CM", 18, 1700), ("Felix Lemarechal", "CM", 21, 1900), ("Sebastian Nanasi", "W", 22, 2600),
        ("Dilane Bakwa", "W", 22, 2700), ("Oscar Perea", "W", 19, 1400), ("Rayane Messi", "W", 17, 1000),
        ("Emanuel Emegha", "ST", 21, 2600), ("Sekou Mara", "ST", 22, 2200), ("Milos Lukovic", "ST", 19, 1500)
    ],
    "Nantes": [
        ("Alban Lafont", "GK", 25, 2700), ("Patrik Carlgren", "GK", 32, 1000), ("Jean-Charles Castelletto", "CB", 29, 2700),
        ("Nathan Zeze", "CB", 19, 2600), ("Nicolas Pallois", "CB", 37, 1800), ("Kelvin Amian", "FB", 26, 2600),
        ("Nicolas Cozza", "FB", 25, 2400), ("Marcus Coco", "FB", 28, 2100), ("Fabien Centonze", "FB", 28, 1400),
        ("Pedro Chirivella", "CM", 27, 2700), ("Douglas Augusto", "CM", 27, 2600), ("Johann Lepenant", "CM", 22, 2500),
        ("Sorba Thomas", "CM", 25, 2400), ("Florent Mollet", "CM", 33, 1700), ("Moses Simon", "W", 29, 2700),
        ("Matthis Abline", "W", 21, 2600), ("Tino Kadewere", "W", 28, 2000), ("Ignatius Ganago", "W", 25, 1600),
        ("Mostafa Mohamed", "ST", 27, 2600), ("Herba Guirassy", "ST", 18, 1200), ("Bahereba Guirassy", "ST", 18, 1100)
    ],
    "Le Havre": [
        ("Arthur Desmas", "GK", 30, 2700), ("Mathieu Gorgelin", "GK", 34, 900), ("Gautier Lloris", "CB", 29, 2700),
        ("Yoann Salmier", "CB", 32, 2400), ("Arouna Sangante", "CB", 22, 2600), ("Etienne Youte Kinkoue", "CB", 22, 2300),
        ("Loic Nego", "FB", 33, 2600), ("Christopher Operi", "FB", 27, 2700), ("Timothee Pembele", "FB", 22, 1800),
        ("Yaniss Zouaoui", "FB", 26, 1500), ("Abdoulaye Toure", "CM", 30, 2700), ("Oussama Targhalline", "CM", 22, 2500),
        ("Yassine Kechta", "CM", 22, 2600), ("Daler Kuzyaev", "CM", 31, 2300), ("Rassoul Ndiaye", "CM", 23, 2000),
        ("Alois Confais", "CM", 28, 1400), ("Josue Casimir", "W", 23, 2400), ("Antoine Joujou", "W", 21, 2000),
        ("Issa Soumare", "W", 24, 1800), ("Emmanuel Sabbi", "ST", 27, 2500), ("Ilyes Housni", "ST", 19, 1700),
        ("Steve Ngoura", "ST", 19, 1400)
    ],
    "Auxerre": [
        ("Donovan Leon", "GK", 32, 2700), ("Theo De Percin", "GK", 23, 900), ("Jubal", "CB", 31, 2800),
        ("Gabriel Osho", "CB", 26, 2500), ("Sinaly Diomande", "CB", 23, 2400), ("Theo Pellenard", "CB", 30, 1600),
        ("Paul Joly", "FB", 24, 2600), ("Ki-Jana Hoever", "FB", 22, 2300), ("Gideon Mensah", "FB", 26, 2500),
        ("Clement Akpa", "FB", 22, 2000), ("Elisha Owusu", "CM", 27, 2700), ("Rayan Raveloson", "CM", 27, 2600),
        ("Kevin Danois", "CM", 20, 2200), ("Assane Diousse", "CM", 27, 1800), ("Hamza Sakhi", "CM", 28, 1500),
        ("Gaetan Perrin", "W", 28, 2700), ("Lassine Sinayoko", "W", 25, 2600), ("Ado Onaiwu", "W", 29, 2200),
        ("Florian Aye", "ST", 27, 2400), ("Thelonius Bair", "ST", 25, 2200), ("Aristide Zossou", "ST", 19, 1100)
    ],
    "Angers": [
        ("Yahia Fofana", "GK", 24, 2800), ("Melvin Zinga", "GK", 22, 900), ("Cedric Hountondji", "CB", 30, 2600),
        ("Jordan Lefort", "CB", 31, 2700), ("Abdoulaye Bamba", "CB", 34, 1800), ("Emmanuel Biumla", "CB", 19, 1900),
        ("Carlens Arcus", "FB", 28, 2600), ("Florent Hanin", "FB", 34, 2400), ("Lilian Rao-Lisoa", "FB", 24, 2200),
        ("Jacques Ekomie", "FB", 21, 1600), ("Pierrick Capelle", "CM", 37, 1900), ("Haris Belkebla", "CM", 30, 2600),
        ("Jean-Eudes Aholou", "CM", 30, 2500), ("Himad Abdelli", "CM", 25, 2800), ("Yassin Belkhdim", "CM", 22, 2100),
        ("Zinedine Ferhat", "W", 31, 2300), ("Farid El Melali", "W", 27, 2600), ("Jim Allevinah", "W", 29, 2400),
        ("Zinedine Ould Khaled", "W", 24, 1600), ("Esteban Lepaul", "ST", 24, 2500), ("Ibrahima Niane", "ST", 25, 2200),
        ("Bamba Dieng", "ST", 24, 2300), ("Sidiki Cherif", "ST", 18, 1200)
    ],
    "Saint-Etienne": [
        ("Gautier Larsonneur", "GK", 27, 2800), ("Brice Maubleu", "GK", 35, 900), ("Yunis Abdelhamid", "CB", 37, 2400),
        ("Mickael Nade", "CB", 25, 2500), ("Dylan Batubinsika", "CB", 28, 2400), ("Leo Petrot", "CB", 27, 2200),
        ("Dennis Appiah", "FB", 32, 2600), ("Pierre Cornud", "FB", 28, 2300), ("Yvann Macon", "FB", 26, 2100),
        ("Florian Tardieu", "CM", 32, 2200), ("Pierre Ekwah", "CM", 22, 2600), ("Aimen Moueffek", "CM", 23, 2400),
        ("Louis Mouton", "CM", 22, 2100), ("Benjamin Bouchouari", "CM", 23, 2300), ("Mathis Amougou", "CM", 18, 2000),
        ("Igor Miladinovic", "CM", 21, 1600), ("Zuriko Davitashvili", "W", 23, 2800), ("Mathieu Cafaro", "W", 27, 2500),
        ("Ben Old", "W", 22, 1900), ("Augustine Boakye", "W", 24, 1800), ("Ibrahim Sissoko", "ST", 29, 2600),
        ("Lucas Stassin", "ST", 20, 2400), ("Ibrahima Wadji", "ST", 29, 1400)
    ]
}
