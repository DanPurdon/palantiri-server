DROP TABLE palantiriAPI_circle
DROP TABLE palantiriAPI_circlemember
DROP TABLE palantiriAPI_comment
DROP TABLE palantiriAPI_invitation
DROP TABLE palantiriAPI_message
DROP TABLE palantiriAPI_post
DROP TABLE palantiriAPI_user

In the database: DELETE FROM django_migrations WHERE app = 'palantiriAPI'