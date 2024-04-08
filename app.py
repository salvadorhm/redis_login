import sqlite3
import web
import redis

urls = (
    '/', 'Login',
    '/bienvenida', 'Bienvenida'
)

app = web.application(urls, globals())
render = web.template.render('templates/')


class Login:
    def GET(self):
        return render.login()

    def POST(self):
        try:
            form = web.input()
            user = form['user']
            password = form['password']

            conexion = sqlite3.connect("sql/base.db")
            sql = "SELECT user FROM users WHERE user= ? AND password = ?;"

            cursor = conexion.execute(sql, (user, password))
            numero = 0
            for fila in cursor:
                print(fila)
                numero += 1

            conexion.close()
            if numero > 0:
                r = redis.Redis(host='localhost',
                                port=6379,
                                decode_responses=True)
                r.set('user', user)
                r.set('status', '1')
                raise web.seeother('/bienvenida')
            else:
                r = redis.Redis(host='localhost',
                                port=6379,
                                decode_responses=True)
                r.set('user', 'null')
                r.set('status', '0')
                return render.login()
        except sqlite3.Error as error:
            print(f"Error SQLite3: {error.args}")
        except redis.RedisError as error:
            print(f"Error Redis: {error.args}")
        except Exception as error:
            print(f"Error : {error.args}")


class Bienvenida:
    def GET(self):
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        user = r.get('user')
        if user != 'null':
            return render.bienvenida()
        else:
            raise web.seeother("/")


if __name__ == "__main__":
    app.run()
