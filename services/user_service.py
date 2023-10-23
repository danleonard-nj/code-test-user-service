from utils.utils import ArgumentNullException, USERS_DB, get_logger

logger = get_logger(__name__)

# Sample in-memory db easily replaced w/ a real NoSQL DB
# or ORM implementation (i.e. SQLAlchemy)


class UserService:
    def __init__(
        self
    ):
        # A repository class could be injected here w/ a real DB implementation
        pass

    def get_users(
        self
    ):
        '''
        Get all users
        '''

        # Fetch all users from mock DB
        logger.info(f'Fetching all users')
        all_users = USERS_DB.values()

        # Return all users
        return {
            'users': list(all_users)
        }

    def get_user(
        self,
        user_id: int
    ) -> dict:
        '''
        Gets a user by ID
        '''

        ArgumentNullException.if_none_or_whitespace(
            user_id, 'user_id')

        logger.info(f'Fetching user with ID {user_id}')

        # Verify user exists
        if user_id not in USERS_DB:
            raise Exception(f"No user with the ID '{user_id}' exists'")

        return USERS_DB[user_id]

    def create_user(
        self,
        data: dict
    ) -> dict:
        '''
        Create a new user
        '''

        ArgumentNullException.if_none(data, 'data')

        logger.info(f'Creating new user: {data}')

        # Simulate auto-incrementing ID for fake DB
        user_id = max(USERS_DB.keys(), key=int) + 1
        logger.info(f'New user ID: {user_id}')

        # Verify friends are valid
        logger.info(f'Verifying friends')
        self._verify_friends(data.get('friends', []))

        # Create the new user
        user = {
            'user_id': user_id,
            'friends': data.get('friends', [])
        }

        logger.info(f'New user: {user}')

        # Store the user to the fake DB
        USERS_DB[user_id] = user

        return user

    def update_user(
        self,
        data: dict
    ) -> dict:
        '''
        Updates an existing user
        '''

        ArgumentNullException.if_none(data, 'data')

        id = int(data.get('user_id', 0))
        logger.info(f'Updating user with ID {id}')

        # Verify the user exists
        if id == 0 or id not in USERS_DB:
            raise Exception(f"No user with the ID '{id}' exists'")

        # Get the existing user from the DB
        existing_user = USERS_DB[id]

        # Verify friends are valid
        logger.info(f'Verifying friends')
        self._verify_friends(data.get('friends', []))

        # Update the user w/ new friend values
        updated_user = existing_user | {
            'friends': data.get('friends', [])
        }

        logger.info(f'Updated user: {updated_user}')

        # Store to fake DB
        USERS_DB[id] = updated_user

        return updated_user

    def delete_user(
        self,
        user_id: str
    ) -> dict:
        '''
        Delete a user by ID
        '''

        ArgumentNullException.if_none_or_whitespace(user_id, 'user_id')

        logger.info(f'Deleting user with ID {user_id}')

        if user_id not in USERS_DB:
            raise Exception(f"No user with the ID '{user_id}' exists'")

        del USERS_DB[user_id]

        return {
            'result': True
        }

    def get_degrees_separated(
        self,
        user_one: int,
        user_two: int
    ) -> dict:

        ArgumentNullException.if_none_or_whitespace(user_one, 'user_one')
        ArgumentNullException.if_none_or_whitespace(user_two, 'user_two')

        logger.info(
            f'Getting degrees of separation between users {user_one} and {user_two}')

        # Verify both users exist
        if user_one not in USERS_DB:
            raise Exception(f"No user with the ID '{user_one}' exists'")

        if user_two not in USERS_DB:
            raise Exception(f"No user with the ID '{user_two}' exists'")

        # Get the shortest path between the two users
        distance = self._calculate_degrees_separation(
            user_one,
            user_two)

        logger.info(f'Degrees of separation: {distance}')

        if distance < 0:
            raise Exception(
                f"Users '{user_one}' and '{user_two}' are not connected")

        return {
            'user_one': user_one,
            'user_two': user_two,
            'degrees_separated': distance
        }

    def _verify_friends(
        self,
        friend_ids: list[int]
    ):
        # Verify each friend ID exists in fake DB
        for friend_id in friend_ids:
            # This could be done in a single query w/ a real DB like MongoDB
            if friend_id not in USERS_DB:
                raise Exception(f"No user with the ID '{friend_id}' exists'")

        return True

    def _calculate_degrees_separation(
        self,
        user_id_one: int,
        user_id_two: int
    ):
        # Known distinct users
        known_users = set()
        users = []

        # Add the first user to the queue
        users.append((user_id_one, 0))

        while any(users):

            # Get the next user detail in the queue
            current_user, distance = users.pop(0)
            logger.info(f'User {current_user} at distance {distance}')

            # Return the distance for t
            if current_user == user_id_two:
                logger.info(f'Found target at distance {distance}')
                return distance

            # Add known processed user
            known_users.add(current_user)

            # Add the friends of the current user to the queue
            # Caching opportunity to avoid repeated lookups
            for friend in USERS_DB[current_user].get('friends', []):
                if friend not in known_users:
                    logger.info(
                        f'Adding friend {friend} to chain at distance {distance + 1}')
                    users.append((friend, distance + 1))

        # No valid path
        return -1
