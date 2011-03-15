from django.db import models, connection, transaction

class TwitterUserProfileManager(models.Manager):

    def bulk_cached_statuses(self, tp, statuses):
        base_sql = "INSERT INTO twitter_twitteruserprofile_cached_statuses \
                    (twitteruserprofile_id, status_id) VALUES "

        values_sql = []
        values_data = []

        for status in statuses:
            placeholders = ['%s' for i in range(2)]
            values_sql.append("(%s)" % ','.join(placeholders))
            values_data.extend((tp.id, status.id))

        sql = '%s%s' % (base_sql, ', '.join(values_sql))

        curs = connection.cursor()
        curs.execute(sql, values_data)
        transaction.commit_unless_managed()

    # Todo: customize create_in_bulk
    def create_in_bulk(self, values):
        base_sql = "INSERT INTO tbl_name (a,b,c) VALUES "
        values_sql = []
        values_data = []

        for value_list in values:
            placeholders = ['%s' for i in range(len(value_list))]
            values_sql.append("(%s)" % ','.join(placeholders))
            values_data.extend(value_list)

        sql = '%s%s' % (base_sql, ', '.join(values_sql))

        curs = connection.cursor()
        curs.execute(sql, values_data)
        transaction.commit_unless_managed()


class StatusManager(models.Manager):

    fields = ('id', 'text', 'user_id', 'source', 
              'content_length', 'punctuation', 'has_hyperlink', 'created_at', 
              'in_reply_to_user_id', 'in_reply_to_status_id', 'is_cached')

    def create_in_bulk(self, statuses):

        base_sql = "INSERT INTO twitter_status (id, text, user_id, \
                    source, content_length, punctuation, has_hyperlink, \
                    created_at, in_reply_to_user_id, in_reply_to_status_id, \
                    is_cached) VALUES "

        values_sql = []
        values_data = []


        for status in statuses:
            placeholders = ['%s' for i in range(len(self.fields))]
            values_sql.append("(%s)" % ','.join(placeholders))
            tup = [getattr(status, field) for field in self.fields]
            values_data.extend(tup)

        sql = '%s%s' % (base_sql, ', '.join(values_sql))

        curs = connection.cursor()
        curs.execute(sql, values_data)
        transaction.commit_unless_managed()
