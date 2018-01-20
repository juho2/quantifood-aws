# mod these to get minimum working version
# recipe_matrix to another (numeric) DB table? ->only needed on DB update
import time
import numpy as np

from postgres_IO import *

from .models import Food

# NB. db info now coming from postgres_IO !

# recipe_matrix nutrient cols are in alphabetical order
foodcom_target = {'208':2000.,
                  '205':300.,
                  '601':300.,
                  '204':65.,
                  '291':25.,
                  '203':50.,
                  '606':20.,
                  '307':2400.,                  
                  '269':25.,
                  }
nutrient_conv_foodcom = {'calories':'208',
                         'carbohydrate':'205',
                         'cholesterol':'601',
                         'fat':'204',
                         'fiber':'291',
                         'protein':'203',
                         'saturatedfat':'606',
                         'sodium':'307',
                         'sugar':'269'
                         }
initial_target = [foodcom_target[key] for key in [nutrient_conv_foodcom[key2] for key2 in sorted(nutrient_conv_foodcom)]]

def make_recipe_matrix_from_postgres(cur):
    t = time.time()
    cur.execute("SELECT id_string,nutrients FROM recommender_food")
    tuplelist = cur.fetchall()
    recipe_ids = [item[0] for item in tuplelist] # will be in ascending order
    nut_dicts = [item[1] for item in tuplelist]
    recipe_matrix = np.zeros([len(recipe_ids), len(nut_dicts[0])])
    for rownum, nut_dict in zip(range(len(nut_dicts)), nut_dicts):
        nutlist = [nut_dict[key][0] for key in sorted(nut_dict)]
        row = np.asarray(nutlist).astype(np.float)
        recipe_matrix[rownum,:] = row
#    print(str(recipe_matrix.shape[0]) + ' rows, ' + str(recipe_matrix.shape[1]) + \
#    ' columns constructed in ' + str(time.time()-t) + ' s')
    return(recipe_ids, recipe_matrix)
 
def insert_recipe_matrix_to_postgres(recipe_matrix, cur):
#    print(str(recipe_matrix.shape[0]) + ' rows, ' + str(recipe_matrix.shape[1]) + \
#    ' columns inserted in ' + str(time.time()-t) + ' s')    
    pass

def get_recipe_matrix_from_postgres(cur):
    pass
   
def filter_recipes(recipe_matrix, banned_keywords, banned_recipes):
    #return(filtered_recipe_matrix)
    pass

def rate_recipes(recipe_matrix, target, rating_constant=20):
    """ Ratings wrt. other recipes in DB (1 serving). """
    # target is recommended daily intake
    target_vector = np.asarray(target)
    nutrient_weights = np.ones(len(target_vector)) # TBD reasonable weights
    target_vector *= nutrient_weights
    # relative errors
    errors = np.sum(np.power((recipe_matrix - target_vector)/target_vector, 2), axis=1)
    errors /= np.max(errors)
    # foods rated relative to rating_constant (%) best foods
    rating_constant = len(errors) * (100 - rating_constant) // 100
    min_errors = sorted(list(errors))[:rating_constant]
    ratings = 100 * (1 - errors/np.max(min_errors)) # worst 100-rating_constant % of foods will be negative
#    print(sorted(ratings)[-10:])
    return(ratings)

def recommend_foods(recipe_index, ratings, pos = (0,9)):
    recommended = {}
    best_indices = ratings.argsort()[-len(ratings):][::-1]
    best_IDs = []
#    print('Recommeded:')
    for index in best_indices[pos[0]:pos[1]]:
        recipe_id = sorted(recipe_index)[index]
        best_IDs.append(recipe_id)
        recommended[recipe_id] = ratings[index]
        print(str(round(ratings[index],1)) + ' % rated ' + recipe_index[recipe_id])
    return(recommended, best_IDs)



 
conn, cur = open_DB(DB_NAME, DB_USER)
recipe_ids, recipe_matrix = make_recipe_matrix_from_postgres(cur)
commit_and_close_DB(conn, cur)    
target = initial_target
ratings = rate_recipes(recipe_matrix, target)


    

    
def eat_food(local_path, recipe_index, old_target, nutrient_history, nut_conv, choice='random'):
    """ Calculate nutrients consumed (per day) based on user input (food history). """
    nutrients_consumed = {}
    recipe_path = local_path + 'recipes\\'
    if choice == 'random':
        files = []
        for file in os.listdir(recipe_path):
            files.append(file)
        file = random.choice(files)
        print('Random_user ate a serving of ' + recipe_index[file.split('.')[0]])
    else:
        eat_ID = random.choice(choice) # random food from top recommended
        file = eat_ID + '.txt'
        print('Smart_user ate a serving of ' + recipe_index[file.split('.')[0]])
    with open(recipe_path + file) as f:
        recipe = json.load(f)
    for nutrient in recipe['nutrients']:
        nut_id = nut_conv[nutrient]
        nutrients_consumed[nut_id] = float(recipe['nutrients'][nutrient][0])
    nutrient_history.append(nutrients_consumed)
    new_target = update_target(old_target, nutrients_consumed)
    return(nutrient_history, new_target)

def update_target(old_target, nutrients_consumed):
    new_target = {}
    for nutrient in old_target:
        if nutrient in nutrients_consumed:
            new_target[nutrient] = old_target[nutrient] - nutrients_consumed[nutrient]
    return(new_target)
    
def plot_single(nutrient_history, nutrient_list, daily_target, ID):
    index, meal_no = 0, []
    amounts = np.zeros(len(nutrient_history))
    for meal in nutrient_history:
        #index = nutrient_history.index(meal)
        meal_no.append(index + 1)
        if ID in meal and index > 0:
            amounts[index] = amounts[index-1] + meal[ID]
        else:
            amounts[index] = 0
        index += 1
    target_amount = np.ones(len(nutrient_history)) * daily_target[ID]
    
    plt.plot(meal_no, amounts)
    plt.plot(meal_no, target_amount, '--')
    leg = [nutrient_list[ID][0] + ' (' + nutrient_list[ID][1] + ')']
    leg.append('Recommended intake ' + ' (' + nutrient_list[ID][1] + ')')
    plt.legend(leg, loc=2, prop={'size':10})
    plt.xlabel('Meal number')
    plt.ylabel('Nutrient consumed')
#    plt.xticks(range(1, len(meal_no)))
    plt.show()
    return()

def plot_foodcom_nutrients(nutrient_history, nutrient_list, daily_target):
    plt.figure(figsize=(16,9))
    index = 1
    for ID in daily_target:
        plt.subplot(3,3,index)
        plot_single(nutrient_history, nutrient_list, daily_target, ID)
        index += 1

def plot_history(nutrient_history, nutrient_list, plot_what = 'all'):
    """ Plots cumulative nutrient history for nutrient IDs given in the plot_what list, or 'all'. """
    all_nutrients, meal_number, index = {}, [], 0
    for meal in nutrient_history:
        meal_number.append(index+1)
        for ID in meal:
            all_nutrients[ID] = []
        index += 1
    for ID in all_nutrients:
        index = 0
        for meal in nutrient_history:
            if ID in meal:
                if all_nutrients[ID] != []:
                    prev = all_nutrients[ID][index-1]
                else:
                    prev = 0
                all_nutrients[ID].append(prev + meal[ID])
            else:
                all_nutrients[ID].append(0)
            index += 1
    plt.figure('Nutrient levels')
    leg = []
    if plot_what == 'all':
        plot_what = all_nutrients
    for ID in plot_what:
        plt.plot(meal_number, all_nutrients[ID])
        leg.append(nutrient_list[ID][0] + ' (' + nutrient_list[ID][1] + ')')
    plt.legend(leg)
    plt.xlabel('Meal number')
    plt.ylabel('Nutrients consumed')
    plt.xticks(range(1, len(meal_number)))
    plt.show()
    return()
    
def reset_history(nutrient_history, daily_target, target):
    nutrient_history, food_count = [], 0
    target = daily_target
    return(nutrient_history, food_count, target)
