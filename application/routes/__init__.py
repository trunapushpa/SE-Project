import json, io, os
from flask import render_template, session, redirect, request, flash
from application import app, db, login_manager
from application.dbModels.users import Users
from application.dbModels.wordVector import WordVector
from application.routes.indexRoutes import home
from application.routes.messageRoutes import message
from application.routes.myItemsRoutes import my_items
from application.routes.myProfileRoutes import my_profile
from application.routes.topUsersRoutes import top_users
from application.routes.uploadItemRoutes import upload_item
from application.routes.userRoutes import user
from application.routes.allItemsRoutes import all_items
from application.routes.allUsersRoutes import all_users

app.register_blueprint(home, prefix_url='')
app.register_blueprint(user, prefix_url='')
app.register_blueprint(top_users, prefix_url='')
app.register_blueprint(my_items, prefix_url='')
app.register_blueprint(my_profile, prefix_url='')
app.register_blueprint(upload_item, prefix_url='')
app.register_blueprint(message, prefix_url='')
app.register_blueprint(all_items, prefix_url='')
app.register_blueprint(all_users, prefix_url='')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route("/switch_theme/<theme>", methods=['POST'])
def switch_theme(theme):
    session['theme'] = theme
    return redirect(request.referrer)


@app.route('/about')
def about():
    file = open('team.json', 'r')
    team = json.load(file)
    return render_template('about.html', about=True, team=team)


@app.route("/add_vectors", methods=['GET'])
def save_word_vectors():
    word_list = ['hairless', 'native', 'tape', 'spoonbill', 'stop', 'chetah', 'vat', 'miniature', 'trilobite', 'dunlin',
                 'carrousel', 'eft', 'dingo', 'common', 'hankey', 'hot', 'asiatic', 'slot', 'sandbar', 'armored',
                 'tobacconist', 'griffon', 'measuring', 'sub', 'carpodacus', 'camera', 'nematode', 'accordion', 'silky',
                 'hognose', 'mobile', 'bridegroom', 'spaniel', 'bulldog', 'barber', 'pharos', 'loggerhead', 'lakeside',
                 'gold', 'plinth', 'parking', 'shepherd', 'board', 'hautboy', 'racing', 'robustus', 'vulpes',
                 'butternut', 'abaya', 'canadensis', 'rack', 'bulbul', 'komondor', 'boston', 'go', 'bobsleigh',
                 'cardigan', 'pipe', 'amoenus', 'projector', 'roof', 'jewelers', 'gecko', 'tinca', 'miniskirt',
                 'bloodhound', 'net', 'bittern', 'banjo', 'menu', 'courgette', 'amphibian', 'bald', 'screw', 'walker',
                 'dock', 'reef', 'oystercatcher', 'orange', 'bolete', 'swan', 'weimaraner', 'cimarron', 'ram', 'hard',
                 'wheel', 'apiary', 'tibetan', 'sock', 'bowtie', 'hawk', 'spiral', 'garter', 'vehicle', 'arch',
                 'taxicab', 'dark', 'vizsla', 'saltshaker', 'macrotis', 'whiptail', 'buckler', 'shower', 'back',
                 'kangaroo', 'basset', 'paralithodes', 'crawfish', 'bulwark', 'otter', 'heater', 'brambling',
                 'sunglasses', 'langouste', 'gasmask', 'flagstaff', 'sunscreen', 'banister', 'dwelling', 'sciureus',
                 'dutch', 'kuvasz', 'cairn', 'frondosus', 'beauty', 'goose', 'amphibious', 'duck', 'cock', 'alaskan',
                 'panthera', 'xylophone', 'chopper', 'frying', 'italian', 'squirrel', 'rosehip', 'boot', 'spot', 'sign',
                 'anteater', 'cerastes', 'sunglass', 'plectrum', 'shirt', 'snoek', 'tissue', 'compass', 'symphalangus',
                 'rhinoceros', 'piece', 'suspension', 'painter', 'tam', 'digital', 'hummingbird', 'banded', 'papillon',
                 'lady', 'punching', 'ouzel', 'gray', 'bathing', 'pismire', 'towel', 'syringe', 'bernese', 'icecream',
                 'rana', 'trolley', 'phone', 'carrier', 'taper', 'trimaran', 'borzoi', 'racquet', 'stethoscope',
                 'nudibranch', 'st', 'capra', 'trackless', 'peacock', 'hankie', 'snail', 'pinscher', 'english',
                 'thimble', 'ashbin', 'flat', 'umbrella', 'shop', 'duckbilled', 'custard', 'brush', 'gasoline',
                 'smoothing', 'commode', 'muzzle', 'chimp', 'wolfhound', 'fur', 'salamander', 'apso', 'nipple', 'vault',
                 'cicada', 'calceolus', 'dishcloth', 'pepper', 'newfoundland', 'boat', 'coated', 'coat', 'baseball',
                 'highland', 'squealer', 'rhodesian', 'cauldron', 'coffeepot', 'flute', 'laptop', 'troglodytes',
                 'hammerhead', 'corn', 'guacamole', 'cyanea', 'pit', 'limpkin', 'solar', 'flattop', 'washer', 'elephas',
                 'mug', 'island', 'racket', 'ringtail', 'petri', 'cancer', 'tringa', 'podenco', 'ribbed', 'cask',
                 'setter', 'mexican', 'longlegs', 'cornet', 'pier', 'bucket', 'window', 'carolinensis', 'dane',
                 'barometer', 'curly', 'joystick', 'larvatus', 'aranea', 'trike', 'dryer', 'bee', 'skillet', 'great',
                 'cocktail', 'pop', 'vending', 'brake', 'torpedo', 'jay', 'labrador', 'chickadee', 'puffer', 'aegis',
                 'potpie', 'eschrichtius', 'hedgehog', 'comforter', 'rain', 'adamanteus', 'triumphal', 'rickshaw',
                 'slipper', 'building', 'junco', 'and', 'maritimus', 'house', 'bustard', 'mosquito', 'opilio', 'bagel',
                 'sturgeon', 'beam', 'center', 'ocean', 'cuvieri', 'reflex', 'hand', 'hornbill', 'bathroom', 'puppy',
                 'manhole', 'ailuropoda', 'stupa', 'brain', 'geta', 'pomegranate', 'cape', 'bolo', 'mergus', 'golfcart',
                 'perfume', 'acorn', 'fungus', 'fly', 'sleigh', 'lampshade', 'hamster', 'closet', 'saluki', 'irish',
                 'greyhound', 'cat', 'sled', 'bow', 'prairie', 'greenhouse', 'store', 'totanus', 'tandem', 'ferret',
                 'trifle', 'reflector', 'lakeshore', 'thalarctos', 'billfold', 'deerhound', 'toucan', 'patagonica',
                 'rocking', 'airedale', 'turnstile', 'duckbill', 'dial', 'mud', 'drum', 'megalithic', 'saxophone',
                 'soup', 'folding', 'fulica', 'knee', 'velocipede', 'eel', 'banana', 'school', 'norfolk', 'doctor',
                 'ballpen', 'plaque', 'ladybug', 'holster', 'boar', 'apple', 'toaster', 'terrier', 'shetland', 'maine',
                 'aptenodytes', 'black', 'cannon', 'harmonica', 'weevil', 'horn', 'bear', 'sleuthhound', 'glass',
                 'cassette', 'ping', 'carousel', 'capitulum', 'peke', 'ostrich', 'leonberg', 'mailbox', 'rubber',
                 'porphyrio', 'ballplayer', 'bullterrier', 'comfort', 'wool', 'cheeseburger', 'smith', 'cote',
                 'fringilla', 'church', 'penny', 'australian', 'skeeter', 'pineapple', 'squash', 'dinmont', 'loupe',
                 'ten', 'german', 'balustrade', 'armour', 'cuirass', 'fiddle', 'alsatian', 'marimba', 'langur', 'clock',
                 'cocker', 'dyke', 'border', 'armor', 'tower', 'flandres', 'obelisk', 'crab', 'iguana', 'beaker',
                 'pelican', 'medicine', 'pekinese', 'valley', 'widow', 'ladys', 'paper', 'off', 'dalmatian', 'billfish',
                 'projectile', 'streetcar', 'eatery', 'trolleybus', 'curtain', 'caretta', 'lock', 'quill', 'promontory',
                 'popsicle', 'tub', 'bell', 'sun', 'coyote', 'pearly', 'shaker', 'schnauzer', 'corgi', 'track',
                 'megalith', 'porcupine', 'coffee', 'bicycle', 'whorl', 'running', 'spaghetti', 'boa', 'mini',
                 'spiders', 'marmoset', 'blow', 'haversack', 'salt', 'earthstar', 'canis', 'transverse', 'strawberry',
                 'mailbag', 'candle', 'montifringilla', 'sliding', 'warrigal', 'erythrocebus', 'petrol', 't',
                 'chestnut', 'carpenters', 'hockey', 'stone', 'scabbard', 'trash', 'meat', 'whippet', 'lionfish',
                 'magnetic', 'jug', 'crane', 'horizontal', 'snowplough', 'disk', 'long', 'cellular', 'lupus', 'unit',
                 'thrasher', 'roundworm', 'ricksha', 'microwave', 'groom', 'crutch', 'whistle', 'buffalo', 'kakatoe',
                 'entertainment', 'keypad', 'river', 'jersey', 'lip', 'crotalus', 'cockroach', 'field', 'helmet',
                 'stove', 'penguin', 'chair', 'watch', 'oven', 'cavia', 'panpipe', 'ski', 'mongoose', 'welcome',
                 'partridge', 'sloth', 'gas', 'paperknife', 'paddlewheel', 'koala', 'carabid', 'grey', 'aepyceros',
                 'brabancon', 'clumber', 'japanese', 'necked', 'fowl', 'cart', 'wine', 'hip', 'globefish',
                 'combination', 'round', 'puck', 'rottweiler', 'ocarina', 'squeeze', 'car', 'snowmobile', 'chiton',
                 'mitten', 'broccoli', 'lollipop', 'poncho', 'lion', 'otterhound', 'pen', 'damselfly', 'cream', 'eater',
                 'lemon', 'power', 'laboratory', 'cab', 'snorkel', 'ruffed', 'trailer', 'jeep', 'potato', 'diaper',
                 'pongo', 'orangutang', 'barrel', 'foreland', 'dumbbell', 'bruin', 'bradypus', 'danaus', 'hippopotamus',
                 'mexicanus', 'bull', 'theater', 'prayer', 'jinrikisha', 'devilfish', 'pedestal', 'sandal', 'harvester',
                 'geyser', 'beigel', 'pong', 'lacewing', 'comic', 'platform', 'docking', 'filing', 'armadillo',
                 'plunger', 'bouviers', 'alaska', 'mosque', 'ovis', 'gong', 'beer', 'slipstick', 'chime', 'grouse',
                 'pigboat', 'orang', 'book', 'rv', 'drumstick', 'screen', 'backpack', 'chihuahua', 'bobtail', 'greater',
                 'pin', 'ladybeetle', 'cacatua', 'barracouta', 'signal', 'french', 'drop', 'barrow', 'canoe', 'sewing',
                 'remote', 'wreck', 'mactans', 'switch', 'home', 'dugon', 'tailed', 'tennis', 'file', 'coot',
                 'putorius', 'goldfinch', 'madagascar', 'nigripes', 'daddy', 'hanky', 'impala', 'dipper', 'bay',
                 'cinema', 'rock', 'cricket', 'lagopus', 'shade', 'snowplow', 'galerita', 'chambered', 'guenon',
                 'articulated', 'u', 'maraca', 'cot', 'worm', 'swab', 'lighter', 'carrion', 'typewriter', 'bakeshop',
                 'soap', 'samoyed', 'lhasa', 'spatula', 'whirligig', 'acoustic', 'urchin', 'taxi', 'vacuum', 'terrain',
                 'acinonyx', 'balusters', 'blocker', 'shako', 'cabinet', 'engine', 'soda', 'wrecker', 'upright',
                 'skunk', 'elkhound', 'maculatum', 'held', 'police', 'guinea', 'trombone', 'teller', 'agama',
                 'rucksack', 'patrol', 'roundabout', 'pool', 'soft', 'bird', 'adder', 'built', 'three', 'gorilla',
                 'confectionery', 'pot', 'macaque', 'arctic', 'roader', 'candy', 'siamang', 'wallet', 'modem',
                 'fountain', 'maria', 'suspectum', 'hypsiglena', 'shell', 'denim', 'hay', 'suit', 'yorkshire', 'altar',
                 'grasshopper', 'mower', 'screwdriver', 'shih', 'ring', 'polar', 'hylobates', 'tractor', 'ball',
                 'handkerchief', 'ground', 'handbasin', 'cockatoo', 'timber', 'spotted', 'motor', 'eskimo', 'seawall',
                 'web', 'coon', 'beaver', 'pay', 'ruler', 'couch', 'west', 'lantern', 'ananas', 'wallaby', 'shovel',
                 'blowfish', 'of', 'trunks', 'wheelbarrow', 'hussar', 'turtle', 'lycaon', 'carphophis', 'wild',
                 'speaker', 'leo', 'odometer', 'mashed', 'schipperke', 'gibbosus', 'cup', 'paling', 'cradle',
                 'sunblock', 'needle', 'chesapeake', 'sussex', 'teddy', 'latrodectus', 'killer', 'volute', 'fire',
                 'ship', 'rifle', 'platyhelminth', 'parachute', 'scope', 'leaf', 'monarch', 'collector', 'vale',
                 'backed', 'ciconia', 'missile', 'ibex', 'bottlecap', 'redshank', 'military', 'afghan', 'station',
                 'melursus', 'manufactured', 'waffle', 'naja', 'dung', 'kart', 'ant', 'moving', 'ambystoma',
                 'recreational', 'pan', 'dustcart', 'trench', 'lab', 'owl', 'entlebucher', 'espresso', 'refrigerator',
                 'hippo', 'collie', 'pencil', 'chain', 'rig', 'shades', 'torquata', 'basket', 'ridgeback', 'crossword',
                 'pictus', 'daisy', 'dockage', 'caerulea', 'wardrobe', 'linnet', 'dungeness', 'kit', 'armed', 'shoji',
                 'breakwater', 'rotisserie', 'drilling', 'flowerpot', 'diamondback', 'half', 'wing', 'short',
                 'camtschatica', 'elephant', 'tool', 'assault', 'spoon', 'gila', 'des', 'snowbird', 'pandean', 'heron',
                 'jacket', 'jacamar', 'grass', 'opener', 'balance', 'website', 'train', 'bib', 'lepisosteus',
                 'dispenser', 'ignitor', 'bookstall', 'dome', 'oboe', 'stoplight', 'plane', 'traffic', 'cypripedium',
                 'pygmaeus', 'sciurus', 'high', 'norwegian', 'speedboat', 'mierkat', 'planetarium', 'coil', 'green',
                 'membranophone', 'stinkhorn', 'star', 'academic', 'throne', 'vessel', 'safe', 'gazelle', 'wash',
                 'freight', 'park', 'pyrenees', 'bob', 'hotpot', 'bookcase', 'burrito', 'pretzel', 'briard', 'eastern',
                 'chest', 'christmas', 'cornutus', 'tent', 'tree', 'viridis', 'niloticus', 'tusker', 'leathery', 'ear',
                 'tick', 'conch', 'bighorn', 'saimiri', 'snow', 'mike', 'bedlington', 'mortarboard', 'warthog',
                 'insect', 'rabbit', 'handrail', 'coonhound', 'bassinet', 'blower', 'chameleon', 'rouge', 'dishwashing',
                 'dromedary', 'grille', 'egyptian', 'egis', 'thatched', 'toad', 'tram', 'dishrag', 'napkin', 'niger',
                 'homarus', 'baboon', 'carassius', 'swimming', 'cap', 'rugby', 'castle', 'vine', 'tricolor',
                 'ambulance', 'basin', 'maypole', 'shopping', 'coral', 'tigris', 'barbershop', 'interpres', 'rufus',
                 'footed', 'loafer', 'monitor', 'o', 'vestment', 'telescope', 'warragal', 'dandie', 'orca', 'yawl',
                 'coast', 'orangutan', 'atm', 'sheepdog', 'bassoon', 'maned', 'flatworm', 'brass', 'picket',
                 'woodworking', 'ailurus', 'groin', 'locomotive', 'bannister', 'tympan', 'syrup', 'stretcher',
                 'triturus', 'bullet', 'king', 'norwich', 'overskirt', 'landrover', 'puff', 'four', 'unicycle', 'ruddy',
                 'sabot', 'garpike', 'nappy', 'lar', 'lorry', 'polyporus', 'crayfish', 'cloak', 'polyplacophore',
                 'patas', 'glasses', 'cobaya', 'bearskin', 'sorrel', 'birdhouse', 'pitcher', 'american', 'bernard',
                 'horse', 'waggon', 'cathode', 'mantis', 'hog', 'bowl', 'tope', 'clog', 'carriage', 'saint', 'scorpion',
                 'bluetick', 'plexippus', 'pekingese', 'scooter', 'aid', 'mexicanum', 'woollen', 'cinereus', 'alp',
                 'llama', 'bikini', 'trump', 'jackfruit', 'submarine', 'toy', 'meerkat', 'patio', 'hound', 'spray',
                 'tow', 'pole', 'saw', 'reel', 'sawmill', 'hodometer', 'jellyfish', 'devils', 'apron', 'one', 'uncia',
                 'hack', 'bin', 'trucking', 'salamandra', 'giant', 'fan', 'picture', 'steam', 'newt', 'darning',
                 'badger', 'parviflorum', 'admiral', 'cash', 'photocopier', 'carbonara', 'drake', 'basketball',
                 'flagpole', 'truck', 'nile', 'standard', 'plumbers', 'hourglass', 'tramcar', 'carcharias', 'sleeping',
                 'hamper', 'hungarian', 'zucchini', 'siamese', 'rug', 'wire', 'rapeseed', 'weasel', 'strainer',
                 'helper', 'chimpanzee', 'frog', 'pad', 'convertible', 'bandit', 'stage', 'bathtub', 'poodle',
                 'loxodonta', 'automated', 'cd', 'oil', 'flamingo', 'virginia', 'respirator', 'buckeye', 'crawdad',
                 'coach', 'dust', 'siberian', 'sealyham', 'cucumber', 'hartebeest', 'mantid', 'trumpet', 'mousetrap',
                 'food', 'arenaria', 'site', 'garden', 'shooter', 'european', 'ballpoint', 'limousine', 'isopod',
                 'sidewinder', 'pardus', 'plectron', 'rose', 'dogsled', 'ipod', 'numbfish', 'combat', 'knapsack', 'box',
                 'scottish', 'patten', 'osseus', 'model', 'bouvier', 'weighing', 'minivan', 'robin', 'lolly', 'yurt',
                 'oncorhynchus', 'blue', 'ringlet', 'jetty', 'studio', 'fireboat', 'snooker', 'merganser', 'anemone',
                 'hatchet', 'concolor', 'ashcan', 'scottie', 'nursery', 'bar', 'case', 'washing', 'bonasa', 'tin',
                 'bubalus', 'redbone', 'mouth', 'foxhound', 'lipstick', 'chamaeleon', 'platypus', 'phascolarctos',
                 'lumbermill', 'knife', 'aramus', 'oscilloscope', 'notecase', 'diademata', 'pomeranian', 'washbowl',
                 'nigra', 'tundrarum', 'alligator', 'abacus', 'scale', 'cabbage', 'catamaran', 'bandeau', 'shoe',
                 'system', 'beagle', 'feather', 'jak', 'chocolate', 'african', 'chicken', 'lesser', 'bike', 'rocky',
                 'sweatshirt', 'aircraft', 'tile', 'rail', 'pyjama', 'matchstick', 'rule', 'swob', 'foumart', 'guitar',
                 'strix', 'table', 'catcher', 'gown', 'thresher', 'caldron', 'boxer', 'holocanthus', 'dustbin',
                 'tridactylus', 'wood', 'pie', 'palace', 'biro', 'africana', 'boathouse', 'jaguar', 'welsh', 'water',
                 'stick', 'frypan', 'maximus', 'disc', 'albus', 'affenpinscher', 'polecat', 'place', 'wombat',
                 'kisutch', 'rattlesnake', 'monastery', 'tricycle', 'knot', 'computer', 'lakeland', 'bison', 'coucal',
                 'cottontail', 'brittany', 'passerina', 'roach', 'confectionary', 'kite', 'billed', 'arabian', 'judges',
                 'purse', 'ice', 'man', 'electrical', 'aurantia', 'yellow', 'pocketbook', 'ounce', 'oxygen', 'cleaner',
                 'vest', 'safety', 'igniter', 'bus', 'milometer', 'tabby', 'mustela', 'brevicaudatus', 'six',
                 'ringneck', 'globe', 'alopex', 'sheep', 'race', 'northern', 'pickelhaube', 'fiddler', 'gallinule',
                 'starfish', 'lifeboat', 'restaurant', 'face', 'machine', 'radiator', 'poster', 'billiard', 'shuttle',
                 'crash', 'carcharodon', 'spider', 'silver', 'tiger', 'envelope', 'dromedarius', 'walkingstick',
                 'marmot', 'titi', 'milk', 'lemur', 'gyromitra', 'capucinus', 'barn', 'uniform', 'frondosa', 'mortar',
                 'onca', 'containership', 'sauce', 'jubatus', 'door', 'bullfrog', 'angora', 'anole', 'paddy', 'nail',
                 'packsack', 'groenendael', 'chow', 'sports', 'plough', 'cardoon', 'paintbrush', 'dining', 'centipede',
                 'cheetah', 'pickup', 'hyaena', 'lighthouse', 'geoffroyi', 'retriever', 'bobsled', 'plow', 'wall',
                 'mixing', 'cauliflower', 'neck', 'volleyball', 'brassiere', 'container', 'ptarmigan', 'movie',
                 'mileometer', 'viper', 'artichoke', 'albatross', 'jammies', 'violin', 'pussy', 'arctos', 'sulfur',
                 'theatre', 'labyrinth', 'leucocephalus', 'spotlight', 'buckle', 'anatinus', 'all', 'night', 'schooner',
                 'forklift', 'auratus', 'breasted', 'swing', 'potters', 'erithacus', 'sax', 'head', 'dermochelys',
                 'gordon', 'bubble', 'pointer', 'howler', 'two', 'army', 'offshore', 'harp', 'shark', 'plastic',
                 'fixed', 'terrace', 'vulture', 'structure', 'carton', 'ray', 'bubalis', 'jack', 'monocycle',
                 'internet', 'mole', 'eating', 'tray', 'mop', 'hen', 'nasalis', 'lycaenid', 'hammer', 'feeder', 'pig',
                 'quail', 'mouse', 'diver', 'ascaphus', 'panda', 'serrator', 'soccer', 'desktop', 'lavabo', 'headland',
                 'dhole', 'honeycomb', 'umbellus', 'python', 'white', 'mirror', 'magister', 'crate', 'tank',
                 'phalangium', 'turnstone', 'turdus', 'opera', 'goldfish', 'crinoline', 'wax', 'sundial', 'fitch',
                 'tan', 'bottle', 'hat', 'bunting', 'toilet', 'macaw', 'powder', 'constrictor', 'wireless', 'airship',
                 'russian', 'beacon', 'sport', 'threshing', 'moped', 'wok', 'brace', 'snake', 'seatbelt', 'echidna',
                 'chute', 'crampfish', 'husky', 'fox', 'blenheim', 'letter', 'light', 'struthio', 'parallel', 'vase',
                 'nebulosa', 'helix', 'seat', 'hair', 'drill', 'radio', 'indris', 'gar', 'cellphone', 'organ', 'ursus',
                 'samoyede', 'malemute', 'punch', 'padlock', 'sus', 'harvestman', 'urocyon', 'puma', 'magpie', 'mail',
                 'necklace', 'tripod', 'facility', 'printer', 'crested', 'conker', 'press', 'irroratus', 'windsor',
                 'fulgens', 'americana', 'carduelis', 'haired', 'balloon', 'coho', 'spike', 'atratus', 'cowboy',
                 'sydney', 'dike', 'automatic', 'agaric', 'salmon', 'spindle', 'slug', 'mississipiensis', 'pug', 'van',
                 'space', 'barbell', 'airliner', 'drier', 'bola', 'hopper', 'hermit', 'cobra', 'appenzeller',
                 'malamute', 'lorikeet', 'oyster', 'control', 'cebus', 'guillotine', 'whiskey', 'chlamydosaurus', 'gun',
                 'golden', 'keeshond', 'chainlink', 'mushroom', 'terrapin', 'lobster', 'kingi', 'mask', 'kingsnake',
                 'ox', 'crock', 'latrans', 'glasshouse', 'sweet', 'wrapper', 'busby', 'pillow', 'dowitcher', 'alpinus',
                 'bulletproof', 'golf', 'maltese', 'binder', 'wagon', 'horned', 'euarctos', 'bridge', 'microphone',
                 'hyena', 'football', 'polaroid', 'tobacco', 'hare', 'postbag', 'toed', 'ash', 'coriacea', 'maillot',
                 'amphibius', 'wolf', 'melampus', 'poke', 'plate', 'dough', 'americanus', 'claw', 'woolen', 'marsh',
                 'r.v.', 'teapot', 'pajama', 'chainsaw', 'stocking', 'stork', 'stole', 'cicala', 'cliff', 'tortoise',
                 'proboscis', 'player', 'doormat', 'sandpiper', 'robe', 'icebox', 'sea', 'eagle', 'vulgaris', 'groyne',
                 'sand', 'granny', 'mink', 'tarantula', 'dog', 'malinois', 'torch', 'lamp', 'alpina', 'pick', 'cohoe',
                 'cover', 'pinwheel', 'bed', 'puzzle', 'sharpener', 'punchball', 'cello', 'old', 'brown', 'goblet',
                 'haliaeetus', 'melanoleuca', 'kelpie', 'limo', 'jigsaw', 'wastebin', 'for', 'doberman', 'bench',
                 'gibbon', 'longicorn', 'library', 'woods', 'velvet', 'persian', 'bag', 'pump', 'sombrero', 'hunting',
                 'scotch', 'mamba', 'leatherback', 'liner', 'monkey', 'walking', 'minibus', 'axolotl', 'pjs', 'little',
                 'hook', 'footstall', 'holothurian', 'pail', 'cinereoargenteus', 'binoculars', 'garbage', 'garfish',
                 'springer', 'tup', 'gondola', 'bakehouse', 'meter', 'hautbois', 'grocery', 'scrofa', 'cuon',
                 'ornithorhynchus', 'fireguard', 'felis', 'bookstore', 'egret', 'grampus', 'bra', 'emmet', 'fish',
                 'pirate', 'scuba', 'thunder', 'croquet', 'wheaten', 'tench', 'belt', 'prison', 'argiope', 'maker',
                 'ursinus', 'hotdog', 'iron', 'hoopskirt', 'piggy', 'loudspeaker', 'chiffonier', 'nautilus',
                 'television', 'corkscrew', 'camel', 'scoreboard', 'whale', 'chrysanthemum', 'notebook', 'desk',
                 'lizard', 'erolia', 'crib', 'komodo', 'maze', 'lynx', 'reaper', 'loaf', 'clothes', 'land', 'butterfly',
                 'ai', 'stopwatch', 'crawdaddy', 'dirigible', 'varanus', 'breastplate', 'mat', 'sebae', 'passenger',
                 'bars', 'slide', 'psittacus', 'catamount', 'ateles', 'migratorius', 'zebra', 'tie', 'crocodylus',
                 'araneus', 'packet', 'revolver', 'armoured', 'sarong', 'komodoensis', 'lawn', 'telephone', 'syrinx',
                 'oxcart', 'jean', 'sulphur', 'seacoast', 'beach', 'trui', 'pembroke', 'dishwasher', 'foulmart',
                 'kerry', 'attack', 'tee', 'spiny', 'red', 'bakery', 'milkweed', 'quilt', 'anolis', 'wooden', 'rocker',
                 'grand', 'beasts', 'mountain', 'frilled', 'asp', 'band', 'wig', 'heloderma', 'consomme', 'dragonfly',
                 'cougar', 'keyboard', 'estate', 'steel', 'leopard', 'ladle', 'crt', 'electric', 'indian', 'ladybird',
                 'essence', 'galeocerdo', 'seashore', 'orcinus', 'catta', 'mastiff', 'cygnus', 'microcomputer',
                 'lotion', 'fig', 'warplane', 'indigo', 'toyshop', 'racer', 'stingray', 'bonnet', 'piano', 'butcher',
                 'eraser', 'chrysomelid', 'grunter', 'leafhopper', 'cro', 'panther', 'bookshop', 'pill', 'street',
                 'indri', 'beetle', 'paddle', 'shield', 'can', 'eggnog', 'volcano', 'furnace', 'filter', 'lens',
                 'tablet', 'dragon', 'basenji', 'merry', 'swiss', 'triceratops', 'mollymawk', 'bath', 'kimono', 'cell',
                 'analog', 'crocodile', 'colobus', 'ewer', 'cleaver', 'dish', 'capuchin', 'dam', 'thatch', 'market',
                 'tzu', 'day', 'pack', 'pufferfish', 'cuke', 'fence', 'finch', 'memorial', 'washbasin', 'dugong',
                 'pizza', 'ibizan', 'violoncello', 'lacerta', 'camelus', 'the', 'cavaticus', 'syndactylus', 'totem',
                 'meatloaf', 'china', 'semi', 'monster', 'bank', 'chamaeleo', 'gallon', 'catesbeiana', 'broom',
                 'egretta', 'grifola', 'viaduct', 'staffordshire']
    WordVector.query.delete()
    db.session.commit()
    fname = os.path.join(os.getcwd(), 'application/ml', 'wiki-news-300d-1M-subword.vec')
    count = 0;
    with open(fname) as fp:
        res = fp.readline()
        while True:
            res = fp.readline()
            if not res:
                break;
            res = res.split()
            w, wv = res[0], []
            if w not in word_list:
                continue;
            for idx in range(1, len(res)):
                wv.append(float(res[idx]))
            wv_obj = WordVector(w, wv)
            count = count + 1
            if count % 10 == 0:
                db.session.commit()
                print('Commit!')
            db.session.add(wv_obj)
            print('Added:', count)
    print('Done!', count)
    db.session.commit()
    print('Commit!')
    file = open('team.json', 'r')
    team = json.load(file)
    return render_template('about.html', about=True, team=team)


@app.route("/show_vectors", methods=['GET'])
def show_word_vectors():
    res = WordVector.query.all()
    print(res)
    flash('Vectors!', 'success')
    file = open('team.json', 'r')
    team = json.load(file)
    return render_template('about.html', about=True, team=team)


@app.errorhandler(Exception)
def all_exception_handler(e):
    if hasattr(e, 'code') and e.code and isinstance(e.code, int):
        return render_template("error.html", error=e), e.code
    return render_template("error.html", error=e), 500
