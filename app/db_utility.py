import logging
import os
import threading
from flask_sqlalchemy import SQLAlchemy


class DatabaseUtility:

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.db_filename = 'sqlite.db'
        self.sqlite_prefix = 'sqlite:///'
        self.db_path = self.sqlite_prefix + os.path.join(str(os.path.abspath(os.getcwd())), self.db_filename)
        self.db = None
        self.ipsToViews = {}
        self.usersToViews = {}

    def initialize_db(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
        self.db = SQLAlchemy(app)

        # enable foreign keys for sqlite
        self.db.engine.execute("PRAGMA foreign_keys = 1")

        # create/connect sqlalchemy db
        self.db.create_all()
        self.log.info('connected to db')

    def start_hello_world_timer(self, ip):
        self.log.info('get_hello_world from ip: ' + ip)

        # check if ip address has already been seen in the past minute
        if ip in self.ipsToViews:
            self.ipsToViews[ip] += 1
            self.log.info('increment views for ip: ' + ip)
        else:
            self.ipsToViews[ip] = 1
            self.log.info('add ip to map with 1 view: ' + ip)
            threading.Timer(60, self.record_hello_world_views, args=(ip,)).start()

        self.log.info('view count so far this minute: ' + str(self.ipsToViews[ip]))

    def record_hello_world_views(self, ip):
        sql = '''insert into hello_world_views (minute_view_id, ip_address, views, dt_received) 
                values(NULL, '{}', {}, CURRENT_TIMESTAMP)'''.format(ip, self.ipsToViews[ip])

        self.db.engine.execute(sql)
        self.log.info('added ip to db: ' + str(ip) + ' with views count: ' + str(self.ipsToViews[ip]))
        del self.ipsToViews[ip]

    def start_hello_name_timer(self, ip, name):
        self.log.info('get_hello_name from ip: ' + ip + ' with name: ' + name)

        # check if user has already been seen in the past minute
        if (ip, name) in self.usersToViews:
            self.usersToViews[(ip, name)] += 1
            self.log.info('increment views for ip: ' + ip + ' with name: ' + name)
        else:
            self.usersToViews[(ip, name)] = 1
            self.log.info('add user to map with 1 view for ip: ' + ip + ' with name: ' + name)
            threading.Timer(60, self.record_hello_name_views, args=(ip, name)).start()

        self.log.info('view count so far this minute: ' + str(self.usersToViews[(ip, name)]))

    def record_hello_name_views(self, ip, name):
        sql = '''insert into hello_name_views (minute_view_id, ip_address, name, views, dt_received) 
                values(NULL, '{}', '{}', {}, CURRENT_TIMESTAMP)'''.format(ip, name, self.usersToViews[(ip, name)])

        self.db.engine.execute(sql)
        self.log.info('added ip to db: {} with views count: {}'.format(str(ip), str(self.usersToViews[(ip, name)])))
        del self.usersToViews[(ip, name)]

    def get_hello_world_logs(self):
        sql = '''select ip_address, views, dt_received from hello_world_views'''
        results = self.db.engine.execute(sql)
        log_list = []
        for ip_address, views, dt_received in results:
            log_msg = 'ip_address: {}, views: {}, dt_received: {}'.format(ip_address, str(views), dt_received)
            log_list.append(log_msg)

        return log_list

    def get_hello_name_logs(self):
        sql = '''select ip_address, name, views, dt_received from hello_name_views'''
        results = self.db.engine.execute(sql)
        log_list = []
        for ip_address, name, views, dt_received in results:
            log_msg = 'ip_address: {}, name: {}, views: {}, dt_received: {}'.format(ip_address, name, str(views), dt_received)
            log_list.append(log_msg)

        return log_list

    def get_all_logs(self):
        sql = '''select ip_address, name, views, dt_received
                from hello_name_views
                union
                select ip_address, NULL, views, dt_received
                from hello_world_views
                order by dt_received asc'''
        results = self.db.engine.execute(sql)
        log_list = []
        for ip_address, name, views, dt_received in results:
            log_msg = 'ip_address: {}, name: {}, views: {}, dt_received: {}'.format(ip_address, name, str(views), dt_received)
            log_list.append(log_msg)

        return log_list


class User:
    def __init__(self, ip_address, name):
        self.ip_address = ip_address
        self.name = name
