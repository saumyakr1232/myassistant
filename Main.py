import threading

import assist.whatsapp.monitorWhatsapp as monitorWhatsapp
import assist.whatsapp.ChatAnalysis as ChatAnalysis
import time


def read():
    while True:
        print(ChatAnalysis.look_for_imp_messages(ChatAnalysis.get_messages(), [ChatAnalysis.KeywordSets.keyWordsSet3]))
        time.sleep(2)


if __name__ == '__main__':
    threadRefresh = threading.Thread(target=read, daemon=True)
    threadRefresh.start()
    monitorWhatsapp.main()


