import json
import requests
import random
import os

folder = os.path.dirname(os.path.abspath(__file__))

# load config
with open(folder + '/config.json') as f:
    conf = json.load(f)

NUMBER_OF_USERS = conf['number_of_users']
MAX_POSTS_PER_USER = conf['max_posts_per_user']
MAX_LIKES_PER_USER = conf['max_likes_per_user']
tradecore = [
    'aleksandar.ostojic@tradecore.com', 
    'jelena.prodanovic@tradecore.com', 
    'vidoje.gavrilovic@tradecore.com', 
    'dusan.minic@tradecore.com', 
    'boris.jelisavac@tradecore.com', 
    'jelena.rajak@tradecore.com', 
    'milan.stanojevic@tradecore.com',
    'djurdja.peric@tradecore.com'
]

users = {}
lorem = ('Et dolore aut et doloribus velit. '
         'Maiores sint ipsum eos voluptas. '
         'Earum velit non velit et ut quis voluptas. '
         'Non et aspernatur saepe illo voluptatem. '
         'Expedita est sed occaecati rem aspernatur et.')

# Register users
for user in range(1, NUMBER_OF_USERS + 1):

    # When we ran out of emails from Tradecore folks
    # we are registering some generated emails
    try:
        email = tradecore[user-1]
        password = email.split('.')[0]
    
    except IndexError:        
        email = f'user{user}@example.com'
        password = f'password{user}'
    data = {
        'email': email,
        'password': password
    }
    users[user] = data
    
    # Registering users
    r = requests.post('http://127.0.0.1:8000/auth/register/', json=data)
    user_data = json.loads(r.content)

    # Updating users data
    users[user].update(user_data)

    # Printing result
    un = ''
    if not users[user]['email_verified']:
        un = 'un'
    print(f"{users[user]['first_name']} registered with {un}verified email address: {users[user]['email']}.")

# Posting
for user in users:
    data = {
        'email': users[user]['email'],
        'password': users[user]['password'],
    }
    # Retrieve token
    r = requests.post('http://127.0.0.1:8000/auth/login/', json=data)
    token = json.loads(r.text)['token']
    headers = {'Authorization': f'Token {token}'}

    # Posting random number of lorem ipsum posts
    for el in range(random.randint(1, MAX_POSTS_PER_USER)):

        # Post is lorem ipsum. Start of post is in the first third of our lorem string,
        # End is in the last third of lorem string
        data = {'content': lorem[random.randint(0, len(lorem)//3):-(random.randint(0, len(lorem)//3))]}
        r = requests.post('http://127.0.0.1:8000/user/create_post/', json=data, headers=headers)

        # Printing result
        print(f"{users[user]['first_name']} posted something!")


# Get users by the number of posts and sorting them accordingly
r = requests.get('http://127.0.0.1:8000/user/number_of_posts/')
no_of_posts_by_user = json.loads(r.content)
no_of_posts_by_user = sorted(no_of_posts_by_user.items(), key=lambda k: k[1], reverse=True)

# Printing result
for user in no_of_posts_by_user:
    print(f"{users[int(user[0])]['first_name']} created {user[1]} posts.")

users_left = True

# Liking
for user in no_of_posts_by_user:
    
    # If there is no users with posts with zero likes, break
    if not users_left:
        break

    # Printing info
    print(f"{users[int(user[0])]['first_name']} is going into liking spree!")

    # Retrieve token and preparing headers
    data = {'email': users[int(user[0])]['email'], 'password': users[int(user[0])]['password']}
    r = requests.post('http://127.0.0.1:8000/auth/login/', json=data)
    token = json.loads(r.content)['token']
    headers = {'Authorization': f'Token {token}'}

    # Initialize list of liked post for a user
    liked_posts = []

    for _el in range(MAX_LIKES_PER_USER):

        # Retrieve users with posts with zero likes
        users_with_zero_likes = list(json.loads(requests.get('http://127.0.0.1:8000/user/zero_like/').content))

        # If there are no such users, say good bye
        if len(users_with_zero_likes) == 0:
            users_left = False
            print('No more unliked posts! Good bye!')
            break

        # Printing result
        name_list = [users[user]['first_name'] for user in users_with_zero_likes]
        strng = str(name_list).strip('[]')
        print(strng, 'have posts with zero likes.')

        # Remove current user from list of zero likes(user can not like own posts)
        if int(user[0]) in users_with_zero_likes:
            users_with_zero_likes.remove(int(user[0]))

        # There is possibility that current user has posts with zero likes.
        # We can not break out the outer loop because of that.
        if len(users_with_zero_likes) == 0:
            break
    
        # Get random user
        random_user = random.choice(users_with_zero_likes)

        # Retrieve all post from random user
        posts_by_user = list(json.loads(requests.get(f'http://127.0.0.1:8000/post/user/{random_user}/').content))
        
        # Remove posts already liked
        unliked_posts = list(set(posts_by_user) - set(liked_posts))
        post_to_like = random.choice(unliked_posts)

        # Like post
        r = requests.post(f'http://127.0.0.1:8000/post/like/{post_to_like}/', headers=headers)

        # Print result
        print(f"{users[int(user[0])]['first_name']} liked post with id {post_to_like} from {users[random_user]['first_name']}!")
        
        # Add liked post to array of liked posts
        liked_posts.append(post_to_like)

# If users ran out of likes, print some info
if users_left:
    print('Users ran out of likes!')
