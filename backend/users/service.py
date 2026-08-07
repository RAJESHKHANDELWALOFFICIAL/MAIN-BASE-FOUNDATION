def get_all_users(self):

    rows = self.database.fetchall(
        """
        SELECT
            user_id,
            full_name,
            username,
            email,
            phone,
            password,
            role,
            status
        FROM users
        """
    )

    users = []

    for row in rows:

        users.append(
            User(
                user_id=row[0],
                full_name=row[1],
                username=row[2],
                email=row[3],
                phone=row[4],
                password=row[5],
                role=row[6],
                status=row[7],
            )
        )

    return users
