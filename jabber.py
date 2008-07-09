from jabberbot import JabberBot
import datetime
from necroposter import necroposter
import xmpp

class non7top_jabberbot(JabberBot):
    def bot_serverinfo( self, mess, args):
        """Displays information about the server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )

    def bot_wa (self, mess, args):
	"""Returns bb code"""
        np=necroposter()
        np.dw_wapage(str(args))
        np.init_data()
        return np.gen_bbcode()

    def bot_conf (self, mess, args):
        """connects to conference"""
        #presence = xmpp.Presence(to="file@chat.im.aaanet.ru" + '/' + "bot")
        #presence.setFrom("non7top@isn7.ru")
        #self.conn.send(presence)
        return None

    def bot_subscribe( self, mess, args):
        "Send the subscribe command to have me authorize your subscription to my presence"
        f = mess.getFrom()
        self.conn.Roster.Authorize( f)
        return 'Authorized.'

	 
username = 'jabberbot@isn7.ru'
password = 'isn7.ru'
bot = non7top_jabberbot(username,password)
bot.serve_forever()
