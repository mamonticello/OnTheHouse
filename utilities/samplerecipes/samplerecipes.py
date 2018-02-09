import recipedb

from voussoirkit import pathclass
image_dir = pathclass.Path(__file__).parent.with_child('sample_images')

rdb = recipedb.RecipeDB()

angela = rdb.new_user(
    username = "A",
    display_name = "Angela",
    password = "A",
    bio_text = "Hello! This is a sample biography for Angela.",
    profile_image = rdb.new_image(image_dir.with_child('angel_cake.jpg'))
)

bob = rdb.new_user(
    username = "B",
    display_name = "Bob",
    password = "A",
    bio_text = "Hello! This is a sample biography for Bob.",
    profile_image = rdb.new_image(image_dir.with_child('homemade_pizza.jpg'))
)

caitlyn = rdb.new_user(
    username = "C",
    display_name = "Caitlyn",
    password = "A",
    bio_text = "Hello! This is a sample biography for Caitlyn.",
    profile_image = rdb.new_image(image_dir.with_child('meringue.jpg'))
)

anonymous = rdb.new_user(
    username='anon',
    display_name='Rainbowman',
    password='A',
    bio_text='You cant touch me.',
    profile_image=None,
)

# 1
instructions = '''
Soften cream cheese and Brie cheese.

For pesto, in a blender container combine basil, parsley, Parmesan cheese,
almonds, garlic, and 2 tablespoons oil. Cover; blend with on-off turns till a
paste forms. Gradually add remaining oil, blending on low speed till smooth.

Beat cream cheese and Brie together till nearly smooth. Beat whipping cream till
soft peaks form. Fold whipped cream into cheese mixture.

Line a 3 1/2- or 4-cup mold with plastic wrap. Spread one-fourth of cheese
mixture into mold. Top with one-third of pesto. Repeat layers twice. Top with
cheese mixture. Chill 6 to 24 hours.

To serve, unmold on plate. Remove plastic wrap. Garnish with fresh basil, if
desired. Serve with crackers.
'''
rdb.new_recipe(
    author=angela, #author="Better Homes and Gardens",
    blurb="This spread goes well with crackers or slided French bread.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["cream cheese",
               "Brie cheese",
               "basil",
               "parsley",
               "Parmesan cheese",
               "almonds",
               "garlic",
               "olive oil",
               "whipping cream"],
    instructions=instructions,
    meal_type="Appetizer",
    name="Cheese and Pesto Spread",
    prep_time=10,
    serving_size=24,
    recipe_image=rdb.new_image(image_dir.with_child('cheese_pesto.jpg')),
)

# 2
blurb = '''
Need an egg dish for breakfast? Make these veggie stuffed omeletes that are
ready in just 15 minutes.
'''
instructions = '''
In 8-inch nonstick skillet, heat oil over medium-high heat. Add bell pepper,
onion and mushrooms to oil. Cook 2 minutes, stirring frequently, until onion is
tender. Stir in spinach; continue cooking and stirring just until spinach wilts.
Remove vegetables from pan to small bowl.

In medium bowl, beat egg product, water, salt and pepper with fork or whisk
until well mixed. Reheat same skillet over medium-high heat. Quickly pour egg
mixture into pan. While sliding pan back and forth rapidly over heat, quickly
stir with spatula to spread eggs continuously over bottom of pan as they
thicken. Let stand over heat a few seconds to lightly brown bottom of omelet.
Do not overcook; omelet will continue to cook after folding.

Place cooked vegetable mixture over half of omelet; top with cheese. With
spatula, fold other half of omelet over vegetables. Gently slide out of pan onto
plate. Serve immediately.
'''
rdb.new_recipe(
    author=bob, #author="Betty Crocker",
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["olive oil",
               "red bell pepper",
               "onion",
               "mushroom",
               "spinach",
               "egg",
               "water",
               "salt",
               "pepper",
               "Cheddar cheese"],
    instructions=instructions,
    meal_type="Breakfast",
    name="Veggie Stuffed Omelete",
    prep_time=15,
    serving_size=1,
    recipe_image=rdb.new_image(image_dir.with_child('veggie_stuffed_omelette.jpg')),
)

# 3
blurb = '''
A great recipe for homemade pizza dough and sauce. The sauce is especially good.
Top with whatever you like.
'''
instructions = '''
In a small bowl, dissolve yeast in warm water.
Let stand until creamy, about 10 minutes.

In a large bowl, combine flour, salt and shortening. Stir in the yeast mixture.
When the dough has pulled together, turn it out onto a lightly floured surface,
and knead until smooth and elastic, about 8 minutes. Lightly oil a large bowl,
place the dough in the bowl, and turn to coat with oil. Cover with a damp cloth,
and let rise in a warm place until doubled in volume, about 45 minutes.

Heat oil in a small saucepan over medium heat. Saute onion until tender.
Stir in tomato paste and water. Season with sugar, salt, black pepper, garlic
powder, basil, oregano, marjoram, cumin, chili powder and red pepper flakes.
Simmer 15 to 20 minutes.

Recipe makes 2 (12 inch) pizzas. Divide dough in half, and spread onto pizza
pans. Cover with sauce, and desired toppings. Bake at 400 degrees for 20
minutes, or until crust is golden brown.
'''
rdb.new_recipe(
    author=caitlyn, #author="Mike",
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["dry yeast",
               "water",
               "all-purpose flour",
               "salt",
               "shortening",
               "vegetable oil",
               "onion",
               "tomato paste",
               "white sugar",
               "black pepper",
               "garlic powder",
               "basil",
               "oregano",
               "marjoram",
               "cumin",
               "chili powder",
               "red pepper flake"],
    instructions=instructions,
    meal_type="Anytime",
    name="Mike's Homemade Pizza",
    prep_time=90,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('homemade_pizza.jpg')),
)

# 4
instructions = '''
To make the churro dough: Combine 1 cup of water with the butter or margarine
and the salt in a saucepan and bring to a boil over high heat. Using a wooden
spoon, stir in flour. Reduce the heat to low and stir vigorously until the
mixture forms a ball, about 1 minute. Remove the dough from the heat and, while
stirring constantly, gradually beat the eggs into the dough.

To make the chocolate for dunking: In a small bowl, dissolve the cornstarch in
1 cup of milk and reserve. Combine the chocolate with the remaining cup of milk
in a saucepan. Stirring constantly, melt the chocolate over medium-low heat.
Whisk the sugar and the dissolved cornstarch into the melted chocolate mixture.
Reduce the heat to low and cook, whisking constantly, until the chocolate is
thickened, about 5 minutes. (Add extra cornstarch if it doesn't start to thicken
    after 5 minutes.) Remove the pan from the heat and whisk until smooth then
reserve in a warm place.

Heat about 2 inches of oil in a heavy, high-sided pot over medium-high heat
until the oil reaches 360 degrees F. Mix the sugar with the cinnamon on a plate
and reserve.

Meanwhile, spoon the churro dough into a pastry bag fitted with a large tip.
Squeeze a 4- inch strip of dough into the hot oil. Repeat, frying 3 or 4 strips
at a time. Fry the churros, turning them once, until golden brown, about 2
minutes per side. Transfer the cooked churros to a plate lined with paper towels
to drain.

When the churros are just cool enough to handle, roll them in the cinnamon-sugar
(in Spain churros are simply rolled in sugar.)

Pour the chocolate into individual bowls or cups. Serve the warm churros with
the chocolate dip.
'''
rdb.new_recipe(
    author=angela, #author="Food Network",
    blurb="Recipe courtesy of Chocolateria San Gines",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["water",
               "butter",
               "salt",
               "all-purpose flour",
               "egg",
               "vegetable oil",
               "sugar",
               "cinnamon",
               "cornstarch",
               "milk",
               "dark chocolate"],
    instructions=instructions,
    meal_type="Dessert",
    name="Churros",
    prep_time=40,
    serving_size=10,
    recipe_image=rdb.new_image(image_dir.with_child('churro.jpg')),
)

# 5
instructions = '''
Place a nori sheet lengthwise on a bamboo rolling mat, shiny-side down.
Position the sheet about 1-inch from the edge of the mat closest to you and 
eave some of the bamboo mat exposed on either side of the nori sheet. Wet your
hands in cool water and take a handful of sushi rice. Place the rice in the
center of the nori and use your fingers to spread the rice evenly over the nori.
Be sure to leave a 3/4-inch strip of nori uncovered on the far side. Place tuna
strips and some julienne vegetable, cucumber or avocado along the center of the
rice. Be careful not to overfill the nori. Place your fingertips over the fillings
to hold them in place. Then, use your thumbs to lift up the edge of the bamboo 
rolling mat closest to you. Begin rolling the mat away from you, while applying
pressure to the fillings to keep the roll firm. Roll the mat over slowly until
it covers the rice and the near and far sides of rice join, still leaving the
3/4-inch strip of nori, rice-free, exposed. While holding the bamboo mat in
position, apply pressure to the roll with your fingers to make the roll firm.
Slice the roll in half, then cut both rolls twice to make 6 equal sized pieces.
Repeat this process with the salmon and various fillings, nori and rice.

Rinse the rice in cold water while stirring briskly to remove any dirt. Drain
the rice completely. Place the rice and the 6 cups of water in a medium sized
saucepan and cover it with a tight fitting lid. Bring the water to a boil over
medium heat. Allow the water to boil for 3 minutes and then reduce the heat to
low and continue cooking 15 minutes without removing the lid. Remove the rice
from the heat and remove the lid (the water should no longer be visible). Turn
the rice out evenly on a well-greased cookie sheet using a spatula or rice
paddle. Sprinkle the rice with the vinegar, sugar, and salt while mixing with a
spatula or rice paddle until the rice reaches body temperature. Keep the rice
covered with damp paper towels or napkin until the rice is ready to use.
'''
rdb.new_recipe(
    author=bob, #author="Food Network",
    blurb="Recipe courtesy of Jill Davie",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["nori",
               "sushi rice",
               "tuna",
               "salmon",
               "cucumber",
               "carrot",
               "avocado",
               "water",
               "rice vinegar",
               "sugar",
               "salt"],
    instructions=instructions,
    meal_type="Anytime",
    name="Sushi",
    prep_time=55,
    serving_size=30,
    recipe_image=rdb.new_image(image_dir.with_child('sushi.jpg')),
)

# 6
instructions = '''
Place a nori sheet lengthwise on a bamboo rolling mat, shiny-side down.
Position the sheet about 1-inch from the edge of the mat closest to you and
leave some of the bamboo mat exposed on either side of the nori sheet. Wet your
hands in cool water and take a handful of sushi rice. Place the rice in the
center of the nori and use your fingers to spread the rice evenly over the nori.
Be sure to leave a 3/4-inch strip of nori uncovered on the far side. Place tuna
strips and some julienne vegetable, cucumber or avocado along the center of the
rice. Be careful not to overfill the nori. Place your fingertips over the
fillings to hold them in place. Then, use your thumbs to lift up the edge of
the bamboo rolling mat closest to you. Begin rolling the mat away from you, while
applying pressure to the fillings to keep the roll firm. Roll the mat over
slowly until it covers the rice and the near and far sides of rice join, still
leaving the 3/4-inch strip of nori, rice-free, exposed. While holding the bamboo
mat in position, apply pressure to the roll with your fingers to make the roll
firm. Slice the roll in half, then cut both rolls twice to make 6 equal sized
ieces. Repeat this process with the salmon and various fillings, nori and rice.

Rinse the rice in cold water while stirring briskly to remove any dirt.
Drain the rice completely. Place the rice and the 6 cups of water in a medium
sized saucepan and cover it with a tight fitting lid. Bring the water to a boil
over medium heat. Allow the water to boil for 3 minutes and then reduce the heat
to low and continue cooking 15 minutes without removing the lid. Remove the rice
from the heat and remove the lid (the water should no longer be visible). Turn
the rice out evenly on a well-greased cookie sheet using a spatula or rice
paddle. Sprinkle the rice with the vinegar, sugar, and salt while mixing with a
spatula or rice paddle until the rice reaches body temperature. Keep the rice
covered with damp paper towels or napkin until the rice is ready to use.
'''
rdb.new_recipe(
    author=caitlyn, #author="Food Network",
    blurb="Recipe courtesy of Jill Davie",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["nori",
               "sushi rice",
               "tuna",
               "salmon",
               "cucumber",
               "carrot",
               "avocado",
               "water",
               "rice vinegar",
               "sugar",
               "salt"],
    instructions=instructions,
    meal_type="Anytime",
    name="Sushi Rolls",
    prep_time=55,
    serving_size=30,
    recipe_image=rdb.new_image(image_dir.with_child('sushi_roll.jpg')),
)

# 7
blurb = '''
Sauerkraut is probably the most well-known lacto-fermented vegetable.
Like any traditionally homemade food, sauerkraut can be made in a number of
ways. Even if each kraut-making method is different there are a few common
basics to remember when fermenting sauerkraut at home.
'''
instructions = '''
Chop or shred cabbage. Sprinkle with salt.

Knead the cabbage with clean hands, or pound with a potato masher or Cabbage
Crusher about 10 minutes, until there is enough liquid to cover.

Stuff the cabbage into a quart jar, pressing the cabbage underneath the liquid.
If necessary, add a bit of water to completely cover cabbage.

Cover the jar with a tight lid, airlock lid, or coffee filter secured with a
rubber band.

Culture at room temperature (60-70F is preferred) for at least 2 weeks until
desired flavor and texture are achieved. If using a tight lid, burp daily to
release excess pressure.

Once the sauerkraut is finished, put a tight lid on the jar and move to cold
storage. The sauerkraut's flavor will continue to develop as it ages.
'''
rdb.new_recipe(
    author=angela, #author="Cultures for Health",
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["cabbage",
               "sea salt"],
    instructions=instructions,
    meal_type="Anytime",
    name="Homemade Sauerkraut",
    prep_time=10,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('sauerkraut.jpg')),
)

# 8
instructions = '''
In a large heavy saucepan mix eggs, milk, and 1/3 cup sugar. Cook and stir over
medium heat till mixture coats a metal spoon. Remove from heat. Cool quickly by
placing pan in a sink or bowl of ice water and stirring 1 to 2 minutes. Stir in
rum, bourbon, and vanilla. Chill 4 to 24 hours.

At serving time, in a bowl whip cream and 2 tablespoons sugar till soft peaks
form. Transfer chilled egg mixture to a punch bowl. Fold in whipped cream
mixture. Serve at once. Sprinkle each serving with nutmeg.
'''
rdb.new_recipe(
    author=bob, #author="Better Homes and Gardens",
    blurb="Always a hit at our annual staff Christmas party.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["egg",
               "milk",
               "sugar",
               "light rum",
               "bourbon",
               "vanilla",
               "whipping cream",
               "sugar",
               "nutmeg"],
    instructions=instructions,
    meal_type="Drink",
    name="Eggnog",
    prep_time=15,
    serving_size=10,
    recipe_image=rdb.new_image(image_dir.with_child('eggnog.jpg')),
)

# 9
instructions = '''
Preheat the oven to 350 F. Bring egg whites to room temperature. Sift powdered
sugar and flour together 3 times. In a large bowl beat egg whites, cream of
tartar, and vanilla with an electric mixer on medium speed till soft peaks form
(tips curl). Gradually add sugar, about 2 tablespoons at a time, beating till
stiff peaks form (tips stand straight).

Sift about one-fourth of the flour mixture over beaten egg whites; fold in
gently. (If bowl is too full, transfer to a larger bowl.) Repeat, folding in
remaining flour mixture by fourths.

Pour into an ungreased 10-inch tube pan. Bake on the lowest rack in a 350 F
oven for 40 to 45 minutes or until top springs back when lightly touched.
Immediately invert cake (leave in pan); cook thoroughly. Loosen sides of cake
from pan; remove cake.
'''
rdb.new_recipe(
    author=caitlyn, #author="Better Homes and Gardens",
    blurb="Eat your cake and diet, too. Angel Cake is low in calories and has no fat.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["egg white",
               "powdered sugar",
               "cake flour",
               "cream of tartar",
               "vanilla",
               "sugar"],
    instructions=instructions,
    meal_type="Dessert",
    name="Angel Cake",
    prep_time=60,
    serving_size=12,
    recipe_image=rdb.new_image(image_dir.with_child('angel_cake.jpg')),
)

# 10
blurb = '''
This recipe has been handed down from my mother.
It is a family favorite and will not be replaced! (Definite husband pleaser!)
'''
instructions = '''
Combine ground beef, onion, garlic, and green pepper in a large saucepan.
Cook and stir until meat is brown and vegetables are tender. Drain grease.

Stir diced tomatoes, tomato sauce, and tomato paste into the pan.
Season with oregano, basil, salt, and pepper. Simmer spaghetti sauce for 1 hour,
stirring occasionally.
'''
rdb.new_recipe(
    author=angela, #author="Hank's Mom",
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["beef",
               "onion",
               "garlic",
               "green bell pepper",
               "tomato",
               "tomato sauce",
               "tomato paste",
               "oregano",
               "basil",
               "salt",
               "black pepper"],
    instructions=instructions,
    meal_type="Dinner",
    name="Spaghetti Sauce with Ground Beef",
    prep_time=85,
    serving_size=6,
    recipe_image=rdb.new_image(image_dir.with_child('spaghetti_sauce.jpg')),
)

# 11
blurb = '''
This is a very fun recipe to follow, because Grandma makes it sweet and simple.
This pie is thickened with cornstarch and flour in addition to egg yolks, and
contains no milk.
'''
instructions = '''
Preheat oven to 350 degrees F (175 degrees C).

To Make Lemon Filling: In a medium saucepan, whisk together 1 cup sugar, flour,
cornstarch, and salt. Stir in water, lemon juice and lemon zest. Cook over
medium-high heat, stirring frequently, until mixture comes to a boil. Stir in
butter. Place egg yolks in a small bowl and gradually whisk in 1/2 cup of hot
sugar mixture. Whisk egg yolk mixture back into remaining sugar mixture.
Bring to a boil and continue to cook while stirring constantly until thick.
Remove from heat. Pour filling into baked pastry shell.

To Make Meringue: In a large glass or metal bowl, whip egg whites until foamy.
Add sugar gradually, and continue to whip until stiff peaks form. Spread
meringue over pie, sealing the edges at the crust.

Bake in preheated oven for 10 minutes, or until meringue is golden brown.
'''
rdb.new_recipe(
    author=bob, #author="Emilie S.",
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["white sugar",
               "all-purpose flour",
               "cornstarch",
               "salt",
               "water",
               "lemon",
               "butter",
               "egg yolk",
               "pie crust",
               "egg white"],
    instructions=instructions,
    meal_type="Dessert",
    name="Grandma's Lemon Meringue",
    prep_time=40,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('meringue.jpg')),
)

# 12
instructions = '''
Spritz 2 pieces of newspaper lightly with vegetable oil and place in the bottom
of a charcoal chimney starter. Fill the chimney starter with natural chunk
charcoal, 2 to 3 pounds, and set on the charcoal grate of a kettle grill until
hot and ashy, approximately 15 to 20 minutes.

Meanwhile, butter the bread slices on each side. Combine the cheeses, mustard,
paprika and pepper in small bowl.

Fold a long (24-inches) piece of heavy-duty aluminum foil in half. Set a large
metal griddle spatula in the center and fold the sides up around the spatula,
forming a tray. Spritz the spatula-tray with vegetable oil. Repeat with a second
piece of aluminum foil and another griddle spatula. Divide the cheese mixture
evenly between the spatula-trays, and set aside. Set aside two additional
15-inch sheets of heavy-duty aluminum foil.

Carefully and distribute the hot charcoal onto one side of the charcoal grate.
Set the cooking grate in place and heat for 2 to 3 minutes.

Set the cheese-filled spatula-trays on the grill over indirect heat. Cook for
6 to 9 minutes or until the cheese melts and bubbles around the edges. You may
have to adjust the placement of the spatula-trays to ensure even melting and
keep the cheese from overheating and breaking.

Grill the bread for 1 to 2 minutes per side over direct heat.

Place 1 slice of bread on each of the reserved sheets of aluminum foil. Pour
off excess grease into a bowl, if desired, then drizzle one spatula’s worth of
cheese onto one slice of bread and top with the a second slice of bread. Fold
the foil around the sandwich. Repeat with remaining cheese and bread slices,
and then return the sandwich packets to the grill over indirect heat for 1 to
2 minutes.

Unwrap and serve immediately.
'''
rdb.new_recipe(
    author=caitlyn, #author="Alton Brown",
    blurb="This grilled cheese sandwich recipe actually grills the cheese.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["country bread",
               "butter",
               "extra sharp Cheddar cheese",
               "Gruyere cheese",
               "dry mustard",
               "smoked paprika",
               "black pepper",
               "egg yolk",
               "pie crust",
               "egg white"],
    instructions=instructions,
    meal_type="Lunch",
    name="Grilled Grilled Cheese",
    prep_time=30,
    serving_size=2,
    recipe_image=rdb.new_image(image_dir.with_child('grilled_cheese.jpg')),
)

# 13
blurb = '''
If you love good, old fashioned mashed potatoes this is the perfect recipe.
Simple and delicious.
'''
instructions = '''
Bring a pot of salted water to a boil. Add potatoes and cook until tender but
still firm, about 15 minutes; drain.

In a small saucepan heat butter and milk over low heat until butter is melted.
Using a potato masher or electric beater, slowly blend milk mixture into
potatoes until smooth and creamy. Season with salt and pepper to taste.
'''
rdb.new_recipe(
    author=angela, #author="Esmee Williams",
    blurb=blurb,
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["potato",
               "butter",
               "milk",
               "salt",
               "pepper"],
    instructions=instructions,
    meal_type="Dinner",
    name="Basic Mashed Potatoes",
    prep_time=35,
    serving_size=4,
    recipe_image=rdb.new_image(image_dir.with_child('mashed_potatoes.jpg')),
)

# 14
instructions = '''
Cut margarine into thirds and bring it to room temperature. In the top of a
double boiler combine egg yoolk, water, lemon juice, pepper, and dash salt.
Add one piece of the margarine. Place over boiling water (upper pan should not
    touch water). Cook, stirring rapidly, till margarine melts and sauce begins
to thicken.

Add the remaining margarine, a piece at a time, stirring constantly. Cook and
stir till sauce thickens (1 to 2 minutes). Immediately remove from heat.
If sauce is too thick or curdles, immediately beat in 1 to 2 tablespoons hot
tap water. Serve the sauce with cooked vegetables, pultry, fish, or eggs.
'''
rdb.new_recipe(
    author=bob, #author="Better Homes and Gardens",
    blurb="A classic creamy sauce with a rich lemon flavor.",
    country_of_origin="Unknown",
    cuisine="Unknown",
    ingredients=["margarine",
               "egg yolk",
               "water",
               "lemon juice",
               "pepper"],
    instructions=instructions,
    meal_type="Sauce",
    name="Hollandaise Sauce",
    prep_time=20,
    serving_size=8,
    recipe_image=rdb.new_image(image_dir.with_child('hollandaise.jpg')),
)
