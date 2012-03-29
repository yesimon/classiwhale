from django.db import models, connection, transaction

class TwitterUserProfileManager(models.Manager):


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

class CachedStatusManager(models.Manager):

    def create_in_bulk(self, tp, statuses, predictions):
        base_sql = "INSERT INTO twitter_cachedstatus \
                    (user_id, status_id, prediction) VALUES "

        values_sql = []
        values_data = []

        if len(statuses) == 0: return

        for status, prediction in zip(statuses, predictions):
            placeholders = ['%s' for i in range(3)]
            values_sql.append("(%s)" % ','.join(placeholders))
            values_data.extend((tp.id, status.id, prediction))

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

        if len(statuses) == 0: return

        for status in statuses:
            placeholders = ['%s' for i in range(len(self.fields))]
            values_sql.append("(%s)" % ','.join(placeholders))
            tup = [getattr(status, field) for field in self.fields]
            values_data.extend(tup)

        sql = '%s%s' % (base_sql, ', '.join(values_sql))

        curs = connection.cursor()
        curs.execute(sql, values_data)
        transaction.commit_unless_managed()
