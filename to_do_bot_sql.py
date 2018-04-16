from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters

from telegram import ChatAction

import sql_db

def insert(st):
    sql_db.insert(st)

def remove(task):
    sql_db.remove(task)

def start(bot,update):
    update.message.reply_text("Hello!")
    print("Hello!")

def nomsg(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I'm sorry, I can't do that.")

def show(bot, update):
    result = sql_db.showAll()
    if not result:
        update.message.reply_text("Nothing to show.")
    else:
        for x in result:
            update.message.reply_text(x)

def rmv(bot, update, args):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    string = " ".join(str(x) for x in args)

    if not sql_db.check(string):
        update.message.reply_text(string + "not found!")
    else:
        sql_db.remove(string)
        update.message.reply_text(string + "removed successfully!")

def rmvall(bot, update, args):
    name = str(args[0])
    removed = []

    if sql_db.match(name) == None :
        update.message.reply_text("No matches.")
    else:

        string = "\" and \"".join(str(x[1]) for x in sql_db.match(name))
        sql_db.removeAll(name)
        update.message.reply_text("The elements \"" + string + "\" successfully removed!")

def new(bot, update, args):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    string = " ".join(str(x) for x in args)
    insert(string)
    update.message.reply_text("Successfully added!")

def help(bot,update):
    update.message.reply_text("To-do Manager:\n1. Insert new task with /newTask"
                              "\n2. Remove task with /removeTask or /removeAllTasks (matching a string)"
                              "\n3. Show all tasks with /showTasks")


def main():
    """
    My First Bot
    """
    inpt=open("TOKEN.txt","r")
    updater=Updater(inpt.readline())

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(MessageHandler(Filters.text,nomsg))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("showTasks",show))
    dp.add_handler(CommandHandler("newTask",new, pass_args=True))
    dp.add_handler(CommandHandler("removeTask",rmv,pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks",rmvall, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()