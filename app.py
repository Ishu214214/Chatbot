from flask import Flask ,render_template , request
import nltk
from nltk.chat.util import Chat
from flask_sqlalchemy import SQLAlchemy

#Flask instalization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chat_bots'

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

qa_pairs = [    [ 'what is your owner name' ,                               ['ishu'] ]  ,
                [ '(.*)name' ,                                              [ 'ishu kumar' ] ]  ,           
                [ 'what is your favourate colour' ,                         ['black'] ]  ,
                [ 'what is your age'              ,                         [ '12' ] ]                     ,
                [ 'what is your favourate book'    ,                        ['Java'] ]        ,
                [ 'what is your favourate food' ,                           [ 'chiken' ] ]      ,                                      
                [ 'what is your creater' ,                                  [ 'ishu kumar' ] ]       ,       
                [ 'what is the favourate colour of your owner' ,            ['black'] ]    ,            
                [ '(hi|HI|Hi|hey|HEY|Hey|HELLO|Hello|hello)',               [' \t hello 👋 \n how can i help u'  ,  '👋 '] ] ,            
                [ '(.*)(location|city|address|place|Place) ?',              ['khagaria bihar']   ]   ,
                [ '(.*)contact(.*)' ,                                       ['call - 7004718739 for more information ℹ '] ]   ,
                [  '(.*)weather(.*)' ,                                      ['it cool 😎 ']    ] ,
                [ '(.*)',                                                   ['sorry']  ]
                
            ]

cb = Chat(qa_pairs)

    
class chat_bots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)


@app.route('/',methods=['GET','POST'])
def chatbot_responses():
    response=''
    if request.method == 'POST':

        msg = request.form['name']
        response= cb.respond(msg)
        
        name = request.form.get('name')
        entry=chat_bots(name=name)
        
        db.session.add(entry)
        db.session.commit()


    return render_template('database_of_chatbot.html',response1=response)

if __name__ == '__main__':
    app.run(debug=True)
        
           
